# Quick Start Guide

## Get Started in 5 Minutes

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Setup Database with Sample Data
```bash
python setup.py
```

This will:
- Create the database schema
- Add 5 sample products (textiles, electronics, furniture, etc.)
- Create inventory entries
- Set up chart of accounts
- Add sample transactions and sales

### 3. Run the Demo
```bash
python demo.py
```

This will show you:
- Dashboard summary
- Inventory trend analysis
- Demand forecasting
- Pricing optimization
- Anomaly detection

### 4. Start the API Server
```bash
python app.py
```

The server will start at `http://localhost:5000`

### 5. Test the API

#### Get Dashboard Summary
```bash
curl http://localhost:5000/api/dashboard
```

#### Get All Products
```bash
curl http://localhost:5000/api/products
```

#### Get Inventory Status
```bash
curl http://localhost:5000/api/inventory
```

#### Generate AI Insights
```bash
curl -X POST http://localhost:5000/api/insights/generate
```

#### View AI Insights
```bash
curl http://localhost:5000/api/insights
```

#### Get Demand Forecast
```bash
curl http://localhost:5000/api/insights/forecast/1?days=30
```

#### Get Pricing Suggestion
```bash
curl http://localhost:5000/api/insights/pricing/1
```

## Example: Create a New Product

```bash
curl -X POST http://localhost:5000/api/products \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Silk Scarf",
    "sku": "ACC-002",
    "category": "accessories",
    "description": "Premium silk scarf",
    "cost_price": 30.0,
    "selling_price": 55.0,
    "supplier": "Silk Road Traders",
    "country_of_origin": "China"
  }'
```

## Example: Record a Sale

```bash
curl -X POST http://localhost:5000/api/sales \
  -H "Content-Type: application/json" \
  -d '{
    "product_id": 1,
    "quantity": 3,
    "unit_price": 40.0,
    "customer_name": "ABC Trading",
    "customer_contact": "contact@abc.com"
  }'
```

## Development Tips

### Use SQLite for Development
SQLite is already configured as the default database. No additional setup needed!

### Switch to PostgreSQL for Production
Update `.env`:
```
DATABASE_URL=postgresql://user:password@localhost:5432/bukharasawda
```

### Enable Debug Mode
Already enabled by default. Check `.env`:
```
DEBUG=True
```

### View Database
Use any SQLite browser or:
```bash
sqlite3 bukharasawda.db
.tables
SELECT * FROM products;
```

## Next Steps

1. Explore the API documentation in `README.md`
2. Customize the AI algorithms in `ai_engine.py`
3. Add your own product categories
4. Integrate with your existing systems
5. Deploy to production

## Troubleshooting

### Import Errors
Make sure you're in the virtual environment:
```bash
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Database Errors
Delete the database and recreate:
```bash
rm bukharasawda.db
python setup.py
```

### Port Already in Use
Change the port in `.env` or:
```bash
PORT=8000 python app.py
```

## Support

For issues and questions, check the main `README.md` file for detailed documentation.
