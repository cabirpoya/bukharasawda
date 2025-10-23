"""
Setup script for initializing the database with sample data
"""
from datetime import datetime, timedelta
import random
from models import (
    init_db, get_session, Product, InventoryItem, Account, 
    Transaction, Sale, ProductCategory, TransactionType
)


def setup_database(database_url='sqlite:///bukharasawda.db'):
    """Initialize database with sample data"""
    print("Initializing database...")
    engine = init_db(database_url)
    session = get_session(engine)
    
    try:
        # Create sample products
        print("Creating sample products...")
        products_data = [
            {
                'name': 'Premium Cotton Fabric',
                'sku': 'TXT-001',
                'category': ProductCategory.TEXTILES,
                'description': 'High-quality imported cotton fabric',
                'cost_price': 25.0,
                'selling_price': 40.0,
                'supplier': 'Global Textiles Ltd',
                'country_of_origin': 'India'
            },
            {
                'name': 'Smartphone XR Pro',
                'sku': 'ELC-001',
                'category': ProductCategory.ELECTRONICS,
                'description': 'Latest smartphone model',
                'cost_price': 450.0,
                'selling_price': 650.0,
                'supplier': 'TechWorld Inc',
                'country_of_origin': 'China'
            },
            {
                'name': 'Wooden Office Desk',
                'sku': 'FUR-001',
                'category': ProductCategory.FURNITURE,
                'description': 'Solid wood executive desk',
                'cost_price': 200.0,
                'selling_price': 350.0,
                'supplier': 'Fine Furniture Co',
                'country_of_origin': 'Vietnam'
            },
            {
                'name': 'Leather Handbag',
                'sku': 'ACC-001',
                'category': ProductCategory.ACCESSORIES,
                'description': 'Premium leather handbag',
                'cost_price': 80.0,
                'selling_price': 150.0,
                'supplier': 'Fashion Imports',
                'country_of_origin': 'Italy'
            },
            {
                'name': 'Coffee Beans - Premium Blend',
                'sku': 'FOD-001',
                'category': ProductCategory.FOOD_BEVERAGES,
                'description': 'Organic coffee beans',
                'cost_price': 15.0,
                'selling_price': 25.0,
                'supplier': 'Coffee Masters',
                'country_of_origin': 'Colombia'
            }
        ]
        
        products = []
        for data in products_data:
            product = Product(**data)
            session.add(product)
            products.append(product)
        
        session.commit()
        print(f"Created {len(products)} products")
        
        # Create inventory items
        print("Creating inventory items...")
        for product in products:
            inventory = InventoryItem(
                product_id=product.id,
                quantity=random.randint(50, 200),
                location=f"Hall {random.choice(['A', 'B', 'C'])} - Section {random.randint(1, 5)}",
                minimum_stock=random.randint(10, 30),
                maximum_stock=random.randint(300, 500)
            )
            session.add(inventory)
        
        session.commit()
        print(f"Created inventory for {len(products)} products")
        
        # Create chart of accounts
        print("Creating chart of accounts...")
        accounts_data = [
            {'account_number': '1000', 'name': 'Cash', 'account_type': 'Asset'},
            {'account_number': '1100', 'name': 'Accounts Receivable', 'account_type': 'Asset'},
            {'account_number': '1200', 'name': 'Inventory', 'account_type': 'Asset'},
            {'account_number': '2000', 'name': 'Accounts Payable', 'account_type': 'Liability'},
            {'account_number': '3000', 'name': 'Owner Equity', 'account_type': 'Equity'},
            {'account_number': '4000', 'name': 'Sales Revenue', 'account_type': 'Revenue'},
            {'account_number': '5000', 'name': 'Cost of Goods Sold', 'account_type': 'Expense'},
            {'account_number': '6000', 'name': 'Operating Expenses', 'account_type': 'Expense'},
        ]
        
        accounts = []
        for data in accounts_data:
            account = Account(**data, description=f"{data['name']} account")
            session.add(account)
            accounts.append(account)
        
        session.commit()
        print(f"Created {len(accounts)} accounts")
        
        # Create sample transactions
        print("Creating sample transactions...")
        # Initial capital
        transaction = Transaction(
            account_id=accounts[0].id,  # Cash
            transaction_type=TransactionType.DEBIT,
            amount=50000.0,
            description='Initial capital investment',
            reference_number='INV-001'
        )
        session.add(transaction)
        
        transaction = Transaction(
            account_id=accounts[4].id,  # Owner Equity
            transaction_type=TransactionType.CREDIT,
            amount=50000.0,
            description='Initial capital investment',
            reference_number='INV-001'
        )
        session.add(transaction)
        
        session.commit()
        print("Created initial transactions")
        
        # Create sample sales
        print("Creating sample sales...")
        for i in range(20):
            product = random.choice(products)
            quantity = random.randint(1, 5)
            
            sale = Sale(
                product_id=product.id,
                quantity=quantity,
                unit_price=product.selling_price,
                total_amount=quantity * product.selling_price,
                customer_name=f"Customer {i+1}",
                customer_contact=f"customer{i+1}@example.com",
                sale_date=datetime.utcnow() - timedelta(days=random.randint(1, 60)),
                notes=f"Sample sale #{i+1}"
            )
            session.add(sale)
        
        session.commit()
        print("Created 20 sample sales")
        
        print("\n✅ Database setup complete!")
        print(f"\nDatabase location: {database_url}")
        print("\nYou can now start the application with: python app.py")
        
    except Exception as e:
        print(f"Error during setup: {e}")
        session.rollback()
        raise
    
    finally:
        session.close()


if __name__ == '__main__':
    import sys
    
    # Get database URL from command line or use default
    db_url = sys.argv[1] if len(sys.argv) > 1 else 'sqlite:///bukharasawda.db'
    
    setup_database(db_url)
