def first_or_default(sequence, condition, default=None):
    return next((item for item in sequence if condition(item)), default)
