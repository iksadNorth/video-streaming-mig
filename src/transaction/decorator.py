from functools import wraps


def synchronized_method(func):
    """객체 단위로 lock을 유지하는 데코레이터"""
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        with self.lock:  # 객체 단위 Lock 적용
            return func(self, *args, **kwargs)
    return wrapper
