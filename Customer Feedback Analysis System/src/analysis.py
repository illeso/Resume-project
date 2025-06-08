import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

class DataAnalyzer:
    def __init__(self, df):
        self.df = df
        plt.style.use('seaborn')
        
    def analyze_customer_demographics(self):
        """Analyze customer demographics and create visualizations."""
        print("\nCustomer Demographics Analysis:")
        
        # Age distribution
        plt.figure(figsize=(10, 6))
        sns.histplot(data=self.df, x='customer_age', bins=30)
        plt.title('Customer Age Distribution')
        plt.xlabel('Age')
        plt.ylabel('Count')
        plt.savefig('../data/age_distribution.png')
        plt.close()
        
        # Regional distribution
        plt.figure(figsize=(10, 6))
        self.df['customer_region'].value_counts().plot(kind='bar')
        plt.title('Customer Distribution by Region')
        plt.xlabel('Region')
        plt.ylabel('Count')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('../data/regional_distribution.png')
        plt.close()
        
    def analyze_purchase_patterns(self):
        """Analyze purchase patterns and create visualizations."""
        print("\nPurchase Patterns Analysis:")
        
        # Purchase amount by category
        plt.figure(figsize=(12, 6))
        sns.boxplot(data=self.df, x='product_category', y='purchase_amount')
        plt.title('Purchase Amount by Product Category')
        plt.xlabel('Product Category')
        plt.ylabel('Purchase Amount')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('../data/purchase_by_category.png')
        plt.close()
        
        # Purchase channel distribution
        plt.figure(figsize=(10, 6))
        self.df['purchase_channel'].value_counts().plot(kind='pie', autopct='%1.1f%%')
        plt.title('Purchase Channel Distribution')
        plt.ylabel('')
        plt.tight_layout()
        plt.savefig('../data/purchase_channel_distribution.png')
        plt.close()
        
    def analyze_customer_satisfaction(self):
        """Analyze customer satisfaction metrics."""
        print("\nCustomer Satisfaction Analysis:")
        
        # Rating distribution
        plt.figure(figsize=(10, 6))
        sns.countplot(data=self.df, x='rating')
        plt.title('Customer Rating Distribution')
        plt.xlabel('Rating')
        plt.ylabel('Count')
        plt.savefig('../data/rating_distribution.png')
        plt.close()
        
        # Average rating by category
        plt.figure(figsize=(12, 6))
        category_ratings = self.df.groupby('product_category')['rating'].mean().sort_values(ascending=False)
        category_ratings.plot(kind='bar')
        plt.title('Average Rating by Product Category')
        plt.xlabel('Product Category')
        plt.ylabel('Average Rating')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('../data/ratings_by_category.png')
        plt.close()
        
    def generate_summary_statistics(self):
        """Generate summary statistics for the dataset."""
        print("\nSummary Statistics:")
        
        # Numeric columns summary
        numeric_summary = self.df.describe()
        print("\nNumeric Columns Summary:")
        print(numeric_summary)
        
        # Categorical columns summary
        categorical_columns = self.df.select_dtypes(include=['object']).columns
        print("\nCategorical Columns Summary:")
        for col in categorical_columns:
            print(f"\n{col} value counts:")
            print(self.df[col].value_counts())
            
    def save_analysis_report(self):
        """Save analysis results to a text file."""
        with open('../data/analysis_report.txt', 'w') as f:
            f.write("Data Analysis Report\n")
            f.write("===================\n\n")
            
            f.write("Dataset Overview:\n")
            f.write(f"Total records: {len(self.df)}\n")
            f.write(f"Total columns: {len(self.df.columns)}\n\n")
            
            f.write("Summary Statistics:\n")
            f.write(self.df.describe().to_string())
            
            f.write("\n\nMissing Values:\n")
            f.write(self.df.isnull().sum().to_string())
            
            f.write("\n\nCorrelation Analysis:\n")
            numeric_df = self.df.select_dtypes(include=[np.number])
            f.write(numeric_df.corr().to_string())
            
        print("\nAnalysis report saved to '../data/analysis_report.txt'")

if __name__ == "__main__":
    # Load the cleaned data
    df = pd.read_csv('../data/cleaned_customer_feedback.csv')
    
    # Initialize analyzer
    analyzer = DataAnalyzer(df)
    
    # Perform analysis
    analyzer.analyze_customer_demographics()
    analyzer.analyze_purchase_patterns()
    analyzer.analyze_customer_satisfaction()
    analyzer.generate_summary_statistics()
    analyzer.save_analysis_report() 