"""
=======================
Random Library
=======================
"""

import random
import string


def random_str(length=16, only_digits=False):
    """
    create random string
    :return: string
    """

    choices = string.digits
    if not only_digits:
        choices += string.ascii_uppercase

    return ''.join(random.SystemRandom().choice(choices)
                   for _ in range(length))


def random_number(length=6):
    return random_str(length, only_digits=True)
