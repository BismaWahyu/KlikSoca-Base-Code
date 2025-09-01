from flask import Flask, request, jsonify, render_template
from flask_socketio import SocketIO, emit
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# Koneksi ke MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['flask_db']
collection = db['users']

@app.route('/')
def index():
    return render_template('index.html')

# Endpoint untuk membuat user baru (Create)
@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    new_user = {'name': data['name'], 'email': data['email']}
    result = collection.insert_one(new_user)
    # Broadcast ke semua client bahwa ada user baru
    socketio.emit('new_user', {'id': str(result.inserted_id), 'name': new_user['name'], 'email': new_user['email']})
    return jsonify({'message': 'User created successfully!', 'id': str(result.inserted_id)}), 201

# Endpoint untuk membaca semua user (Read)
@app.route('/users', methods=['GET'])
def get_users():
    users = []
    for user in collection.find():
        users.append({'id': str(user['_id']), 'name': user['name'], 'email': user['email']})
    return jsonify(users)

# Endpoint untuk membaca satu user berdasarkan ID (Read)
@app.route('/users/<id>', methods=['GET'])
def get_user(id):
    try:
        user = collection.find_one({'_id': ObjectId(id)})
        if user:
            return jsonify({'id': str(user['_id']), 'name': user['name'], 'email': user['email']})
        else:
            return jsonify({'message': 'User not found!'}), 404
    except Exception:
        return jsonify({'message': 'Invalid ID format!'}), 400


# Endpoint untuk mengupdate user (Update)
@app.route('/users/<id>', methods=['PUT'])
def update_user(id):
    try:
        data = request.get_json()
        updated_user = {'name': data['name'], 'email': data['email']}
        result = collection.update_one({'_id': ObjectId(id)}, {'$set': updated_user})
        if result.modified_count > 0:
            # Broadcast ke semua client bahwa ada user yang diupdate
            socketio.emit('updated_user', {'id': id, 'name': updated_user['name'], 'email': updated_user['email']})
            return jsonify({'message': 'User updated successfully!'})
        else:
            return jsonify({'message': 'User not found!'}), 404
    except Exception:
        return jsonify({'message': 'Invalid ID format!'}), 400

# Endpoint untuk menghapus user (Delete)
@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    try:
        result = collection.delete_one({'_id': ObjectId(id)})
        if result.deleted_count > 0:
            # Broadcast ke semua client bahwa ada user yang dihapus
            socketio.emit('deleted_user', {'id': id})
            return jsonify({'message': 'User deleted successfully!'})
        else:
            return jsonify({'message': 'User not found!'}), 404
    except Exception:
        return jsonify({'message': 'Invalid ID format!'}), 400

# Event handler untuk koneksi client
@socketio.on('connect')
def handle_connect():
    print('Client connected')

# Event handler untuk diskoneksi client
@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    socketio.run(app, debug=True)
