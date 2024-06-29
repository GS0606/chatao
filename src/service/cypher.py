import logging
import base64

class CypherService:
    def __init__(self):
        pass
    
    def cypher_password(self, password) -> str:
        try:
            b = base64.b64encode(bytes(password, 'utf-8')) # bytes
            return b.decode('utf-8') # convert bytes to string
        except Exception as e:
            logging.error(f"[CypherService] Error cyphering password: {e}")
            return None

    def create_token(self, email, password) -> str:
        try:
            input = f"{email}:{password}"
            b = base64.b64encode(bytes(input, 'utf-8')) # bytes
            return b.decode('utf-8') # convert bytes to string
        except Exception as e:
            logging.error(f"[CypherService] Error creating token: {e}")
            return None    