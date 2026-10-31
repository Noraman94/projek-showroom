from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# 1. MODEL USER / ADMIN (Dashboard User & Admin)
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='customer')  # 'admin' atau 'customer'

    # Relasi
    transactions = db.relationship('Transaction', backref='user', lazy=True)
    purchase_histories = db.relationship('PurchaseHistory', backref='user', lazy=True)

    def __repr__(self):
        return f"<User {self.email} - Role: {self.role}>"


# 2. MODEL MOBIL
class Car(db.Model):
    __tablename__ = 'cars'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Numeric(15, 2), nullable=False)
    image_url = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), default='available')  # 'available' atau 'sold'

    def __repr__(self):
        return f"<Car {self.title} - Rp{self.price}>"


# 3. MODEL MOTOR
class Motorcycle(db.Model):
    __tablename__ = 'motorcycles'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Numeric(15, 2), nullable=False)
    image_url = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), default='available')  # 'available' atau 'sold'

    def __repr__(self):
        return f"<Motorcycle {self.title} - Rp{self.price}>"


# 4. MODEL TRANSAKSI (Transaksi Berjalan)
class Transaction(db.Model):
    __tablename__ = 'transactions'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    
    vehicle_type = db.Column(db.String(10), nullable=False)  # 'car' atau 'motorcycle'
    car_id = db.Column(db.Integer, db.ForeignKey('cars.id', ondelete='SET NULL'), nullable=True)
    motorcycle_id = db.Column(db.Integer, db.ForeignKey('motorcycles.id', ondelete='SET NULL'), nullable=True)
    
    amount = db.Column(db.Numeric(15, 2), nullable=False)
    status = db.Column(db.String(20), default='pending')  # 'pending', 'paid', 'cancelled'

    # Relasi opsional
    car = db.relationship('Car', backref='transactions')
    motorcycle = db.relationship('Motorcycle', backref='transactions')

    def __repr__(self):
        return f"<Transaction #{self.id} - Status: {self.status}>"


# 5. MODEL RIWAYAT PEMBELIAN (History Selesai)
class PurchaseHistory(db.Model):
    __tablename__ = 'purchase_history'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    vehicle_title = db.Column(db.String(100), nullable=False)
    total_price = db.Column(db.Numeric(15, 2), nullable=False)
    purchased_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<PurchaseHistory {self.vehicle_title} - {self.purchased_at}>"