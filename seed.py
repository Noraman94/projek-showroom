from app.app import app, db
from app.models import Car, Motorcycle

with app.app_context():
    try:
        # Tambah Data Mobil (menggunakan id, title, price, image_url, status)
        c1 = Car(
            title='Toyota Avanza G 2019', 
            price=165000000, 
            image_url='https://images.unsplash.com/photo-1549399542-7e3f8b79c341?w=500', 
            status='available'
        )
        c2 = Car(
            title='Honda Civic Turbo 2021', 
            price=380000000, 
            image_url='https://images.unsplash.com/photo-1606152421802-db97b9c7a11b?w=500', 
            status='available'
        )
        
        # Tambah Data Motor
        m1 = Motorcycle(
            title='Yamaha NMAX 155 2020', 
            price=24500000, 
            image_url='https://images.unsplash.com/photo-1558981806-ec527fa84c39?w=500', 
            status='available'
        )
        m2 = Motorcycle(
            title='Honda Vario 160 2022', 
            price=22000000, 
            image_url='https://images.unsplash.com/photo-1568772585407-9361f9bf3a87?w=500', 
            status='available'
        )

        db.session.add_all([c1, c2, m1, m2])
        db.session.commit()
        print("✅ Data stok mobil dan motor berhasil ditambahkan!")
    except Exception as e:
        db.session.rollback()
        print(f"❌ Terjadi kesalahan: {e}")