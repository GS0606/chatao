# Este arquivo define o serviço de autenticação da aplicação.
import logging
from service.cypher import CypherService
from service.user import UserService

class AuthService:
    def __init__(self, userService: UserService, cypherService: CypherService) -> None:
        self.userService = userService
        self.cypherService = cypherService

    def authenticate(self, email, password) -> str:
        try:
            user = self.userService.get_user(email)
 
            if user is None:
                return None
            
            cypthered_password = self.cypherService.cypher_password(password)

            if user.password == cypthered_password:
                return self.cypherService.create_token(email, cypthered_password)

        except Exception as e:
            logging.error(f"[AuthService] Error authenticating user: {e}")
            return None

    def validate_token(self, email: str, token: str) -> bool:
        try:
            user = self.userService.get_user(email)

            if user is None:
                logging.warning(f"[AuthService] User {email} not found")
                return False
            
            userToken = self.cypherService.create_token(user.email, user.password)

            if userToken == token:
                return True
            
        except Exception as e:
            logging.error(f"[AuthService] Error validating token: {e}")
            return