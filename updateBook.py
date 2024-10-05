@app.route('/update-book/<int:id>', methods=['PUT'])
def update_book(id):
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Veritabanına bağlanılamadı"}), 500

    try:
        data = request.json
        baslik = data.get('Başlık')
        yayin_yili_str = data.get('YayınYılı')

        if baslik is None or yayin_yili_str is None:
            return jsonify({"error": "Başlık ve YayınYılı gerekli."}), 400

        try:
            yayin_yili = datetime.strptime(yayin_yili_str, '%Y-%m-%d').date()
        except ValueError:
            return jsonify({"error": "YayınYılı geçersiz formatta. Format: YYYY-MM-DD."}), 400

        cursor = conn.cursor()
        cursor.execute("""
            UPDATE dbo.Kitaplar
            SET Baslik = ?, YayınYılı = ?
            WHERE ID = ?
        """, (baslik, yayin_yili, id))
        conn.commit()

        return jsonify({"message": "Kitap başarıyla güncellendi."}), 200

    except pyodbc.Error as e:
        print("Hata:", e)
        return jsonify({"error": f"Veritabanı hatası: {e}"}), 500

    finally:
        conn.close()
