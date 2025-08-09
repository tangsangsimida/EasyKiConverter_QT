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
    
    // 页面加载时恢复上次设置
    loadLastSettings();
    
    async function loadLastSettings() {
        try {
            const response = await fetch('/api/config');
            if (response.ok) {
                const data = await response.json();
                if (data.success && data.config) {
                    const config = data.config;
                    
                    // 恢复表单字段
                    if (config.output_folder_path) {
                        document.getElementById('output_folder_path').value = config.output_folder_path;
                    }
                    if (config.output_lib_name) {
                        document.getElementById('output_lib_name').value = config.output_lib_name;
                    }
                    
                    // 恢复导出选项
                    if (config.export_options) {
                        document.getElementById('export_symbol').checked = config.export_options.symbol !== false;
                        document.getElementById('export_footprint').checked = config.export_options.footprint !== false;
                        document.getElementById('export_3d_model').checked = config.export_options.model3d !== false;
                    }
                    
                    // 可选：恢复上次的组件ID（作为提示）
                    if (config.last_component_ids && config.last_component_ids.length > 0) {
                        const urlsTextarea = document.getElementById('urls');
                        if (!urlsTextarea.value.trim()) {
                            urlsTextarea.placeholder = `例如：\n${config.last_component_ids.slice(0, 3).join('\n')}\n...`;
                        }
                    }
                    
                    console.log('已恢复上次设置');
                }
            }
        } catch (error) {
            console.warn('加载上次设置失败:', error);
        }
     }
     
     function createResultsTable(results, stats, processingTime) {
         // 清空之前的结果
         resultsList.innerHTML = '';
         
         // 创建统计信息
         const statsDiv = document.createElement('div');
         statsDiv.className = 'results-stats';
         statsDiv.innerHTML = `
             <div class="stats-summary">
                 <div class="stat-item stat-total">
                     <span class="stat-number">${stats.total}</span>
                     <span class="stat-label">总计</span>
                 </div>
                 <div class="stat-item stat-success">
                     <span class="stat-number">${stats.success}</span>
                     <span class="stat-label">成功</span>
                 </div>
                 <div class="stat-item stat-failed">
                     <span class="stat-number">${stats.failed}</span>
                     <span class="stat-label">失败</span>
                 </div>
                 <div class="stat-item stat-time">
                     <span class="stat-number">${processingTime}s</span>
                     <span class="stat-label">耗时</span>
                 </div>
             </div>
         `;
         resultsList.appendChild(statsDiv);
         
         // 创建结果表格
         const table = document.createElement('table');
         table.className = 'results-table';
         
         // 表头
         const thead = document.createElement('thead');
         thead.innerHTML = `
             <tr>
                 <th class="col-status">状态</th>
                 <th class="col-component">组件ID</th>
                 <th class="col-files">文件数量</th>
                 <th class="col-message">消息</th>
             </tr>
         `;
         table.appendChild(thead);
         
         // 表体
         const tbody = document.createElement('tbody');
         results.forEach(result => {
             const row = document.createElement('tr');
             const statusClass = result.success ? 'status-success' : 'status-failed';
             const statusIcon = result.success ? '✓' : '✗';
             const statusText = result.success ? '成功' : '失败';
             const fileCount = result.files ? result.files.length : 0;
             
             row.className = `result-row ${statusClass}`;
             row.innerHTML = `
                 <td class="col-status">
                     <span class="status-badge ${statusClass}">
                         <span class="status-icon">${statusIcon}</span>
                         <span class="status-text">${statusText}</span>
                     </span>
                 </td>
                 <td class="col-component">
                     <span class="component-id">${result.componentId}</span>
                 </td>
                 <td class="col-files">
                     <span class="file-count">${fileCount}</span>
                 </td>
                 <td class="col-message">
                     <span class="message-text">${result.message}</span>
                 </td>
             `;
             tbody.appendChild(row);
         });
         table.appendChild(tbody);
         
         resultsList.appendChild(table);
     }
 
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
                // 创建结果统计
                const stats = {
                    total: result.results.length,
                    success: result.results.filter(r => r.success).length,
                    failed: result.results.filter(r => !r.success).length
                };
                
                // 创建结果表格
                createResultsTable(result.results, stats, processingTime);
                
                // 更新进度条
                progressFill.style.width = '100%';
                
                // 最终完成消息
                if (total_components > 1) {
                    progressText.textContent = `导出完成！处理了 ${total_components} 个组件，耗时 ${processingTime}s（并行处理）`;
                } else {
                    progressText.textContent = `导出完成！耗时 ${processingTime}s`;
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