# Este é o arquivo que define o serviço de usuários da aplicação.

from domain.user import User
from storage.user import UserStorage
from service.cypher import CypherService
import logging

class UserService:
    def __init__(self, user_storage: UserStorage, cypherService: CypherService) -> None:
        self.user_storage = user_storage
        self.cypherService = cypherService

    def add_user(self, email, password, nickname) -> None:
        try:
            cyphered_password = self.cypherService.cypher_password(password)
            user = User(email, cyphered_password, nickname)
            self.user_storage.add_user(user)
            logging.info(f"[UserService] User {email} added")
        except Exception as e:  
            logging.error(f"[UserService] Error adding user: {e}")
            return None

    def get_user(self, email) -> User:
        try:
            user = self.user_storage.get_user(email)
            if user:
                return user
            return None
        except Exception as e:
            logging.error(f"[UserService] Error getting user: {e}")
            return None        

    def get_all_users(self) -> list[User]:
        try:
            return self.user_storage.get_all_users()
        except Exception as e:
            logging.error(f"[UserService] Error getting all users: {e}")
            return None

    def update_user(self, email, password, nickname) -> bool:
        try:
            cyphered_password = self.cypherService.cypher_password(password)
            user = User(email, cyphered_password, nickname)
            return self.user_storage.update_user(user)
        except Exception as e:
            logging.error(f"[UserService] Error updating user: {e}")
            return False

    def delete_user(self, email) -> bool:
        try:
            return self.user_storage.delete_user(email)
        except Exception as e:
            logging.error(f"[UserService] Error deleting user: {e}")
            return False