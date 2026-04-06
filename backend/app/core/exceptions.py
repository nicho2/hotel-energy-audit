class AppError(Exception):
    code = "APPLICATION_ERROR"
    message = "Application error"

    def __init__(self, message: str | None = None, field: str | None = None, details: dict | None = None):
        self.message = message or self.message
        self.field = field
        self.details = details or {}
        super().__init__(self.message)


class NotFoundError(AppError):
    code = "NOT_FOUND"
    message = "Resource not found"


class ValidationError(AppError):
    code = "VALIDATION_ERROR"
    message = "Validation error"


class BusinessRuleError(AppError):
    code = "BUSINESS_RULE_ERROR"
    message = "Business rule error"


class CalculationNotReadyError(AppError):
    code = "CALCULATION_NOT_READY"
    message = "Scenario cannot be calculated yet"


class UnauthorizedError(AppError):
    code = "UNAUTHORIZED"
    message = "Unauthorized"
