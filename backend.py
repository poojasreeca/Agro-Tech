from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import tensorflow as tf
import numpy as np
from PIL import Image
import io
import cv2
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///agrotech.db'
db = SQLAlchemy(app)

# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(15), nullable=False)

class SoilTestAppointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default='pending')

class Machinery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    rent_per_day = db.Column(db.Float, nullable=False)
    available_from = db.Column(db.DateTime, nullable=False)
    available_to = db.Column(db.DateTime, nullable=False)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    seller_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# Load the plant disease detection model
model = tf.keras.models.load_model('plant_disease_model.h5')
disease_classes = [
    'Healthy',
    'Bacterial Leaf Blight',
    'Brown Spot',
    'Leaf Blast'
]

def preprocess_image(image_bytes):
    # Convert bytes to image
    image = Image.open(io.BytesIO(image_bytes))
    # Resize to model input size
    image = image.resize((224, 224))
    # Convert to array and normalize
    image_array = np.array(image) / 255.0
    # Add batch dimension
    return np.expand_dims(image_array, axis=0)

@app.route('/api/detect-disease', methods=['POST'])
def detect_disease():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400
    
    image_file = request.files['image']
    image_bytes = image_file.read()
    
    # Preprocess the image
    processed_image = preprocess_image(image_bytes)
    
    # Make prediction
    predictions = model.predict(processed_image)
    predicted_class = disease_classes[np.argmax(predictions[0])]
    confidence = float(np.max(predictions[0]))
    
    return jsonify({
        'disease': predicted_class,
        'confidence': confidence
    })

@app.route('/api/book-appointment', methods=['POST'])
def book_appointment():
    data = request.json
    
    user = User.query.filter_by(email=data['email']).first()
    if not user:
        user = User(
            name=data['name'],
            email=data['email'],
            phone=data['phone']
        )
        db.session.add(user)
        db.session.commit()
    
    appointment = SoilTestAppointment(
        user_id=user.id,
        date=datetime.strptime(data['date'], '%Y-%m-%d')
    )
    db.session.add(appointment)
    db.session.commit()
    
    return jsonify({'message': 'Appointment booked successfully'})

@app.route('/api/machinery/available', methods=['GET'])
def get_available_machinery():
    machinery = Machinery.query.all()
    return jsonify([{
        'id': m.id,
        'name': m.name,
        'type': m.type,
        'rent_per_day': m.rent_per_day,
        'available_from': m.available_from.isoformat(),
        'available_to': m.available_to.isoformat()
    } for m in machinery])

@app.route('/api/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([{
        'id': p.id,
        'name': p.name,
        'price': p.price,
        'quantity': p.quantity,
        'seller': User.query.get(p.seller_id).name
    } for p in products])

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
