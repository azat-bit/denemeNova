from flask import Flask, request, jsonify

app = Flask(__name__)

# Bellekte ürün verisi
products = []

@app.route('/api/products', methods=['GET'])
def get_products():
    """Tüm ürünleri listele"""
    return jsonify(products)

@app.route('/api/products', methods=['POST'])
def add_product():
    """Yeni bir ürün ekle"""
    product = request.get_json()
    if 'name' not in product or 'price' not in product:
        return jsonify({'error': 'Name and price are required'}), 400
    product['id'] = len(products) + 1  # Basit ID atama
    products.append(product)
    return jsonify(product), 201

@app.route('/api/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    """Ürün bilgilerini güncelle"""
    product = next((product for product in products if product['id'] == product_id), None)
    if product:
        data = request.get_json()
        product.update(data)
        return jsonify(product)
    return jsonify({'error': 'Product not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
