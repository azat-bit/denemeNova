@app.route('/delete-book/<int:id>', methods=['DELETE'])
def delete_book(id):
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Veritabanına bağlanılamadı"}), 500

    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM dbo.Kitaplar WHERE ID = ?", id)
        conn.commit()

        return jsonify({"message": "Kitap başarıyla silindi."}), 200

    except pyodbc.Error as e:
        print("Hata:", e)
        return jsonify({"error": f"Veritabanı hatası: {e}"}), 500

    finally:
        conn.close()
