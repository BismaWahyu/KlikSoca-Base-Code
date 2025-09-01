from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
from pymongo import MongoClient
from bson.objectid import ObjectId
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS

app = Flask(__name__)

# --- Konfigurasi Swagger UI ---
SWAGGER_URL = '/docs'  # URL untuk mengakses UI Swagger
API_URL = '/static/openapi.yaml'  # Path ke file openapi.yaml Anda

# Panggil factory untuk membuat blueprint Swagger UI
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Flask Real-time API"
    }
)

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

# --- Konfigurasi Lainnya ---
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*") # Izinkan semua origin untuk Socket.IO
CORS(app) # Aktifkan CORS untuk semua rute Flask

# Koneksi ke MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['flask_db']
users_collection = db['users']
playlist_collection = db['playlist']

# Endpoint untuk membuat user baru (Create)
@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    new_user = {'name': data['name'], 'email': data['email']}
    result = users_collection.insert_one(new_user)
    # Broadcast ke semua client bahwa ada user baru
    socketio.emit('new_user', {'id': str(result.inserted_id), 'name': new_user['name'], 'email': new_user['email']})
    return jsonify({'message': 'User created successfully!', 'id': str(result.inserted_id)}), 201

# Endpoint untuk membaca semua user (Read)
@app.route('/users', methods=['GET'])
def get_users():
    users = []
    for user in users_collection.find():
        users.append({'id': str(user['_id']), 'name': user['name'], 'email': user['email']})
    return jsonify(users)

# Endpoint untuk membaca satu user berdasarkan ID (Read)
@app.route('/users/<id>', methods=['GET'])
def get_user(id):
    try:
        user = users_collection.find_one({'_id': ObjectId(id)})
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
        result = users_collection.update_one({'_id': ObjectId(id)}, {'$set': updated_user})
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
        result = users_collection.delete_one({'_id': ObjectId(id)})
        if result.deleted_count > 0:
            # Broadcast ke semua client bahwa ada user yang dihapus
            socketio.emit('deleted_user', {'id': id})
            return jsonify({'message': 'User deleted successfully!'})
        else:
            return jsonify({'message': 'User not found!'}), 404
    except Exception:
        return jsonify({'message': 'Invalid ID format!'}), 400

# Playlist endpoints
@app.route('/playlist/songs', methods=['GET'])
def get_playlist():
    songs = []
    for song in playlist_collection.find():
        songs.append({'id': str(song['_id']), 'title': song['title'], 'artist': song['artist']})
    return jsonify(songs)

# Event handler untuk koneksi client
@socketio.on('connect')
def handle_connect():
    print('Client connected')

# Event handler untuk diskoneksi client
@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

# Event handler untuk menambah lagu
@socketio.on('add_song')
def handle_add_song(data):
    new_song = {'title': data['title'], 'artist': data['artist']}
    result = playlist_collection.insert_one(new_song)
    emit('new_song', {'id': str(result.inserted_id), 'title': new_song['title'], 'artist': new_song['artist']}, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)