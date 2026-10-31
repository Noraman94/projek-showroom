def calculate_ai_price(category, brand, model_name, year, mileage, condition_rating):
    # Patokan harga acuan dasar (mockup data awal)
    base_price = 150000000 if category == 'car' else 25000000
    
    current_year = 2026
    age = max(0, current_year - int(year))
    
    # 1. Depresiasi per tahun (~7% per tahun)
    year_deprec = base_price * (0.07 * age)
    
    # 2. Depresiasi jarak tempuh (per 10.000 KM)
    mileage_deprec = (int(mileage) / 10000) * (base_price * 0.02)
    
    # 3. Faktor Kondisi Fisik (1-5)
    condition_multiplier = 1.0 + ((int(condition_rating) - 3) * 0.04)
    
    estimated_price = (base_price - year_deprec - mileage_deprec) * condition_multiplier
    estimated_price = max(estimated_price, base_price * 0.15) # Batas minimal 15% harga dasar
    
    # Rentang harga pasar (+/- 5%)
    suggested_min = round(estimated_price * 0.95, -5)
    suggested_max = round(estimated_price * 1.05, -5)
    
    return {
        "estimated_price": round(estimated_price, -5),
        "suggested_min": suggested_min,
        "suggested_max": suggested_max
    }