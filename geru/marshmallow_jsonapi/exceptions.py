class BaseApiException(Exception):
    """
    Base Exception
    """

    def __init__(self, message, status=400, *args, **kwargs):
        super(BaseApiException, self).__init__(*args, **kwargs)
        self.message = {"error": message, "status": status}
