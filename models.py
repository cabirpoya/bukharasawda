"""
Database models for AI-Integrated Inventory and Accounting System
"""
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey, Text, Boolean, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
import enum

Base = declarative_base()


class ProductCategory(enum.Enum):
    """Product categories for import show hall"""
    ELECTRONICS = "electronics"
    TEXTILES = "textiles"
    FURNITURE = "furniture"
    ACCESSORIES = "accessories"
    FOOD_BEVERAGES = "food_beverages"
    MACHINERY = "machinery"
    OTHER = "other"


class TransactionType(enum.Enum):
    """Transaction types for accounting"""
    DEBIT = "debit"
    CREDIT = "credit"


class Product(Base):
    """Product model representing items in the show hall"""
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    sku = Column(String(100), unique=True, nullable=False)
    category = Column(Enum(ProductCategory), nullable=False)
    description = Column(Text)
    cost_price = Column(Float, nullable=False)
    selling_price = Column(Float, nullable=False)
    supplier = Column(String(255))
    country_of_origin = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    inventory_items = relationship("InventoryItem", back_populates="product")
    
    def __repr__(self):
        return f"<Product(id={self.id}, name='{self.name}', sku='{self.sku}')>"


class InventoryItem(Base):
    """Inventory tracking for products"""
    __tablename__ = 'inventory_items'
    
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    quantity = Column(Integer, nullable=False, default=0)
    location = Column(String(100))  # Hall section/location
    minimum_stock = Column(Integer, default=10)
    maximum_stock = Column(Integer, default=1000)
    last_restocked = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    product = relationship("Product", back_populates="inventory_items")
    
    @property
    def needs_restock(self):
        """AI helper: Check if item needs restocking"""
        return self.quantity <= self.minimum_stock
    
    @property
    def stock_status(self):
        """AI helper: Get stock status"""
        if self.quantity == 0:
            return "OUT_OF_STOCK"
        elif self.quantity <= self.minimum_stock:
            return "LOW_STOCK"
        elif self.quantity >= self.maximum_stock:
            return "OVERSTOCKED"
        return "NORMAL"
    
    def __repr__(self):
        return f"<InventoryItem(id={self.id}, product_id={self.product_id}, quantity={self.quantity})>"


class Account(Base):
    """Chart of Accounts for double-entry bookkeeping"""
    __tablename__ = 'accounts'
    
    id = Column(Integer, primary_key=True)
    account_number = Column(String(50), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    account_type = Column(String(50), nullable=False)  # Asset, Liability, Equity, Revenue, Expense
    description = Column(Text)
    parent_account_id = Column(Integer, ForeignKey('accounts.id'))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    parent_account = relationship("Account", remote_side=[id])
    transactions = relationship("Transaction", back_populates="account")
    
    def __repr__(self):
        return f"<Account(id={self.id}, name='{self.name}', type='{self.account_type}')>"


class Transaction(Base):
    """Transaction entries for accounting ledger"""
    __tablename__ = 'transactions'
    
    id = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey('accounts.id'), nullable=False)
    transaction_type = Column(Enum(TransactionType), nullable=False)
    amount = Column(Float, nullable=False)
    description = Column(Text)
    reference_number = Column(String(100))
    transaction_date = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    account = relationship("Account", back_populates="transactions")
    
    def __repr__(self):
        return f"<Transaction(id={self.id}, type='{self.transaction_type}', amount={self.amount})>"


class Sale(Base):
    """Sales transactions"""
    __tablename__ = 'sales'
    
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)
    total_amount = Column(Float, nullable=False)
    customer_name = Column(String(255))
    customer_contact = Column(String(100))
    sale_date = Column(DateTime, default=datetime.utcnow)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    product = relationship("Product")
    
    def __repr__(self):
        return f"<Sale(id={self.id}, product_id={self.product_id}, amount={self.total_amount})>"


class AIInsight(Base):
    """Store AI-generated insights and predictions"""
    __tablename__ = 'ai_insights'
    
    id = Column(Integer, primary_key=True)
    insight_type = Column(String(100), nullable=False)  # demand_forecast, restock_alert, pricing_suggestion
    entity_type = Column(String(50))  # product, inventory, account
    entity_id = Column(Integer)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    confidence_score = Column(Float)  # 0-1
    action_required = Column(Boolean, default=False)
    is_resolved = Column(Boolean, default=False)
    generated_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<AIInsight(id={self.id}, type='{self.insight_type}', title='{self.title}')>"


# Database initialization
def init_db(database_url):
    """Initialize database and create all tables"""
    engine = create_engine(database_url)
    Base.metadata.create_all(engine)
    return engine


def get_session(engine):
    """Get database session"""
    Session = sessionmaker(bind=engine)
    return Session()
