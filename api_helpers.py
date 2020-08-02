import api_exceptions as _exc


GET_BIRD_VALID_PARAMETERS = (
    'attribute',
    'limit',
    'offset',
    'order',
)

BIRD_VALID_ATTRIBUTES = (
    'species'
    'name',
    'color',
    'body_length',
    'wingspan',
)


def _validate_birds_select_kwar(key, value):
    if key == 'attribute' and value not in BIRD_VALID_ATTRIBUTES and value != '1':
        raise _exc.UnexpectedParameterValue(f'Got unexpected value {value!r} of {key!r} parameter')

    # Verify LIMIT and OFFSET are non-negative integers.
    if (key == 'limit' and value.upper() != 'ALL') or key == 'offset':
        try:
            value = float(value)
            if value % 1 or value < 0:
                raise ValueError
        except ValueError:
            raise _exc.UnexpectedParameterValue(f'Got unexpected value {value!r} of {key!r} parameter')

    if key == 'order' and value.upper() not in ('ASC', 'DESC'):
        raise _exc.UnexpectedParameterValue(f'Got unexpected value {value!r} of {key!r} parameter')


def validate_bird_select_parameters(params):
    if len(params) > 4:
        raise _exc.TooManyParameters(f'Request takes up to 4 parameters, got {len(params)}')
    for p, v in params.items():
        if p not in GET_BIRD_VALID_PARAMETERS:
            raise _exc.UnexpectedParameter(f'Got unexpected parameter {p!r}')
        _validate_birds_select_kwar(p, v)


def validate_bird_body_length_and_wingspan(bird_dict):
    if bird_dict['body_length'] < 0:
        raise _exc.BodyLengthIsNegative
    if bird_dict['wingspan'] < 0:
        raise _exc.WingspanLengthIsNegative


def validate_no_extra_parameters(bird_dict):
    if len(bird_dict) > 5:
        extra_params = ['\'' + k + '\'' for k in bird_dict.keys() if k.lower() not in BIRD_VALID_ATTRIBUTES]
        extra_params_as_string = ', '.join(extra_params)
        raise _exc.TooManyParameters(f'Got unexpected parameter(s) {extra_params_as_string}')