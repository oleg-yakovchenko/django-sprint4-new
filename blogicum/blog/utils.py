def doc(docstring):
    """Декоратор: устанавливает docstring функции (см. StackOverflow 36091548)."""
    def decorator(func):
        func.__doc__ = docstring
        return func
    return decorator
