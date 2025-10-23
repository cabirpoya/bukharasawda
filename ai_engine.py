"""
AI Integration Module for Intelligent Insights
"""
import os
from datetime import datetime, timedelta
from typing import List, Dict, Any
import numpy as np
from sklearn.linear_model import LinearRegression
from models import AIInsight, Product, InventoryItem, Sale


class AIEngine:
    """AI Engine for generating intelligent insights and predictions"""
    
    def __init__(self, session):
        self.session = session
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
    
    def analyze_inventory_trends(self) -> List[Dict[str, Any]]:
        """Analyze inventory trends and generate insights"""
        insights = []
        
        # Get all inventory items
        inventory_items = self.session.query(InventoryItem).all()
        
        for item in inventory_items:
            # Check for low stock
            if item.needs_restock:
                insight = {
                    'insight_type': 'restock_alert',
                    'entity_type': 'inventory',
                    'entity_id': item.id,
                    'title': f'Low Stock Alert: {item.product.name}',
                    'description': f'Current quantity ({item.quantity}) is below minimum stock level ({item.minimum_stock}). Immediate restocking recommended.',
                    'confidence_score': 0.95,
                    'action_required': True
                }
                insights.append(insight)
        
        return insights
    
    def forecast_demand(self, product_id: int, days_ahead: int = 30) -> Dict[str, Any]:
        """Forecast product demand using historical sales data"""
        # Get historical sales data
        sales = self.session.query(Sale).filter(
            Sale.product_id == product_id
        ).order_by(Sale.sale_date).all()
        
        if len(sales) < 5:
            return {
                'forecast': None,
                'confidence': 0.0,
                'message': 'Insufficient historical data for forecasting'
            }
        
        # Prepare data for linear regression
        dates = [(sale.sale_date - sales[0].sale_date).days for sale in sales]
        quantities = [sale.quantity for sale in sales]
        
        X = np.array(dates).reshape(-1, 1)
        y = np.array(quantities)
        
        # Train model
        model = LinearRegression()
        model.fit(X, y)
        
        # Predict future demand
        future_date = (sales[-1].sale_date - sales[0].sale_date).days + days_ahead
        predicted_demand = model.predict([[future_date]])[0]
        
        # Calculate confidence (R² score)
        confidence = model.score(X, y)
        
        return {
            'forecast': max(0, predicted_demand),  # Ensure non-negative
            'confidence': confidence,
            'message': f'Predicted demand for next {days_ahead} days: {predicted_demand:.2f} units'
        }
    
    def suggest_optimal_pricing(self, product_id: int) -> Dict[str, Any]:
        """Suggest optimal pricing based on cost, market trends, and sales velocity"""
        product = self.session.query(Product).filter_by(id=product_id).first()
        
        if not product:
            return {'error': 'Product not found'}
        
        # Get sales history
        sales = self.session.query(Sale).filter(
            Sale.product_id == product_id
        ).all()
        
        # Calculate average sales velocity
        if sales:
            total_quantity = sum(sale.quantity for sale in sales)
            days_range = (max(sale.sale_date for sale in sales) - 
                         min(sale.sale_date for sale in sales)).days or 1
            velocity = total_quantity / days_range
        else:
            velocity = 0
        
        # Pricing strategy based on velocity and margin
        current_margin = ((product.selling_price - product.cost_price) / 
                         product.cost_price * 100)
        
        # Suggest pricing adjustments
        if velocity < 1 and current_margin > 20:
            # Low velocity, high margin - suggest price reduction
            suggested_price = product.selling_price * 0.95
            strategy = 'Reduce price to increase sales velocity'
        elif velocity > 5 and current_margin < 30:
            # High velocity, low margin - suggest price increase
            suggested_price = product.selling_price * 1.05
            strategy = 'Increase price to optimize margin'
        else:
            suggested_price = product.selling_price
            strategy = 'Current pricing is optimal'
        
        return {
            'current_price': product.selling_price,
            'suggested_price': suggested_price,
            'current_margin': current_margin,
            'sales_velocity': velocity,
            'strategy': strategy,
            'confidence': 0.75
        }
    
    def detect_anomalies(self) -> List[Dict[str, Any]]:
        """Detect anomalies in inventory and sales patterns"""
        anomalies = []
        
        # Check for stale inventory (no movement for 90 days)
        ninety_days_ago = datetime.utcnow() - timedelta(days=90)
        
        inventory_items = self.session.query(InventoryItem).all()
        
        for item in inventory_items:
            recent_sales = self.session.query(Sale).filter(
                Sale.product_id == item.product_id,
                Sale.sale_date >= ninety_days_ago
            ).count()
            
            if recent_sales == 0 and item.quantity > 0:
                anomalies.append({
                    'insight_type': 'stale_inventory',
                    'entity_type': 'inventory',
                    'entity_id': item.id,
                    'title': f'Stale Inventory: {item.product.name}',
                    'description': f'No sales in the last 90 days. Consider promotional pricing or clearance.',
                    'confidence_score': 0.85,
                    'action_required': True
                })
        
        return anomalies
    
    def generate_all_insights(self) -> List[AIInsight]:
        """Generate all AI insights and save to database"""
        all_insights = []
        
        # Inventory trend analysis
        inventory_insights = self.analyze_inventory_trends()
        for insight in inventory_insights:
            ai_insight = AIInsight(**insight)
            self.session.add(ai_insight)
            all_insights.append(ai_insight)
        
        # Anomaly detection
        anomalies = self.detect_anomalies()
        for anomaly in anomalies:
            ai_insight = AIInsight(**anomaly)
            self.session.add(ai_insight)
            all_insights.append(ai_insight)
        
        self.session.commit()
        return all_insights
    
    def get_dashboard_summary(self) -> Dict[str, Any]:
        """Generate AI-powered dashboard summary"""
        # Count products and inventory
        total_products = self.session.query(Product).count()
        total_inventory_value = self.session.query(
            InventoryItem, Product
        ).join(Product).with_entities(
            (InventoryItem.quantity * Product.cost_price)
        ).all()
        
        inventory_value = sum(val[0] for val in total_inventory_value if val[0])
        
        # Count active alerts
        active_alerts = self.session.query(AIInsight).filter(
            AIInsight.action_required == True,
            AIInsight.is_resolved == False
        ).count()
        
        # Recent sales
        recent_sales = self.session.query(Sale).filter(
            Sale.sale_date >= datetime.utcnow() - timedelta(days=30)
        ).count()
        
        return {
            'total_products': total_products,
            'inventory_value': inventory_value,
            'active_alerts': active_alerts,
            'recent_sales_30d': recent_sales,
            'generated_at': datetime.utcnow().isoformat()
        }
