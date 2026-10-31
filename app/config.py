import os

class Config:
    # ---------------------------------------------------------
    # 1. Konfigurasi Keamanan (Secret Key)
    # ---------------------------------------------------------
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'kunci-rahasia-marketplace-123'

    # ---------------------------------------------------------
    # 2. Pengaturan Parameter Database PostgreSQL
    # ---------------------------------------------------------
    DB_USER = os.environ.get('DB_USER') or 'postgres'
    DB_PASSWORD = os.environ.get('DB_PASSWORD') or '123456'
    DB_HOST = os.environ.get('DB_HOST') or 'localhost'
    DB_PORT = os.environ.get('DB_PORT') or '5432'
    DB_NAME = os.environ.get('DB_NAME') or 'showroom_iwan'

    # Combine parameter di atas menjadi URL koneksi SQLAlchemy
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get('DATABASE_URL') or 
        f'postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    )

    # ---------------------------------------------------------
    # 3. Fitur Tambahan SQLAlchemy
    # ---------------------------------------------------------
    # Matikan peringatan/modifikasi berlebih untuk menghemat memori
    SQLALCHEMY_TRACK_MODIFICATIONS = False