from app.app import app, db

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Otomatis buat tabel jika belum ada
    app.run(debug=True)