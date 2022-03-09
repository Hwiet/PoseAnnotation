from collections.abc import Iterable

def linear(from_, to_, progress=0):
    """Linearly interpolate between two values. If 

    Args:
        from_ (float)
        to_ (float)
        progress (float, optional): A float between 0 and 1. Defaults to 0.
    """
    if progress > 1 or progress < 0:
        raise AttributeError('progress must be a float between 0 and 1')
    if isinstance(from_, int) or isinstance(from_, float):
        return _linear_value(from_, to_, progress)
    if len(from_) != len(to_):
        raise AttributeError(f'{from_} and {to_} cannot be interpolated')
        return None
    d = type(from_)(from_)
    for i in range(len(from_)):
        d[i] = _linear_value(from_[i], to_[i], progress)
    return d

def _linear_value(from_, to_, progress):
    return progress * (to_ - from_) + from_