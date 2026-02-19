# HomeRights AI - Complete Application Architecture

## Executive Summary

This document outlines the complete architecture for HomeRights AI, a legal document scanning web application that helps UK tenants understand their housing rights. The system uses Flask (backend), Angular (frontend), and TensorFlow (ML for document processing).

---

## 1. System Architecture Overview

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         CLIENT LAYER                             │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │           Angular Frontend (Port 4200)                    │  │
│  │  - Chat Interface (Claude-like UI)                        │  │
│  │  - Document Upload Component                              │  │
│  │  - Topics Browser                                         │  │
│  │  - Local Support Finder                                   │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              │ HTTPS/REST API
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      APPLICATION LAYER                           │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │         Flask Backend API (Port 5000)                     │  │
│  │  ┌────────────────┐  ┌─────────────────┐                 │  │
│  │  │  REST API      │  │  Authentication │                 │  │
│  │  │  Endpoints     │  │  (JWT)          │                 │  │
│  │  └────────────────┘  └─────────────────┘                 │  │
│  │  ┌────────────────┐  ┌─────────────────┐                 │  │
│  │  │  Business      │  │  ML Service     │                 │  │
│  │  │  Logic         │  │  Integration    │                 │  │
│  │  └────────────────┘  └─────────────────┘                 │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      ML PROCESSING LAYER                         │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │         TensorFlow ML Service (Port 8501)                 │  │
│  │  ┌────────────────┐  ┌─────────────────┐                 │  │
│  │  │  Document OCR  │  │  Text           │                 │  │
│  │  │  (Tesseract)   │  │  Classification │                 │  │
│  │  └────────────────┘  └─────────────────┘                 │  │
│  │  ┌────────────────┐  ┌─────────────────┐                 │  │
│  │  │  NLP Analysis  │  │  Pattern        │                 │  │
│  │  │  (spaCy)       │  │  Detection      │                 │  │
│  │  └────────────────┘  └─────────────────┘                 │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                         DATA LAYER                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │   MongoDB    │  │   Redis      │  │   File       │          │
│  │   Database   │  │   Cache      │  │   Storage    │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└─────────────────────────────────────────────────────────────────┘
```

---

## 2. Detailed Component Architecture

### 2.1 Frontend Layer (Angular)

#### Project Structure
```
frontend/
├── src/
│   ├── app/
│   │   ├── core/                    # Singleton services, guards
│   │   │   ├── services/
│   │   │   │   ├── auth.service.ts
│   │   │   │   ├── api.service.ts
│   │   │   │   └── document.service.ts
│   │   │   ├── guards/
│   │   │   │   └── auth.guard.ts
│   │   │   └── interceptors/
│   │   │       └── jwt.interceptor.ts
│   │   │
│   │   ├── shared/                  # Shared components
│   │   │   ├── components/
│   │   │   │   ├── header/
│   │   │   │   ├── sidebar/
│   │   │   │   └── loading-spinner/
│   │   │   ├── directives/
│   │   │   └── pipes/
│   │   │
│   │   ├── features/                # Feature modules
│   │   │   ├── chat/               # Main chat interface
│   │   │   │   ├── chat.component.ts
│   │   │   │   ├── chat.component.html
│   │   │   │   ├── chat.component.scss
│   │   │   │   └── chat.module.ts
│   │   │   │
│   │   │   ├── document-upload/    # Document scanning
│   │   │   │   ├── upload.component.ts
│   │   │   │   ├── document-preview.component.ts
│   │   │   │   └── scan-results.component.ts
│   │   │   │
│   │   │   ├── topics/             # Housing law topics
│   │   │   │   ├── topics-list.component.ts
│   │   │   │   └── topic-detail.component.ts
│   │   │   │
│   │   │   ├── support/            # Local support finder
│   │   │   │   └── support-finder.component.ts
│   │   │   │
│   │   │   ├── auth/               # Login/Register
│   │   │   │   ├── login.component.ts
│   │   │   │   └── register.component.ts
│   │   │   │
│   │   │   └── dashboard/          # User dashboard
│   │   │       ├── dashboard.component.ts
│   │   │       └── saved-items.component.ts
│   │   │
│   │   ├── models/                 # TypeScript interfaces
│   │   │   ├── user.model.ts
│   │   │   ├── document.model.ts
│   │   │   ├── topic.model.ts
│   │   │   └── analysis-result.model.ts
│   │   │
│   │   └── app-routing.module.ts
│   │
│   ├── assets/
│   │   ├── styles/
│   │   │   ├── _variables.scss
│   │   │   ├── _mixins.scss
│   │   │   └── _theme.scss
│   │   └── images/
│   │
│   └── environments/
│       ├── environment.ts
│       └── environment.prod.ts
│
├── angular.json
├── package.json
└── tsconfig.json
```

#### Key Components Design

**Chat Component (Claude-like Interface)**
```typescript
// chat.component.ts
interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
  attachments?: DocumentAttachment[];
}

export class ChatComponent {
  messages: Message[] = [];
  userInput: string = '';
  isProcessing: boolean = false;
  
  sendMessage() { }
  uploadDocument() { }
  regenerateResponse() { }
}
```

**Document Upload Component**
```typescript
// upload.component.ts
export class DocumentUploadComponent {
  acceptedFileTypes = ['.pdf', '.jpg', '.png'];
  maxFileSize = 10 * 1024 * 1024; // 10MB
  
  onFileSelected(event: any) { }
  uploadFile(file: File) { }
  displayResults(results: DocumentAnalysis) { }
}
```

#### UI/UX Design Principles
- **Claude-inspired Interface**: Clean, minimal, conversational
- **Accessibility**: WCAG 2.2 AA compliant
- **Responsive**: Mobile-first approach
- **Material Design**: Using Angular Material components

---

### 2.2 Backend Layer (Flask)

#### Project Structure
```
backend/
├── app/
│   ├── __init__.py              # Flask app factory
│   ├── config.py                # Configuration classes
│   │
│   ├── api/                     # API endpoints
│   │   ├── __init__.py
│   │   ├── auth.py              # Authentication routes
│   │   ├── topics.py            # Housing law topics
│   │   ├── documents.py         # Document processing
│   │   ├── support.py           # Local support finder
│   │   ├── chat.py              # Chat interface backend
│   │   └── admin.py             # Admin CMS routes
│   │
│   ├── services/                # Business logic
│   │   ├── __init__.py
│   │   ├── auth_service.py      # JWT handling
│   │   ├── document_service.py  # Document processing orchestration
│   │   ├── ml_service.py        # ML model integration
│   │   ├── nlp_service.py       # Text analysis
│   │   └── postcode_service.py  # Postcode lookup
│   │
│   ├── models/                  # Database models
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── topic.py
│   │   ├── document.py
│   │   ├── agency.py
│   │   └── feedback.py
│   │
│   ├── ml/                      # ML integration
│   │   ├── __init__.py
│   │   ├── document_classifier.py
│   │   ├── text_extractor.py
│   │   ├── pattern_detector.py
│   │   └── model_loader.py
│   │
│   ├── utils/                   # Utility functions
│   │   ├── __init__.py
│   │   ├── validators.py
│   │   ├── helpers.py
│   │   └── decorators.py
│   │
│   └── extensions.py            # Flask extensions (DB, JWT, etc.)
│
├── ml_models/                   # Trained models storage
│   ├── document_classifier/
│   ├── text_extraction/
│   └── pattern_detection/
│
├── tests/                       # Unit and integration tests
│   ├── test_api/
│   ├── test_services/
│   └── test_ml/
│
├── migrations/                  # Database migrations
├── requirements.txt
├── wsgi.py
└── .env.example
```

#### Core Flask Application Setup

```python
# app/__init__.py
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from pymongo import MongoClient

