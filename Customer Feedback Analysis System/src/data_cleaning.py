import pandas as pd
import numpy as np
from datetime import datetime

class DataCleaner:
    def __init__(self, df):
        self.df = df.copy()
        self.original_shape = df.shape
        
    def remove_duplicates(self):
        """Remove duplicate rows from the dataset."""
        initial_rows = len(self.df)
        self.df.drop_duplicates(inplace=True)
        removed_rows = initial_rows - len(self.df)
        print(f"Removed {removed_rows} duplicate rows")
        return self
        
    def handle_missing_values(self, strategy='mean'):
        """
        Handle missing values in the dataset.
        strategy: 'mean', 'median', 'mode', or 'drop'
        """
        for column in self.df.columns:
            missing_count = self.df[column].isnull().sum()
            if missing_count > 0:
                print(f"\nHandling missing values in {column}:")
                print(f"Missing values: {missing_count}")
                
                if strategy == 'drop':
                    self.df.dropna(subset=[column], inplace=True)
                elif strategy == 'mean' and pd.api.types.is_numeric_dtype(self.df[column]):
                    self.df[column].fillna(self.df[column].mean(), inplace=True)
                elif strategy == 'median' and pd.api.types.is_numeric_dtype(self.df[column]):
                    self.df[column].fillna(self.df[column].median(), inplace=True)
                elif strategy == 'mode':
                    self.df[column].fillna(self.df[column].mode()[0], inplace=True)
                
                print(f"Missing values after cleaning: {self.df[column].isnull().sum()}")
        return self
        
    def handle_outliers(self, columns, method='iqr', threshold=1.5):
        """
        Handle outliers in specified columns using IQR method.
        method: 'iqr' or 'zscore'
        """
        for column in columns:
            if pd.api.types.is_numeric_dtype(self.df[column]):
                if method == 'iqr':
                    Q1 = self.df[column].quantile(0.25)
                    Q3 = self.df[column].quantile(0.75)
                    IQR = Q3 - Q1
                    lower_bound = Q1 - threshold * IQR
                    upper_bound = Q3 + threshold * IQR
                    
                    outliers = ((self.df[column] < lower_bound) | 
                              (self.df[column] > upper_bound)).sum()
                    print(f"\nOutliers in {column}: {outliers}")
                    
                    # Cap outliers
                    self.df[column] = self.df[column].clip(lower_bound, upper_bound)
                    
                elif method == 'zscore':
                    z_scores = np.abs((self.df[column] - self.df[column].mean()) / 
                                    self.df[column].std())
                    outliers = (z_scores > threshold).sum()
                    print(f"\nOutliers in {column}: {outliers}")
                    
                    # Cap outliers
                    self.df[column] = self.df[column].clip(
                        self.df[column].mean() - threshold * self.df[column].std(),
                        self.df[column].mean() + threshold * self.df[column].std()
                    )
        return self
        
    def standardize_dates(self, date_column):
        """Standardize date format in the specified column."""
        self.df[date_column] = pd.to_datetime(self.df[date_column])
        return self
        
    def get_cleaning_summary(self):
        """Print summary of data cleaning operations."""
        print("\nData Cleaning Summary:")
        print(f"Original shape: {self.original_shape}")
        print(f"Final shape: {self.df.shape}")
        print("\nMissing values after cleaning:")
        print(self.df.isnull().sum())
        return self
        
    def save_cleaned_data(self, filepath):
        """Save cleaned data to CSV file."""
        self.df.to_csv(filepath, index=False)
        print(f"\nCleaned data saved to {filepath}")
        return self

if __name__ == "__main__":
    # Load the data
    df = pd.read_csv('../data/customer_feedback.csv')
    
    # Initialize cleaner
    cleaner = DataCleaner(df)
    
    # Perform cleaning operations
    cleaner.remove_duplicates()\
           .handle_missing_values(strategy='mean')\
           .handle_outliers(columns=['purchase_amount', 'customer_age'])\
           .standardize_dates('date')\
           .get_cleaning_summary()\
           .save_cleaned_data('../data/cleaned_customer_feedback.csv') 