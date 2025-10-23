"""
API Layer for AI-Integrated Inventory and Accounting System
"""
import os
from datetime import datetime
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from models import (
    init_db, get_session, Product, InventoryItem, Account, 
    Transaction, Sale, AIInsight, ProductCategory, TransactionType
)
from ai_engine import AIEngine

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')

# Initialize database
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///bukharasawda.db')
engine = init_db(DATABASE_URL)


@app.route('/')
def index():
    """API root endpoint"""
    return jsonify({
        'message': 'AI-Integrated Inventory and Accounting System',
        'version': '1.0.0',
        'endpoints': {
            'products': '/api/products',
            'inventory': '/api/inventory',
            'accounts': '/api/accounts',
            'transactions': '/api/transactions',
            'sales': '/api/sales',
            'ai_insights': '/api/insights',
            'dashboard': '/api/dashboard'
        }
    })


# ==================== Product Endpoints ====================

@app.route('/api/products', methods=['GET', 'POST'])
def products():
    """Get all products or create a new product"""
    session = get_session(engine)
    
    try:
        if request.method == 'GET':
            products = session.query(Product).all()
            return jsonify([{
                'id': p.id,
                'name': p.name,
                'sku': p.sku,
                'category': p.category.value,
                'description': p.description,
                'cost_price': p.cost_price,
                'selling_price': p.selling_price,
                'supplier': p.supplier,
                'country_of_origin': p.country_of_origin
            } for p in products])
        
        elif request.method == 'POST':
            data = request.json
            product = Product(
                name=data['name'],
                sku=data['sku'],
                category=ProductCategory[data['category'].upper()],
                description=data.get('description'),
                cost_price=data['cost_price'],
                selling_price=data['selling_price'],
                supplier=data.get('supplier'),
                country_of_origin=data.get('country_of_origin')
            )
            session.add(product)
            session.commit()
            
            return jsonify({
                'message': 'Product created successfully',
                'id': product.id
            }), 201
    
    finally:
        session.close()


@app.route('/api/products/<int:product_id>', methods=['GET', 'PUT', 'DELETE'])
def product_detail(product_id):
    """Get, update, or delete a specific product"""
    session = get_session(engine)
    
    try:
        product = session.query(Product).filter_by(id=product_id).first()
        
        if not product:
            return jsonify({'error': 'Product not found'}), 404
        
        if request.method == 'GET':
            return jsonify({
                'id': product.id,
                'name': product.name,
                'sku': product.sku,
                'category': product.category.value,
                'description': product.description,
                'cost_price': product.cost_price,
                'selling_price': product.selling_price,
                'supplier': product.supplier,
                'country_of_origin': product.country_of_origin
            })
        
        elif request.method == 'PUT':
            data = request.json
            for key, value in data.items():
                if key == 'category':
                    value = ProductCategory[value.upper()]
                setattr(product, key, value)
            product.updated_at = datetime.utcnow()
            session.commit()
            return jsonify({'message': 'Product updated successfully'})
        
        elif request.method == 'DELETE':
            session.delete(product)
            session.commit()
            return jsonify({'message': 'Product deleted successfully'})
    
    finally:
        session.close()


# ==================== Inventory Endpoints ====================

@app.route('/api/inventory', methods=['GET', 'POST'])
def inventory():
    """Get all inventory items or create a new inventory item"""
    session = get_session(engine)
    
    try:
        if request.method == 'GET':
            items = session.query(InventoryItem).all()
            return jsonify([{
                'id': item.id,
                'product_id': item.product_id,
                'product_name': item.product.name,
                'quantity': item.quantity,
                'location': item.location,
                'minimum_stock': item.minimum_stock,
                'maximum_stock': item.maximum_stock,
                'stock_status': item.stock_status,
                'needs_restock': item.needs_restock
            } for item in items])
        
        elif request.method == 'POST':
            data = request.json
            item = InventoryItem(
                product_id=data['product_id'],
                quantity=data['quantity'],
                location=data.get('location'),
                minimum_stock=data.get('minimum_stock', 10),
                maximum_stock=data.get('maximum_stock', 1000)
            )
            session.add(item)
            session.commit()
            
            return jsonify({
                'message': 'Inventory item created successfully',
                'id': item.id
            }), 201
    
    finally:
        session.close()


@app.route('/api/inventory/<int:item_id>', methods=['GET', 'PUT'])
def inventory_detail(item_id):
    """Get or update a specific inventory item"""
    session = get_session(engine)
    
    try:
        item = session.query(InventoryItem).filter_by(id=item_id).first()
        
        if not item:
            return jsonify({'error': 'Inventory item not found'}), 404
        
        if request.method == 'GET':
            return jsonify({
                'id': item.id,
                'product_id': item.product_id,
                'product_name': item.product.name,
                'quantity': item.quantity,
                'location': item.location,
                'minimum_stock': item.minimum_stock,
                'maximum_stock': item.maximum_stock,
                'stock_status': item.stock_status,
                'needs_restock': item.needs_restock
            })
        
        elif request.method == 'PUT':
            data = request.json
            for key, value in data.items():
                setattr(item, key, value)
            item.updated_at = datetime.utcnow()
            session.commit()
            return jsonify({'message': 'Inventory updated successfully'})
    
    finally:
        session.close()


# ==================== Sales Endpoints ====================

