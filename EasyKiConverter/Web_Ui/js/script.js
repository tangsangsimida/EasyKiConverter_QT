document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('export-form');
    const exportBtn = document.getElementById('export-btn');
    const btnText = exportBtn.querySelector('.btn-text');
    const loadingSpinner = exportBtn.querySelector('.loading-spinner');
    const progressContainer = document.getElementById('progress-container');
    const progressFill = document.getElementById('progress-fill');
    const progressText = document.getElementById('progress-text');
    const resultsContainer = document.getElementById('results-container');
    const resultsList = document.getElementById('results-list');

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        // --- UI Setup for Loading --- 
        exportBtn.disabled = true;
        exportBtn.classList.add('loading');
        progressContainer.style.display = 'block';
        resultsContainer.style.display = 'none';
        resultsList.innerHTML = '';
        progressFill.style.width = '0%';
        progressText.textContent = 'Starting...';

        const formData = new FormData(form);
        const data = {
            componentIds: formData.get('urls').split(/\s+/).filter(Boolean),
            options: {
                symbol: formData.has('export_symbol'),
                footprint: formData.has('export_footprint'),
                model3d: formData.has('export_3d_model')
            },
            exportPath: formData.get('output_folder_path'),
            filePrefix: formData.get('output_lib_name')
        };

        let total_components = data.componentIds.length;
        let processed_components = 0;

        try {
            const response = await fetch('/api/export', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data),
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const result = await response.json();
            
            if (result.success) {
                // Process each component result
                result.results.forEach((componentResult, index) => {
                    processed_components++;
                    const percentage = Math.round((processed_components / total_components) * 100);
                    
                    // --- Update Progress Bar --- 
                    progressFill.style.width = `${percentage}%`;
                    progressText.textContent = `Processing ${componentResult.componentId} (${processed_components}/${total_components})...`;

                    // --- Display Result Item --- 
                    const resultItem = document.createElement('div');
                    resultItem.className = `result-item ${componentResult.success ? 'success' : 'error'}`;
                    resultItem.innerHTML = `
                        <div class="result-icon">${componentResult.success ? '&#10004;' : '&#10008;'}</div>
                        <div class="result-details">
                            <div class="result-name">${componentResult.componentId}</div>
                            <div class="result-path">${componentResult.message}</div>
                        </div>
                    `;
                    resultsList.appendChild(resultItem);
                });
                
                progressText.textContent = 'Export complete!';
                resultsContainer.style.display = 'block';
            } else {
                throw new Error(result.error || 'Unknown error occurred');
            }

        } catch (error) {
            console.error('Export failed:', error);
            progressText.textContent = 'An error occurred. Check console for details.';
            const errorItem = document.createElement('div');
            errorItem.className = 'result-item error';
            errorItem.innerHTML = `<div class="result-details"><div class="result-name">Error</div><div class="result-path">${error.message}</div></div>`;
            resultsList.appendChild(errorItem);
            resultsContainer.style.display = 'block';
        } finally {
            // --- Reset Button --- 
            exportBtn.disabled = false;
            exportBtn.classList.remove('loading');
        }
    });
});