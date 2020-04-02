import hashlib
import hmac
import logging

logger = logging.getLogger(__name__)


class SigningService:
    def __init__(self, secret: str):
        self.secret = secret

    def generate_signature(self, timestamp: int, payload: bytes) -> str:
        logger.debug('Signing payload.')

        req = f'v0:{str(timestamp)}:'.encode('utf-8') + payload
        signature = 'v0=' + hmac.new(self.secret.encode('utf-8'), req, hashlib.sha256).hexdigest()
        logger.debug(f'Signature {signature}')
        return signature
