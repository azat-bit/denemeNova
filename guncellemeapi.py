from flask import Flask, request, jsonify
import pyodbc
from datetime import datetime
import traceback

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
    

@app.route('/update-book/<int:kitap_id>', methods=['PUT'])
def update_book(kitap_id):
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Veritabanına bağlanılamadı"}), 500

    try:
        data = request.json
        print(f"Güncellenen veri: {data}")  # Debug için alınan veriyi yazdırıyoruz

        yazar_id = data.get('YazarID')
        baslik = data.get('Başlık')
        yayin_yili_str = data.get('YayınYılı')

        if yazar_id is None or baslik is None or yayin_yili_str is None:
            return jsonify({"error": "Eksik veri: YazarID, Başlık ve YayınYılı gerekli."}), 400

        # Yayın yılını doğrulama ve formatlama
        try:
            yayin_yili = datetime.strptime(yayin_yili_str, '%Y-%m-%d').date()
        except ValueError:
            return jsonify({"error": "YayınYılı geçersiz formatta. Format: YYYY-MM-DD."}), 400

        cursor = conn.cursor()
        cursor.execute(
            "UPDATE dbo.Kitaplar SET YazarID = ?, Başlık = ?, YayınYılı = ? WHERE KitapID = ?",
            (yazar_id, baslik, yayin_yili, kitap_id)
        )
        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({"error": "Kitap bulunamadı."}), 404

        return jsonify({"message": "Kitap başarıyla güncellendi."}), 200

    except pyodbc.Error as e:
        # Hata detaylarını loglama
        print("Hata:", e)
        print("Traceback:", traceback.format_exc())
        return jsonify({"error": f"Veritabanı hatası: {e}"}), 500

    finally:
        conn.close()

if __name__ == '__main__':
    app.run(debug=True)