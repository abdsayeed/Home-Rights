"""
Structured logging configuration for production
Provides JSON-formatted logs with trace context
"""
import logging
import json
import sys
from datetime import datetime
from typing import Optional


class StructuredFormatter(logging.Formatter):
    """
    JSON formatter for structured logging
    Adds standard fields for log aggregation and analysis
    """
    
    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON"""
        
        # Base log structure
        log_data = {
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'service': 'homerights-ai',
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno
        }
        
        # Add trace context if available
        if hasattr(record, 'trace_id'):
            log_data['trace_id'] = record.trace_id
        if hasattr(record, 'document_id'):
            log_data['document_id'] = record.document_id
        if hasattr(record, 'user_id'):
            log_data['user_id'] = record.user_id
        if hasattr(record, 'request_id'):
            log_data['request_id'] = record.request_id
        
        # Add exception info if present
        if record.exc_info:
            log_data['exception'] = {
                'type': record.exc_info[0].__name__,
                'message': str(record.exc_info[1]),
                'traceback': self.formatException(record.exc_info)
            }
        
        # Add extra fields
        if hasattr(record, 'extra_data'):
            log_data['extra'] = record.extra_data
        
        return json.dumps(log_data)


class SimpleFormatter(logging.Formatter):
    """
    Human-readable formatter for development
    """
    
    def format(self, record: logging.LogRecord) -> str:
        """Format log record for console"""
        timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        
        # Color codes for different log levels
        colors = {
            'DEBUG': '\033[36m',      # Cyan
            'INFO': '\033[32m',       # Green
            'WARNING': '\033[33m',    # Yellow
            'ERROR': '\033[31m',      # Red
            'CRITICAL': '\033[35m'    # Magenta
        }
        reset = '\033[0m'
        
        color = colors.get(record.levelname, '')
        
        message = f"{timestamp} {color}{record.levelname:8}{reset} [{record.name}] {record.getMessage()}"
        
        # Add trace context if available
        context_parts = []
        if hasattr(record, 'document_id'):
            context_parts.append(f"doc={record.document_id[:8]}")
        if hasattr(record, 'user_id'):
            context_parts.append(f"user={record.user_id[:8]}")
        
        if context_parts:
            message += f" ({', '.join(context_parts)})"
        
        # Add exception if present
        if record.exc_info:
            message += '\n' + self.formatException(record.exc_info)
        
        return message


def setup_logging(
    level: str = 'INFO',
    json_format: bool = False,
    log_file: Optional[str] = None
):
    """
    Configure application logging
    
    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        json_format: Use JSON format (True for production, False for development)
        log_file: Optional file path for file logging
    """
    
    # Remove existing handlers
    root_logger = logging.getLogger()
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # Set level
    log_level = getattr(logging, level.upper(), logging.INFO)
    root_logger.setLevel(log_level)
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    
    if json_format:
        console_handler.setFormatter(StructuredFormatter())
    else:
        console_handler.setFormatter(SimpleFormatter())
    
    root_logger.addHandler(console_handler)
    
    # File handler for errors (always JSON format)
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.ERROR)
        file_handler.setFormatter(StructuredFormatter())
        root_logger.addHandler(file_handler)
    
    # Configure specific loggers
    logging.getLogger('werkzeug').setLevel(logging.WARNING)
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    
    logging.info(f"Logging configured: level={level}, json_format={json_format}")


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger with the specified name
    
    Usage:
        logger = get_logger(__name__)
        logger.info("Message", extra={'document_id': doc_id})
    """
    return logging.getLogger(name)


class LogContext:
    """
    Context manager for adding trace context to logs
    
    Usage:
        with LogContext(document_id=doc_id, user_id=user_id):
            logger.info("Processing document")
    """
    
    def __init__(self, **context):
        self.context = context
        self.old_factory = None
    
    def __enter__(self):
        self.old_factory = logging.getLogRecordFactory()
        
        def record_factory(*args, **kwargs):
            record = self.old_factory(*args, **kwargs)
            for key, value in self.context.items():
                setattr(record, key, value)
            return record
        
        logging.setLogRecordFactory(record_factory)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        logging.setLogRecordFactory(self.old_factory)
