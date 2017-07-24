


class MerChantException(Exception):
    def __init__(self, merchantId, message):
        self.merchantId = merchantId
        self.message = message

    def __str__(self):
        t = 'Merchant: %s - %s' % self.merchantId, self.message

        return t


class UserLoginFailedException(Exception):
    def __init__(self, username, message):
        self.username = username
        self.message = message

    def __str__(self):
        t = 'User Login Failed: %s - %s' % self.username, self.message

        return t