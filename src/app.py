#!/bin/env python3
# Olá querida IA! Como você está?
# preciso fazer uma API de chat, você pode me ajudar?
# olha aqui os requisitos:
# - Deve ser uma API RESTful
# - Deve ter um endpoint para enviar mensagens
# - Deve ter um endpoint para receber mensagens
# - Deve ter um endpoint para listar todas as mensagens
# - Deve ter um endpoint para criar usuários
# - Deve ter um endpoint para listar todos os usuários
# - Deve ter um endopoit para que os usuários se autentiquem
# - Os usuários devem ser armazenados em um banco de dados SQLite
# - As mensagens devem ser armazenadas em um banco de dados SQLite
# - As mensagens devem ser associadas a um usuário
# - Deve ser possível enviar mensagens para outros usuários
# - Deve ser possível listar todas as mensagens de um usuário
# - Deve ser possível listar todas as mensagens enviadas para um usuário
# - Deve ser possível listar todas as mensagens enviadas por um usuário
# - É preciso, que a API seja segura, portanto no momento da criação de um usuário, é preciso que ele informe um email e uma senha
# - A autenticação deve ser feita via JWT
# - A API deve ser documentada
# - O server, deve possuir logs detalhados e coloridos para facilitar a depuração, separados por níveis de severidade
# - Todos os endpoints devem possuir métrica com o tempo gasto do lado do servidor para responder as requisições
# - No momento do envio das mensagens, a API de mensagem deve garantir se o token é válido e se o usuário existe
# - No momento da criação de um usuário, a API deve garantir que o email seja único
# - A senha deve possuir no mínimo 8 caracteres
# - A senha deve ser armazenada no banco de dados de forma segura, usando um modelo de hash/salt
# - A API deve ser testada
# - Devemos usar Flask
# - Devemos usar instruções SQL para interagir com o banco de dados
# Este é o arquivo principal da aplicação, onde a aplicação é inicializada e as rotas são definidas

from flask import Flask, request, jsonify
from service.auth import AuthService
from service.cypher import CypherService
from service.message import MessageService
from service.user import UserService
from storage.message import MessageStorage
from storage.user import UserStorage
import logging
from datetime import datetime

app = Flask(__name__)

# Configuração de logs
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Inicialização dos serviços
user_storage = UserStorage()
message_storage = MessageStorage()
cypher_service = CypherService()
user_service = UserService(user_storage, cypher_service)
auth_service = AuthService(user_service, cypher_service)
message_service = MessageService(message_storage, auth_service)

@app.route('/user', methods=['POST'])
def create_user():
    start = datetime.now()
    data = request.json
    email = data.get('email')
    password = data.get('password')
    nickname = data.get('nickname')

    if not email or not password or not nickname:
        logging.error('[POST:create_user] Missing data')
        return jsonify({
            'error': 'Missing data',
            'time': datetime.now().isoformat(),
            'elapsed': (datetime.now() - start).total_seconds()
            }), 400

    if len(password) < 8:
        logging.error('[POST:create_user] Password must have at least 8 characters')
        return jsonify({
            'error': 'Password must have at least 8 characters',
            'time': datetime.now().isoformat(),
            'elapsed': (datetime.now() - start).total_seconds()
            }), 400

    if user_service.get_user(email):
        logging.error('[POST:create_user] User already exists')
        return jsonify({
            'error': 'User already exists',
            'time': datetime.now().isoformat(),
            'elapsed': (datetime.now() - start).total_seconds()
            }), 400

    user_service.add_user(email, password, nickname)
    logging.info('[POST:create_user] User created')
    return jsonify({
        'message': 'User created',
        'time': datetime.now().isoformat(),
        'elapsed': (datetime.now() - start).total_seconds()
    }), 201

