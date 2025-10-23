# Usage Examples

## Getting Started

### 1. Basic Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Initialize database with sample data
python setup.py

# Run demo to see AI features
python demo.py

# Start the API server
python app.py
```

## API Usage Examples

### Product Management

#### Create a New Product
```bash
curl -X POST http://localhost:5000/api/products \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Premium Leather Wallet",
    "sku": "ACC-005",
    "category": "accessories",
    "description": "Handcrafted Italian leather wallet",
    "cost_price": 45.00,
    "selling_price": 89.99,
    "supplier": "Italian Leather Goods",
    "country_of_origin": "Italy"
  }'
```

#### Get All Products
```bash
curl http://localhost:5000/api/products
```

#### Get Specific Product
```bash
curl http://localhost:5000/api/products/1
```

#### Update Product Price
```bash
curl -X PUT http://localhost:5000/api/products/1 \
  -H "Content-Type: application/json" \
  -d '{"selling_price": 95.00}'
```

### Inventory Management

#### Add Inventory Item
```bash
curl -X POST http://localhost:5000/api/inventory \
  -H "Content-Type: application/json" \
  -d '{
    "product_id": 1,
    "quantity": 250,
    "location": "Hall B - Section 2",
    "minimum_stock": 50,
    "maximum_stock": 500
  }'
```

#### Check Inventory Status
```bash
curl http://localhost:5000/api/inventory
```

#### Update Stock Level
```bash
curl -X PUT http://localhost:5000/api/inventory/1 \
  -H "Content-Type: application/json" \
  -d '{
    "quantity": 300,
    "last_restocked": "2025-10-23T00:00:00"
  }'
```

### Sales Recording

#### Record a Sale
```bash
curl -X POST http://localhost:5000/api/sales \
  -H "Content-Type: application/json" \
  -d '{
    "product_id": 1,
    "quantity": 5,
    "unit_price": 40.00,
    "customer_name": "Global Imports LLC",
    "customer_contact": "orders@globalimports.com",
    "notes": "Bulk order - corporate client"
  }'
```

**Note**: This automatically:
- Creates the sale record
- Reduces inventory quantity
- Updates inventory timestamp

#### Get Sales History
```bash
curl http://localhost:5000/api/sales
```

### Accounting

#### Create Chart of Accounts
```bash
# Assets
curl -X POST http://localhost:5000/api/accounts \
  -H "Content-Type: application/json" \
  -d '{
    "account_number": "1500",
    "name": "Equipment",
    "account_type": "Asset",
    "description": "Office and show hall equipment"
  }'

# Revenue
curl -X POST http://localhost:5000/api/accounts \
  -H "Content-Type: application/json" \
  -d '{
    "account_number": "4100",
    "name": "Sales - Textiles",
    "account_type": "Revenue",
    "description": "Revenue from textile sales"
  }'
```

#### Record Financial Transaction (Double-Entry)
```bash
# Debit entry
curl -X POST http://localhost:5000/api/transactions \
  -H "Content-Type: application/json" \
  -d '{
    "account_id": 1,
    "transaction_type": "debit",
    "amount": 5000.00,
    "description": "Equipment purchase",
    "reference_number": "PO-2025-001"
  }'

# Credit entry
curl -X POST http://localhost:5000/api/transactions \
  -H "Content-Type: application/json" \
  -d '{
    "account_id": 2,
    "transaction_type": "credit",
    "amount": 5000.00,
    "description": "Equipment purchase",
    "reference_number": "PO-2025-001"
  }'
```

### AI-Powered Insights

#### Get Dashboard Summary
```bash
curl http://localhost:5000/api/dashboard
```

Response:
```json
{
  "total_products": 5,
  "inventory_value": 116760.00,
  "active_alerts": 0,
  "recent_sales_30d": 11,
  "generated_at": "2025-10-23T00:18:00"
}
```

#### Generate AI Insights
```bash
curl -X POST http://localhost:5000/api/insights/generate
```

#### View All Insights
```bash
curl http://localhost:5000/api/insights
```

#### Get Demand Forecast
```bash
# Forecast for next 30 days
curl http://localhost:5000/api/insights/forecast/1?days=30

# Forecast for next 60 days
curl http://localhost:5000/api/insights/forecast/1?days=60
```

Response:
```json
{
  "forecast": 125.5,
  "confidence": 0.87,
  "message": "Predicted demand for next 30 days: 125.50 units"
}
```

#### Get Pricing Recommendations
```bash
curl http://localhost:5000/api/insights/pricing/1
```

Response:
```json
{
  "current_price": 150.00,
  "suggested_price": 157.50,
  "current_margin": 25.0,
  "sales_velocity": 5.2,
  "strategy": "Increase price to optimize margin",
  "confidence": 0.75
}
```

## Python API Usage

### Direct Database Access

```python
from models import init_db, get_session, Product, ProductCategory

# Initialize
engine = init_db('sqlite:///bukharasawda.db')
session = get_session(engine)

# Create a product
product = Product(
    name="Organic Green Tea",
    sku="FOD-002",
    category=ProductCategory.FOOD_BEVERAGES,
    cost_price=12.00,
    selling_price=22.00,
    supplier="Tea Masters Inc",
    country_of_origin="Japan"
)
session.add(product)
session.commit()

