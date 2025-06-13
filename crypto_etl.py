import requests
import pandas as pd
import sqlite3
from datetime import datetime
import json
import logging
import time
from typing import Dict, List, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class CryptoETLPipeline:
    """ETL Pipeline for cryptocurrency data from CoinGecko API"""
    
    def __init__(self, db_path: str = "crypto_data.db"):
        self.base_url = "https://api.coingecko.com/api/v3"
        self.db_path = db_path
        self.conn = None
        
    def __enter__(self):
        """Context manager entry"""
        self.conn = sqlite3.connect(self.db_path)
        self._create_tables()
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        if self.conn:
            self.conn.close()
    
    def _create_tables(self):
        """Create database tables if they don't exist"""
        cursor = self.conn.cursor()
        
        # Create main crypto data table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS crypto_prices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                coin_id TEXT NOT NULL,
                symbol TEXT NOT NULL,
                name TEXT NOT NULL,
                current_price REAL,
                market_cap REAL,
                total_volume REAL,
                price_change_24h REAL,
                price_change_percentage_24h REAL,
                market_cap_rank INTEGER,
                circulating_supply REAL,
                total_supply REAL,
                ath REAL,
                ath_date TEXT,
                atl REAL,
                atl_date TEXT,
                last_updated TEXT,
                etl_timestamp TEXT NOT NULL
            )
        ''')
        
        # Create historical data table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS price_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                coin_id TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                price REAL NOT NULL,
                market_cap REAL,
                volume REAL,
                UNIQUE(coin_id, timestamp)
            )
        ''')
        
        # Create data quality metrics table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS etl_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                run_timestamp TEXT NOT NULL,
                records_extracted INTEGER,
                records_transformed INTEGER,
                records_loaded INTEGER,
                errors INTEGER,
                duration_seconds REAL
            )
        ''')
        
        self.conn.commit()
    
    def extract(self, coin_ids: List[str] = None, vs_currency: str = 'usd') -> Optional[List[Dict]]:
        """Extract cryptocurrency data from CoinGecko API"""
        try:
            if coin_ids is None:
                # Default to top 10 cryptocurrencies
                coin_ids = ['bitcoin', 'ethereum', 'tether', 'binancecoin', 'solana',
                           'xrp', 'usd-coin', 'cardano', 'avalanche-2', 'dogecoin']
            
            # API endpoint for market data
            endpoint = f"{self.base_url}/coins/markets"
            
            params = {
                'vs_currency': vs_currency,
                'ids': ','.join(coin_ids),
                'order': 'market_cap_desc',
                'per_page': 100,
                'page': 1,
                'sparkline': False,
                'price_change_percentage': '24h'
            }
            
            logger.info(f"Extracting data for coins: {coin_ids}")
            response = requests.get(endpoint, params=params)
            
            if response.status_code == 200:
                data = response.json()
                logger.info(f"Successfully extracted {len(data)} records")
                return data
            else:
                logger.error(f"API request failed with status code: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Error during extraction: {str(e)}")
            return None
    
    def transform(self, raw_data: List[Dict]) -> pd.DataFrame:
        """Transform raw API data into cleaned DataFrame"""
        try:
            logger.info("Starting data transformation")
            
            # Convert to DataFrame
            df = pd.DataFrame(raw_data)
            
            # Add ETL timestamp
            df['etl_timestamp'] = datetime.now().isoformat()
            
            # Data type conversions
            numeric_columns = ['current_price', 'market_cap', 'total_volume', 
                             'price_change_24h', 'price_change_percentage_24h',
                             'circulating_supply', 'total_supply', 'ath', 'atl']
            
            for col in numeric_columns:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
            
            # Handle missing values
            df['total_supply'] = df['total_supply'].fillna(df['circulating_supply'])
            df['price_change_24h'] = df['price_change_24h'].fillna(0)
            df['price_change_percentage_24h'] = df['price_change_percentage_24h'].fillna(0)
            
            # Data validation
            df = df[df['current_price'] > 0]  # Remove invalid prices
            
            # Feature engineering
            df['market_dominance'] = (df['market_cap'] / df['market_cap'].sum()) * 100
            df['volume_to_market_cap_ratio'] = df['total_volume'] / df['market_cap']
            df['supply_ratio'] = df['circulating_supply'] / df['total_supply']
            
            # Calculate price metrics
            df['distance_from_ath'] = ((df['ath'] - df['current_price']) / df['ath']) * 100
            df['distance_from_atl'] = ((df['current_price'] - df['atl']) / df['current_price']) * 100
            
            logger.info(f"Transformation complete. {len(df)} records processed")
            return df
            
        except Exception as e:
            logger.error(f"Error during transformation: {str(e)}")
            raise
    
    def load(self, df: pd.DataFrame) -> int:
        """Load transformed data into SQLite database"""
        try:
            logger.info("Loading data to database")
            
            # Select columns for main table
            main_columns = ['id', 'symbol', 'name', 'current_price', 'market_cap',
                          'total_volume', 'price_change_24h', 'price_change_percentage_24h',
                          'market_cap_rank', 'circulating_supply', 'total_supply',
                          'ath', 'ath_date', 'atl', 'atl_date', 'last_updated',
                          'etl_timestamp']
            
            # Rename 'id' column to 'coin_id' to avoid confusion with primary key
            df_to_load = df[main_columns].copy()
            df_to_load.rename(columns={'id': 'coin_id'}, inplace=True)
            
            # Load to database
            records_loaded = df_to_load.to_sql(
                'crypto_prices', 
                self.conn, 
                if_exists='append', 
                index=False
            )
            
            self.conn.commit()
            logger.info(f"Successfully loaded {len(df_to_load)} records")
            
            return len(df_to_load)
            
        except Exception as e:
            logger.error(f"Error during loading: {str(e)}")
            self.conn.rollback()
            raise
    
    def run_pipeline(self, coin_ids: List[str] = None) -> Dict:
        """Run the complete ETL pipeline"""
        start_time = time.time()
        metrics = {
            'records_extracted': 0,
            'records_transformed': 0,
            'records_loaded': 0,
            'errors': 0,
            'duration_seconds': 0
        }
        
        try:
            # Extract
            raw_data = self.extract(coin_ids)
            if raw_data:
                metrics['records_extracted'] = len(raw_data)
            else:
                metrics['errors'] += 1
                return metrics
            
            # Transform
            transformed_df = self.transform(raw_data)
            metrics['records_transformed'] = len(transformed_df)
            
            # Load
            records_loaded = self.load(transformed_df)
            metrics['records_loaded'] = records_loaded
            
        except Exception as e:
            logger.error(f"Pipeline failed: {str(e)}")
            metrics['errors'] += 1
        
        finally:
            # Calculate duration
            metrics['duration_seconds'] = round(time.time() - start_time, 2)
            
            # Log metrics
            self._log_metrics(metrics)
            
        return metrics
    
    def _log_metrics(self, metrics: Dict):
        """Log ETL metrics to database"""
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                INSERT INTO etl_metrics 
                (run_timestamp, records_extracted, records_transformed, 
                 records_loaded, errors, duration_seconds)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                datetime.now().isoformat(),
                metrics['records_extracted'],
                metrics['records_transformed'],
                metrics['records_loaded'],
                metrics['errors'],
                metrics['duration_seconds']
            ))
            self.conn.commit()
        except Exception as e:
            logger.error(f"Failed to log metrics: {str(e)}")
    
    def get_latest_prices(self) -> pd.DataFrame:
        """Retrieve latest price data from database"""
        query = '''
            SELECT * FROM crypto_prices
            WHERE etl_timestamp = (
                SELECT MAX(etl_timestamp) FROM crypto_prices
            )
            ORDER BY market_cap_rank
        '''
        return pd.read_sql_query(query, self.conn)
    
    def get_pipeline_metrics(self) -> pd.DataFrame:
        """Retrieve ETL pipeline metrics"""
        query = '''
            SELECT * FROM etl_metrics
            ORDER BY run_timestamp DESC
            LIMIT 10
        '''
        return pd.read_sql_query(query, self.conn)


# Example usage
if __name__ == "__main__":
    # Run the ETL pipeline
    with CryptoETLPipeline("crypto_data.db") as pipeline:
        # Run pipeline for specific coins
        coins = ['bitcoin', 'ethereum', 'solana', 'cardano', 'polkadot']
        
        print("Starting ETL Pipeline...")
        metrics = pipeline.run_pipeline(coins)
        
        print("\nPipeline Results:")
        print(f"Records extracted: {metrics['records_extracted']}")
        print(f"Records transformed: {metrics['records_transformed']}")
        print(f"Records loaded: {metrics['records_loaded']}")
        print(f"Errors: {metrics['errors']}")
        print(f"Duration: {metrics['duration_seconds']} seconds")
        
        # Display latest data
        print("\nLatest Cryptocurrency Prices:")
        latest_prices = pipeline.get_latest_prices()
        print(latest_prices[['coin_id', 'symbol', 'current_price', 'market_cap_rank']].to_string())
        
        # Show pipeline history
        print("\nRecent Pipeline Runs:")
        pipeline_metrics = pipeline.get_pipeline_metrics()
        print(pipeline_metrics.to_string())
