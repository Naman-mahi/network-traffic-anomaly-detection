import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
import json
import logging
from datetime import datetime

class MitigationEngine:
    def __init__(self):
        self.mitigation_rules = self._load_mitigation_rules()
        
    def _load_mitigation_rules(self):
        """Load predefined mitigation rules"""
        try:
            return {
                "TRAFFIC_SPIKE": {
                    "description": "Unusual spike in network traffic",
                    "recommendations": [
                        "Implement rate limiting",
                        "Enable traffic throttling",
                        "Deploy DDoS protection"
                    ],
                    "severity": "HIGH"
                },
                "PROTOCOL_ANOMALY": {
                    "description": "Unusual protocol behavior",
                    "recommendations": [
                        "Update firewall rules",
                        "Enable deep packet inspection",
                        "Implement protocol validation"
                    ],
                    "severity": "MEDIUM"
                },
                "PATTERN_ANOMALY": {
                    "description": "Unusual traffic patterns",
                    "recommendations": [
                        "Enable behavioral analysis",
                        "Update IDS signatures",
                        "Implement traffic segmentation"
                    ],
                    "severity": "MEDIUM"
                },
                "DATA_EXFILTRATION": {
                    "description": "Potential data exfiltration",
                    "recommendations": [
                        "Enable data loss prevention",
                        "Implement egress filtering",
                        "Monitor data transfer patterns"
                    ],
                    "severity": "HIGH"
                }
            }
        except Exception as e:
            logging.error(f"Error loading mitigation rules: {str(e)}")
            raise

    def analyze_anomalies(self, df):
        """Analyze anomalies and generate mitigation recommendations"""
        try:
            anomalies_df = df[df['anomaly'] == 'Anomaly'].copy()
            
            if len(anomalies_df) == 0:
                return []
                
            recommendations = []
            
            # Analyze traffic patterns
            traffic_patterns = self._analyze_traffic_patterns(anomalies_df)
            protocol_patterns = self._analyze_protocol_patterns(anomalies_df)
            temporal_patterns = self._analyze_temporal_patterns(anomalies_df)
            
            # Generate recommendations based on patterns
            recommendations.extend(self._generate_traffic_recommendations(traffic_patterns))
            recommendations.extend(self._generate_protocol_recommendations(protocol_patterns))
            recommendations.extend(self._generate_temporal_recommendations(temporal_patterns))
            
            return recommendations
            
        except Exception as e:
            logging.error(f"Error in analyze_anomalies: {str(e)}")
            raise

    def _analyze_traffic_patterns(self, df):
        """Analyze traffic patterns in anomalies"""
        try:
            patterns = {
                'high_volume': len(df[df['bytes_transferred'] > df['bytes_transferred'].mean() + 2*df['bytes_transferred'].std()]) > 0,
                'low_volume': len(df[df['bytes_transferred'] < df['bytes_transferred'].mean() - 2*df['bytes_transferred'].std()]) > 0,
                'burst_pattern': self._detect_burst_pattern(df)
            }
            return patterns
        except Exception as e:
            logging.error(f"Error in analyze_traffic_patterns: {str(e)}")
            raise
        
    def _analyze_protocol_patterns(self, df):
        """Analyze protocol distribution in anomalies"""
        try:
            protocol_dist = df['protocol'].value_counts(normalize=True)
            patterns = {
                'protocol_dominance': any(protocol_dist > 0.7),
                'protocol_diversity': len(protocol_dist) > 2,
                'unusual_protocols': set(df['protocol']) - {'TCP', 'UDP', 'HTTP', 'HTTPS', 'SSH', 'FTP'}
            }
            return patterns
        except Exception as e:
            logging.error(f"Error in analyze_protocol_patterns: {str(e)}")
            raise
        
    def _analyze_temporal_patterns(self, df):
        """Analyze temporal patterns in anomalies"""
        try:
            df = df.copy()
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            time_diffs = df['timestamp'].diff().dt.total_seconds()
            patterns = {
                'regular_interval': time_diffs.std() < time_diffs.mean() * 0.1,
                'burst_timing': any(time_diffs < 1),
                'time_concentration': self._detect_time_concentration(df)
            }
            return patterns
        except Exception as e:
            logging.error(f"Error in analyze_temporal_patterns: {str(e)}")
            raise

    def _detect_burst_pattern(self, df):
        """Detect burst patterns in traffic"""
        try:
            if len(df) < 3:
                return False
            rolling_mean = df['bytes_transferred'].rolling(window=3).mean()
            return any(rolling_mean > df['bytes_transferred'].mean() * 2)
        except Exception as e:
            logging.error(f"Error in detect_burst_pattern: {str(e)}")
            raise

    def _detect_time_concentration(self, df):
        """Detect concentration of anomalies in time periods"""
        try:
            df['hour'] = df['timestamp'].dt.hour
            hour_counts = df['hour'].value_counts()
            return any(hour_counts > len(df) * 0.3)
        except Exception as e:
            logging.error(f"Error in detect_time_concentration: {str(e)}")
            raise

    def _generate_traffic_recommendations(self, patterns):
        """Generate recommendations based on traffic patterns"""
        try:
            recommendations = []
            
            if patterns['high_volume']:
                recommendations.append({
                    'type': 'TRAFFIC_SPIKE',
                    **self.mitigation_rules['TRAFFIC_SPIKE']
                })
                
            if patterns['burst_pattern']:
                recommendations.append({
                    'type': 'PATTERN_ANOMALY',
                    **self.mitigation_rules['PATTERN_ANOMALY']
                })
                
            return recommendations
        except Exception as e:
            logging.error(f"Error in generate_traffic_recommendations: {str(e)}")
            raise

    def _generate_protocol_recommendations(self, patterns):
        """Generate recommendations based on protocol patterns"""
        try:
            recommendations = []
            
            if patterns['protocol_dominance'] or patterns['unusual_protocols']:
                recommendations.append({
                    'type': 'PROTOCOL_ANOMALY',
                    **self.mitigation_rules['PROTOCOL_ANOMALY']
                })
                
            return recommendations
        except Exception as e:
            logging.error(f"Error in generate_protocol_recommendations: {str(e)}")
            raise

    def _generate_temporal_recommendations(self, patterns):
        """Generate recommendations based on temporal patterns"""
        try:
            recommendations = []
            
            if patterns['regular_interval'] or patterns['time_concentration']:
                recommendations.append({
                    'type': 'DATA_EXFILTRATION',
                    **self.mitigation_rules['DATA_EXFILTRATION']
                })
                
            return recommendations
        except Exception as e:
            logging.error(f"Error in generate_temporal_recommendations: {str(e)}")
            raise 