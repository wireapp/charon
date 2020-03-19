import hashlib
import hmac
import logging

logger = logging.getLogger(__name__)


class SigningService:
    def __init__(self, secret: str):
        self.secret = secret

    def generate_signature(self, timestamp: int, payload: bytes) -> str:
        logger.info('Signing payload.')

        req = str.encode('v0:' + str(timestamp) + ':') + payload
        request_hash = 'v0=' + hmac.new(
            str.encode(self.secret),
            req, hashlib.sha256
        ).hexdigest()
        return request_hash
