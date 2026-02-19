from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
from datetime import datetime
from bson import ObjectId
from app.services.ml_service import MLService
from app.services.degradation_handler import GracefulDegradationHandler
from app.utils.validators import FileValidator
from app.utils.retry_strategies import RetryStrategies
from app.utils.logging_config import get_logger
from app.utils.metrics import (
    track_document_upload,
    track_time,
    MetricNames,
    GaugeContext
)
import os
import uuid

bp = Blueprint('documents', __name__)
logger = get_logger('api.documents')

ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}
UPLOAD_FOLDER = 'uploads'

# Initialize file validator and degradation handler
file_validator = FileValidator()
degradation_handler = GracefulDegradationHandler()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/upload', methods=['POST'])
@jwt_required()
def upload_document():
    """
    Upload and analyze a legal document with production-grade error handling
    
    Request:
        - file: Document file (PDF, JPG, PNG)
        - document_type: Optional hint
    
    Response:
        - document_id: Unique identifier
        - extracted_text: OCR/extracted text
        - classification: Document type + confidence
        - detected_issues: List of problems found
        - severity_analysis: Overall risk assessment
        - summary: Plain English explanation
    """
    request_id = str(uuid.uuid4())
    user_id = get_jwt_identity()
    start_time = datetime.utcnow()
    
    logger.info(
        "Document upload request received",
        extra={
            'request_id': request_id,
            'user_id': user_id
        }
    )
    
    # Track active processing
    with GaugeContext(MetricNames.ACTIVE_PROCESSING_TASKS):
        try:
            # Validate file presence
            if 'file' not in request.files:
                logger.warning("No file in request", extra={'request_id': request_id})
                track_document_upload('validation_error')
                return jsonify({'error': 'No file provided'}), 400
            
            file = request.files['file']
            
            if file.filename == '':
                logger.warning("Empty filename", extra={'request_id': request_id})
                track_document_upload('validation_error')
                return jsonify({'error': 'No file selected'}), 400
            
            # Enhanced file validation
            validation_result = file_validator.validate_file(file)
            if not validation_result['valid']:
                logger.warning(
                    "File validation failed",
                    extra={
                        'request_id': request_id,
                        'errors': validation_result['errors']
                    }
                )
                track_document_upload('validation_error')
                return jsonify({
                    'error': 'File validation failed',
                    'details': validation_result['errors']
                }), 400
            
            document_type = request.form.get('document_type', 'other')
            filename = secure_filename(file.filename)
            file_extension = filename.rsplit('.', 1)[1].lower()
            
            # Generate unique document ID and filename
            document_id = str(uuid.uuid4())
            timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
            unique_filename = f"{user_id}_{timestamp}_{filename}"
            
            # Calculate file hash for duplicate detection
            file_hash = file_validator.calculate_file_hash(file)
            
            # Check for duplicate uploads
            db = current_app.db
            existing_doc = db.documents.find_one({
                'userId': ObjectId(user_id),
                'fileHash': file_hash
            })
            
            if existing_doc:
                logger.info(
                    "Duplicate document detected",
                    extra={
                        'request_id': request_id,
                        'document_id': str(existing_doc['_id']),
                        'file_hash': file_hash
                    }
                )
                track_document_upload('duplicate', document_type)
                return jsonify({
                    'message': 'Document already processed',
                    'document_id': str(existing_doc['_id']),
                    'status': existing_doc['processing']['status'],
                    'duplicate': True
                }), 200
            
            # Save file to storage
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)
            file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
            
            try:
                file.save(file_path)
                file_size = os.path.getsize(file_path)
                
                logger.info(
                    "File saved successfully",
                    extra={
                        'request_id': request_id,
                        'document_id': document_id,
                        'file_path': file_path,
                        'file_size': file_size
                    }
                )
            except Exception as e:
                logger.error(
                    "Failed to save file",
                    extra={
                        'request_id': request_id,
                        'error': str(e)
                    },
                    exc_info=True
                )
                track_document_upload('storage_error', document_type)
                return jsonify({
                    'error': 'Failed to save file',
                    'request_id': request_id
                }), 500
            
            try:
                # Process document with ML service using degradation handler
                logger.info(
                    "Starting document processing with graceful degradation",
                    extra={
                        'request_id': request_id,
                        'document_id': document_id,
                        'file_name': filename  # Changed from 'filename' to avoid conflict
                    }
                )
                
                ml_result = _process_document_with_degradation(
                    file_path,
                    file_extension,
                    document_id
                )
                
                if not ml_result.get('success'):
                    logger.error(
                        "Document processing failed",
                        extra={
                            'request_id': request_id,
                            'document_id': document_id,
                            'error': ml_result.get('error')
                        }
                    )
                    track_document_upload('processing_error', document_type)
                    return jsonify({
                        'error': ml_result.get('error', 'Failed to process document'),
                        'document_id': document_id,
                        'request_id': request_id
                    }), 400
                
                # Store in database
                document = {
                    '_id': ObjectId(),
                    'documentId': document_id,
                    'userId': ObjectId(user_id),
                    'fileName': filename,
                    'fileType': file_extension,
                    'fileSize': file_size,
                    'fileHash': file_hash,
                    'storagePath': file_path,
                    'processing': {
                        'status': 'completed',
                        'startedAt': start_time,
                        'completedAt': datetime.utcnow(),
                        'error': None,
                        'requestId': request_id,
                        'analysisTier': ml_result.get('analysis_tier', 'UNKNOWN')
                    },
                    'extractedText': ml_result.get('extracted_text'),
                    'classification': ml_result.get('classification'),
                    'detectedIssues': ml_result.get('detected_issues', []),
                    'severityAnalysis': ml_result.get('severity_analysis'),
                    'summary': ml_result.get('summary'),
                    'recommendations': ml_result.get('recommendations', []),
                    'warning': ml_result.get('warning'),
                    'createdAt': datetime.utcnow(),
                    'updatedAt': datetime.utcnow()
                }
                
                result = db.documents.insert_one(document)
                
                # Track successful upload
                track_document_upload('success', document_type)
                
                logger.info(
                    "Document processed successfully",
                    extra={
                        'request_id': request_id,
                        'document_id': document_id,
                        'db_id': str(result.inserted_id),
                        'analysis_tier': ml_result.get('analysis_tier')
                    }
                )
                
                return jsonify({
                    'document_id': document_id,
                    'status': 'completed',
                    'analysis_tier': ml_result.get('analysis_tier'),
                    'extracted_text': ml_result.get('extracted_text'),
                    'classification': ml_result.get('classification'),
                    'detected_issues': ml_result.get('detected_issues', []),
                    'severity_analysis': ml_result.get('severity_analysis'),
                    'summary': ml_result.get('summary'),
                    'recommendations': ml_result.get('recommendations', []),
                    'warning': ml_result.get('warning'),
                    'request_id': request_id
                }), 200
                
            except Exception as e:
                logger.error(
                    "Unexpected error processing document",
                    extra={
                        'request_id': request_id,
                        'document_id': document_id,
                        'error': str(e)
                    },
                    exc_info=True
                )
                
                # Track error
                track_document_upload('error', document_type)
                
                # Update document status to failed
                try:
                    db.documents.update_one(
                        {'documentId': document_id},
                        {
                            '$set': {
                                'processing.status': 'failed',
                                'processing.error': str(e),
                                'processing.completedAt': datetime.utcnow()
                            }
                        }
                    )
                except Exception:
                    pass
                
                return jsonify({
                    'error': 'Error processing document',
                    'document_id': document_id,
                    'request_id': request_id
                }), 500
        
        except Exception as e:
            logger.error(
                "Unexpected error in upload handler",
                extra={'request_id': request_id, 'error': str(e)},
                exc_info=True
            )
            track_document_upload('error')
            return jsonify({
                'error': 'Internal server error',
                'request_id': request_id
            }), 500


