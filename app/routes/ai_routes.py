from flask import Blueprint, request, jsonify
from app.services.ai_pricing import calculate_ai_price

ai_bp = Blueprint('ai', __name__)

@ai_bp.route('/api/v1/predict-price', methods=['POST'])
def predict_price():
    data = request.get_json() or {}
    
    required_fields = ['category', 'brand', 'model_name', 'year', 'mileage']
    for field in required_fields:
        if field not in data:
            return jsonify({"status": "error", "message": f"Field '{field}' wajib diisi"}), 400

    result = calculate_ai_price(
        category=data['category'],
        brand=data['brand'],
        model_name=data['model_name'],
        year=data['year'],
        mileage=data['mileage'],
        condition_rating=data.get('condition_rating', 3)
    )

    return jsonify({
        "status": "success",
        "data": result
    }), 200