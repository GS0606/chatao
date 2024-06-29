# Este é o arquivo onde definimos o domínio message, que é responsável por armazenar as mensagens enviadas pelos usuários.

from datetime import datetime

class Message:
    def __init__(self, source, target, message) -> None:
        self.source = source
        self.target = target
        self.message = message
        self.when = datetime.now()

    def __str__(self) -> str:
        return f"[{self.when}] {self.source} -> {self.target}: {self.message}"