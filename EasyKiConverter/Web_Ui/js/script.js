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
        const startTime = Date.now();

        // 显示多线程处理信息
        if (total_components > 1) {
            progressText.textContent = `Starting parallel processing of ${total_components} components...`;
        } else {
            progressText.textContent = 'Processing component...';
        }

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
            const endTime = Date.now();
            const processingTime = ((endTime - startTime) / 1000).toFixed(2);
            
            if (result.success) {
                // Process each component result with enhanced progress display
                result.results.forEach((componentResult, index) => {
                    processed_components++;
                    const percentage = Math.round((processed_components / total_components) * 100);
                    
                    // --- Update Progress Bar --- 
                    progressFill.style.width = `${percentage}%`;
                    
                    // Enhanced progress text with timing info
                    if (total_components > 1) {
                        progressText.textContent = `Completed ${componentResult.componentId} (${processed_components}/${total_components}) - ${processingTime}s total`;
                    } else {
                        progressText.textContent = `Completed ${componentResult.componentId} in ${processingTime}s`;
                    }

                    // --- Display Result Item with enhanced info --- 
                    const resultItem = document.createElement('div');
                    resultItem.className = `result-item ${componentResult.success ? 'success' : 'error'}`;
                    
                    // Show file count if available
                    let fileInfo = '';
                    if (componentResult.files && componentResult.files.length > 0) {
                        fileInfo = ` (${componentResult.files.length} files)`;
                    }
                    
                    resultItem.innerHTML = `
                        <div class="result-icon">${componentResult.success ? '&#10004;' : '&#10008;'}</div>
                        <div class="result-details">
                            <div class="result-name">${componentResult.componentId}${fileInfo}</div>
                            <div class="result-path">${componentResult.message}</div>
                        </div>
                    `;
                    resultsList.appendChild(resultItem);
                });
                
                // Final completion message with performance info
                if (total_components > 1) {
                    progressText.textContent = `Export complete! Processed ${total_components} components in ${processingTime}s (parallel processing)`;
                } else {
                    progressText.textContent = `Export complete! Processed in ${processingTime}s`;
                }
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