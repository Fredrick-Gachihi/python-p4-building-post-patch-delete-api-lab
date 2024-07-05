#!/usr/bin/env python3

from flask import Flask, request, jsonify
from flask_migrate import Migrate
from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)
db.init_app(app)

@app.route('/')
def home():
    return '<h1>Bakery GET-POST-PATCH-DELETE API</h1>'

@app.route('/bakeries')
def get_bakeries():
    bakeries = [bakery.to_dict() for bakery in Bakery.query.all()]
    return jsonify(bakeries), 200

@app.route('/bakeries/<int:id>')
def get_bakery_by_id(id):
    bakery = Bakery.query.get_or_404(id)
    return jsonify(bakery.to_dict()), 200

@app.route('/baked_goods/by_price')
def get_baked_goods_by_price():
    baked_goods_by_price = BakedGood.query.order_by(BakedGood.price.desc()).all()
    baked_goods_by_price_serialized = [bg.to_dict() for bg in baked_goods_by_price]
    return jsonify(baked_goods_by_price_serialized), 200

@app.route('/baked_goods/most_expensive')
def get_most_expensive_baked_good():
    most_expensive = BakedGood.query.order_by(BakedGood.price.desc()).first_or_404()
    return jsonify(most_expensive.to_dict()), 200

@app.route('/baked_goods', methods=['POST'])
def create_baked_good():
    data = request.form
    name = data.get('name')
    price = data.get('price')
    
    if not name or not price:
        return jsonify({'error': 'Missing data: name and price are required'}), 400
    
    new_baked_good = BakedGood(name=name, price=price)
    db.session.add(new_baked_good)
    db.session.commit()
    
    return jsonify(new_baked_good.to_dict()), 201

@app.route('/bakeries/<int:id>', methods=['PATCH'])
def update_bakery(id):
    bakery = Bakery.query.get_or_404(id)
    
    data = request.form
    new_name = data.get('name')
    
    if new_name:
        bakery.name = new_name
    
    db.session.commit()
    
    return jsonify(bakery.to_dict()), 200

@app.route('/baked_goods/<int:id>', methods=['DELETE'])
def delete_baked_good(id):
    baked_good = BakedGood.query.get_or_404(id)
    
    db.session.delete(baked_good)
    db.session.commit()
    
    return jsonify({'message': 'Baked good successfully deleted'}), 200

if __name__ == '__main__':
    app.run(port=5555, debug=True)
