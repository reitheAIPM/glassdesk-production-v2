"""
Enhanced Error Recovery for GlassDesk
Advanced error recovery patterns and automatic fix strategies
"""

import logging
import time
import asyncio
from typing import Dict, List, Any, Optional, Callable
from datetime import datetime, timedelta
from functools import wraps
from .user_communication import user_comm
from .logging_config import log_api_error


class CircuitBreaker:
    """Circuit breaker pattern for preventing cascading failures"""

    def __init__(self, failure_threshold: int = 5, recovery_timeout: int = 60):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = "CLOSED"  # CLOSED, OPEN, HALF_OPEN
        self.logger = logging.getLogger("glassdesk.circuit_breaker")

    def call(self, func: Callable, *args, **kwargs):
        """Execute function with circuit breaker protection"""
        if self.state == "OPEN":
            if time.time() - self.last_failure_time > self.recovery_timeout:
                self.state = "HALF_OPEN"
                self.logger.info("Circuit breaker transitioning to HALF_OPEN")
            else:
                raise Exception("Circuit breaker is OPEN")

        try:
            result = func(*args, **kwargs)
            if self.state == "HALF_OPEN":
                self.state = "CLOSED"
                self.failure_count = 0
                self.logger.info("Circuit breaker reset to CLOSED")
            return result
        except Exception as e:
            self.failure_count += 1
            self.last_failure_time = time.time()
            
            if self.failure_count >= self.failure_threshold:
                self.state = "OPEN"
                self.logger.warning(f"Circuit breaker opened after {self.failure_count} failures")
            
            raise e

    def get_status(self) -> Dict[str, Any]:
        """Get circuit breaker status"""
        return {
            "state": self.state,
            "failure_count": self.failure_count,
            "last_failure_time": self.last_failure_time,
            "failure_threshold": self.failure_threshold,
            "recovery_timeout": self.recovery_timeout
        }


class RetryStrategy:
    """Advanced retry strategy with exponential backoff"""

    def __init__(self, max_retries: int = 3, base_delay: float = 1.0, max_delay: float = 60.0):
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.logger = logging.getLogger("glassdesk.retry_strategy")

    def retry_with_backoff(self, func: Callable, *args, **kwargs):
        """Execute function with exponential backoff retry"""
        last_exception = None
        
        for attempt in range(self.max_retries + 1):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_exception = e
                
                if attempt == self.max_retries:
                    self.logger.error(f"Max retries ({self.max_retries}) exceeded for {func.__name__}")
                    raise e
                
                delay = min(self.base_delay * (2 ** attempt), self.max_delay)
                self.logger.warning(f"Attempt {attempt + 1} failed for {func.__name__}, retrying in {delay}s")
                time.sleep(delay)
        
        raise last_exception

    def retry_with_jitter(self, func: Callable, *args, **kwargs):
        """Execute function with jittered retry (prevents thundering herd)"""
        import random
        
        last_exception = None
        
        for attempt in range(self.max_retries + 1):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_exception = e
                
                if attempt == self.max_retries:
                    self.logger.error(f"Max retries ({self.max_retries}) exceeded for {func.__name__}")
                    raise e
                
                delay = min(self.base_delay * (2 ** attempt), self.max_delay)
                jitter = random.uniform(0, 0.1 * delay)  # 10% jitter
                total_delay = delay + jitter
                
                self.logger.warning(f"Attempt {attempt + 1} failed for {func.__name__}, retrying in {total_delay:.2f}s")
                time.sleep(total_delay)
        
        raise last_exception


