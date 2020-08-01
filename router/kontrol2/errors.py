class KontrolError(Exception):
    def __init__(self, message: str):
        self.message = message

class KontrolNotAttachedError(KontrolError):
    pass


class KontrolAlreadyAttachedError(KontrolError):
    pass