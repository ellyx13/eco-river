

class UnicornException(Exception):
    def __init__(self, status_code:int, status: str, message: str):
        self.status_code = status_code
        self.status = status
        self.message = message