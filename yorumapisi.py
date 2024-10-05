from flask import Flask, request, jsonify

app = Flask(__name__)

# Bellekte yorum verisi
comments = []

@app.route('/api/comments', methods=['GET'])
def get_comments():
    """Tüm yorumları listele"""
    return jsonify(comments)

@app.route('/api/comments', methods=['POST'])
def add_comment():
    """Yeni bir yorum ekle"""
    comment = request.get_json()
    if 'author' not in comment or 'text' not in comment:
        return jsonify({'error': 'Author and text are required'}), 400
    comment['id'] = len(comments) + 1  # Basit ID atama
    comments.append(comment)
    return jsonify(comment), 201

@app.route('/api/comments/<int:comment_id>', methods=['PUT'])
def update_comment(comment_id):
    """Yorum bilgilerini güncelle"""
    comment = next((comment for comment in comments if comment['id'] == comment_id), None)
    if comment:
        data = request.get_json()
        comment.update(data)
        return jsonify(comment)
    return jsonify({'error': 'Comment not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
