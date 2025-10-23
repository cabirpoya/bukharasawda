# Bukhara Sawda - AI-Integrated Inventory and Accounting System

## 🚀 Overview

**Bukhara Sawda** is an elite, AI-driven database ecosystem designed for international import show halls. This system combines cutting-edge artificial intelligence with robust inventory management and double-entry accounting to provide intelligent business insights and automation.

### ✨ Key Features

- **Smart Inventory Management**: Real-time tracking with AI-powered stock alerts
- **AI-Driven Insights**: Demand forecasting, pricing optimization, and anomaly detection
- **Double-Entry Accounting**: Complete financial tracking with chart of accounts
- **Sales Analytics**: Comprehensive sales tracking and reporting
- **RESTful API**: Full-featured API for integration with other systems
- **Intelligent Alerts**: Proactive notifications for low stock, stale inventory, and more

## 🎯 Architecture

The system is built with a modern, scalable architecture:

- **Backend**: Python with Flask framework
- **Database**: SQLAlchemy ORM (supports PostgreSQL, MySQL, SQLite)
- **AI/ML**: scikit-learn for predictive analytics
- **API**: RESTful JSON API

### Core Modules

1. **Models** (`models.py`): Database schema and data models
2. **AI Engine** (`ai_engine.py`): Machine learning and intelligence layer
3. **API** (`app.py`): REST API endpoints
4. **Configuration**: Environment-based configuration

## 📦 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- PostgreSQL (optional, can use SQLite for development)

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/cabirpoya/bukharasawda.git
   cd bukharasawda
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Initialize the database**
   ```bash
   python -c "from models import init_db; init_db('sqlite:///bukharasawda.db')"
   ```

6. **Run the application**
   ```bash
   python app.py
   ```

The API will be available at `http://localhost:5000`

## 🔧 Configuration

Edit the `.env` file to configure the system:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/bukharasawda
OPENAI_API_KEY=your_openai_api_key_here
SECRET_KEY=your_secret_key_here
PORT=5000
DEBUG=True
```

## 📚 API Documentation

### Products API

#### Get all products
```bash
GET /api/products
```

#### Create a product
```bash
POST /api/products
Content-Type: application/json

{
  "name": "Premium Textile",
  "sku": "TXT-001",
  "category": "textiles",
  "description": "High-quality imported textile",
  "cost_price": 50.0,
  "selling_price": 75.0,
  "supplier": "Global Textiles Inc",
  "country_of_origin": "India"
}
```

#### Get a specific product
```bash
GET /api/products/{product_id}
```

### Inventory API

#### Get all inventory items
```bash
GET /api/inventory
```

#### Create inventory item
```bash
POST /api/inventory
Content-Type: application/json

{
  "product_id": 1,
  "quantity": 100,
  "location": "Hall A - Section 3",
  "minimum_stock": 20,
  "maximum_stock": 500
}
```

#### Update inventory
```bash
PUT /api/inventory/{item_id}
Content-Type: application/json

{
  "quantity": 150
}
```

### Sales API

#### Record a sale
```bash
POST /api/sales
Content-Type: application/json

{
  "product_id": 1,
  "quantity": 5,
  "unit_price": 75.0,
  "customer_name": "ABC Trading Co",
  "customer_contact": "contact@abctrading.com"
}
```

#### Get all sales
```bash
GET /api/sales
```

### Accounting API

#### Create an account
```bash
POST /api/accounts
Content-Type: application/json

{
  "account_number": "1000",
  "name": "Cash",
  "account_type": "Asset",
  "description": "Cash on hand"
}
```

#### Record a transaction
```bash
POST /api/transactions
Content-Type: application/json

{
  "account_id": 1,
  "transaction_type": "debit",
  "amount": 1000.0,
  "description": "Initial capital",
  "reference_number": "REF-001"
}
```

### AI Insights API

#### Get all insights
```bash
GET /api/insights
```

#### Generate new insights
```bash
POST /api/insights/generate
```

#### Get demand forecast
```bash
GET /api/insights/forecast/{product_id}?days=30
```

#### Get pricing suggestions
```bash
GET /api/insights/pricing/{product_id}
```

### Dashboard API

#### Get dashboard summary
```bash
GET /api/dashboard
```

Response:
```json
{
  "total_products": 150,
  "inventory_value": 125000.50,
  "active_alerts": 5,
  "recent_sales_30d": 42,
  "generated_at": "2025-10-23T00:00:00"
}
```

## 🤖 AI Features

### 1. Demand Forecasting
Uses linear regression to predict future product demand based on historical sales data.

### 2. Pricing Optimization
Analyzes sales velocity and profit margins to suggest optimal pricing strategies.

### 3. Inventory Alerts
Automatically generates alerts for:
- Low stock levels
- Overstocked items
- Stale inventory (no sales in 90 days)

### 4. Anomaly Detection
Identifies unusual patterns in inventory and sales data.

## 🗄️ Database Schema

### Products
- Product information (name, SKU, category, pricing)
- Supplier details
- Country of origin

### Inventory
- Stock levels
- Location tracking
- Min/max stock thresholds
- Auto-calculated stock status

### Accounts (Chart of Accounts)
- Account types: Asset, Liability, Equity, Revenue, Expense
- Hierarchical structure
- Active/inactive status

### Transactions
- Double-entry ledger entries
- Debit/Credit transactions
- Reference tracking

### Sales
- Sale records
- Customer information
- Automatic inventory updates

### AI Insights
- Generated insights and predictions
- Confidence scores
- Action tracking

## 🔐 Security

- Environment-based configuration
- SQL injection protection via ORM
- Input validation
- Secure secret management

## 📊 Product Categories

- Electronics
- Textiles
- Furniture
- Accessories
- Food & Beverages
- Machinery
- Other

## 🧪 Testing

Create a test script to validate the system:

```python
from models import init_db, get_session, Product, InventoryItem, ProductCategory
from ai_engine import AIEngine

# Initialize
engine = init_db('sqlite:///test.db')
session = get_session(engine)

# Create test product
product = Product(
    name="Test Product",
    sku="TEST-001",
    category=ProductCategory.ELECTRONICS,
    cost_price=100.0,
    selling_price=150.0
)
session.add(product)
session.commit()

# Create inventory
inventory = InventoryItem(
    product_id=product.id,
    quantity=5,
    minimum_stock=10
)
session.add(inventory)
session.commit()

# Generate AI insights
ai = AIEngine(session)
insights = ai.generate_all_insights()
print(f"Generated {len(insights)} insights")
```

## 🚀 Deployment

### Production Considerations

1. Use PostgreSQL for production database
2. Set `DEBUG=False` in production
3. Use a proper WSGI server (Gunicorn, uWSGI)
4. Configure proper logging
5. Set up database backups
6. Use environment variables for secrets

### Example with Gunicorn

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## 🤝 Contributing

This is a professional enterprise system. Contributions should maintain code quality and follow best practices.

## 📄 License

Proprietary - All rights reserved

## 👥 Authors

Built with the vision of elite tech founders, combining the best practices from industry leaders.

---

**Bukhara Sawda** - Where AI meets inventory intelligence 🚀