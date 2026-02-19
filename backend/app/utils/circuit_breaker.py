"""
Circuit Breaker Pattern Implementation
Prevents cascading failures by failing fast when services are unavailable
"""
import time
import logging
from functools import wraps
from enum import Enum
from threading import Lock

logger = logging.getLogger(__name__)


class CircuitState(Enum):
    """Circuit breaker states"""
    CLOSED = "closed"  # Normal operation
    OPEN = "open"  # Service unavailable, fail fast
    HALF_OPEN = "half_open"  # Testing if service recovered


class CircuitBreakerError(Exception):
    """Raised when circuit breaker is open"""
    pass


class ServiceUnavailableException(Exception):
    """Raised when service is temporarily unavailable"""
    pass


class CircuitBreaker:
    """
    Circuit breaker for external service calls
    
    Prevents cascading failures by:
    - Tracking failure rate
    - Opening circuit after threshold
    - Allowing periodic recovery attempts
    - Closing circuit when service recovers
    """
    
    def __init__(
        self,
        failure_threshold: int = 5,
        recovery_timeout: int = 60,
        expected_exception: type = Exception,
        name: str = "unnamed"
    ):
        """
        Initialize circuit breaker
        
        Args:
            failure_threshold: Number of failures before opening circuit
            recovery_timeout: Seconds to wait before attempting recovery
            expected_exception: Exception type to catch
            name: Circuit breaker name for logging
        """
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.expected_exception = expected_exception
        self.name = name
        
        self.failure_count = 0
        self.last_failure_time = None
        self.state = CircuitState.CLOSED
        self.lock = Lock()
    
    def __call__(self, func):
        """Decorator to wrap function with circuit breaker"""
        @wraps(func)
        def wrapper(*args, **kwargs):
            return self.call(func, *args, **kwargs)
        return wrapper
    
    def call(self, func, *args, **kwargs):
        """
        Execute function with circuit breaker protection
        
        Raises:
            CircuitBreakerError: When circuit is open
            ServiceUnavailableException: When service is unavailable
        """
        with self.lock:
            # Check if circuit should transition to half-open
            if self.state == CircuitState.OPEN:
                if self._should_attempt_reset():
                    logger.info(
                        f"Circuit breaker '{self.name}' transitioning to HALF_OPEN"
                    )
                    self.state = CircuitState.HALF_OPEN
                else:
                    logger.warning(
                        f"Circuit breaker '{self.name}' is OPEN. "
                        f"Service unavailable."
                    )
                    raise ServiceUnavailableException(
                        f"{self.name} temporarily unavailable. "
                        f"Try again in {self._time_until_retry():.0f}s"
                    )
        
        # Attempt to call the function
        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
            
        except self.expected_exception as e:
            self._on_failure()
            raise
    
    def _should_attempt_reset(self) -> bool:
        """Check if enough time has passed to attempt recovery"""
        if self.last_failure_time is None:
            return True
        
        elapsed = time.time() - self.last_failure_time
        return elapsed >= self.recovery_timeout
    
    def _time_until_retry(self) -> float:
        """Calculate seconds until next retry attempt"""
        if self.last_failure_time is None:
            return 0
        
        elapsed = time.time() - self.last_failure_time
        return max(0, self.recovery_timeout - elapsed)
    
    def _on_success(self):
        """Handle successful call"""
        with self.lock:
            if self.state == CircuitState.HALF_OPEN:
                logger.info(
                    f"Circuit breaker '{self.name}' recovered. "
                    f"Transitioning to CLOSED"
                )
            
            self.failure_count = 0
            self.state = CircuitState.CLOSED
    
    def _on_failure(self):
        """Handle failed call"""
        with self.lock:
            self.failure_count += 1
            self.last_failure_time = time.time()
            
            if self.failure_count >= self.failure_threshold:
                if self.state != CircuitState.OPEN:
                    logger.error(
                        f"Circuit breaker '{self.name}' OPENED after "
                        f"{self.failure_count} failures"
                    )
                    self.state = CircuitState.OPEN
            else:
                logger.warning(
                    f"Circuit breaker '{self.name}' failure "
                    f"{self.failure_count}/{self.failure_threshold}"
                )
    
    def reset(self):
        """Manually reset circuit breaker"""
        with self.lock:
            logger.info(f"Circuit breaker '{self.name}' manually reset")
            self.failure_count = 0
            self.last_failure_time = None
            self.state = CircuitState.CLOSED
    
    def get_state(self) -> dict:
        """Get current circuit breaker state"""
        with self.lock:
            return {
                'name': self.name,
                'state': self.state.value,
                'failure_count': self.failure_count,
                'failure_threshold': self.failure_threshold,
                'time_until_retry': self._time_until_retry() if self.state == CircuitState.OPEN else 0
            }


# Pre-configured circuit breakers for common services
ocr_circuit_breaker = CircuitBreaker(
    failure_threshold=5,
    recovery_timeout=120,
    expected_exception=Exception,
    name="OCR Service"
)

ml_circuit_breaker = CircuitBreaker(
    failure_threshold=3,
    recovery_timeout=60,
    expected_exception=Exception,
    name="ML Service"
)

database_circuit_breaker = CircuitBreaker(
    failure_threshold=5,
    recovery_timeout=30,
    expected_exception=Exception,
    name="Database"
)
