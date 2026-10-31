import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

# 1. Tentukan path folder templates agar tidak TemplateNotFound
base_dir = os.path.dirname(os.path.abspath(__file__))
template_dir = os.path.join(base_dir, 'templates')

app = Flask(__name__, template_folder=template_dir)

# 2. Konfigurasi App
app.config['SECRET_KEY'] = 'rahasia_super_aman_123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///showroom.db' # Atau PostgreSQL kamu
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 3. IMPORT 'db' DAN SEMUA MODEL DARI models.py (PENTING BIAR BISA DIPAKAI)
from app.models import db, User, Car, Motorcycle, Transaction, PurchaseHistory

# 4. Inisialisasi db dengan app
db.init_app(app)


# ==========================================
# HELPER DECORATOR (Hak Akses / Protected Route)
# ==========================================
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Silakan login terlebih dahulu!', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or session.get('role') != 'admin':
            flash('Akses ditolak! Halaman ini khusus untuk Admin.', 'danger')
            return redirect(url_for('user_dashboard'))
        return f(*args, **kwargs)
    return decorated_function


# ==========================================
# ROUTE REGISTRASI & LOGIN
# ==========================================
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        full_name = request.form.get('full_name')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role', 'customer') # 'customer' atau 'admin'

        # Cek apakah email sudah terdaftar
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email sudah terdaftar! Gunakan email lain.', 'danger')
            return redirect(url_for('register'))

        # Hash password & simpan user baru
        hashed_pw = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(
            full_name=full_name,
            email=email,
            password=hashed_pw,
            role=role
        )
        db.session.add(new_user)
        db.session.commit()

        flash('Registrasi berhasil! Silakan login.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        identifier = request.form.get('identifier') or request.form.get('email')
        password = request.form.get('password')

        # Query pencarian berbasis email
        user = User.query.filter_by(email=identifier).first()

        # Verifikasi password
        if user and check_password_hash(user.password_hash if hasattr(user, 'password_hash') else user.password, password):
            session['user_id'] = user.id
            session['role'] = user.role
            session['full_name'] = getattr(user, 'full_name', 'User')
            
            flash('Login berhasil!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Email atau password salah.', 'danger')

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    flash('Anda berhasil logout.', 'info')
    return redirect(url_for('login'))


# ==========================================
# INSIALISASI DATABASE & JALANKAN SERVER
# ==========================================
if __name__ == '__main__':
    with app.app_context():
        # Membuat semua tabel berdasarkan models.py jika belum ada
        db.create_all()
        print("Sistem siap. Database berhasil disinkronisasi.")

    app.run(debug=True)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/dashboard')
@login_required
def dashboard():
    # Ambil data filter dari pencarian
    jenis = request.args.get('jenis', 'Semua Jenis')
    merek = request.args.get('merek', 'Semua Merek')
    harga = request.args.get('harga', 'Semua Harga')

    # Query dasar untuk Mobil dan Motor
    query_cars = Car.query
    query_motos = Motorcycle.query

    # Filter Merek jika dipilih
    if merek != 'Semua Merek':
        query_cars = query_cars.filter(Car.title.ilike(f'%{merek}%'))
        query_motos = query_motos.filter(Motorcycle.title.ilike(f'%{merek}%'))

    # Eksekusi Query
    if jenis == 'Mobil':
        cars = query_cars.all()
        motorcycles = []
    elif jenis == 'Motor':
        cars = []
        motorcycles = query_motos.all()
    else:
        cars = query_cars.all()
        motorcycles = query_motos.all()

    user_name = session.get('full_name', 'User')
    user_role = session.get('role', 'customer')

    # 🔑 JIKA ROLE ADALAH ADMIN, TAMPILKAN TAMPLIAN ADMIN (admin.html)
    if user_role == 'admin':
        return render_template(
            'admin.html',
            cars=cars,
            motorcycles=motorcycles,
            user_name=user_name,
            selected_jenis=jenis,
            selected_merek=merek,
            selected_harga=harga
        )

    # JIKA CUSTOMER, TAMPILKAN KAN TAMPILAN USER BIASA (user.html)
    return render_template(
        'user.html',
        cars=cars,
        motorcycles=motorcycles,
        user_name=user_name,
        selected_jenis=jenis,
        selected_merek=merek,
        selected_harga=harga
    )


@app.route('/buy/<type>/<int:item_id>', methods=['POST'])
@login_required
def buy_vehicle(type, item_id):
    # 1. Cari kendaraan berdasarkan tipe
    if type == 'car':
        item = Car.query.get_or_404(item_id)
    else:
        item = Motorcycle.query.get_or_404(item_id)

    # 2. Cek apakah kendaraan masih tersedia
    if item.status != 'available':
        flash('Maaf, kendaraan ini sudah terjual.', 'warning')
        return redirect(url_for('dashboard'))

    # 3. Ubah status kendaraan menjadi 'sold'
    item.status = 'sold'
    db.session.commit()

    # 4. Berikan pesan notifikasi sukses ke pengguna
    flash(f'Selamat! Pengajuan pembelian {item.title} berhasil terkirim.', 'success')
    return redirect(url_for('dashboard'))

# ==========================================
# ROUTE KHUSUS ADMIN (CRUD PRODUK)
# ==========================================

# 1. TAMBAH KENDARAAN BARU
@app.route('/admin/add', methods=['POST'])
@login_required
def add_vehicle():
    if session.get('role') != 'admin':
        flash('Akses ditolak! Khusus administrator.', 'danger')
        return redirect(url_for('dashboard'))

    v_type = request.form.get('type')  # 'car' atau 'motorcycle'
    title = request.form.get('title')
    price = float(request.form.get('price', 0))
    image_url = request.form.get('image_url')

    if v_type == 'car':
        new_unit = Car(title=title, price=price, image_url=image_url, status='available')
    else:
        new_unit = Motorcycle(title=title, price=price, image_url=image_url, status='available')

    db.session.add(new_unit)
    db.session.commit()
    flash(f'Unit {title} berhasil ditambahkan!', 'success')
    return redirect(url_for('dashboard'))


# 2. EDIT KENDARAAN
@app.route('/admin/edit/<type>/<int:item_id>', methods=['GET', 'POST'])
@login_required
def edit_vehicle(type, item_id):
    if session.get('role') != 'admin':
        flash('Akses ditolak! Khusus administrator.', 'danger')
        return redirect(url_for('dashboard'))

    if type == 'car':
        item = Car.query.get_or_404(item_id)
    else:
        item = Motorcycle.query.get_or_404(item_id)

    if request.method == 'POST':
        item.title = request.form.get('title')
        item.price = float(request.form.get('price', 0))
        item.image_url = request.form.get('image_url')
        item.status = request.form.get('status')

        db.session.commit()
        flash(f'Data {item.title} berhasil diperbarui!', 'success')
        return redirect(url_for('dashboard'))

    return render_template('update.html', item=item, type=type)


# 3. HAPUS KENDARAAN
@app.route('/admin/delete/<type>/<int:item_id>', methods=['POST'])
@login_required
def delete_vehicle(type, item_id):
    if session.get('role') != 'admin':
        flash('Akses ditolak! Khusus administrator.', 'danger')
        return redirect(url_for('dashboard'))

    if type == 'car':
        item = Car.query.get_or_404(item_id)
    else:
        item = Motorcycle.query.get_or_404(item_id)

    db.session.delete(item)
    db.session.commit()
    flash(f'Unit {item.title} berhasil dihapus.', 'success')
    return redirect(url_for('dashboard'))