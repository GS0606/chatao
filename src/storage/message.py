# Neste arquivo, codificamos a lógica de armazenamento de dados de mensagens.

from domain.message import Message
import logging
import sqlite3

class MessageStorage:
    def __init__(self) -> None:
        try:
            #cria conexão com um banco de dados SQLite3
            self.connection = sqlite3.connect('message.db', check_same_thread=False)
            self.cursor = self.connection.cursor()
            #cria a tabela de mensagens
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS messages (
                    source TEXT,
                    target TEXT,
                    message TEXT,
                    created_at TEXT NOT NULL DEFAULT current_timestamp
                )
            ''')
            self.connection.commit()
            logging.info('[MessageStorage] Message table created')
        except sqlite3.Error as e:
            logging.error(f'[MessageStorage] Error creating message table: {e}')

    def add_message(self, message) -> None:
        try:
            #insere uma mensagem no banco de dados
            self.cursor.execute('''
                INSERT INTO messages (source, target, message)
                VALUES (?, ?, ?)
            ''', (message.source, message.target, message.message))
            self.connection.commit()
            logging.info('[MessageStorage] Message added')
        except sqlite3.Error as e:
            logging.error(f'[MessageStorage] Error adding message: {e}')

    def get_messages(self, target) -> list[Message]:
        try:
            #busca todas as mensagens no banco de dados
            self.cursor.execute('''
                SELECT source, target, message
                FROM messages
                WHERE target = ?
            ''', (target,))
            return [Message(*message) for message in self.cursor.fetchall()]
        except sqlite3.Error as e:
            logging.error(f'[MessageStorage] SQLite - Error getting messages: {e}')
        except Exception as e:
            logging.error(f'[MessageStorage] Error getting messages: {e}')
            return None
