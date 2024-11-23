from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
import os
from datetime import datetime, timedelta
from main import NetworkAnomalyDetector
import pandas as pd
from generate_sample_data import generate_sample_data

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure required directories exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs('outputs', exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'csv'}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            # Initialize detector
            detector = NetworkAnomalyDetector()
            
            # Process data
            df = detector.load_and_preprocess_data(filepath)
            df = detector.detect_anomalies(df)
            
            # Generate visualizations
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            detector.visualize_results(df)
            
            # Get statistics
            anomaly_count = df['anomaly'].value_counts().get('Anomaly', 0)
            total_records = len(df)
            
            # Save anomalies to CSV
            if anomaly_count > 0:
                anomalies_df = df[df['anomaly'] == 'Anomaly'].sort_values('anomaly_score')
                anomaly_file = os.path.join('outputs', f'anomalies_{timestamp}.csv')
                anomalies_df.to_csv(anomaly_file, index=False)
            
            # Get mitigation recommendations
            recommendations = detector.get_mitigation_recommendations(df)
            
            return jsonify({
                'success': True,
                'timestamp': timestamp,
                'statistics': {
                    'total_records': total_records,
                    'anomaly_count': int(anomaly_count),
                    'anomaly_percentage': round((anomaly_count/total_records) * 100, 2)
                },
                'recommendations': recommendations
            })
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        
    return jsonify({'error': 'Invalid file type'}), 400

@app.route('/download/<timestamp>')
def download(timestamp):
    try:
        return send_file(
            f'outputs/anomalies_{timestamp}.csv',
            as_attachment=True,
            download_name=f'anomalies_{timestamp}.csv'
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@app.route('/visualization/<timestamp>/<type>')
def get_visualization(timestamp, type):
    try:
        if type == 'scatter':
            filename = f'anomaly_scatter_{timestamp}.png'
        else:
            filename = f'anomaly_distribution_{timestamp}.png'
            
        return send_file(
            f'outputs/{filename}',
            mimetype='image/png'
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@app.route('/generate_data', methods=['POST'])
def generate_data():
    try:
        data = request.json
        start_date = datetime.fromisoformat(data['start_date'].replace('Z', '+00:00'))
        duration = int(data['duration'])
        
        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f'network_traffic_{timestamp}.csv'
        
        # Generate sample data
        df = generate_sample_data(
            start_date=start_date,
            duration_hours=duration,
            output_file=os.path.join(app.config['UPLOAD_FOLDER'], filename)
        )
        
        return jsonify({
            'success': True,
            'filename': filename,
            'records': len(df)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download_sample/<filename>')
def download_sample(filename):
    try:
        return send_file(
            os.path.join(app.config['UPLOAD_FOLDER'], filename),
            as_attachment=True,
            download_name=filename
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 404

if __name__ == '__main__':
    app.run(debug=True) 