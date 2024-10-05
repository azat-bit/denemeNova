@app.route('/search-books', methods=['GET'])
def search_books():
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Veritabanına bağlanılamadı"}), 500

    try:
        query = request.args.get('query', '')
        cursor = conn.cursor()
        cursor.execute("""
            SELECT k.Baslik, k.YayinYili, y.Ad AS YazarAdi
            FROM dbo.Kitaplar k
            JOIN dbo.Yazarlar y ON k.YazarID = y.ID
            WHERE k.Baslik LIKE ? OR y.Ad LIKE ?
        """, ('%' + query + '%', '%' + query + '%'))
        rows = cursor.fetchall()

        books = []
        for row in rows:
            books.append({
                'Başlık': row.Baslik,
                'Yayın Yılı': row.YayinYili.strftime('%Y-%m-%d'),
                'Yazar Adı': row.YazarAdi
            })

        return jsonify(books), 200

    except pyodbc.Error as e:
        print("Hata:", e)
        return jsonify({"error": f"Veritabanı hatası: {e}"}), 500

    finally:
        conn.close()
