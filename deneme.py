from flask import Flask, jsonify, request

app = Flask(__name__)

data = [{'id': 1, 'name': 'Item One'}, {'id': 2, 'name': 'Item Two'}]

@app.route('/api/items', methods=['GET'])
def get_items():
    return jsonify(data)

@app.route('/api/items', methods=['POST'])
def add_item():
    new_item = request.get_json()
    data.append(new_item)
    return jsonify({'message': 'Item added'}), 201

@app.route('/api/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    for item in data:
        if item['id'] == item_id:
            item.update(request.get_json())
            return jsonify({'message': 'Item updated'})
    return jsonify({'message': 'Item not found'}), 404

@app.route('/api/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    global data
    data = [item for item in data if item['id'] != item_id]
    return jsonify({'message': 'Item deleted'})

if __name__ == '__main__':
    app.run(debug=True)
