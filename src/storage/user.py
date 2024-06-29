# Neste arquivo, codificamos a lógica de armazenamento de dados de usuários.

from domain.user import User
import sqlite3
import logging

class UserStorage:
    def __init__(self) -> None:
        #cria conexão com um banco de dados SQLite3
        try:
            self.connection = sqlite3.connect('user.db', check_same_thread=False)
            self.cursor = self.connection.cursor()
            #cria a tabela de usuários
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    email TEXT PRIMARY KEY,
                    password TEXT,
                    nickname TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP                            
                )
            ''')        
            self.connection.commit()        
            logging.info('[UserStorage] User table created')
        except sqlite3.Error as e:
            logging.error(f'[UserStorage] Error creating user table: {e}')

    def add_user(self, user) -> None:
        try:
            #insere um usuário no banco de dados
            self.cursor.execute('''
                INSERT INTO users (email, password, nickname)
                VALUES (?, ?, ?)
            ''', (user.email, user.password, user.nickname))
            self.connection.commit()
            logging.info(f'[UserStorage] User {user.email} added')
        except sqlite3.Error as e:
            logging.error(f'[UserStorage] Error adding user: {e}')

    def get_user(self, email) -> User:
        try:
            #busca um usuário no banco de dados
            self.cursor.execute('''
                SELECT email, password, nickname
                FROM users
                WHERE email = ?
            ''', (email,))
            user = self.cursor.fetchone()
            if user:
                return User(*user)
            return None
        except sqlite3.Error as e:
            logging.error(f'[UserStorage] Error getting user: {e}')

    def get_all_users(self) -> list[User]:
        try:
            #busca todos os usuários no banco de dados
            self.cursor.execute('''
                SELECT email, password, nickname
                FROM users
            ''')
            return [User(*user) for user in self.cursor.fetchall()]
        except sqlite3.Error as e:
            logging.error(f'[UserStorage] Error getting all users: {e}')

    def update_user(self, user) -> bool:
        try:
            #atualiza um usuário no banco de dados
            self.cursor.execute('''
                UPDATE users
                SET password = ?, nickname = ?
                WHERE email = ?
            ''', (user.password, user.nickname, user.email))
            self.connection.commit()
            logging.info(f'[UserStorage] User {user.email} updated')
            return True
        except sqlite3.Error as e:
            logging.error(f'[UserStorage] Error updating user: {e}')
            return False

    def delete_user(self, email) -> bool:
        try:
            #deleta um usuário no banco de dados
            self.cursor.execute('''
                DELETE FROM users
                WHERE email = ?
            ''', (email,))
            self.connection.commit()
            logging.info(f'[UserStorage] User {email} deleted')
            return True
        except sqlite3.Error as e:
            logging.error(f'[UserStorage] Error deleting user: {e}')
            return False