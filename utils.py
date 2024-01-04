def first_or_default(sequence, condition, default=None):
    return next((item for item in sequence if condition(item)), default)

import random
import string

def random_string(n: int) -> str:
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=n))