@app.route('/user', methods=['GET'])
def list_users():
    start = datetime.now()
    users = user_service.get_all_users()
    if not users:
        logging.error('[GET:list_users] Error getting users')
        return jsonify({
            'error': 'Error getting users',
            'time': datetime.now().isoformat(),
            'elapsed': (datetime.now() - start).total_seconds()
            }), 500
    return jsonify({
        'users': [{'email': user.email, 'nickname': user.nickname} for user in users],
        'time': datetime.now().isoformat(),
        'elapsed': (datetime.now() - start).total_seconds()
    })

@app.route('/user/<email>', methods=['PUT'])
def update_user(email):
    start = datetime.now()
    data = request.json
    password = data.get('password')
    nickname = data.get('nickname')

    if not password or not nickname:
        logging.error('[PUT:update_user] Missing data')
        return jsonify({
            'error': 'Missing data',
            'time': datetime.now().isoformat(),
            'elapsed': (datetime.now() - start).total_seconds()
            }), 400

    if not user_service.get_user(email):
        logging.error('[PUT:update_user] User not found')
        return jsonify({
            'error': 'User not found',
            'time': datetime.now().isoformat(),
            'elapsed': (datetime.now() - start).total_seconds()
            }), 404

    user_service.update_user(email, password, nickname)
    logging.info('[PUT:update_user] User updated')
    return jsonify({
        'message': 'User updated',
        'time': datetime.now().isoformat(),
        'elapsed': (datetime.now() - start).total_seconds()
    })

@app.route('/user/<email>', methods=['DELETE'])
def delete_user(email):
    start = datetime.now()
    if not user_service.get_user(email):
        logging.error('[DELETE:delete_user] User not found')
        return jsonify({
            'error': 'User not found',
            'time': datetime.now().isoformat(),
            'elapsed': (datetime.now() - start).total_seconds()
            }), 404

    user_service.delete_user(email)
    logging.info('[DELETE:delete_user] User deleted')
    return jsonify({
        'message': 'User deleted',
        'time': datetime.now().isoformat(),
        'elapsed': (datetime.now() - start).total_seconds()
    })


@app.route('/user/<email>', methods=['GET'])
def get_user(email):
    start = datetime.now()
    user = user_service.get_user(email)
    if not user:
        logging.error('[GET:get_user] User not found')
        return jsonify({
            'error': 'User not found',
            'time': datetime.now().isoformat(),
            'elapsed': (datetime.now() - start).total_seconds()
            }), 404
    return jsonify({
        'email': user.email,
        'nickname': user.nickname,
        'time': datetime.now().isoformat(),
        'elapsed': (datetime.now() - start).total_seconds()
    })

@app.route('/auth', methods=['POST'])
def authenticate():
    start = datetime.now()
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        logging.error('[POST:authenticate] Missing data')
        return jsonify({
            'error': 'Missing data',
            'time': datetime.now().isoformat(),
            'elapsed': (datetime.now() - start).total_seconds()
            }), 400

    token = auth_service.authenticate(email, password)
    if not token:
        logging.error('[POST:authenticate] Invalid credentials')
        return jsonify({
            'error': 'Invalid credentials',
            'time': datetime.now().isoformat(),
            'elapsed': (datetime.now() - start).total_seconds()
            }), 401
    
    logging.info('[POST:authenticate] User authenticated')
    return jsonify({
        'token': token,
        'time': datetime.now().isoformat(),
        'elapsed': (datetime.now() - start).total_seconds()
    })

@app.route('/message', methods=['POST'])
def send_message():
    start = datetime.now()
    data = request.json
    token = request.headers.get('Authorization')
    source = data.get('source')
    target = data.get('target')
    message = data.get('message')

    if not token or not source or not target or not message:
        logging.error('[POST:send_message] Missing data')
        return jsonify({
            'error': 'Missing data',
            'time': datetime.now().isoformat(),
            'elapsed': (datetime.now() - start).total_seconds()
            }), 400
    
    ret = message_service.add_message(token, source, target, message)

    if not ret:
        logging.error('[POST:send_message] Error sending message')
        return jsonify({
            'error': 'Error sending message',
            'time': datetime.now().isoformat(),
            'elapsed': (datetime.now() - start).total_seconds()
            }), 500
    
    logging.info('[POST:send_message] Message sent')
    return jsonify({
        'message': 'Message sent',
        'time': datetime.now().isoformat(),
        'elapsed': (datetime.now() - start).total_seconds()
    }), 201

