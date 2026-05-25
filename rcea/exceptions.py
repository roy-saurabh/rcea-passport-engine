class RCEAError(Exception):
    pass


class RuleMatchError(RCEAError):
    pass


class TraceabilityError(RCEAError):
    pass


class SchemaValidationError(RCEAError):
    pass


class LimitationPropagationError(RCEAError):
    pass


class SuppressionLogError(RCEAError):
    pass


class ReproducibilityError(RCEAError):
    pass


class UnsupportedClaimError(RCEAError):
    pass
