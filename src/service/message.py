# Este é o arquivo que define o serviço de mensagens da aplicação.

import logging
from domain.message import Message
from storage.message import MessageStorage
from service.auth import AuthService

class MessageService:
    def __init__(self, message_storage: MessageStorage, authService: AuthService) -> None:
        self.message_storage = message_storage
        self.authService = authService

    def add_message(self, token, source, target, message) -> bool:
        try:
            if not self.authService.validate_token(source, token):
                logging.error('[MessageService] Invalid token')
                return False

            data = Message(source, target, message)
            self.message_storage.add_message(data)
            logging.info(f'[MessageService] Message added-> {source} to {target}:{message}')
            return True
        except Exception as e:
            logging.error(f'[MessageService] Error adding message: {e}')
            return False

    def get_messages(self, token, target) -> list[Message]:
        try:
            if not self.authService.validate_token(target, token):
                logging.error(f'[MessageService] Invalid token {token} to target {target}')
                return None

            return self.message_storage.get_messages(target)
        except Exception as e:
            logging.error(f'[MessageService] Error getting messages: {e}')
            return None