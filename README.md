# Network Traffic Anomaly Detection System

## Overview
This project implements an AI-driven network traffic anomaly detection system using machine learning techniques. It provides real-time analysis of network traffic patterns, detects potential security threats, and offers mitigation recommendations.

## Features
- Real-time network traffic analysis
- Machine learning-based anomaly detection using Isolation Forest
- Interactive web interface for data visualization
- Custom traffic data generation for testing
- Automated mitigation recommendations
- Detailed anomaly reporting and exports
- Support for multiple traffic patterns and protocols
- Time-based analysis and pattern detection

## Technology Stack
- Python 3.8+
- Flask (Web Framework)
- scikit-learn (Machine Learning)
- pandas & numpy (Data Processing)
- matplotlib & seaborn (Visualization)
- Bootstrap 5 (Frontend)

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git

### Clone the Repository
```
git clone https://github.com/naman-mahi/network-traffic-anomaly-detection.git
```

### Navigate to the project directory
```
cd network-traffic-anomaly-detection
```

### Set Up Virtual Environment
```
python -m venv venv
```

### Install Dependencies
```
pip install -r requirements.txt
```

### Create virtual environment
```
python -m venv venv
```

### Activate virtual environment
```
On Windows:
venv\Scripts\activate
```
```
On Unix or MacOS:
source venv/bin/activate
```

### Install Dependencies
```
pip install -r requirements.txt
```
### Create Required Directories
```
mkdir logs
mkdir data
```
```
mkdir -p logs outputs uploads
```


## Configuration

### Update config.json
The system can be configured by modifying `config.json`:

- `features`: List of features to be used for anomaly detection.
- `contamination`: Proportion of outliers in the data.

```json
{
"features": [
"bytes_transferred",
"packet_count",
"connection_duration",
"retransmission_rate",
"bytes_per_packet",
"packets_per_second"
],
"contamination": 0.15,
"n_estimators": 100,
"random_state": 42,
"visualization": {
"scatter_plot": {
"figsize": [12, 8],
"alpha": 0.6,
"colors": {
"Normal": "blue",
"Anomaly": "red"
}
},
"distribution_plot": {
"figsize": [12, 6],
"bins": 50
}
}
}
```


## Usage

### Running the Application

Start the Flask server
```
python app.py
```

The application will be available at `http://localhost:5000`

### Generating Sample Data
1. Access the web interface
2. Use the "Generate Sample Data" section
3. Set start date and duration
4. Click "Generate Sample Data"
5. Download the generated CSV file

### Analyzing Network Traffic
1. Upload a CSV file containing network traffic data
2. View real-time analysis results
3. Examine visualizations and anomaly detection
4. Review mitigation recommendations
5. Download detailed anomaly reports

## Project Structure
project/
├── app.py                  # Flask application
├── main.py                 # Core anomaly detection logic
├── config.json            # Configuration settings
├── requirements.txt       # Project dependencies
├── README.md             # Documentation
├── generate_sample_data.py # Sample data generator
├── static/               # Static files
│   ├── style.css         # Custom CSS
│   └── script.js         # Frontend JavaScript
├── templates/            # HTML templates
│   └── index.html        # Main page template
├── utils/               # Utility modules
│   ├── helpers.py        # Helper functions
│   └── mitigation_engine.py # Mitigation logic
├── uploads/             # Upload directory
├── outputs/             # Generated files
└── logs/                # Application logs



## API Endpoints

### `/analyze` (POST)
- Analyzes uploaded network traffic data
- Returns analysis results and recommendations

### `/generate_data` (POST)
- Generates sample network traffic data
- Parameters: start_date, duration

### `/download/<timestamp>` (GET)
- Downloads anomaly report CSV

### `/visualization/<timestamp>/<type>` (GET)
- Retrieves visualization images
- Types: scatter, distribution

## Deployment

### Docker Deployment

Build Docker image
```
docker build -t network-anomaly-detection .
```
Run container
```
docker run -p 5000:5000 network-anomaly-detection
```


### Production Deployment
For production deployment, consider:
1. Using a production-grade WSGI server (e.g., Gunicorn)
2. Setting up reverse proxy (e.g., Nginx)
3. Implementing proper security measures
4. Using environment variables for sensitive configurations

Example production setup:

### Install Gunicorn
```
pip install gunicorn
```
### Run with Gunicorn
```
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```


## Security Considerations
- Implement user authentication
- Use HTTPS in production
- Validate all file uploads
- Sanitize input data
- Regular security updates
- Monitor system logs

## Monitoring and Maintenance
- Check logs in `logs/` directory
- Monitor system performance
- Regular backup of configuration
- Update dependencies regularly
- Monitor disk usage for uploads/outputs

## Contributing
1. Fork the repository
2. Create a feature branch
3. Commit changes
4. Push to the branch
5. Create a Pull Request

## Troubleshooting
Common issues and solutions:
- File upload errors: Check file permissions
- Visualization errors: Verify matplotlib backend
- Memory issues: Adjust batch processing
- Performance issues: Check logging levels

## License
[MIT License](LICENSE)

## Contact
Sunil K khobragade - skhobragade993@gmail.com
Project Link: https://github.com/naman-mahi/network-traffic-anomaly-detection

## Acknowledgments
- scikit-learn documentation
- Flask documentation
- Network security best practices
- Open-source community