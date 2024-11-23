document.getElementById('generateBtn').addEventListener('click', async () => {
    const startDate = document.getElementById('startDate').value;
    const duration = document.getElementById('duration').value;
    
    if (!startDate) {
        alert('Please select a start date');
        return;
    }
    
    const generationStatus = document.getElementById('generationStatus');
    generationStatus.classList.remove('d-none');
    
    try {
        const response = await fetch('/generate_data', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                start_date: startDate,
                duration: duration
            })
        });
        
        const data = await response.json();
        
        if (data.error) {
            throw new Error(data.error);
        }
        
        generationStatus.innerHTML = `
            <div class="alert alert-success">
                Sample data generated successfully!
                <a href="/download_sample/${data.filename}" class="btn btn-sm btn-primary ms-2">Download</a>
            </div>
        `;
        
    } catch (error) {
        generationStatus.innerHTML = `
            <div class="alert alert-danger">
                Error generating sample data: ${error.message}
            </div>
        `;
    }
});

document.getElementById('uploadForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const fileInput = document.getElementById('fileInput');
    const file = fileInput.files[0];
    
    if (!file) {
        alert('Please select a file');
        return;
    }
    
    // Show loading spinner
    document.getElementById('loading').classList.remove('d-none');
    document.getElementById('results').classList.add('d-none');
    
    const formData = new FormData();
    formData.append('file', file);
    
    try {
        const response = await fetch('/analyze', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (data.error) {
            throw new Error(data.error);
        }
        
        // Update statistics
        document.getElementById('totalRecords').textContent = data.statistics.total_records;
        document.getElementById('anomalyCount').textContent = data.statistics.anomaly_count;
        document.getElementById('anomalyPercentage').textContent = `${data.statistics.anomaly_percentage}%`;
        
        // Update visualizations
        document.getElementById('scatterPlot').src = `/visualization/${data.timestamp}/scatter`;
        document.getElementById('distributionPlot').src = `/visualization/${data.timestamp}/distribution`;
        
        // Setup download button
        const downloadBtn = document.getElementById('downloadBtn');
        downloadBtn.onclick = () => {
            window.location.href = `/download/${data.timestamp}`;
        };
        
        // Show results
        document.getElementById('loading').classList.add('d-none');
        document.getElementById('results').classList.remove('d-none');
        
        if (data.recommendations && data.recommendations.length > 0) {
            const recommendationsList = document.getElementById('recommendationsList');
            recommendationsList.innerHTML = data.recommendations.map(rec => `
                <div class="recommendation-item mb-3">
                    <h6 class="text-${rec.severity === 'HIGH' ? 'danger' : 'warning'}">
                        ${rec.type} (${rec.severity} Severity)
                    </h6>
                    <p class="mb-2">${rec.description}</p>
                    <ul class="list-group">
                        ${rec.recommendations.map(r => `
                            <li class="list-group-item">${r}</li>
                        `).join('')}
                    </ul>
                </div>
            `).join('');
            document.getElementById('recommendationsCard').classList.remove('d-none');
        } else {
            document.getElementById('recommendationsCard').classList.add('d-none');
        }
        
    } catch (error) {
        alert('Error: ' + error.message);
        document.getElementById('loading').classList.add('d-none');
    }
}); 