def create_app(config_name='development'):
    app = Flask(__name__)
    app.config.from_object(f'app.config.{config_name.capitalize()}Config')
    
    # Initialize extensions
    CORS(app)
    jwt = JWTManager(app)
    
    # MongoDB connection
    mongo_client = MongoClient(app.config['MONGODB_URI'])
    app.db = mongo_client[app.config['DB_NAME']]
    
    # Register blueprints
    from app.api import auth, topics, documents, support, chat, admin
    app.register_blueprint(auth.bp, url_prefix='/api/auth')
    app.register_blueprint(topics.bp, url_prefix='/api/topics')
    app.register_blueprint(documents.bp, url_prefix='/api/documents')
    app.register_blueprint(support.bp, url_prefix='/api/support')
    app.register_blueprint(chat.bp, url_prefix='/api/chat')
    app.register_blueprint(admin.bp, url_prefix='/api/admin')
    
    return app
```

#### API Endpoints Design

```python
# app/api/documents.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.document_service import DocumentService
from app.services.ml_service import MLService

bp = Blueprint('documents', __name__)

@bp.route('/upload', methods=['POST'])
@jwt_required()
def upload_document():
    """
    Upload and process a legal document
    
    Request:
        - file: Document file (PDF, JPG, PNG)
        - document_type: Optional hint (tenancy_agreement, notice, etc.)
    
    Response:
        - document_id: Unique identifier
        - extracted_text: OCR result
        - classification: Document type
        - analysis: Legal analysis results
        - warnings: Potential issues detected
    """
    file = request.files.get('file')
    document_type = request.form.get('document_type')
    
    # Process document
    result = DocumentService.process_document(
        file=file,
        user_id=get_jwt_identity(),
        document_type=document_type
    )
    
    return jsonify(result), 200


@bp.route('/analyze', methods=['POST'])
@jwt_required()
def analyze_text():
    """
    Analyze pasted text for legal issues
    
    Request:
        - text: Document text content
        - context: Optional context (from_tenancy, from_notice, etc.)
    
    Response:
        - summary: Plain English summary
        - issues: List of potential legal issues
        - recommendations: Suggested actions
        - relevant_laws: Applicable housing laws
        - confidence: Analysis confidence score
    """
    data = request.get_json()
    text = data.get('text')
    context = data.get('context')
    
    result = MLService.analyze_legal_text(text, context)
    
    return jsonify(result), 200


@bp.route('/<document_id>', methods=['GET'])
@jwt_required()
def get_document(document_id):
    """Retrieve document details and analysis"""
    result = DocumentService.get_document(document_id, get_jwt_identity())
    return jsonify(result), 200


@bp.route('/<document_id>/explain', methods=['POST'])
@jwt_required()
def explain_section(document_id):
    """
    Explain specific section of a document
    
    Request:
        - section_text: Text to explain
        - question: Optional specific question
    """
    data = request.get_json()
    result = DocumentService.explain_section(
        document_id=document_id,
        section_text=data.get('section_text'),
        question=data.get('question')
    )
    return jsonify(result), 200
```

---

## 3. Machine Learning Layer (TensorFlow)

### 3.1 ML Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    ML PIPELINE                               │
│                                                              │
│  Input Document (PDF/Image)                                 │
│           ↓                                                  │
│  ┌─────────────────────────┐                                │
│  │   Preprocessing         │                                │
│  │   - Image enhancement   │                                │
│  │   - Deskewing          │                                │
│  │   - Noise reduction    │                                │
│  └─────────────────────────┘                                │
│           ↓                                                  │
│  ┌─────────────────────────┐                                │
│  │   Text Extraction       │                                │
│  │   - Tesseract OCR      │                                │
│  │   - PDF text extract   │                                │
│  │   - Layout analysis    │                                │
│  └─────────────────────────┘                                │
│           ↓                                                  │
│  ┌─────────────────────────┐                                │
│  │   Document              │                                │
│  │   Classification        │                                │
│  │   (TensorFlow Model)   │                                │
│  └─────────────────────────┘                                │
│           ↓                                                  │
│  ┌─────────────────────────┐                                │
│  │   NLP Analysis         │                                │
│  │   - Entity extraction  │                                │
│  │   - Pattern matching   │                                │
│  │   - Clause detection   │                                │
│  └─────────────────────────┘                                │
│           ↓                                                  │
│  ┌─────────────────────────┐                                │
│  │   Legal Analysis       │                                │
│  │   - Risk assessment    │                                │
│  │   - Compliance check   │                                │
│  │   - Recommendation     │                                │
│  └─────────────────────────┘                                │
│           ↓                                                  │
│  Output: Structured Analysis                                │
└─────────────────────────────────────────────────────────────┘
```

### 3.2 ML Models Implementation

#### Model 1: Document Classification

**Purpose**: Classify legal documents into categories
- Tenancy Agreement
- Section 21 Notice
- Section 8 Notice
- Repair Request
- Rent Statement
- General Correspondence

**Architecture**: CNN + LSTM Hybrid
```python
# ml_service/models/document_classifier.py
import tensorflow as tf
from tensorflow.keras import layers, models

def build_document_classifier():
    """
    Build CNN-LSTM model for document classification
    Input: Document embeddings (300 dimensions)
    Output: Document category (6 classes)
    """
    model = models.Sequential([
        # Embedding layer for text
        layers.Embedding(input_dim=10000, output_dim=300, input_length=500),
        
        # CNN layers for feature extraction
        layers.Conv1D(128, 5, activation='relu'),
        layers.MaxPooling1D(5),
        layers.Conv1D(128, 5, activation='relu'),
        layers.MaxPooling1D(5),
        layers.Conv1D(128, 5, activation='relu'),
        layers.GlobalMaxPooling1D(),
        
        # Dense layers
        layers.Dense(256, activation='relu'),
        layers.Dropout(0.5),
        layers.Dense(128, activation='relu'),
        layers.Dropout(0.3),
        
        # Output layer
        layers.Dense(6, activation='softmax')
    ])
    
    model.compile(
        optimizer='adam',
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    
    return model


class DocumentClassifier:
    def __init__(self, model_path='ml_models/document_classifier/'):
        self.model = tf.keras.models.load_model(model_path)
        self.tokenizer = self._load_tokenizer(model_path)
        self.label_encoder = self._load_label_encoder(model_path)
    
    def predict(self, text):
        """
        Predict document type from text
        
        Args:
            text: Extracted document text
            
        Returns:
            {
                'category': 'section_21_notice',
                'confidence': 0.95,
                'probabilities': {...}
            }
        """
        # Preprocess text
        sequences = self.tokenizer.texts_to_sequences([text])
        padded = tf.keras.preprocessing.sequence.pad_sequences(
            sequences, maxlen=500
        )
        
        # Predict
        predictions = self.model.predict(padded)
        
        # Get category and confidence
        category_idx = predictions.argmax()
        confidence = predictions[0][category_idx]
        category = self.label_encoder.inverse_transform([category_idx])[0]
        
        return {
            'category': category,
            'confidence': float(confidence),
            'probabilities': {
                label: float(prob) 
                for label, prob in zip(
                    self.label_encoder.classes_, 
                    predictions[0]
                )
            }
        }
```

