import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time

def generate_sample_data(start_date=None, duration_hours=24, output_file='network_traffic.csv'):
    """Generate sample network traffic data with unique patterns each time"""
    # Use current timestamp as seed for unique data generation
    current_seed = int(time.time() * 1000) % 2**32
    np.random.seed(current_seed)
    
    if start_date is None:
        start_date = datetime.now()
    
    # Generate timestamps
    timestamps = pd.date_range(
        start=start_date,
        periods=duration_hours * 60,  # One record per minute
        freq='1min'
    )
    
    # Calculate total records needed
    total_records = len(timestamps)
    n_normal = int(total_records * 0.85)  # 85% normal traffic
    n_anomalous = total_records - n_normal  # 15% anomalous traffic
    
    # Generate base patterns with randomization
    base_patterns = {
        'normal_traffic_mean': np.random.uniform(400000, 600000),
        'normal_traffic_std': np.random.uniform(100000, 200000),
        'normal_packet_mean': np.random.uniform(800, 1200),
        'normal_packet_std': np.random.uniform(200, 400),
        'anomaly_multiplier': np.random.uniform(3, 5)
    }
    
    # Generate normal traffic data
    normal_data = {
        'bytes_transferred': np.random.normal(
            base_patterns['normal_traffic_mean'],
            base_patterns['normal_traffic_std'],
            n_normal
        ),
        'packet_count': np.random.normal(
            base_patterns['normal_packet_mean'],
            base_patterns['normal_packet_std'],
            n_normal
        ),
        'connection_duration': np.random.gamma(shape=3, scale=10, size=n_normal),
        'source_port': np.random.randint(1024, 65535, n_normal),
        'destination_port': np.random.choice(
            [80, 443, 22, 21, 3306, 5432, 8080, 8443, 25, 53],
            n_normal,
            p=[0.3, 0.25, 0.1, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05]
        ),
        'retransmission_rate': np.random.beta(2, 50, n_normal),
    }
    
    # Split anomalous data into three equal parts
    n_each_anomaly = n_anomalous // 3
    remainder = n_anomalous % 3
    
    # Adjust sizes to account for remainder
    anomaly_sizes = [n_each_anomaly] * 3
    for i in range(remainder):
        anomaly_sizes[i] += 1
    
    # Generate different types of anomalous patterns
    ddos_pattern = {
        'bytes': np.random.normal(
            base_patterns['normal_traffic_mean'] * base_patterns['anomaly_multiplier'],
            base_patterns['normal_traffic_std'] * 2,
            anomaly_sizes[0]
        ),
        'packets': np.random.normal(
            base_patterns['normal_packet_mean'] * base_patterns['anomaly_multiplier'],
            base_patterns['normal_packet_std'] * 2,
            anomaly_sizes[0]
        )
    }
    
    data_exfil_pattern = {
        'bytes': np.random.normal(100, 50, anomaly_sizes[1]),
        'packets': np.random.normal(50, 20, anomaly_sizes[1])
    }
    
    scan_pattern = {
        'bytes': np.random.normal(
            base_patterns['normal_traffic_mean'] * 0.1,
            base_patterns['normal_traffic_std'] * 0.1,
            anomaly_sizes[2]
        ),
        'packets': np.random.normal(
            base_patterns['normal_packet_mean'] * 2,
            base_patterns['normal_packet_std'],
            anomaly_sizes[2]
        )
    }
    
    # Combine anomalous patterns
    anomalous_data = {
        'bytes_transferred': np.concatenate([
            ddos_pattern['bytes'],
            data_exfil_pattern['bytes'],
            scan_pattern['bytes']
        ]),
        'packet_count': np.concatenate([
            ddos_pattern['packets'],
            data_exfil_pattern['packets'],
            scan_pattern['packets']
        ]),
        'connection_duration': np.concatenate([
            np.random.uniform(0.1, 1, anomaly_sizes[0]),     # DDoS: very short connections
            np.random.uniform(300, 600, anomaly_sizes[1]),   # Data exfil: long connections
            np.random.uniform(0.1, 0.5, anomaly_sizes[2])    # Scan: very short connections
        ]),
        'source_port': np.random.randint(1024, 65535, n_anomalous),
        'destination_port': np.concatenate([
            np.random.choice([80, 443], anomaly_sizes[0]),                 # DDoS: common ports
            np.random.choice([21, 22, 3306], anomaly_sizes[1]),           # Data exfil: sensitive ports
            np.random.randint(1, 65535, anomaly_sizes[2])                 # Scan: random ports
        ]),
        'retransmission_rate': np.concatenate([
            np.random.beta(5, 2, anomaly_sizes[0]),      # DDoS: high retransmission
            np.random.beta(1, 50, anomaly_sizes[1]),     # Data exfil: low retransmission
            np.random.beta(2, 20, anomaly_sizes[2])      # Scan: medium retransmission
        ])
    }
    
    # Combine normal and anomalous data
    for key in normal_data.keys():
        normal_data[key] = np.concatenate([normal_data[key], anomalous_data[key]])
    
    # Create DataFrame
    df = pd.DataFrame(normal_data)
    
    # Add protocols with realistic distribution
    protocols = np.random.choice(
        ['TCP', 'UDP', 'HTTP', 'HTTPS', 'SSH', 'FTP'],
        size=len(df),
        p=[0.3, 0.2, 0.2, 0.15, 0.1, 0.05]
    )
    
    # Add protocol-specific patterns
    df['protocol'] = protocols
    df.loc[df['destination_port'] == 80, 'protocol'] = np.random.choice(['HTTP', 'TCP'], size=len(df[df['destination_port'] == 80]))
    df.loc[df['destination_port'] == 443, 'protocol'] = np.random.choice(['HTTPS', 'TCP'], size=len(df[df['destination_port'] == 443]))
    df.loc[df['destination_port'] == 22, 'protocol'] = 'SSH'
    df.loc[df['destination_port'] == 21, 'protocol'] = 'FTP'
    
    # Add timestamp and ensure it matches the total number of records
    df['timestamp'] = pd.Series(timestamps[:len(df)]).sample(n=len(df), replace=False).sort_values().reset_index(drop=True)
    
    # Add derived features with some noise
    df['bytes_per_packet'] = (df['bytes_transferred'] / df['packet_count']) * np.random.normal(1, 0.1, len(df))
    df['packets_per_second'] = (df['packet_count'] / df['connection_duration']) * np.random.normal(1, 0.1, len(df))
    
    # Add time-based patterns
    hour_of_day = df['timestamp'].dt.hour
    df.loc[hour_of_day.between(1, 5), 'bytes_transferred'] *= np.random.uniform(0.5, 0.8, len(df[hour_of_day.between(1, 5)]))
    df.loc[hour_of_day.between(9, 17), 'bytes_transferred'] *= np.random.uniform(1.2, 1.5, len(df[hour_of_day.between(9, 17)]))
    
    # Sort by timestamp
    df = df.sort_values('timestamp').reset_index(drop=True)
    
    # Ensure all values are positive
    df['bytes_transferred'] = df['bytes_transferred'].abs()
    df['packet_count'] = df['packet_count'].abs()
    df['connection_duration'] = df['connection_duration'].abs()
    df['retransmission_rate'] = df['retransmission_rate'].abs()
    
    # Save to specified output file
    df.to_csv(output_file, index=False)
    print(f"Sample network traffic data generated successfully: {output_file}")
    
    # Print some statistics
    print("\nDataset Statistics:")
    print(f"Total Records: {len(df)}")
    print("\nFeature Statistics:")
    print(df.describe())
    
    return df

if __name__ == "__main__":
    generate_sample_data() 