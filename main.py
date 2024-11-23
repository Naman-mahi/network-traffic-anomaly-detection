import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler, MinMaxScaler
import matplotlib.pyplot as plt
import seaborn as sns
import logging
from datetime import datetime
import os
import json
from utils.mitigation_engine import MitigationEngine

# Create logs directory if it doesn't exist
os.makedirs('logs', exist_ok=True)
os.makedirs('outputs', exist_ok=True)

# Enhanced logging setup
logging.basicConfig(
    filename=os.path.join('logs', f'security_logs_{datetime.now().strftime("%Y%m%d")}.log'),
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class NetworkAnomalyDetector:
    def __init__(self, config_file='config.json'):
        """Initialize detector with configuration."""
        self.config = self.load_config(config_file)
        self.scaler = StandardScaler()
        self.model = None
        self.mitigation_engine = MitigationEngine()
        
    @staticmethod
    def load_config(config_file):
        """Load configuration from JSON file or use defaults."""
        default_config = {
            'features': ['feature1', 'feature2', 'feature3'],
            'contamination': 0.05,
            'n_estimators': 100,
            'random_state': 42
        }
        try:
            with open(config_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logging.warning(f"Config file {config_file} not found. Using defaults.")
            return default_config

    def load_and_preprocess_data(self, filepath):
        """Load and preprocess network traffic data."""
        try:
            df = pd.read_csv(filepath)
            logging.info(f"Successfully loaded data from {filepath}")
            
            # Data validation
            self._validate_data(df)
            
            # Handle missing values
            df = self._handle_missing_values(df)
            
            # Feature scaling
            df = self._scale_features(df)
            
            return df
            
        except Exception as e:
            logging.error(f"Error loading data: {str(e)}")
            raise

    def _validate_data(self, df):
        """Validate input data structure."""
        missing_features = set(self.config['features']) - set(df.columns)
        if missing_features:
            raise ValueError(f"Missing required features: {missing_features}")

    def _handle_missing_values(self, df):
        """Handle missing values in the dataset."""
        # Check for missing values
        missing_stats = df[self.config['features']].isnull().sum()
        if missing_stats.any():
            logging.warning(f"Missing values detected: {missing_stats.to_dict()}")
            
        # Fill missing values with mean
        df[self.config['features']] = df[self.config['features']].fillna(df[self.config['features']].mean())
        return df

    def _scale_features(self, df):
        """Scale features using StandardScaler."""
        df[self.config['features']] = self.scaler.fit_transform(df[self.config['features']])
        return df

    def detect_anomalies(self, df):
        """Detect anomalies using Isolation Forest."""
        try:
            self.model = IsolationForest(
                contamination=self.config['contamination'],
                random_state=self.config['random_state'],
                n_estimators=self.config['n_estimators']
            )
            
            # Fit and predict
            predictions = self.model.fit_predict(df[self.config['features']])
            df['anomaly'] = predictions
            df['anomaly'] = df['anomaly'].map({1: 'Normal', -1: 'Anomaly'})
            
            # Calculate anomaly scores
            df['anomaly_score'] = self.model.score_samples(df[self.config['features']])
            
            # Log anomaly statistics
            self._log_anomaly_stats(df)
            
            return df
            
        except Exception as e:
            logging.error(f"Error in anomaly detection: {str(e)}")
            raise

    def _log_anomaly_stats(self, df):
        """Log detailed anomaly statistics."""
        anomaly_stats = {
            'total_records': len(df),
            'anomaly_counts': df['anomaly'].value_counts().to_dict(),
            'anomaly_score_stats': {
                'mean': df['anomaly_score'].mean(),
                'min': df['anomaly_score'].min(),
                'max': df['anomaly_score'].max()
            }
        }
        logging.info(f"Anomaly detection statistics: {json.dumps(anomaly_stats, indent=2)}")

    def visualize_results(self, df):
        """Create and save visualization of anomalies."""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Create multiple visualizations
            self._create_scatter_plot(df, timestamp)
            self._create_anomaly_score_distribution(df, timestamp)
            
        except Exception as e:
            logging.error(f"Error in visualization: {str(e)}")
            raise

    def _create_scatter_plot(self, df, timestamp):
        """Create scatter plot of anomalies."""
        plt.figure(figsize=(12, 8))
        sns.scatterplot(
            x=self.config['features'][0],
            y=self.config['features'][1],
            hue='anomaly',
            data=df,
            palette={'Normal': 'blue', 'Anomaly': 'red'},
            alpha=0.6
        )
        plt.title('Network Traffic Anomaly Detection')
        plt.savefig(os.path.join('outputs', f'anomaly_scatter_{timestamp}.png'))
        plt.close()

    def _create_anomaly_score_distribution(self, df, timestamp):
        """Create distribution plot of anomaly scores."""
        plt.figure(figsize=(12, 6))
        sns.histplot(data=df, x='anomaly_score', hue='anomaly', bins=50)
        plt.title('Distribution of Anomaly Scores')
        plt.savefig(os.path.join('outputs', f'anomaly_distribution_{timestamp}.png'))
        plt.close()

    def get_mitigation_recommendations(self, df):
        """Get mitigation recommendations for detected anomalies."""
        try:
            recommendations = self.mitigation_engine.analyze_anomalies(df)
            
            # Log recommendations
            logging.info(f"Generated {len(recommendations)} mitigation recommendations")
            for rec in recommendations:
                logging.info(f"Recommendation: {rec['type']} - {rec['description']}")
                
            return recommendations
            
        except Exception as e:
            logging.error(f"Error generating mitigation recommendations: {str(e)}")
            raise

def main():
    try:
        detector = NetworkAnomalyDetector()
        
        # Load and process data
        df = detector.load_and_preprocess_data("network_traffic.csv")
        
        # Detect anomalies
        df = detector.detect_anomalies(df)
        
        # Visualize results
        detector.visualize_results(df)
        
        # Generate alerts and export results
        anomaly_count = df['anomaly'].value_counts().get('Anomaly', 0)
        if anomaly_count > 0:
            alert_msg = f"ALERT: Detected {anomaly_count} anomalous activities in network traffic!"
            print(alert_msg)
            logging.warning(alert_msg)
            
            # Export anomalous records
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            anomalies_df = df[df['anomaly'] == 'Anomaly'].sort_values('anomaly_score')
            anomalies_df.to_csv(os.path.join('outputs', f'anomalies_{timestamp}.csv'), index=False)
            logging.info(f"Anomalous records exported to anomalies_{timestamp}.csv")
        else:
            logging.info("No anomalies detected in network traffic")
            print("Network traffic is normal.")

    except Exception as e:
        logging.error(f"Error in main execution: {str(e)}")
        print(f"An error occurred. Check the logs for details.")

if __name__ == "__main__":
    main()
