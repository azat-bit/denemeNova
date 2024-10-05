from flask import Flask, request, jsonify

app = Flask(__name__)
def get_db_connection():
    try:
        conn = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=.\\SQLEXPRESS;'
            'DATABASE=NovaAkademi;'
            'Trusted_Connection=yes;'
        )
        return conn
    except pyodbc.Error as e:
        print(f"Veritabanı bağlantı hatası: {e}")
        return None
# Bellekte görev verisi
tasks = []

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    """Tüm görevleri listele"""
    return jsonify(tasks)

@app.route('/api/tasks', methods=['POST'])
def add_task():
    """Yeni bir görev ekle"""
    task = request.get_json()
    if 'title' not in task:
        return jsonify({'error': 'Title is required'}), 400
    task['id'] = len(tasks) + 1  # Basit ID atama
    task['completed'] = False  # Varsayılan olarak tamamlanmamış
    tasks.append(task)
    return jsonify(task), 201

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """Görev bilgilerini güncelle"""
    task = next((task for task in tasks if task['id'] == task_id), None)
    if task:
        data = request.get_json()
        task.update(data)
        return jsonify(task)
    return jsonify({'error': 'Task not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
