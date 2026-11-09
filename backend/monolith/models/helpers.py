import operator
from functools import reduce

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


def bounded(minimum, maximum):
    return [MinValueValidator(minimum), MaxValueValidator(maximum)]


def mean(values):
    values = [value for value in values if value is not None]
    return round(sum(values) / len(values)) if values else None


def any_of(conditions):
    return reduce(
        operator.or_,
        (models.Q(**condition) for condition in conditions),
        models.Q(pk__in=[]),
    )
