from flask import Flask, request, jsonify

app = Flask(__name__)

# Bellekte kullanıcı verisi
users = []

@app.route('/api/users', methods=['GET'])
def list_users():
    """Tüm kullanıcıları listele"""
    return jsonify(users)

@app.route('/api/users', methods=['POST'])
def create_user():
    """Yeni bir kullanıcı oluştur"""
    user = request.get_json()
    if 'name' not in user or 'email' not in user:
        return jsonify({'error': 'Name and email are required'}), 400
    user['id'] = len(users) + 1  # Basit ID atama
    users.append(user)
    return jsonify(user), 201

@app.route('/api/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """Kullanıcı bilgilerini güncelle"""
    user = next((user for user in users if user['id'] == user_id), None)
    if user:
        data = request.get_json()
        user.update(data)
        return jsonify(user)
    return jsonify({'error': 'User not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