#### Model 2: Named Entity Recognition (NER)

**Purpose**: Extract key entities from legal documents
- Person names (landlord, tenant)
- Addresses
- Dates
- Monetary amounts
- Legal references

**Implementation**: Using spaCy + custom training
```python
# ml_service/models/ner_extractor.py
import spacy
from spacy.training import Example
import json

class LegalNERExtractor:
    def __init__(self, model_path='ml_models/legal_ner/'):
        self.nlp = spacy.load(model_path)
        
    def extract_entities(self, text):
        """
        Extract named entities from legal document
        
        Returns:
            {
                'landlord_name': 'John Smith',
                'tenant_name': 'Jane Doe',
                'property_address': '123 Main St, London',
                'notice_date': '2025-02-01',
                'rent_amount': '£1200',
                'deposit_amount': '£1200'
            }
        """
        doc = self.nlp(text)
        
        entities = {
            'persons': [],
            'addresses': [],
            'dates': [],
            'amounts': [],
            'references': []
        }
        
        for ent in doc.ents:
            if ent.label_ == 'PERSON':
                entities['persons'].append({
                    'text': ent.text,
                    'role': self._infer_role(ent, doc)
                })
            elif ent.label_ == 'ADDRESS':
                entities['addresses'].append(ent.text)
            elif ent.label_ == 'DATE':
                entities['dates'].append(ent.text)
            elif ent.label_ == 'MONEY':
                entities['amounts'].append(ent.text)
            elif ent.label_ == 'LAW':
                entities['references'].append(ent.text)
        
        return self._structure_entities(entities)
    
    def _infer_role(self, entity, doc):
        """Infer if person is landlord or tenant based on context"""
        # Implementation of role inference logic
        pass


# Training script for custom NER model
def train_legal_ner(training_data_path, output_path):
    """
    Train custom NER model on legal documents
    
    Training data format:
    [
        ("The landlord, John Smith, at 123 Main St...", 
         {"entities": [(14, 24, "PERSON"), (29, 40, "ADDRESS")]}),
        ...
    ]
    """
    # Load base model
    nlp = spacy.blank("en")
    
    # Create NER pipeline
    if "ner" not in nlp.pipe_names:
        ner = nlp.add_pipe("ner")
    else:
        ner = nlp.get_pipe("ner")
    
    # Add labels
    labels = ["PERSON", "ADDRESS", "DATE", "MONEY", "LAW", 
              "LANDLORD", "TENANT", "PROPERTY"]
    for label in labels:
        ner.add_label(label)
    
    # Load training data
    with open(training_data_path, 'r') as f:
        training_data = json.load(f)
    
    # Training loop
    optimizer = nlp.begin_training()
    for epoch in range(30):
        losses = {}
        for text, annotations in training_data:
            doc = nlp.make_doc(text)
            example = Example.from_dict(doc, annotations)
            nlp.update([example], drop=0.5, losses=losses)
        print(f"Epoch {epoch}: {losses}")
    
    # Save model
    nlp.to_disk(output_path)
```

#### Model 3: Pattern Detection (Unfair Clauses)

**Purpose**: Detect potentially unfair or problematic clauses

```python
# ml_service/models/pattern_detector.py
import re
from typing import List, Dict

class PatternDetector:
    def __init__(self):
        self.patterns = self._load_patterns()
    
    def _load_patterns(self):
        """
        Load pattern rules for detecting unfair clauses
        """
        return {
            'unfair_deposit': {
                'patterns': [
                    r'deposit.*exceed.*\d+.*month',
                    r'non-refundable.*deposit',
                    r'deposit.*not.*protected'
                ],
                'severity': 'high',
                'explanation': 'Deposit must not exceed 5 weeks rent and must be protected in a government scheme',
                'references': ['Housing Act 2004', 'Tenant Fees Act 2019']
            },
            'unfair_repair_terms': {
                'patterns': [
                    r'tenant.*responsible.*all.*repair',
                    r'tenant.*maintain.*structure',
                    r'no.*landlord.*responsibility.*repair'
                ],
                'severity': 'high',
                'explanation': 'Landlord is legally responsible for most repairs',
                'references': ['Landlord and Tenant Act 1985 Section 11']
            },
            'notice_period_issues': {
                'patterns': [
                    r'leave.*without.*notice',
                    r'immediate.*eviction',
                    r'24.*hour.*notice'
                ],
                'severity': 'critical',
                'explanation': 'Minimum notice periods are legally required',
                'references': ['Housing Act 1988']
            },
            'prohibited_fees': {
                'patterns': [
                    r'fee.*for.*reference',
                    r'charge.*for.*viewing',
                    r'administration.*fee'
                ],
                'severity': 'high',
                'explanation': 'Most fees to tenants are now banned',
                'references': ['Tenant Fees Act 2019']
            }
        }
    
    def detect(self, text: str) -> List[Dict]:
        """
        Detect problematic patterns in document text
        
        Returns:
            [
                {
                    'issue': 'unfair_deposit',
                    'severity': 'high',
                    'matched_text': 'non-refundable deposit of £2000',
                    'explanation': '...',
                    'recommendations': ['...'],
                    'legal_references': ['...']
                },
                ...
            ]
        """
        detected_issues = []
        
        text_lower = text.lower()
        
        for issue_type, config in self.patterns.items():
            for pattern in config['patterns']:
                matches = re.finditer(pattern, text_lower, re.IGNORECASE)
                
                for match in matches:
                    detected_issues.append({
                        'issue': issue_type,
                        'severity': config['severity'],
                        'matched_text': match.group(0),
                        'position': match.span(),
                        'explanation': config['explanation'],
                        'legal_references': config['references'],
                        'recommendations': self._get_recommendations(issue_type)
                    })
        
        return detected_issues
    
    def _get_recommendations(self, issue_type: str) -> List[str]:
        """Generate recommendations based on detected issue"""
        recommendations = {
            'unfair_deposit': [
                'Check if deposit is protected in government scheme',
                'Ensure deposit does not exceed 5 weeks rent',
                'Contact Shelter or Citizens Advice for support'
            ],
            'unfair_repair_terms': [
                'Landlord must maintain structure and exterior',
                'Request written clarification of repair responsibilities',
                'Consult local council housing team'
            ],
            # ... more recommendations
        }
        return recommendations.get(issue_type, [])
```

### 3.3 Training Data Preparation

#### Data Collection Strategy

