import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def generate_customer_feedback_data(n_samples=1000):
    """
    Generate synthetic customer feedback data for demonstration purposes.
    """
    # Set random seed for reproducibility
    np.random.seed(42)
    
    # Generate dates for the last 6 months
    end_date = datetime.now()
    start_date = end_date - timedelta(days=180)
    dates = [start_date + timedelta(days=x) for x in range((end_date - start_date).days)]
    
    # Generate data
    data = {
        'customer_id': [f'CUST_{i:04d}' for i in range(n_samples)],
        'date': [random.choice(dates) for _ in range(n_samples)],
        'product_category': np.random.choice(['Electronics', 'Clothing', 'Home', 'Books', 'Sports'], n_samples),
        'purchase_amount': np.random.normal(100, 30, n_samples).round(2),
        'rating': np.random.randint(1, 6, n_samples),
        'feedback_text': [f"Sample feedback {i}" for i in range(n_samples)],
        'customer_age': np.random.randint(18, 80, n_samples),
        'customer_region': np.random.choice(['North', 'South', 'East', 'West'], n_samples),
        'purchase_channel': np.random.choice(['Online', 'Store', 'Mobile'], n_samples)
    }
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Introduce some missing values
    df.loc[df.sample(frac=0.1).index, 'rating'] = np.nan
    df.loc[df.sample(frac=0.05).index, 'feedback_text'] = np.nan
    
    # Introduce some outliers
    df.loc[df.sample(frac=0.02).index, 'purchase_amount'] *= 5
    
    # Save to CSV
    df.to_csv('../data/customer_feedback.csv', index=False)
    print(f"Generated {n_samples} samples of customer feedback data")
    return df

if __name__ == "__main__":
    df = generate_customer_feedback_data()
    print("\nSample of generated data:")
    print(df.head()) 