def _process_document_with_degradation(file_path, file_extension, document_id):
    """
    Process document with graceful degradation
    
    Uses multi-tier fallback strategy:
    1. Full ML pipeline
    2. Rule-based extraction
    3. Basic text analysis
    """
    from app.ml.text_extractor import TextExtractor
    
    try:
        # Extract text first
        if file_extension == 'pdf':
            extracted_text = TextExtractor.extract_from_pdf(file_path)
        else:
            extracted_text = TextExtractor.extract_from_image(file_path)
        
        if not extracted_text:
            return {
                'success': False,
                'error': 'Failed to extract text from document'
            }
        
        # Use degradation handler for analysis
        analysis_result = degradation_handler.analyze_document_with_fallback(
            document_id=document_id,
            extracted_text=extracted_text,
            file_type=file_extension
        )
        
        # Add extracted text to result
        analysis_result['extracted_text'] = extracted_text
        analysis_result['success'] = True
        
        return analysis_result
        
    except Exception as e:
        logger.error(
            f"Document processing failed: {str(e)}",
            extra={'document_id': document_id},
            exc_info=True
        )
        return {
            'success': False,
            'error': str(e)
        }

@bp.route('/analyze', methods=['POST'])
@jwt_required()
def analyze_text():
    """
    Analyze pasted text (no file upload)
    
    Request:
        - text: Document text content
        - context: Optional context hint
    
    Response:
        - classification: Document type
        - detected_issues: Problems found
        - severity_analysis: Risk assessment
        - summary: Plain English explanation
        - recommendations: Suggested actions
    """
    data = request.get_json()
    
    text = data.get('text')
    context = data.get('context')
    
    if not text:
        return jsonify({'error': 'Text is required'}), 400
    
    if len(text) < 10:
        return jsonify({'error': 'Text too short for analysis'}), 400
    
    if len(text) > 50000:
        return jsonify({'error': 'Text too long. Maximum 50,000 characters'}), 400
    
    try:
        # Analyze text with ML service
        result = MLService.analyze_text(text, context)
        
        if not result.get('success'):
            return jsonify({
                'error': result.get('error', 'Failed to analyze text')
            }), 400
        
        return jsonify({
            'classification': result.get('classification'),
            'detected_issues': result.get('detected_issues', []),
            'severity_analysis': result.get('severity_analysis'),
            'summary': result.get('summary'),
            'recommendations': result.get('recommendations', [])
        }), 200
        
    except Exception as e:
        print(f"Error analyzing text: {e}")
        return jsonify({
            'error': f'Error analyzing text: {str(e)}'
        }), 500