```
Training Data Sources:
1. Public Datasets:
   - UK Government example tenancy agreements
   - Court case documents (public domain)
   - Shelter example documents
   
2. Synthetic Data Generation:
   - Template-based generation
   - Variation with parameters
   - Augmentation with noise
   
3. Manual Annotation:
   - Label document types
   - Mark entities (names, dates, amounts)
   - Flag unfair clauses
   - Quality review by legal experts
```

#### Data Preparation Pipeline

```python
# ml_service/training/data_preparation.py
import pandas as pd
from sklearn.model_selection import train_test_split
import json

class DataPreparation:
    def __init__(self):
        self.documents = []
        
    def prepare_classification_data(self):
        """
        Prepare data for document classification
        
        Output format:
        {
            'text': [list of document texts],
            'labels': [list of categories],
            'metadata': [...]
        }
        """
        # Load raw documents
        raw_docs = self._load_documents()
        
        # Extract text and labels
        texts = []
        labels = []
        
        for doc in raw_docs:
            texts.append(doc['text'])
            labels.append(doc['category'])
        
        # Split train/val/test
        X_train, X_temp, y_train, y_temp = train_test_split(
            texts, labels, test_size=0.3, random_state=42
        )
        X_val, X_test, y_val, y_test = train_test_split(
            X_temp, y_temp, test_size=0.5, random_state=42
        )
        
        return {
            'train': {'texts': X_train, 'labels': y_train},
            'val': {'texts': X_val, 'labels': y_val},
            'test': {'texts': X_test, 'labels': y_test}
        }
    
    def prepare_ner_data(self):
        """
        Prepare data for NER training
        
        Output format (spaCy):
        [
            ("The landlord John Smith...", 
             {"entities": [(14, 24, "PERSON"), ...]}),
            ...
        ]
        """
        annotated_docs = self._load_annotated_documents()
        
        training_data = []
        for doc in annotated_docs:
            training_data.append((
                doc['text'],
                {'entities': doc['entities']}
            ))
        
        return training_data
    
    def augment_data(self, texts, labels, augmentation_factor=3):
        """
        Augment training data through:
        - Synonym replacement
        - Back-translation
        - Noise injection
        """
        augmented_texts = []
        augmented_labels = []
        
        for text, label in zip(texts, labels):
            # Original
            augmented_texts.append(text)
            augmented_labels.append(label)
            
            # Augmented versions
            for _ in range(augmentation_factor):
                aug_text = self._augment_text(text)
                augmented_texts.append(aug_text)
                augmented_labels.append(label)
        
        return augmented_texts, augmented_labels
```

### 3.4 Model Training Scripts

```python
# ml_service/training/train_classifier.py
import tensorflow as tf
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from data_preparation import DataPreparation
from models.document_classifier import build_document_classifier

def train_document_classifier():
    """
    Complete training pipeline for document classifier
    """
    # Prepare data
    prep = DataPreparation()
    data = prep.prepare_classification_data()
    
    # Tokenize
    tokenizer = tf.keras.preprocessing.text.Tokenizer(num_words=10000)
    tokenizer.fit_on_texts(data['train']['texts'])
    
    # Convert to sequences
    X_train = tokenizer.texts_to_sequences(data['train']['texts'])
    X_val = tokenizer.texts_to_sequences(data['val']['texts'])
    
    # Pad sequences
    X_train = tf.keras.preprocessing.sequence.pad_sequences(X_train, maxlen=500)
    X_val = tf.keras.preprocessing.sequence.pad_sequences(X_val, maxlen=500)
    
    # Encode labels
    from sklearn.preprocessing import LabelEncoder
    le = LabelEncoder()
    y_train = le.fit_transform(data['train']['labels'])
    y_val = le.transform(data['val']['labels'])
    
    # One-hot encode
    y_train = tf.keras.utils.to_categorical(y_train)
    y_val = tf.keras.utils.to_categorical(y_val)
    
    # Build model
    model = build_document_classifier()
    
    # Callbacks
    callbacks = [
        EarlyStopping(patience=5, restore_best_weights=True),
        ModelCheckpoint(
            'ml_models/document_classifier/best_model.h5',
            save_best_only=True
        )
    ]
    
    # Train
    history = model.fit(
        X_train, y_train,
        validation_data=(X_val, y_val),
        epochs=50,
        batch_size=32,
        callbacks=callbacks
    )
    
    # Save artifacts
    model.save('ml_models/document_classifier/')
    import pickle
    with open('ml_models/document_classifier/tokenizer.pkl', 'wb') as f:
        pickle.dump(tokenizer, f)
    with open('ml_models/document_classifier/label_encoder.pkl', 'wb') as f:
        pickle.dump(le, f)
    
    return history

if __name__ == '__main__':
    train_document_classifier()
```

### 3.5 ML Service Integration

```python
# app/services/ml_service.py
from app.ml.document_classifier import DocumentClassifier
from app.ml.ner_extractor import LegalNERExtractor
from app.ml.pattern_detector import PatternDetector
import pytesseract
from PIL import Image
import pdf2image

class MLService:
    classifier = DocumentClassifier()
    ner_extractor = LegalNERExtractor()
    pattern_detector = PatternDetector()
    
    @staticmethod
    def process_document(file_path, file_type):
        """
        Complete ML processing pipeline for uploaded document
        
        Steps:
        1. Extract text (OCR or PDF extraction)
        2. Classify document type
        3. Extract entities
        4. Detect patterns/issues
        5. Generate analysis
        
        Returns:
            {
                'extracted_text': '...',
                'document_type': 'section_21_notice',
                'confidence': 0.95,
                'entities': {...},
                'detected_issues': [...],
                'analysis': {...},
                'recommendations': [...]
            }
        """
        # Step 1: Text Extraction
        if file_type in ['jpg', 'png', 'jpeg']:
            text = MLService._ocr_extract(file_path)
        elif file_type == 'pdf':
            text = MLService._pdf_extract(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_type}")
        
        # Step 2: Classification
        classification = MLService.classifier.predict(text)
        
        # Step 3: Entity Extraction
        entities = MLService.ner_extractor.extract_entities(text)
        
        # Step 4: Pattern Detection
        issues = MLService.pattern_detector.detect(text)
        
        # Step 5: Generate Analysis
        analysis = MLService._generate_analysis(
            text, classification, entities, issues
        )
        
        return {
            'extracted_text': text,
            'document_type': classification['category'],
            'confidence': classification['confidence'],
            'entities': entities,
            'detected_issues': issues,
            'analysis': analysis,
            'recommendations': MLService._generate_recommendations(issues)
        }
    
    @staticmethod
    def _ocr_extract(image_path):
        """Extract text from image using Tesseract OCR"""
        image = Image.open(image_path)
        
        # Preprocess image
        image = MLService._preprocess_image(image)
        
        # Perform OCR
        text = pytesseract.image_to_string(image, lang='eng')
        
        return text
    
    @staticmethod
    def _preprocess_image(image):
        """Enhance image quality for better OCR"""
        import cv2
        import numpy as np
        
        # Convert to numpy array
        img = np.array(image)
        
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Apply thresholding
        thresh = cv2.threshold(
            gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
        )[1]
        
        # Denoise
        denoised = cv2.fastNlMeansDenoising(thresh)
        
        return Image.fromarray(denoised)
    
    @staticmethod
    def _pdf_extract(pdf_path):
        """Extract text from PDF"""
        import PyPDF2
        
        text = ""
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text += page.extract_text()
        
        # If PDF is scanned (no text), use OCR
        if len(text.strip()) < 100:
            images = pdf2image.convert_from_path(pdf_path)
            text = ""
            for image in images:
                text += MLService._ocr_extract(image)
        
        return text
    
    @staticmethod
    def _generate_analysis(text, classification, entities, issues):
        """
        Generate comprehensive legal analysis
        """
        analysis = {
            'summary': MLService._generate_summary(text, classification),
            'key_points': MLService._extract_key_points(text, entities),
            'risk_assessment': MLService._assess_risks(issues),
            'compliance_check': MLService._check_compliance(text, classification),
            'next_steps': MLService._suggest_next_steps(issues)
        }
        
        return analysis
    
    @staticmethod
    def analyze_legal_text(text, context=None):
        """
        Analyze pasted text without file upload
        Simpler version for chat interface
        """
        # Detect patterns
        issues = MLService.pattern_detector.detect(text)
        
        # Extract entities
        entities = MLService.ner_extractor.extract_entities(text)
        
        # Generate plain English summary
        summary = MLService._generate_plain_summary(text, issues, entities)
        
        # Get relevant laws
        relevant_laws = MLService._find_relevant_laws(text, issues)
        
        return {
            'summary': summary,
            'issues': issues,
            'entities': entities,
            'relevant_laws': relevant_laws,
            'confidence': MLService._calculate_confidence(issues, entities)
        }
```

