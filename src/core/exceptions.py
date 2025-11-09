"""Custom exceptions for the application."""


class AgenticAIException(Exception):
    """Base exception for all custom exceptions."""
    
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class LLMException(AgenticAIException):
    """Exception raised for LLM-related errors."""
    
    def __init__(self, message: str = "LLM processing failed", status_code: int = 500):
        super().__init__(message, status_code)


class ToolException(AgenticAIException):
    """Exception raised for tool-related errors."""
    
    def __init__(self, message: str = "Tool execution failed", status_code: int = 500):
        super().__init__(message, status_code)


class GraphException(AgenticAIException):
    """Exception raised for graph-related errors."""
    
    def __init__(self, message: str = "Graph execution failed", status_code: int = 500):
        super().__init__(message, status_code)


class ConfigurationException(AgenticAIException):
    """Exception raised for configuration errors."""
    
    def __init__(self, message: str = "Configuration error", status_code: int = 500):
        super().__init__(message, status_code)


class AuthenticationException(AgenticAIException):
    """Exception raised for authentication errors."""
    
    def __init__(self, message: str = "Authentication failed", status_code: int = 401):
        super().__init__(message, status_code)


class ValidationException(AgenticAIException):
    """Exception raised for validation errors."""
    
    def __init__(self, message: str = "Validation failed", status_code: int = 422):
        super().__init__(message, status_code)


class RateLimitException(AgenticAIException):
    """Exception raised when rate limit is exceeded."""
    
    def __init__(self, message: str = "Rate limit exceeded", status_code: int = 429):
        super().__init__(message, status_code)
