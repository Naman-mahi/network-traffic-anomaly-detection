import os
import json
import logging
from datetime import datetime

def setup_logging():
    """Setup logging configuration"""
    os.makedirs('logs', exist_ok=True)
    
    logging.basicConfig(
        filename=os.path.join('logs', f'security_logs_{datetime.now().strftime("%Y%m%d")}.log'),
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    # Also log to console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    logging.getLogger().addHandler(console_handler)

def load_config(config_file='config.json'):
    """Load configuration from JSON file"""
    try:
        with open(config_file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        logging.error(f"Configuration file {config_file} not found!")
        raise

def ensure_directories():
    """Ensure all required directories exist"""
    required_dirs = ['logs', 'outputs', 'data']
    for directory in required_dirs:
        os.makedirs(directory, exist_ok=True)
        logging.info(f"Ensured directory exists: {directory}") 