---

## 4. Database Schema (MongoDB)

```javascript
// MongoDB Collections

// 1. users collection
{
  _id: ObjectId,
  email: String (unique, indexed),
  passwordHash: String,
  role: String (enum: ['user', 'admin', 'editor']),
  profile: {
    firstName: String,
    lastName: String,
    postcode: String
  },
  savedItems: [ObjectId], // references to topics
  createdAt: Date,
  updatedAt: Date,
  lastLogin: Date
}

// 2. topics collection (housing law content)
{
  _id: ObjectId,
  title: String,
  slug: String (unique, indexed),
  category: String (enum: ['repairs', 'deposits', 'eviction', 'rent', 'rights']),
  summary: String,
  body: String (markdown),
  tags: [String],
  sources: [{
    title: String,
    url: String,
    lastChecked: Date
  }],
  metadata: {
    views: Number,
    saves: Number,
    avgRating: Number
  },
  lastUpdated: Date,
  updatedBy: ObjectId (ref: users),
  createdAt: Date,
  published: Boolean
}

// 3. documents collection (uploaded documents)
{
  _id: ObjectId,
  userId: ObjectId (ref: users, indexed),
  fileName: String,
  fileType: String,
  fileSize: Number,
  storagePath: String,
  
  // ML Processing Results
  processing: {
    status: String (enum: ['pending', 'processing', 'completed', 'failed']),
    startedAt: Date,
    completedAt: Date,
    error: String
  },
  
  extractedText: String,
  
  classification: {
    documentType: String,
    confidence: Number,
    probabilities: Object
  },
  
  entities: {
    persons: [{
      text: String,
      role: String
    }],
    addresses: [String],
    dates: [String],
    amounts: [String],
    references: [String]
  },
  
  detectedIssues: [{
    issue: String,
    severity: String,
    matchedText: String,
    explanation: String,
    recommendations: [String],
    legalReferences: [String]
  }],
  
  analysis: {
    summary: String,
    keyPoints: [String],
    riskAssessment: Object,
    complianceCheck: Object,
    nextSteps: [String]
  },
  
  createdAt: Date,
  updatedAt: Date
}

// 4. agencies collection (local support)
{
  _id: ObjectId,
  name: String,
  type: String (enum: ['council', 'charity', 'legal_aid', 'advice_center']),
  contact: {
    phone: String,
    email: String,
    website: String
  },
  address: {
    street: String,
    city: String,
    postcode: String,
    coordinates: {
      lat: Number,
      lng: Number
    }
  },
  services: [String],
  openingHours: Object,
  lastVerified: Date,
  createdAt: Date
}

// 5. chat_sessions collection
{
  _id: ObjectId,
  userId: ObjectId (ref: users),
  messages: [{
    role: String (enum: ['user', 'assistant']),
    content: String,
    timestamp: Date,
    attachments: [{
      type: String,
      fileId: ObjectId (ref: documents)
    }]
  }],
  metadata: {
    topic: String,
    resolved: Boolean
  },
  createdAt: Date,
  updatedAt: Date
}

// 6. feedback collection
{
  _id: ObjectId,
  userId: ObjectId (ref: users),
  targetType: String (enum: ['topic', 'document_analysis', 'chat']),
  targetId: ObjectId,
  rating: Number (1-5),
  comment: String,
  helpful: Boolean,
  createdAt: Date
}

// 7. letters collection (generated letters)
{
  _id: ObjectId,
  userId: ObjectId (ref: users, indexed),
  letterType: String (enum: ['repair_request', 'deposit_return', 'complaint']),
  template: String,
  content: String,
  variables: Object,
  generatedAt: Date,
  downloaded: Boolean,
  downloadedAt: Date
}
```

### MongoDB Indexes

```javascript
// Create indexes for performance
db.users.createIndex({ email: 1 }, { unique: true })
db.topics.createIndex({ slug: 1 }, { unique: true })
db.topics.createIndex({ category: 1, published: 1 })
db.topics.createIndex({ tags: 1 })
db.documents.createIndex({ userId: 1, createdAt: -1 })
db.agencies.createIndex({ "address.postcode": 1 })
db.agencies.createIndex({ "address.coordinates": "2dsphere" })
db.chat_sessions.createIndex({ userId: 1, createdAt: -1 })
```

---

## 5. Deployment Architecture (Azure)

```
┌─────────────────────────────────────────────────────────────────┐
│                     AZURE CLOUD INFRASTRUCTURE                   │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Azure App Service (Frontend)                            │  │
│  │  - Angular application                                   │  │
│  │  - Static file serving                                   │  │
│  │  - Auto-scaling enabled                                  │  │
│  └──────────────────────────────────────────────────────────┘  │
│                              │                                   │
│                              │ HTTPS                            │
│                              ▼                                   │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Azure App Service (Backend)                             │  │
│  │  - Flask API                                             │  │
│  │  - Gunicorn workers                                      │  │
│  │  - Auto-scaling enabled                                  │  │
│  └──────────────────────────────────────────────────────────┘  │
│                              │                                   │
│             ┌────────────────┼────────────────┐                │
│             │                │                │                 │
│             ▼                ▼                ▼                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │  Azure VM    │  │  MongoDB     │  │  Azure       │         │
│  │  (ML Service)│  │  Atlas       │  │  Blob        │         │
│  │              │  │              │  │  Storage     │         │
│  │  - TensorFlow│  │  - M30 tier  │  │              │         │
│  │  - Models    │  │  - Replica   │  │  - Documents │         │
│  │  - OCR       │  │    Set       │  │  - Models    │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Azure Redis Cache                                        │  │
│  │  - Session storage                                        │  │
│  │  - API response caching                                   │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Azure Application Insights                               │  │
│  │  - Monitoring                                             │  │
│  │  - Logging                                                │  │
│  │  - Analytics                                              │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

### Deployment Configuration

```yaml
# docker-compose.yml (for local development)
version: '3.8'

