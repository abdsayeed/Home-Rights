"""
Metrics Collection for Prometheus
Tracks application performance and health metrics
"""
import time
import logging
from functools import wraps
from typing import Optional, Dict
from collections import defaultdict
from threading import Lock

logger = logging.getLogger(__name__)


class MetricsCollector:
    """
    Simple metrics collector for tracking application metrics
    
    In production, this would integrate with Prometheus client library.
    For now, provides in-memory metrics collection.
    """
    
    def __init__(self):
        self._counters = defaultdict(int)
        self._histograms = defaultdict(list)
        self._gauges = {}
        self._lock = Lock()
    
    def increment_counter(self, name: str, labels: Optional[Dict] = None, value: int = 1):
        """Increment a counter metric"""
        with self._lock:
            key = self._make_key(name, labels)
            self._counters[key] += value
            logger.debug(f"Counter {key} incremented to {self._counters[key]}")
    
    def observe_histogram(self, name: str, value: float, labels: Optional[Dict] = None):
        """Record a value in a histogram"""
        with self._lock:
            key = self._make_key(name, labels)
            self._histograms[key].append(value)
            logger.debug(f"Histogram {key} observed value {value}")
    
    def set_gauge(self, name: str, value: float, labels: Optional[Dict] = None):
        """Set a gauge value"""
        with self._lock:
            key = self._make_key(name, labels)
            self._gauges[key] = value
            logger.debug(f"Gauge {key} set to {value}")
    
    def increment_gauge(self, name: str, labels: Optional[Dict] = None, value: float = 1):
        """Increment a gauge value"""
        with self._lock:
            key = self._make_key(name, labels)
            self._gauges[key] = self._gauges.get(key, 0) + value
    
    def decrement_gauge(self, name: str, labels: Optional[Dict] = None, value: float = 1):
        """Decrement a gauge value"""
        with self._lock:
            key = self._make_key(name, labels)
            self._gauges[key] = self._gauges.get(key, 0) - value
    
    def get_metrics(self) -> Dict:
        """Get all collected metrics"""
        with self._lock:
            return {
                'counters': dict(self._counters),
                'histograms': {
                    k: {
                        'count': len(v),
                        'sum': sum(v),
                        'avg': sum(v) / len(v) if v else 0,
                        'min': min(v) if v else 0,
                        'max': max(v) if v else 0
                    }
                    for k, v in self._histograms.items()
                },
                'gauges': dict(self._gauges)
            }
    
    def reset(self):
        """Reset all metrics"""
        with self._lock:
            self._counters.clear()
            self._histograms.clear()
            self._gauges.clear()
            logger.info("Metrics reset")
    
    @staticmethod
    def _make_key(name: str, labels: Optional[Dict] = None) -> str:
        """Create a unique key from name and labels"""
        if not labels:
            return name
        
        label_str = ','.join(f"{k}={v}" for k, v in sorted(labels.items()))
        return f"{name}{{{label_str}}}"


# Global metrics collector instance
metrics = MetricsCollector()


# Metric names
class MetricNames:
    """Standard metric names"""
    
    # Counters
    DOCUMENT_UPLOADS_TOTAL = "document_uploads_total"
    ERRORS_TOTAL = "errors_total"
    API_REQUESTS_TOTAL = "api_requests_total"
    
    # Histograms
    OCR_PROCESSING_SECONDS = "ocr_processing_seconds"
    ML_INFERENCE_SECONDS = "ml_inference_seconds"
    API_REQUEST_DURATION_SECONDS = "api_request_duration_seconds"
    DOCUMENT_PROCESSING_SECONDS = "document_processing_seconds"
    
    # Gauges
    ACTIVE_PROCESSING_TASKS = "active_processing_tasks"
    CIRCUIT_BREAKER_STATE = "circuit_breaker_state"


def track_time(metric_name: str, labels: Optional[Dict] = None):
    """
    Decorator to track execution time
    
    Usage:
        @track_time(MetricNames.OCR_PROCESSING_SECONDS, {'engine': 'tesseract'})
        def process_ocr(image):
            # processing logic
            pass
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start = time.time()
            try:
                result = func(*args, **kwargs)
                duration = time.time() - start
                
                metrics.observe_histogram(metric_name, duration, labels)
                
                logger.debug(
                    f"{func.__name__} completed in {duration:.3f}s",
                    extra={'duration': duration, 'function': func.__name__}
                )
                
                return result
                
            except Exception as e:
                duration = time.time() - start
                
                # Track error
                error_labels = {
                    'service': func.__module__,
                    'error_type': type(e).__name__
                }
                metrics.increment_counter(MetricNames.ERRORS_TOTAL, error_labels)
                
                logger.error(
                    f"{func.__name__} failed after {duration:.3f}s: {str(e)}",
                    extra={'duration': duration, 'function': func.__name__},
                    exc_info=True
                )
                
                raise
        
        return wrapper
    return decorator


def track_counter(metric_name: str, labels: Optional[Dict] = None):
    """
    Decorator to increment counter on function call
    
    Usage:
        @track_counter(MetricNames.DOCUMENT_UPLOADS_TOTAL, {'status': 'success'})
        def upload_document():
            # upload logic
            pass
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                metrics.increment_counter(metric_name, labels)
                return result
            except Exception as e:
                error_labels = labels.copy() if labels else {}
                error_labels['status'] = 'error'
                metrics.increment_counter(metric_name, error_labels)
                raise
        
        return wrapper
    return decorator


class GaugeContext:
    """
    Context manager for tracking active tasks
    
    Usage:
        with GaugeContext(MetricNames.ACTIVE_PROCESSING_TASKS):
            # processing logic
            pass
    """
    
    def __init__(self, metric_name: str, labels: Optional[Dict] = None):
        self.metric_name = metric_name
        self.labels = labels
    
    def __enter__(self):
        metrics.increment_gauge(self.metric_name, self.labels)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        metrics.decrement_gauge(self.metric_name, self.labels)


# Convenience functions for common metrics

def track_document_upload(status: str, document_type: str = 'unknown'):
    """Track document upload"""
    metrics.increment_counter(
        MetricNames.DOCUMENT_UPLOADS_TOTAL,
        {'status': status, 'document_type': document_type}
    )


def track_api_request(endpoint: str, method: str, status: int, duration: float):
    """Track API request"""
    metrics.increment_counter(
        MetricNames.API_REQUESTS_TOTAL,
        {'endpoint': endpoint, 'method': method, 'status': str(status)}
    )
    metrics.observe_histogram(
        MetricNames.API_REQUEST_DURATION_SECONDS,
        duration,
        {'endpoint': endpoint, 'method': method}
    )


def track_error(service: str, error_type: str):
    """Track error occurrence"""
    metrics.increment_counter(
        MetricNames.ERRORS_TOTAL,
        {'service': service, 'error_type': error_type}
    )


def get_all_metrics() -> Dict:
    """Get all collected metrics"""
    return metrics.get_metrics()


def reset_metrics():
    """Reset all metrics"""
    metrics.reset()