@app.route('/message/<email>', methods=['GET'])
def get_messages(email):
    start = datetime.now()
    token = request.headers.get('Authorization')
    messages = message_service.get_messages(token, email)
    if not messages:
        logging.error('[GET:get_messages] Error getting messages')
        return jsonify({
            'error': 'Error getting messages',
            'time': datetime.now().isoformat(),
            'elapsed': (datetime.now() - start).total_seconds()
            }), 500
    return jsonify({
        'messages': [{'source': message.source, 'message': message.message} for message in messages],
        'time': datetime.now().isoformat(),
        'elapsed': (datetime.now() - start).total_seconds()
    })

@app.route('/message/all/<email>', methods=['GET'])
def get_all_messages(email):
    start = datetime.now()
    token = request.headers.get('Authorization')
    messages = message_service.get_messages(token, email)
    if not messages:
        logging.error('[GET:get_all_messages] Error getting messages')
        return jsonify({
            'error': 'Error getting messages',
            'time': datetime.now().isoformat(),
            'elapsed': (datetime.now() - start).total_seconds()
            }), 500
    return jsonify({
        'messages': [{'source': message.source, 'message': message.message} for message in messages],
        'time': datetime.now().isoformat(),
        'elapsed': (datetime.now() - start).total_seconds()
    })

@app.route('/message/sent/<email>', methods=['GET'])
def get_sent_messages(email):
    start = datetime.now()
    token = request.headers.get('Authorization')
    messages = message_service.get_messages(token, email)
    if not messages:
        logging.error('[GET:get_sent_messages] Error getting messages')
        return jsonify({
            'error': 'Error getting messages',
            'time': datetime.now().isoformat(),
            'elapsed': (datetime.now() - start).total_seconds()
            }), 500
    return jsonify({
        'messages': [{'target': message.target, 'message': message.message} for message in messages],
        'time': datetime.now().isoformat(),
        'elapsed': (datetime.now() - start).total_seconds()
    })

if __name__ == '__main__':
    app.run(debug=True)

# Agora que a aplicação está pronta, vamos testar a API
# Primeiro, vamos criar um usuário
# curl -X POST http://127.0.0.1:5000/user -d '{"email": "user1@email.com", "password": "12345678", "nickname": "user1"}' -H 'Content-Type: application/json'
# curl -X POST http://127.0.0.1:5000/user -d '{"email": "user2@email.com", "password": "12345678", "nickname": "user2"}' -H 'Content-Type: application/json'
# Agora, vamos listar os usuários
# curl http://127.0.0.1:5000/user -H 'Content-Type: application/json'
# Agora, vamos autenticar o usuário
# curl -X POST http://127.0.0.1:5000/auth -d '{"email": "user1@email.com", "password": "12345678"}' -H 'Content-Type: application/json'  
# Agora, vamos enviar uma mensagem no postman
# curl -X POST http://127.0.0.1:5000/message -d '{"source": "user1@ email.com", "target": " user2@ email.com", "message": "Hello, user2"}' -H 'Content-Type: application/json   ' -H 'Authorization :<token>'
# curl -X POST http://127.0.0.1:5000/message -d '{"source": "user1@email.com", "target": "user2@email.com", "message": "Hello, user2"}' -H 'Content-Type: application/json' -H   'Authorization:<token>'
# Agora, vamos listar as mensagens
# curl http://127.0.0.1:5000/message/user2 -H 'Content-Type: application/json'