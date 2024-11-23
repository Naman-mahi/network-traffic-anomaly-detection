# Network Traffic Anomaly Detection Wiki

Welcome to the Network Traffic Anomaly Detection wiki! This wiki provides detailed documentation about the project's components, setup, and usage.

## Table of Contents
1. [System Overview](#system-overview)
2. [Installation Guide](#installation-guide)
3. [Configuration](#configuration)
4. [Components](#components)
5. [API Documentation](#api-documentation)
6. [Data Generation](#data-generation)
7. [Anomaly Detection](#anomaly-detection)
8. [Mitigation Engine](#mitigation-engine)
9. [Troubleshooting](#troubleshooting)

## System Overview

### Architecture
The system consists of several key components:
- Web Interface (Flask)
- Anomaly Detection Engine (Isolation Forest)
- Mitigation Recommendation System
- Data Generation Module
- Visualization Engine

### Features
- Real-time network traffic analysis
- ML-based anomaly detection
- Interactive visualizations
- Automated mitigation recommendations
- Custom data generation
- Detailed reporting

## Installation Guide

### Prerequisites
```bash
# System requirements
Python 3.8+
pip (Python package manager)
Git
```

### Setup Steps
```bash
# Clone repository
git clone https://github.com/naman-mahi/network-traffic-anomaly-detection.git
cd network-traffic-anomaly-detection

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Unix/MacOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create required directories
mkdir -p logs outputs uploads
```

## Configuration

### config.json
The system's behavior can be customized through `config.json`:

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

## Components

### Web Interface
- Built with Flask
- Bootstrap 5 for styling
- Interactive data upload and visualization
- Real-time analysis feedback

### Anomaly Detection Engine
- Uses Isolation Forest algorithm
- Feature scaling and preprocessing
- Configurable contamination factor
- Anomaly scoring system

### Mitigation Engine
Provides recommendations for:
- Traffic spikes (DDoS)
- Protocol anomalies
- Pattern anomalies
- Data exfiltration

## API Documentation

### Endpoints

#### POST /analyze
Analyzes network traffic data
```json
{
    "success": true,
    "timestamp": "20240101_120000",
    "statistics": {
        "total_records": 1000,
        "anomaly_count": 50,
        "anomaly_percentage": 5.0
    },
    "recommendations": [...]
}
```

#### POST /generate_data
Generates sample network traffic data
```json
{
    "success": true,
    "filename": "network_traffic_20240101_120000.csv",
    "records": 1440
}
```

## Data Generation

### Traffic Patterns
The data generator creates:
1. Normal Traffic
   - Regular network patterns
   - Standard protocol distribution
   - Expected packet sizes

2. Anomalous Traffic
   - DDoS patterns
   - Data exfiltration
   - Port scanning
   - Protocol anomalies

### Usage
```python
from generate_sample_data import generate_sample_data

df = generate_sample_data(
    start_date=datetime.now(),
    duration_hours=24,
    output_file='network_traffic.csv'
)
```

## Anomaly Detection

### Process Flow
1. Data Loading
2. Preprocessing
3. Feature Scaling
4. Anomaly Detection
5. Score Calculation
6. Visualization
7. Recommendation Generation

### Features Used
- Bytes Transferred
- Packet Count
- Connection Duration
- Retransmission Rate
- Derived Metrics

## Mitigation Engine

### Types of Recommendations

#### Traffic Spike (HIGH)
- Rate limiting
- Traffic throttling
- DDoS protection

#### Protocol Anomaly (MEDIUM)
- Firewall updates
- Deep packet inspection
- Protocol validation

#### Pattern Anomaly (MEDIUM)
- Behavioral analysis
- IDS updates
- Traffic segmentation

#### Data Exfiltration (HIGH)
- Data loss prevention
- Egress filtering
- Transfer monitoring

## Troubleshooting

### Common Issues

#### File Upload Errors
```
Error: Check file permissions and format
Solution: Ensure CSV format and proper permissions
```

#### Visualization Errors
```
Error: No display available
Solution: Configure matplotlib backend
```

#### Memory Issues
```
Error: MemoryError during analysis
Solution: Implement batch processing
```

#### Performance Issues
```
Error: Slow analysis
Solution: Optimize feature selection and logging
```

### Logging
- Location: `logs/security_logs_YYYYMMDD.log`
- Format: `timestamp - level - message`
- Levels: INFO, WARNING, ERROR

### Support
For issues and support:
- Create GitHub Issue
- Check existing documentation
- Contact maintainers

## Contributing
See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on:
- Code Style
- Pull Requests
- Testing
- Documentation

## License
This project is licensed under the MIT License - see [LICENSE](LICENSE) for details. 