from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'rahasia_super_123'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///showroom.db' # atau koneksi PostgreSQL kamu
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # Import routes dan models di dalam fungsi agar tidak circular import
    with app.app_context():
        from app import routes, models
        db.create_all()

    return app