def doc(docstring):
    """Декоратор: устанавливает docstring функции"""
    def decorator(func):
        func.__doc__ = docstring
        return func
    return decorator