# Query products
products = session.query(Product).filter(
    Product.category == ProductCategory.FOOD_BEVERAGES
).all()

for p in products:
    print(f"{p.name}: ${p.selling_price}")
```

### Using AI Engine

```python
from models import init_db, get_session
from ai_engine import AIEngine

# Initialize
engine = init_db('sqlite:///bukharasawda.db')
session = get_session(engine)
ai = AIEngine(session)

# Get dashboard summary
summary = ai.get_dashboard_summary()
print(f"Total Products: {summary['total_products']}")
print(f"Inventory Value: ${summary['inventory_value']:.2f}")

# Analyze inventory trends
insights = ai.analyze_inventory_trends()
for insight in insights:
    print(f"Alert: {insight['title']}")
    print(f"  {insight['description']}")

# Forecast demand
forecast = ai.forecast_demand(product_id=1, days_ahead=30)
if forecast['forecast']:
    print(f"Forecast: {forecast['forecast']:.2f} units")
    print(f"Confidence: {forecast['confidence']*100:.1f}%")

# Get pricing suggestions
pricing = ai.suggest_optimal_pricing(product_id=1)
print(f"Current: ${pricing['current_price']}")
print(f"Suggested: ${pricing['suggested_price']}")
print(f"Strategy: {pricing['strategy']}")

# Detect anomalies
anomalies = ai.detect_anomalies()
for anomaly in anomalies:
    print(f"Anomaly: {anomaly['title']}")
```

## Common Workflows

### Workflow 1: New Product Arrival

```bash
# 1. Create product
curl -X POST http://localhost:5000/api/products \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Smart Watch Pro",
    "sku": "ELC-005",
    "category": "electronics",
    "cost_price": 150.00,
    "selling_price": 250.00
  }'

# 2. Add to inventory
curl -X POST http://localhost:5000/api/inventory \
  -H "Content-Type: application/json" \
  -d '{
    "product_id": 6,
    "quantity": 100,
    "location": "Hall A - Section 1",
    "minimum_stock": 20
  }'

# 3. Record purchase transaction
curl -X POST http://localhost:5000/api/transactions \
  -H "Content-Type: application/json" \
  -d '{
    "account_id": 3,
    "transaction_type": "debit",
    "amount": 15000.00,
    "description": "Purchased 100 Smart Watch Pro units"
  }'
```

### Workflow 2: Daily Sales Processing

```bash
# 1. Record sales throughout the day
curl -X POST http://localhost:5000/api/sales \
  -H "Content-Type: application/json" \
  -d '{
    "product_id": 1,
    "quantity": 3,
    "unit_price": 40.00,
    "customer_name": "Customer A"
  }'

# 2. At end of day, check inventory status
curl http://localhost:5000/api/inventory

# 3. Generate AI insights
curl -X POST http://localhost:5000/api/insights/generate

# 4. Review alerts
curl http://localhost:5000/api/insights
```

### Workflow 3: Monthly Analysis

```bash
# 1. Get dashboard summary
curl http://localhost:5000/api/dashboard

# 2. Review all sales
curl http://localhost:5000/api/sales

# 3. Check pricing for top products
curl http://localhost:5000/api/insights/pricing/1
curl http://localhost:5000/api/insights/pricing/2
curl http://localhost:5000/api/insights/pricing/3

# 4. Forecast demand for next month
curl http://localhost:5000/api/insights/forecast/1?days=30
```

## Integration Examples

### JavaScript/Node.js

```javascript
const axios = require('axios');

const API_BASE = 'http://localhost:5000/api';

// Get dashboard
async function getDashboard() {
  const response = await axios.get(`${API_BASE}/dashboard`);
  console.log(response.data);
}

// Create product
async function createProduct(productData) {
  const response = await axios.post(`${API_BASE}/products`, productData);
  return response.data;
}

// Record sale
async function recordSale(saleData) {
  const response = await axios.post(`${API_BASE}/sales`, saleData);
  return response.data;
}
```

### Python/Requests

```python
import requests

API_BASE = 'http://localhost:5000/api'

# Get all products
def get_products():
    response = requests.get(f'{API_BASE}/products')
    return response.json()

# Create inventory
def create_inventory(product_id, quantity, location):
    data = {
        'product_id': product_id,
        'quantity': quantity,
        'location': location
    }
    response = requests.post(f'{API_BASE}/inventory', json=data)
    return response.json()

# Get AI insights
def get_insights():
    response = requests.get(f'{API_BASE}/insights')
    return response.json()
```

## Testing

### Run All Tests
```bash
python test_system.py -v
```

### Run Specific Test
```bash
python -m unittest test_system.TestModels.test_create_product
```

## Troubleshooting

### Reset Database
```bash
rm bukharasawda.db
python setup.py
```

### Check Database Content
```bash
sqlite3 bukharasawda.db "SELECT * FROM products;"
sqlite3 bukharasawda.db "SELECT * FROM inventory_items;"
```

### Debug Mode
```bash
# Set in .env
DEBUG=True

# Or run with
FLASK_DEBUG=1 python app.py
```

---

For more examples and detailed API documentation, see `README.md` and `ARCHITECTURE.md`.
