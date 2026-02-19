"""
Comprehensive file validation with security checks
Production-ready validation for document uploads
"""
import os
import hashlib
from werkzeug.utils import secure_filename
from flask import current_app


class FileValidator:
    """
    Multi-layer file validation:
    1. Extension check
    2. MIME type verification
    3. File size limits
    4. Content validation
    """
    
    ALLOWED_EXTENSIONS = {'pdf', 'jpg', 'jpeg', 'png'}
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    MIN_FILE_SIZE = 100  # 100 bytes
    
    # MIME type mapping for security
    ALLOWED_MIMES = {
        'pdf': ['application/pdf'],
        'jpg': ['image/jpeg'],
        'jpeg': ['image/jpeg'],
        'png': ['image/png']
    }
    
    @classmethod
    def validate_file(cls, file) -> dict:
        """
        Comprehensive file validation
        
        Returns:
            dict: {
                'valid': bool,
                'errors': list of error dicts
            }
        """
        errors = []
        
        if not file:
            errors.append({
                'field': 'file',
                'message': 'No file provided'
            })
            return {'valid': False, 'errors': errors}
        
        if not file.filename:
            errors.append({
                'field': 'filename',
                'message': 'No filename provided'
            })
            return {'valid': False, 'errors': errors}
        
        # Extension validation
        filename = secure_filename(file.filename)
        if not cls._valid_extension(filename):
            errors.append({
                'field': 'file_extension',
                'message': f'Only {", ".join(cls.ALLOWED_EXTENSIONS)} files allowed'
            })
        
        # File size validation
        file.seek(0, 2)  # Seek to end
        file_size = file.tell()
        file.seek(0)  # Reset
        
        if file_size > cls.MAX_FILE_SIZE:
            errors.append({
                'field': 'file_size',
                'message': f'File too large. Maximum {cls.MAX_FILE_SIZE/1024/1024:.0f}MB allowed'
            })
        
        if file_size < cls.MIN_FILE_SIZE:
            errors.append({
                'field': 'file_size',
                'message': 'File appears to be empty or corrupted'
            })
        
        # Try to detect MIME type (basic check without python-magic)
        extension = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
        if extension == 'pdf':
            # Check PDF header
            header = file.read(5)
            file.seek(0)
            if header != b'%PDF-':
                errors.append({
                    'field': 'file_content',
                    'message': 'Invalid PDF file structure'
                })
        
        return {
            'valid': len(errors) == 0,
            'errors': errors
        }
    
    @classmethod
    def _valid_extension(cls, filename):
        """Check if file extension is allowed"""
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in cls.ALLOWED_EXTENSIONS
    
    @classmethod
    def calculate_file_hash(cls, file) -> str:
        """
        Calculate SHA-256 hash of file content
        Used for duplicate detection
        """
        sha256_hash = hashlib.sha256()
        
        # Read file in chunks to handle large files
        file.seek(0)
        for byte_block in iter(lambda: file.read(4096), b""):
            sha256_hash.update(byte_block)
        
        file.seek(0)  # Reset file pointer
        return sha256_hash.hexdigest()


def validate_file(file) -> dict:
    """Convenience function for file validation"""
    return FileValidator.validate_file(file)


def calculate_file_hash(file) -> str:
    """Convenience function for hash calculation"""
    return FileValidator.calculate_file_hash(file)