services:
  frontend:
    build: ./frontend
    ports:
      - "4200:80"
    depends_on:
      - backend
    environment:
      - API_URL=http://backend:5000

  backend:
    build: ./backend
    ports:
      - "5000:5000"
    depends_on:
      - mongodb
      - redis
      - ml-service
    environment:
      - MONGODB_URI=mongodb://mongodb:27017/homerights
      - REDIS_URL=redis://redis:6379
      - ML_SERVICE_URL=http://ml-service:8501
      - JWT_SECRET_KEY=${JWT_SECRET_KEY}
    volumes:
      - ./backend:/app
      - ml_models:/app/ml_models

  ml-service:
    build: ./ml_service
    ports:
      - "8501:8501"
    volumes:
      - ml_models:/models
    environment:
      - MODEL_PATH=/models

  mongodb:
    image: mongo:6.0
    ports:
      - "27017:27017"
    volumes:
      - mongodb_data:/data/db

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

volumes:
  mongodb_data:
  ml_models:
```

```dockerfile
# backend/Dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Download spaCy model
RUN python -m spacy download en_core_web_sm

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "wsgi:app"]
```

```dockerfile
# frontend/Dockerfile
FROM node:18 as build

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build --prod

FROM nginx:alpine
COPY --from=build /app/dist/homerights /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

---

## 6. Security Implementation

### 6.1 Authentication & Authorization

```python
# app/services/auth_service.py
from flask_jwt_extended import create_access_token, create_refresh_token
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta

class AuthService:
    @staticmethod
    def register_user(email, password, first_name, last_name):
        """Register new user"""
        # Validate password strength
        if not AuthService._validate_password(password):
            raise ValueError("Password does not meet requirements")
        
        # Check if user exists
        if db.users.find_one({'email': email}):
            raise ValueError("Email already registered")
        
        # Create user
        user = {
            'email': email,
            'passwordHash': generate_password_hash(password),
            'role': 'user',
            'profile': {
                'firstName': first_name,
                'lastName': last_name
            },
            'savedItems': [],
            'createdAt': datetime.utcnow()
        }
        
        result = db.users.insert_one(user)
        
        # Generate tokens
        access_token = create_access_token(
            identity=str(result.inserted_id),
            expires_delta=timedelta(hours=1)
        )
        refresh_token = create_refresh_token(
            identity=str(result.inserted_id),
            expires_delta=timedelta(days=30)
        )
        
        return {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user': AuthService._serialize_user(user)
        }
    
    @staticmethod
    def login(email, password):
        """Authenticate user"""
        user = db.users.find_one({'email': email})
        
        if not user or not check_password_hash(user['passwordHash'], password):
            raise ValueError("Invalid credentials")
        
        # Update last login
        db.users.update_one(
            {'_id': user['_id']},
            {'$set': {'lastLogin': datetime.utcnow()}}
        )
        
        # Generate tokens
        access_token = create_access_token(
            identity=str(user['_id']),
            expires_delta=timedelta(hours=1)
        )
        refresh_token = create_refresh_token(
            identity=str(user['_id']),
            expires_delta=timedelta(days=30)
        )
        
        return {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user': AuthService._serialize_user(user)
        }
    
    @staticmethod
    def _validate_password(password):
        """
        Password requirements:
        - Min 8 characters
        - At least one uppercase
        - At least one lowercase
        - At least one number
        """
        if len(password) < 8:
            return False
        if not any(c.isupper() for c in password):
            return False
        if not any(c.islower() for c in password):
            return False
        if not any(c.isdigit() for c in password):
            return False
        return True
```

### 6.2 Rate Limiting

```python
# app/utils/rate_limiter.py
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="redis://localhost:6379"
)

# Apply to specific routes
@bp.route('/upload', methods=['POST'])
@limiter.limit("10 per hour")  # Strict limit for expensive operations
@jwt_required()
def upload_document():
    pass
```

### 6.3 Input Validation

```python
# app/utils/validators.py
from marshmallow import Schema, fields, validate, ValidationError

class DocumentUploadSchema(Schema):
    file = fields.Raw(required=True)
    document_type = fields.Str(
        validate=validate.OneOf([
            'tenancy_agreement',
            'section_21_notice',
            'section_8_notice',
            'repair_request',
            'other'
        ])
    )

class TextAnalysisSchema(Schema):
    text = fields.Str(
        required=True,
        validate=validate.Length(min=10, max=50000)
    )
    context = fields.Str()

def validate_request(schema):
    """Decorator for request validation"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                schema_instance = schema()
                data = schema_instance.load(request.get_json())
                request.validated_data = data
                return f(*args, **kwargs)
            except ValidationError as err:
                return jsonify({'errors': err.messages}), 400
        return decorated_function
    return decorator
```

---

## 7. Testing Strategy

### 7.1 Testing Structure

```
tests/
├── unit/
│   ├── test_models.py
│   ├── test_services.py
│   └── test_ml/
│       ├── test_classifier.py
│       ├── test_ner.py
│       └── test_pattern_detector.py
│
├── integration/
│   ├── test_api_endpoints.py
│   ├── test_ml_pipeline.py
│   └── test_database.py
│
├── e2e/
│   ├── test_user_flows.py
│   └── test_document_processing.py
│
└── performance/
    ├── test_api_performance.py
    └── test_ml_performance.py
```

### 7.2 Test Examples

```python
# tests/unit/test_services/test_document_service.py
import pytest
from app.services.document_service import DocumentService

class TestDocumentService:
    def test_process_pdf_document(self, sample_pdf):
        """Test PDF processing"""
        result = DocumentService.process_document(
            file=sample_pdf,
            user_id='test_user_id',
            document_type='tenancy_agreement'
        )
        
        assert result['status'] == 'success'
        assert 'extracted_text' in result
        assert len(result['extracted_text']) > 0
        assert 'classification' in result
    
    def test_invalid_file_type(self):
        """Test invalid file type handling"""
        with pytest.raises(ValueError):
            DocumentService.process_document(
                file='invalid.txt',
                user_id='test_user_id'
            )

# tests/unit/test_ml/test_classifier.py
import pytest
from app.ml.document_classifier import DocumentClassifier

class TestDocumentClassifier:
    @pytest.fixture
    def classifier(self):
        return DocumentClassifier()
    
    def test_section_21_classification(self, classifier, sample_section21_text):
        """Test Section 21 notice classification"""
        result = classifier.predict(sample_section21_text)
        
        assert result['category'] == 'section_21_notice'
        assert result['confidence'] > 0.8
    
    def test_tenancy_agreement_classification(self, classifier, sample_tenancy_text):
        """Test tenancy agreement classification"""
        result = classifier.predict(sample_tenancy_text)
        
        assert result['category'] == 'tenancy_agreement'
        assert result['confidence'] > 0.75

# tests/integration/test_api_endpoints.py
import pytest
from app import create_app

class TestDocumentAPI:
    @pytest.fixture
    def client(self):
        app = create_app('testing')
        return app.test_client()
    
    @pytest.fixture
    def auth_headers(self, client):
        """Get authentication headers"""
        response = client.post('/api/auth/login', json={
            'email': 'test@example.com',
            'password': 'TestPassword123'
        })
        token = response.json['access_token']
        return {'Authorization': f'Bearer {token}'}
    
    def test_upload_document(self, client, auth_headers, sample_pdf):
        """Test document upload endpoint"""
        response = client.post(
            '/api/documents/upload',
            data={'file': (sample_pdf, 'test.pdf')},
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json
        assert 'document_id' in data
        assert 'extracted_text' in data
        assert 'classification' in data
    
    def test_analyze_text(self, client, auth_headers):
        """Test text analysis endpoint"""
        response = client.post(
            '/api/documents/analyze',
            json={
                'text': 'The tenant must pay a non-refundable deposit of £3000.',
                'context': 'tenancy_agreement'
            },
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json
        assert 'summary' in data
        assert 'issues' in data
        assert len(data['issues']) > 0  # Should detect unfair deposit
```