@app.route('/api/sales', methods=['GET', 'POST'])
def sales():
    """Get all sales or create a new sale"""
    session = get_session(engine)
    
    try:
        if request.method == 'GET':
            sales = session.query(Sale).all()
            return jsonify([{
                'id': sale.id,
                'product_id': sale.product_id,
                'product_name': sale.product.name,
                'quantity': sale.quantity,
                'unit_price': sale.unit_price,
                'total_amount': sale.total_amount,
                'customer_name': sale.customer_name,
                'sale_date': sale.sale_date.isoformat()
            } for sale in sales])
        
        elif request.method == 'POST':
            data = request.json
            
            # Create sale record
            sale = Sale(
                product_id=data['product_id'],
                quantity=data['quantity'],
                unit_price=data['unit_price'],
                total_amount=data['quantity'] * data['unit_price'],
                customer_name=data.get('customer_name'),
                customer_contact=data.get('customer_contact'),
                notes=data.get('notes')
            )
            session.add(sale)
            
            # Update inventory
            inventory = session.query(InventoryItem).filter_by(
                product_id=data['product_id']
            ).first()
            
            if inventory:
                inventory.quantity -= data['quantity']
                inventory.updated_at = datetime.utcnow()
            
            session.commit()
            
            return jsonify({
                'message': 'Sale recorded successfully',
                'id': sale.id
            }), 201
    
    finally:
        session.close()


# ==================== Account Endpoints ====================

@app.route('/api/accounts', methods=['GET', 'POST'])
def accounts():
    """Get all accounts or create a new account"""
    session = get_session(engine)
    
    try:
        if request.method == 'GET':
            accounts = session.query(Account).all()
            return jsonify([{
                'id': acc.id,
                'account_number': acc.account_number,
                'name': acc.name,
                'account_type': acc.account_type,
                'description': acc.description,
                'is_active': acc.is_active
            } for acc in accounts])
        
        elif request.method == 'POST':
            data = request.json
            account = Account(
                account_number=data['account_number'],
                name=data['name'],
                account_type=data['account_type'],
                description=data.get('description'),
                parent_account_id=data.get('parent_account_id')
            )
            session.add(account)
            session.commit()
            
            return jsonify({
                'message': 'Account created successfully',
                'id': account.id
            }), 201
    
    finally:
        session.close()


# ==================== Transaction Endpoints ====================

@app.route('/api/transactions', methods=['GET', 'POST'])
def transactions():
    """Get all transactions or create a new transaction"""
    session = get_session(engine)
    
    try:
        if request.method == 'GET':
            transactions = session.query(Transaction).all()
            return jsonify([{
                'id': txn.id,
                'account_id': txn.account_id,
                'account_name': txn.account.name,
                'transaction_type': txn.transaction_type.value,
                'amount': txn.amount,
                'description': txn.description,
                'transaction_date': txn.transaction_date.isoformat()
            } for txn in transactions])
        
        elif request.method == 'POST':
            data = request.json
            transaction = Transaction(
                account_id=data['account_id'],
                transaction_type=TransactionType[data['transaction_type'].upper()],
                amount=data['amount'],
                description=data.get('description'),
                reference_number=data.get('reference_number')
            )
            session.add(transaction)
            session.commit()
            
            return jsonify({
                'message': 'Transaction recorded successfully',
                'id': transaction.id
            }), 201
    
    finally:
        session.close()


# ==================== AI Insights Endpoints ====================

@app.route('/api/insights', methods=['GET'])
def insights():
    """Get all AI insights"""
    session = get_session(engine)
    
    try:
        insights = session.query(AIInsight).filter_by(is_resolved=False).all()
        return jsonify([{
            'id': insight.id,
            'insight_type': insight.insight_type,
            'title': insight.title,
            'description': insight.description,
            'confidence_score': insight.confidence_score,
            'action_required': insight.action_required,
            'generated_at': insight.generated_at.isoformat()
        } for insight in insights])
    
    finally:
        session.close()


@app.route('/api/insights/generate', methods=['POST'])
def generate_insights():
    """Generate new AI insights"""
    session = get_session(engine)
    
    try:
        ai_engine = AIEngine(session)
        insights = ai_engine.generate_all_insights()
        
        return jsonify({
            'message': f'Generated {len(insights)} new insights',
            'count': len(insights)
        })
    
    finally:
        session.close()


@app.route('/api/insights/forecast/<int:product_id>', methods=['GET'])
def demand_forecast(product_id):
    """Get demand forecast for a product"""
    session = get_session(engine)
    
    try:
        days_ahead = request.args.get('days', 30, type=int)
        ai_engine = AIEngine(session)
        forecast = ai_engine.forecast_demand(product_id, days_ahead)
        
        return jsonify(forecast)
    
    finally:
        session.close()


@app.route('/api/insights/pricing/<int:product_id>', methods=['GET'])
def pricing_suggestion(product_id):
    """Get pricing suggestions for a product"""
    session = get_session(engine)
    
    try:
        ai_engine = AIEngine(session)
        suggestion = ai_engine.suggest_optimal_pricing(product_id)
        
        return jsonify(suggestion)
    
    finally:
        session.close()


# ==================== Dashboard Endpoint ====================

@app.route('/api/dashboard', methods=['GET'])
def dashboard():
    """Get AI-powered dashboard summary"""
    session = get_session(engine)
    
    try:
        ai_engine = AIEngine(session)
        summary = ai_engine.get_dashboard_summary()
        
        return jsonify(summary)
    
    finally:
        session.close()


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('DEBUG', 'True') == 'True'
    app.run(host='0.0.0.0', port=port, debug=debug)
