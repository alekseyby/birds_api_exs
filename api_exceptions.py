import werkzeug.exceptions as exc


class BodyLengthIsNegative(exc.BadRequest):
    description = '\'body_length\' cannot be negative'


class TooManyParameters(exc.BadRequest):
    pass


class UnexpectedParameter(exc.BadRequest):
    pass


class UnexpectedParameterValue(exc.BadRequest):
    pass


class WingspanLengthIsNegative(exc.BadRequest):
    description = '\'wingspan_length\' cannot be negative'