---

## 8. Development Workflow

### 8.1 Git Workflow

```
main (production)
  ↑
develop (staging)
  ↑
feature/* (feature branches)
```

### 8.2 CI/CD Pipeline

```yaml
# .github/workflows/ci-cd.yml
name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

jobs:
  test-backend:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.10
    
    - name: Install dependencies
      run: |
        cd backend
        pip install -r requirements.txt
        pip install pytest pytest-cov
    
    - name: Run tests
      run: |
        cd backend
        pytest --cov=app tests/
    
    - name: Upload coverage
      uses: codecov/codecov-action@v2

  test-frontend:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Node.js
      uses: actions/setup-node@v2
      with:
        node-version: 18
    
    - name: Install dependencies
      run: |
        cd frontend
        npm ci
    
    - name: Run tests
      run: |
        cd frontend
        npm run test:ci
    
    - name: Build
      run: |
        cd frontend
        npm run build --prod

  deploy-staging:
    needs: [test-backend, test-frontend]
    if: github.ref == 'refs/heads/develop'
    runs-on: ubuntu-latest
    
    steps:
    - name: Deploy to Azure (Staging)
      run: |
        # Azure deployment commands
        
  deploy-production:
    needs: [test-backend, test-frontend]
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    
    steps:
    - name: Deploy to Azure (Production)
      run: |
        # Azure deployment commands
```

---

## 9. Monitoring & Analytics

### 9.1 Application Insights Setup

```python
# app/monitoring.py
from applicationinsights import TelemetryClient
from applicationinsights.flask.ext import AppInsights

def setup_monitoring(app):
    """Configure Application Insights"""
    app.config['APPINSIGHTS_INSTRUMENTATIONKEY'] = os.getenv('APPINSIGHTS_KEY')
    appinsights = AppInsights(app)
    
    tc = TelemetryClient(app.config['APPINSIGHTS_INSTRUMENTATIONKEY'])
    
    # Track custom events
    @app.before_request
    def before_request():
        tc.track_event('request_started', {
            'endpoint': request.endpoint,
            'method': request.method
        })
    
    @app.after_request
    def after_request(response):
        tc.track_event('request_completed', {
            'endpoint': request.endpoint,
            'status_code': response.status_code
        })
        return response
    
    # Track ML operations
    def track_ml_operation(operation_name, duration, success):
        tc.track_metric(f'ml_{operation_name}_duration', duration)
        tc.track_event(f'ml_{operation_name}', {'success': success})
```

### 9.2 Key Metrics

```python
# Metrics to track
METRICS = {
    'api_metrics': [
        'request_count',
        'request_duration',
        'error_rate',
        'active_users'
    ],
    'ml_metrics': [
        'document_processing_time',
        'classification_accuracy',
        'ocr_success_rate',
        'average_confidence_score'
    ],
    'business_metrics': [
        'documents_processed',
        'issues_detected',
        'topics_viewed',
        'support_requests'
    ]
}
```

---

## 10. Implementation Timeline

### Detailed Sprint Plan

**Sprint 0: Setup (Weeks 1-2)**
- Day 1-3: Environment setup, repository creation
- Day 4-7: Backend Flask skeleton, database connection
- Day 8-10: Frontend Angular setup, routing
- Day 11-14: CI/CD pipeline, Docker configuration

**Sprint 1: Core Content & Topics (Weeks 3-4)**
- Day 1-4: Topic API endpoints, CRUD operations
- Day 5-8: Admin CMS frontend
- Day 9-12: Seed initial housing law content
- Day 13-14: Testing and documentation

**Sprint 2: ML Foundation (Weeks 5-6)**
- Day 1-4: Data collection and preparation
- Day 5-10: Train document classifier
- Day 11-12: Train NER model
- Day 13-14: Pattern detector rules

**Sprint 3: Document Processing (Weeks 7-8)**
- Day 1-4: OCR integration (Tesseract)
- Day 5-8: PDF text extraction
- Day 9-12: ML service API
- Day 13-14: Testing with sample documents

**Sprint 4: Chat Interface (Weeks 9-10)**
- Day 1-5: Angular chat component (Claude-like UI)
- Day 6-10: Chat backend API
- Day 11-14: Document upload in chat

**Sprint 5: Analysis Features (Weeks 11-12)**
- Day 1-7: Text analysis endpoint
- Day 8-12: Pattern detection integration
- Day 13-14: Results visualization

**Sprint 6: Support & Letters (Week 13)**
- Day 1-4: Postcode lookup API
- Day 5-7: Letter generation

**Sprint 7: Testing & Deployment (Week 14)**
- Day 1-5: Comprehensive testing
- Day 6-10: Bug fixes
- Day 11-14: Production deployment

---

## 11. ML Model Training Guide

### Step-by-Step Training Process

**Step 1: Data Collection**
```bash
# Create directories
mkdir -p data/raw data/processed data/annotated

# Collect sample documents (manually or via scraping)
python scripts/collect_training_data.py --source gov_uk --output data/raw/
```

**Step 2: Data Annotation**
```bash
# Install annotation tool
pip install label-studio

# Start annotation server
label-studio start --port 8080

# Import documents and annotate:
# - Document categories
# - Named entities
# - Problematic clauses
```

**Step 3: Data Preprocessing**
```bash
# Preprocess annotated data
python ml_service/training/preprocess_data.py \
  --input data/annotated/ \
  --output data/processed/ \
  --split 0.7/0.15/0.15  # train/val/test split
```

**Step 4: Train Document Classifier**
```bash
# Train the model
python ml_service/training/train_classifier.py \
  --data data/processed/classification/ \
  --output ml_models/document_classifier/ \
  --epochs 50 \
  --batch-size 32

# Evaluate
python ml_service/training/evaluate_classifier.py \
  --model ml_models/document_classifier/ \
  --test-data data/processed/classification/test/
```

**Step 5: Train NER Model**
```bash
# Train NER with spaCy
python ml_service/training/train_ner.py \
  --data data/processed/ner/ \
  --output ml_models/legal_ner/ \
  --iterations 30

# Evaluate
python -m spacy evaluate ml_models/legal_ner/ data/processed/ner/test/
```

