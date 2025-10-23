"""
Demo script showing AI features and capabilities
"""
from models import init_db, get_session, Product, InventoryItem, Sale
from ai_engine import AIEngine
from datetime import datetime


def demo_ai_features():
    """Demonstrate AI capabilities"""
    print("=" * 60)
    print("AI-INTEGRATED INVENTORY AND ACCOUNTING SYSTEM - DEMO")
    print("=" * 60)
    print()
    
    # Initialize
    engine = init_db('sqlite:///bukharasawda.db')
    session = get_session(engine)
    ai = AIEngine(session)
    
    try:
        # 1. Dashboard Summary
        print("📊 DASHBOARD SUMMARY")
        print("-" * 60)
        summary = ai.get_dashboard_summary()
        print(f"Total Products: {summary['total_products']}")
        print(f"Inventory Value: ${summary['inventory_value']:.2f}")
        print(f"Active Alerts: {summary['active_alerts']}")
        print(f"Recent Sales (30d): {summary['recent_sales_30d']}")
        print()
        
        # 2. Inventory Analysis
        print("📦 INVENTORY TREND ANALYSIS")
        print("-" * 60)
        insights = ai.analyze_inventory_trends()
        if insights:
            for i, insight in enumerate(insights[:5], 1):
                print(f"\n{i}. {insight['title']}")
                print(f"   Type: {insight['type']}")
                print(f"   {insight['description']}")
                print(f"   Confidence: {insight['confidence_score']*100:.1f}%")
        else:
            print("No urgent inventory alerts at this time.")
        print()
        
        # 3. Demand Forecasting
        print("🔮 DEMAND FORECASTING")
        print("-" * 60)
        products = session.query(Product).limit(3).all()
        for product in products:
            forecast = ai.forecast_demand(product.id, days_ahead=30)
            print(f"\nProduct: {product.name}")
            print(f"  {forecast['message']}")
            if forecast.get('forecast'):
                print(f"  Confidence: {forecast['confidence']*100:.1f}%")
        print()
        
        # 4. Pricing Optimization
        print("💰 PRICING OPTIMIZATION")
        print("-" * 60)
        for product in products:
            suggestion = ai.suggest_optimal_pricing(product.id)
            if 'error' not in suggestion:
                print(f"\nProduct: {product.name}")
                print(f"  Current Price: ${suggestion['current_price']:.2f}")
                print(f"  Suggested Price: ${suggestion['suggested_price']:.2f}")
                print(f"  Current Margin: {suggestion['current_margin']:.1f}%")
                print(f"  Sales Velocity: {suggestion['sales_velocity']:.2f} units/day")
                print(f"  Strategy: {suggestion['strategy']}")
        print()
        
        # 5. Anomaly Detection
        print("🔍 ANOMALY DETECTION")
        print("-" * 60)
        anomalies = ai.detect_anomalies()
        if anomalies:
            for i, anomaly in enumerate(anomalies[:5], 1):
                print(f"\n{i}. {anomaly['title']}")
                print(f"   {anomaly['description']}")
                print(f"   Confidence: {anomaly['confidence_score']*100:.1f}%")
        else:
            print("No anomalies detected.")
        print()
        
        # 6. Generate and Save All Insights
        print("💡 GENERATING AI INSIGHTS")
        print("-" * 60)
        all_insights = ai.generate_all_insights()
        print(f"Generated and saved {len(all_insights)} insights to database")
        print()
        
        # 7. Stock Status Overview
        print("📈 STOCK STATUS OVERVIEW")
        print("-" * 60)
        inventory_items = session.query(InventoryItem).all()
        status_counts = {}
        for item in inventory_items:
            status = item.stock_status
            status_counts[status] = status_counts.get(status, 0) + 1
        
        for status, count in status_counts.items():
            print(f"{status}: {count} items")
        print()
        
        print("=" * 60)
        print("DEMO COMPLETE")
        print("=" * 60)
        print("\nThe AI engine successfully:")
        print("✓ Analyzed inventory trends")
        print("✓ Generated demand forecasts")
        print("✓ Provided pricing recommendations")
        print("✓ Detected anomalies")
        print("✓ Created actionable insights")
        print("\nStart the API server with: python app.py")
        print("Then access the dashboard at: http://localhost:5000/api/dashboard")
        
    except Exception as e:
        print(f"Error during demo: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        session.close()


if __name__ == '__main__':
    demo_ai_features()