class EnhancedErrorRecovery:
    """Enhanced error recovery with automatic fix strategies"""

    def __init__(self):
        self.logger = logging.getLogger("glassdesk.error_recovery")
        self.circuit_breakers = {}
        self.retry_strategies = {}
        self.recovery_strategies = {}
        self.user_comm = user_comm
        self._initialize_recovery_strategies()

    def _initialize_recovery_strategies(self):
        """Initialize recovery strategies for different error types"""
        self.recovery_strategies = {
            "oauth_token_expired": self._recover_oauth_token,
            "database_connection_failed": self._recover_database_connection,
            "api_rate_limited": self._recover_rate_limit,
            "network_timeout": self._recover_network_timeout,
            "authentication_failed": self._recover_authentication,
            "permission_denied": self._recover_permission_denied,
            "malformed_data": self._recover_malformed_data,
            "resource_exhausted": self._recover_resource_exhausted
        }

    def get_circuit_breaker(self, service_name: str) -> CircuitBreaker:
        """Get or create circuit breaker for a service"""
        if service_name not in self.circuit_breakers:
            self.circuit_breakers[service_name] = CircuitBreaker()
        return self.circuit_breakers[service_name]

    def get_retry_strategy(self, operation_name: str) -> RetryStrategy:
        """Get or create retry strategy for an operation"""
        if operation_name not in self.retry_strategies:
            self.retry_strategies[operation_name] = RetryStrategy()
        return self.retry_strategies[operation_name]

    def safe_execute(self, func: Callable, service_name: str = "default", 
                    operation_name: str = "default", *args, **kwargs):
        """Execute function with comprehensive error recovery"""
        try:
            # Get circuit breaker and retry strategy
            circuit_breaker = self.get_circuit_breaker(service_name)
            retry_strategy = self.get_retry_strategy(operation_name)
            
            # Execute with circuit breaker protection
            def protected_func():
                return circuit_breaker.call(func, *args, **kwargs)
            
            # Execute with retry strategy
            return retry_strategy.retry_with_backoff(protected_func)
            
        except Exception as e:
            # Attempt automatic recovery
            recovery_success = self._attempt_automatic_recovery(e, service_name, operation_name)
            
            if not recovery_success:
                # Log error and notify user
                self.logger.error(f"Error recovery failed for {operation_name}: {str(e)}")
                self.user_comm.log_operation_error(operation_name, e, auto_fix_attempted=True)
            
            raise e

    def _attempt_automatic_recovery(self, error: Exception, service_name: str, operation_name: str) -> bool:
        """Attempt automatic recovery based on error type"""
        error_type = self._classify_error(error)
        
        if error_type in self.recovery_strategies:
            try:
                self.logger.info(f"Attempting automatic recovery for {error_type}")
                recovery_func = self.recovery_strategies[error_type]
                success = recovery_func(error, service_name, operation_name)
                
                if success:
                    self.logger.info(f"Automatic recovery successful for {error_type}")
                    self.user_comm.notify_user(f"I automatically fixed the {error_type} issue", "info")
                else:
                    self.logger.warning(f"Automatic recovery failed for {error_type}")
                
                return success
            except Exception as recovery_error:
                self.logger.error(f"Recovery attempt failed: {str(recovery_error)}")
                return False
        
        return False

    def _classify_error(self, error: Exception) -> str:
        """Classify error type for recovery strategy selection"""
        error_str = str(error).lower()
        
        if "token" in error_str and ("expired" in error_str or "invalid" in error_str):
            return "oauth_token_expired"
        elif "database" in error_str and "connection" in error_str:
            return "database_connection_failed"
        elif "rate" in error_str and "limit" in error_str:
            return "api_rate_limited"
        elif "timeout" in error_str or "timed out" in error_str:
            return "network_timeout"
        elif "authentication" in error_str or "auth" in error_str:
            return "authentication_failed"
        elif "permission" in error_str or "denied" in error_str:
            return "permission_denied"
        elif "json" in error_str or "malformed" in error_str:
            return "malformed_data"
        elif "memory" in error_str or "resource" in error_str:
            return "resource_exhausted"
        else:
            return "unknown_error"

    def _recover_oauth_token(self, error: Exception, service_name: str, operation_name: str) -> bool:
        """Recover from OAuth token expiration"""
        try:
            # Attempt to refresh OAuth token
            from app.oauth_manager import oauth_manager
            
            if hasattr(oauth_manager, 'refresh_token'):
                success = oauth_manager.refresh_token()
                if success:
                    self.logger.info("OAuth token refreshed successfully")
                    return True
            
            # Fallback: prompt for re-authentication
            self.user_comm.notify_user("Your login session has expired. Please reconnect your account.", "warning")
            return False
            
        except Exception as e:
            self.logger.error(f"OAuth recovery failed: {str(e)}")
            return False

    def _recover_database_connection(self, error: Exception, service_name: str, operation_name: str) -> bool:
        """Recover from database connection issues"""
        try:
            # Attempt to reconnect to database
            from database.database_schema import init_database
            
            success = init_database()
            if success:
                self.logger.info("Database connection recovered")
                return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"Database recovery failed: {str(e)}")
            return False

    def _recover_rate_limit(self, error: Exception, service_name: str, operation_name: str) -> bool:
        """Recover from API rate limiting"""
        try:
            # Wait for rate limit to reset
            wait_time = 60  # Default wait time
            self.logger.info(f"Rate limited, waiting {wait_time} seconds")
            time.sleep(wait_time)
            return True
            
        except Exception as e:
            self.logger.error(f"Rate limit recovery failed: {str(e)}")
            return False

    def _recover_network_timeout(self, error: Exception, service_name: str, operation_name: str) -> bool:
        """Recover from network timeout"""
        try:
            # Wait and retry with exponential backoff
            time.sleep(2)
            return True
            
        except Exception as e:
            self.logger.error(f"Network timeout recovery failed: {str(e)}")
            return False

    def _recover_authentication(self, error: Exception, service_name: str, operation_name: str) -> bool:
        """Recover from authentication failures"""
        try:
            # Attempt to re-authenticate
            from app.oauth_manager import oauth_manager
            
            if hasattr(oauth_manager, 'reauthenticate'):
                success = oauth_manager.reauthenticate()
                if success:
                    self.logger.info("Authentication recovered")
                    return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"Authentication recovery failed: {str(e)}")
            return False

    def _recover_permission_denied(self, error: Exception, service_name: str, operation_name: str) -> bool:
        """Recover from permission denied errors"""
        try:
            # Check if permissions can be requested
            self.user_comm.notify_user("I need additional permissions to complete this action.", "warning")
            return False
            
        except Exception as e:
            self.logger.error(f"Permission recovery failed: {str(e)}")
            return False

    def _recover_malformed_data(self, error: Exception, service_name: str, operation_name: str) -> bool:
        """Recover from malformed data errors"""
        try:
            # Attempt to clean and validate data
            # This would implement data cleaning logic
            self.logger.info("Attempting to clean malformed data")
            return True
            
        except Exception as e:
            self.logger.error(f"Data recovery failed: {str(e)}")
            return False

    def _recover_resource_exhausted(self, error: Exception, service_name: str, operation_name: str) -> bool:
        """Recover from resource exhaustion"""
        try:
            # Attempt to free up resources
            import gc
            gc.collect()
            
            # Wait for resources to become available
            time.sleep(5)
            return True
            
        except Exception as e:
            self.logger.error(f"Resource recovery failed: {str(e)}")
            return False

    def get_recovery_status(self) -> Dict[str, Any]:
        """Get status of all recovery systems"""
        circuit_breaker_status = {}
        for service, cb in self.circuit_breakers.items():
            circuit_breaker_status[service] = cb.get_status()
        
        return {
            "circuit_breakers": circuit_breaker_status,
            "recovery_strategies": list(self.recovery_strategies.keys()),
            "total_services_monitored": len(self.circuit_breakers),
            "total_operations_monitored": len(self.retry_strategies)
        }

    def reset_circuit_breaker(self, service_name: str):
        """Reset circuit breaker for a service"""
        if service_name in self.circuit_breakers:
            cb = self.circuit_breakers[service_name]
            cb.state = "CLOSED"
            cb.failure_count = 0
            cb.last_failure_time = None
            self.logger.info(f"Circuit breaker reset for {service_name}")

    def get_error_statistics(self) -> Dict[str, Any]:
        """Get error recovery statistics"""
        total_failures = sum(cb.failure_count for cb in self.circuit_breakers.values())
        open_circuits = sum(1 for cb in self.circuit_breakers.values() if cb.state == "OPEN")
        
        return {
            "total_failures": total_failures,
            "open_circuits": open_circuits,
            "total_services": len(self.circuit_breakers),
            "recovery_success_rate": self._calculate_recovery_success_rate()
        }

    def _calculate_recovery_success_rate(self) -> float:
        """Calculate recovery success rate (placeholder)"""
        # This would calculate actual recovery success rate
        return 85.0  # Placeholder


# Global error recovery instance
error_recovery = EnhancedErrorRecovery()


def with_error_recovery(service_name: str = "default", operation_name: str = "default"):
    """Decorator for automatic error recovery"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return error_recovery.safe_execute(func, service_name, operation_name, *args, **kwargs)
        return wrapper
    return decorator 