@bp.route('/<document_id>', methods=['GET'])
@jwt_required()
def get_document(document_id):
    user_id = get_jwt_identity()
    db = current_app.db
    
    try:
        document = db.documents.find_one({
            '_id': ObjectId(document_id),
            'userId': ObjectId(user_id)
        })
    except:
        return jsonify({'error': 'Invalid document ID'}), 400
    
    if not document:
        return jsonify({'error': 'Document not found'}), 404
    
    return jsonify({
        'document_id': str(document['_id']),
        'fileName': document['fileName'],
        'fileType': document['fileType'],
        'status': document['processing']['status'],
        'extractedText': document.get('extractedText'),
        'classification': document.get('classification'),
        'entities': document.get('entities'),
        'detectedIssues': document.get('detectedIssues', []),
        'analysis': document.get('analysis'),
        'createdAt': document['createdAt'].isoformat()
    }), 200

@bp.route('/', methods=['GET'])
@jwt_required()
def list_documents():
    user_id = get_jwt_identity()
    db = current_app.db
    
    documents = db.documents.find({'userId': ObjectId(user_id)}).sort('createdAt', -1).limit(50)
    
    result = []
    for doc in documents:
        result.append({
            'document_id': str(doc['_id']),
            'fileName': doc['fileName'],
            'fileType': doc['fileType'],
            'status': doc['processing']['status'],
            'createdAt': doc['createdAt'].isoformat()
        })
    
    return jsonify({'documents': result}), 200
