from app.app import app, db
from app.models import User
from werkzeug.security import generate_password_hash

with app.app_context():
    # Cek apakah kolom yang digunakan di model User adalah email atau username
    if hasattr(User, 'email'):
        admin_identifier = 'admin@gmail.com'
        existing_admin = User.query.filter_by(email=admin_identifier).first()
    else:
        admin_identifier = 'admin'
        existing_admin = User.query.filter_by(username=admin_identifier).first()

    if existing_admin:
        print("⚠️ Akun Admin sudah ada di database!")
    else:
        # Buat objek admin baru
        if hasattr(User, 'email'):
            admin_user = User(
                email='admin@gmail.com',
                full_name='Administrator Showroom',
                role='admin'
            )
        else:
            admin_user = User(
                username='admin',
                full_name='Administrator Showroom',
                role='admin'
            )

        # Set password admin (admin123)
        if hasattr(admin_user, 'set_password'):
            admin_user.set_password('admin123')
        elif hasattr(admin_user, 'password'):
            admin_user.password = generate_password_hash('admin123')
        elif hasattr(admin_user, 'password_hash'):
            admin_user.password_hash = generate_password_hash('admin123')

        db.session.add(admin_user)
        db.session.commit()
        print("✅ Akun Admin berhasil dibuat!")
        print("   Login  : iwanjokam337@gmail.com (atau 'iwanfauzi')")
        print("   Pass   : iwan123")