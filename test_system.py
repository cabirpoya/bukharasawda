"""
Basic tests for the AI-Integrated Inventory and Accounting System
"""
import unittest
import os
from datetime import datetime
from models import (
    init_db, get_session, Product, InventoryItem, Account, 
    Transaction, Sale, AIInsight, ProductCategory, TransactionType
)
from ai_engine import AIEngine


class TestModels(unittest.TestCase):
    """Test database models"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test database"""
        cls.engine = init_db('sqlite:///test_bukharasawda.db')
        cls.session = get_session(cls.engine)
    
    @classmethod
    def tearDownClass(cls):
        """Clean up test database"""
        cls.session.close()
        if os.path.exists('test_bukharasawda.db'):
            os.remove('test_bukharasawda.db')
    
    def test_create_product(self):
        """Test creating a product"""
        product = Product(
            name='Test Product',
            sku='TEST-001',
            category=ProductCategory.ELECTRONICS,
            description='A test product',
            cost_price=100.0,
            selling_price=150.0,
            supplier='Test Supplier',
            country_of_origin='USA'
        )
        self.session.add(product)
        self.session.commit()
        
        # Verify
        saved_product = self.session.query(Product).filter_by(sku='TEST-001').first()
        self.assertIsNotNone(saved_product)
        self.assertEqual(saved_product.name, 'Test Product')
        self.assertEqual(saved_product.cost_price, 100.0)
        self.assertEqual(saved_product.selling_price, 150.0)
    
    def test_create_inventory(self):
        """Test creating an inventory item"""
        # First create a product
        product = Product(
            name='Inventory Test Product',
            sku='INV-001',
            category=ProductCategory.FURNITURE,
            cost_price=50.0,
            selling_price=75.0
        )
        self.session.add(product)
        self.session.commit()
        
        # Create inventory
        inventory = InventoryItem(
            product_id=product.id,
            quantity=100,
            location='Test Hall',
            minimum_stock=20,
            maximum_stock=200
        )
        self.session.add(inventory)
        self.session.commit()
        
        # Verify
        saved_inventory = self.session.query(InventoryItem).filter_by(
            product_id=product.id
        ).first()
        self.assertIsNotNone(saved_inventory)
        self.assertEqual(saved_inventory.quantity, 100)
        self.assertEqual(saved_inventory.stock_status, 'NORMAL')
    
    def test_stock_status(self):
        """Test inventory stock status calculation"""
        product = Product(
            name='Stock Status Test',
            sku='STS-001',
            category=ProductCategory.TEXTILES,
            cost_price=25.0,
            selling_price=40.0
        )
        self.session.add(product)
        self.session.commit()
        
        # Test low stock
        inventory = InventoryItem(
            product_id=product.id,
            quantity=5,
            minimum_stock=10,
            maximum_stock=100
        )
        self.assertEqual(inventory.stock_status, 'LOW_STOCK')
        self.assertTrue(inventory.needs_restock)
        
        # Test normal stock
        inventory.quantity = 50
        self.assertEqual(inventory.stock_status, 'NORMAL')
        self.assertFalse(inventory.needs_restock)
        
        # Test overstock
        inventory.quantity = 150
        self.assertEqual(inventory.stock_status, 'OVERSTOCKED')
        
        # Test out of stock
        inventory.quantity = 0
        self.assertEqual(inventory.stock_status, 'OUT_OF_STOCK')
    
    def test_create_account(self):
        """Test creating an account"""
        account = Account(
            account_number='1000',
            name='Test Cash Account',
            account_type='Asset',
            description='Test account for cash'
        )
        self.session.add(account)
        self.session.commit()
        
        # Verify
        saved_account = self.session.query(Account).filter_by(
            account_number='1000'
        ).first()
        self.assertIsNotNone(saved_account)
        self.assertEqual(saved_account.name, 'Test Cash Account')
        self.assertEqual(saved_account.account_type, 'Asset')
    
    def test_create_transaction(self):
        """Test creating a transaction"""
        # Create account first
        account = Account(
            account_number='2000',
            name='Test Transaction Account',
            account_type='Asset'
        )
        self.session.add(account)
        self.session.commit()
        
        # Create transaction
        transaction = Transaction(
            account_id=account.id,
            transaction_type=TransactionType.DEBIT,
            amount=500.0,
            description='Test transaction',
            reference_number='REF-TEST-001'
        )
        self.session.add(transaction)
        self.session.commit()
        
        # Verify
        saved_transaction = self.session.query(Transaction).filter_by(
            reference_number='REF-TEST-001'
        ).first()
        self.assertIsNotNone(saved_transaction)
        self.assertEqual(saved_transaction.amount, 500.0)
        self.assertEqual(saved_transaction.transaction_type, TransactionType.DEBIT)
    
    def test_create_sale(self):
        """Test creating a sale"""
        # Create product
        product = Product(
            name='Sale Test Product',
            sku='SALE-001',
            category=ProductCategory.ACCESSORIES,
            cost_price=30.0,
            selling_price=50.0
        )
        self.session.add(product)
        self.session.commit()
        
        # Create sale
        sale = Sale(
            product_id=product.id,
            quantity=3,
            unit_price=50.0,
            total_amount=150.0,
            customer_name='Test Customer'
        )
        self.session.add(sale)
        self.session.commit()
        
        # Verify
        saved_sale = self.session.query(Sale).filter_by(
            product_id=product.id
        ).first()
        self.assertIsNotNone(saved_sale)
        self.assertEqual(saved_sale.quantity, 3)
        self.assertEqual(saved_sale.total_amount, 150.0)


class TestAIEngine(unittest.TestCase):
    """Test AI engine functionality"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test database with sample data"""
        cls.engine = init_db('sqlite:///test_ai_bukharasawda.db')
        cls.session = get_session(cls.engine)
        cls.ai_engine = AIEngine(cls.session)
        
        # Create test product and inventory
        product = Product(
            name='AI Test Product',
            sku='AI-001',
            category=ProductCategory.ELECTRONICS,
            cost_price=100.0,
            selling_price=150.0
        )
        cls.session.add(product)
        cls.session.commit()
        
        inventory = InventoryItem(
            product_id=product.id,
            quantity=5,  # Low stock
            minimum_stock=10
        )
        cls.session.add(inventory)
        cls.session.commit()
    
    @classmethod
    def tearDownClass(cls):
        """Clean up test database"""
        cls.session.close()
        if os.path.exists('test_ai_bukharasawda.db'):
            os.remove('test_ai_bukharasawda.db')
    
    def test_analyze_inventory_trends(self):
        """Test inventory trend analysis"""
        insights = self.ai_engine.analyze_inventory_trends()
        
        # Should detect low stock
        self.assertGreater(len(insights), 0)
        self.assertEqual(insights[0]['insight_type'], 'restock_alert')
        self.assertTrue(insights[0]['action_required'])
    
    def test_dashboard_summary(self):
        """Test dashboard summary generation"""
        summary = self.ai_engine.get_dashboard_summary()
        
        self.assertIn('total_products', summary)
        self.assertIn('inventory_value', summary)
        self.assertIn('active_alerts', summary)
        self.assertGreater(summary['total_products'], 0)
    
    def test_generate_all_insights(self):
        """Test generating all insights"""
        insights = self.ai_engine.generate_all_insights()
        
        # Should generate at least one insight (low stock alert)
        self.assertGreater(len(insights), 0)


if __name__ == '__main__':
    unittest.main()
