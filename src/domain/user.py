# Este é o arquivo onde definimos o domínio user, que é responsável por armazenar os usuários da aplicação.

class User:
    def __init__(self, email: str, password: str, nickname: str):
        self.email = email
        self.password = password
        self.nickname = nickname

    def __str__(self):
        return f"{self.email}: {self.nickname}"
    
    def __eq__(self, other):
        return self.email == other.email
    
    def __hash__(self):
        return hash(self.email)