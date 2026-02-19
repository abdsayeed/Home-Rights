"""
Retry strategies for resilient service calls
Implements exponential backoff and service-specific retry policies
"""
import time
import logging
from functools import wraps
from typing import Callable, Type, Tuple

logger = logging.getLogger(__name__)


class RetryStrategy:
    """
    Configurable retry strategy with exponential backoff
    """
    
    def __init__(
        self,
        max_attempts: int = 3,
        initial_delay: float = 1.0,
        max_delay: float = 60.0,
        exponential_base: float = 2.0,
        exceptions: Tuple[Type[Exception], ...] = (Exception,)
    ):
        self.max_attempts = max_attempts
        self.initial_delay = initial_delay
        self.max_delay = max_delay
        self.exponential_base = exponential_base
        self.exceptions = exceptions
    
    def __call__(self, func: Callable) -> Callable:
        """Decorator to add retry logic to a function"""
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            
            for attempt in range(1, self.max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                    
                except self.exceptions as e:
                    last_exception = e
                    
                    if attempt == self.max_attempts:
                        logger.error(
                            f"{func.__name__} failed after {self.max_attempts} attempts: {str(e)}",
                            exc_info=True
                        )
                        raise
                    
                    # Calculate delay with exponential backoff
                    delay = min(
                        self.initial_delay * (self.exponential_base ** (attempt - 1)),
                        self.max_delay
                    )
                    
                    logger.warning(
                        f"{func.__name__} attempt {attempt}/{self.max_attempts} failed: {str(e)}. "
                        f"Retrying in {delay:.2f}s..."
                    )
                    
                    time.sleep(delay)
            
            # Should never reach here, but just in case
            raise last_exception
        
        return wrapper


# Predefined retry strategies for different services
class RetryStrategies:
    """Common retry configurations"""
    
    # OCR processing - can be slow, allow more time
    OCR = RetryStrategy(
        max_attempts=3,
        initial_delay=2.0,
        max_delay=30.0,
        exponential_base=2.0,
        exceptions=(IOError, RuntimeError, TimeoutError)
    )
    
    # ML inference - fast but can fail, retry quickly
    ML_INFERENCE = RetryStrategy(
        max_attempts=5,
        initial_delay=0.5,
        max_delay=10.0,
        exponential_base=2.0,
        exceptions=(RuntimeError, ValueError)
    )
    
    # Database operations - retry quickly
    DATABASE = RetryStrategy(
        max_attempts=3,
        initial_delay=0.5,
        max_delay=5.0,
        exponential_base=2.0,
        exceptions=(ConnectionError, TimeoutError)
    )
    
    # External API calls - allow more time
    EXTERNAL_API = RetryStrategy(
        max_attempts=4,
        initial_delay=1.0,
        max_delay=20.0,
        exponential_base=2.0,
        exceptions=(ConnectionError, TimeoutError)
    )
    
    # File operations - retry quickly
    FILE_OPERATION = RetryStrategy(
        max_attempts=3,
        initial_delay=0.5,
        max_delay=5.0,
        exponential_base=2.0,
        exceptions=(IOError, OSError)
    )


def with_retry(
    max_attempts: int = 3,
    initial_delay: float = 1.0,
    max_delay: float = 60.0,
    exceptions: Tuple[Type[Exception], ...] = (Exception,)
):
    """
    Decorator factory for custom retry logic
    
    Usage:
        @with_retry(max_attempts=5, initial_delay=2.0)
        def my_function():
            # function code
    """
    strategy = RetryStrategy(
        max_attempts=max_attempts,
        initial_delay=initial_delay,
        max_delay=max_delay,
        exceptions=exceptions
    )
    return strategy