**Step 6: Export for Production**
```bash
# Convert models to production format
python ml_service/export_models.py \
  --classifier ml_models/document_classifier/ \
  --ner ml_models/legal_ner/ \
  --output ml_models/production/

# Test in production environment
python ml_service/test_production_models.py
```

---

## 12. API Documentation

### Complete API Specification

```yaml
# openapi.yml
openapi: 3.0.0
info:
  title: HomeRights AI API
  version: 1.0.0
  description: Legal document analysis API for UK housing rights

servers:
  - url: https://api.homerights.ai/v1
    description: Production server
  - url: http://localhost:5000/api
    description: Development server

paths:
  /auth/register:
    post:
      summary: Register new user
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                email:
                  type: string
                  format: email
                password:
                  type: string
                  minLength: 8
                firstName:
                  type: string
                lastName:
                  type: string
      responses:
        '201':
          description: User created
          content:
            application/json:
              schema:
                type: object
                properties:
                  access_token:
                    type: string
                  refresh_token:
                    type: string
                  user:
                    $ref: '#/components/schemas/User'

  /auth/login:
    post:
      summary: Login user
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                email:
                  type: string
                password:
                  type: string
      responses:
        '200':
          description: Login successful

  /documents/upload:
    post:
      summary: Upload and analyze document
      security:
        - bearerAuth: []
      requestBody:
        required: true
        content:
          multipart/form-data:
            schema:
              type: object
              properties:
                file:
                  type: string
                  format: binary
                document_type:
                  type: string
                  enum: [tenancy_agreement, section_21_notice, section_8_notice, other]
      responses:
        '200':
          description: Document processed
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/DocumentAnalysis'

  /documents/analyze:
    post:
      summary: Analyze pasted text
      security:
        - bearerAuth: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                text:
                  type: string
                context:
                  type: string
      responses:
        '200':
          description: Analysis completed
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/TextAnalysis'

components:
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT

  schemas:
    User:
      type: object
      properties:
        id:
          type: string
        email:
          type: string
        role:
          type: string
        profile:
          type: object

    DocumentAnalysis:
      type: object
      properties:
        document_id:
          type: string
        extracted_text:
          type: string
        document_type:
          type: string
        confidence:
          type: number
        entities:
          type: object
        detected_issues:
          type: array
          items:
            $ref: '#/components/schemas/DetectedIssue'
        analysis:
          type: object

    DetectedIssue:
      type: object
      properties:
        issue:
          type: string
        severity:
          type: string
          enum: [low, medium, high, critical]
        matched_text:
          type: string
        explanation:
          type: string
        recommendations:
          type: array
          items:
            type: string

    TextAnalysis:
      type: object
      properties:
        summary:
          type: string
        issues:
          type: array
          items:
            $ref: '#/components/schemas/DetectedIssue'
        relevant_laws:
          type: array
          items:
            type: object
```

---

## 13. Environment Variables

```bash
# .env.example

# Flask Configuration
FLASK_APP=wsgi.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-here

# Database
MONGODB_URI=mongodb://localhost:27017/homerights
REDIS_URL=redis://localhost:6379

# ML Service
ML_SERVICE_URL=http://localhost:8501
MODEL_PATH=/path/to/ml_models

# Azure Configuration
AZURE_STORAGE_CONNECTION_STRING=your-connection-string
AZURE_BLOB_CONTAINER=documents
APPINSIGHTS_INSTRUMENTATIONKEY=your-instrumentation-key

# External APIs
POSTCODE_API_KEY=your-api-key
GOOGLE_MAPS_API_KEY=your-api-key

# Email (for notifications)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-password

# Feature Flags
ENABLE_OCR=true
ENABLE_ML_CLASSIFICATION=true
ENABLE_PATTERN_DETECTION=true

# Rate Limiting
RATE_LIMIT_PER_MINUTE=60
RATE_LIMIT_PER_HOUR=1000
```

---

## 14. Quick Start Guide

### Prerequisites
```bash
# Install Python 3.10+
python --version

# Install Node.js 18+
node --version

# Install MongoDB
mongod --version

# Install Redis
redis-server --version

# Install Tesseract OCR
tesseract --version
```

### Setup Instructions

**1. Clone Repository**
```bash
git clone https://github.com/yourusername/homerights-ai.git
cd homerights-ai
```

**2. Backend Setup**
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_sm

# Setup environment
cp .env.example .env
# Edit .env with your configuration

# Initialize database
python scripts/init_db.py

# Run migrations
python scripts/migrate.py

# Seed initial data
python scripts/seed_data.py
```

**3. Frontend Setup**
```bash
cd frontend

# Install dependencies
npm install

# Setup environment
cp src/environments/environment.example.ts src/environments/environment.ts
# Edit environment.ts with your configuration
```

**4. ML Models Setup**
```bash
cd ml_service

# Download pre-trained models (if available)
python scripts/download_models.py

# OR train from scratch
python training/train_classifier.py
python training/train_ner.py
```

**5. Run Application**
```bash
# Terminal 1: Start MongoDB
mongod

# Terminal 2: Start Redis
redis-server

# Terminal 3: Start Backend
cd backend
source venv/bin/activate
flask run

# Terminal 4: Start Frontend
cd frontend
ng serve

# Terminal 5: Start ML Service (optional, for production)
cd ml_service
python serve.py
```

**6. Access Application**
- Frontend: http://localhost:4200
- Backend API: http://localhost:5000
- ML Service: http://localhost:8501

---

## 15. Troubleshooting Guide

### Common Issues

**Issue 1: MongoDB Connection Failed**
```bash
# Check MongoDB is running
sudo systemctl status mongod

# Restart if needed
sudo systemctl restart mongod

# Check connection string in .env
MONGODB_URI=mongodb://localhost:27017/homerights
```

**Issue 2: Tesseract OCR Not Found**
```bash
# Install Tesseract
# Ubuntu/Debian
sudo apt-get install tesseract-ocr

# macOS
brew install tesseract

# Windows
# Download from: https://github.com/UB-Mannheim/tesseract/wiki
```

**Issue 3: ML Models Not Loading**
```bash
# Check model paths
ls -la ml_models/

# Verify model files exist
python -c "import tensorflow as tf; print(tf.__version__)"

# Retrain if necessary
python ml_service/training/train_classifier.py
```

**Issue 4: CORS Errors**
```python
# Update backend CORS configuration
# app/__init__.py
CORS(app, origins=[
    'http://localhost:4200',
    'https://your-frontend-domain.com'
])
```

---

## Conclusion

This architecture provides a complete, production-ready system for HomeRights AI with:

✅ Modern tech stack (Flask + Angular + TensorFlow)
✅ Scalable ML pipeline for document analysis
✅ Claude-inspired user interface
✅ Comprehensive security measures
✅ Cloud-native deployment (Azure)
✅ Extensive testing coverage
✅ Clear development workflow

Next steps:
1. Set up development environment
2. Create repository and branch structure
3. Begin Sprint 0 (infrastructure setup)
4. Start collecting training data
5. Build MVP features iteratively

This architecture supports your academic project requirements while being extensible for future enhancements.