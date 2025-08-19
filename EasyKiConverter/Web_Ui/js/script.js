document.addEventListener('DOMContentLoaded', () => {
    // 导航菜单功能
    const navItems = document.querySelectorAll('.nav-item[data-page]');
    const mainContent = document.querySelector('main');
    const formContainer = document.querySelector('.form-container');
    
    // 保存原始的元件转换页面内容
    const originalComponentContent = formContainer.innerHTML;
    
    // 导航菜单点击事件
    navItems.forEach(item => {
        item.addEventListener('click', (e) => {
            e.preventDefault();
            const page = item.getAttribute('data-page');
            
            // 移除所有活动状态
            navItems.forEach(nav => nav.classList.remove('active'));
            // 添加当前活动状态
            item.classList.add('active');
            
            // 切换页面内容
            switchPage(page);
        });
    });
    
    // 页面切换函数
    function switchPage(page) {
        if (page === 'component') {
            mainContent.style.display = 'block';
            // 恢复元件转换页面的原始内容
            showComponentConversion();
        } else if (page === 'project') {
            mainContent.style.display = 'block';
            // 显示工程转换页面
            showProjectConversion();
        }
    }
    
    // 显示元件转换页面
    function showComponentConversion() {
        formContainer.innerHTML = originalComponentContent;
        // 重新绑定表单事件（因为DOM被重新创建）
        initializeComponentForm();
    }
    
    // 显示工程转换页面（暂时显示提示信息）
    function showProjectConversion() {
        formContainer.innerHTML = `
            <h2>工程转换</h2>
            <div style="text-align: center; padding: 40px; color: #6B7280;">
                <svg width="64" height="64" viewBox="0 0 24 24" fill="currentColor" style="margin-bottom: 20px; opacity: 0.5;">
                    <path d="M10 4H4c-1.11 0-2 .89-2 2v12c0 1.11.89 2 2 2h16c1.11 0 2-.89 2-2V8c0-1.11-.89-2-2-2h-8l-2-2z"/>
                </svg>
                <h3 style="margin-bottom: 10px; color: #374151;">工程转换功能</h3>
                <p>此功能正在开发中，敬请期待...</p>
            </div>
        `;
    }
    
    // 初始化元件转换表单功能
    function initializeComponentForm() {
        const form = document.getElementById('export-form');
        const exportBtn = document.getElementById('export-btn');
        const btnText = exportBtn?.querySelector('.btn-text');
        const loadingSpinner = exportBtn?.querySelector('.loading-spinner');
        const progressContainer = document.getElementById('progress-container');
        const progressFill = document.getElementById('progress-fill');
        const progressText = document.getElementById('progress-text');
        const resultsContainer = document.getElementById('results-container');
        const resultsList = document.getElementById('results-list');
        
        if (!form || !exportBtn) return; // 如果元素不存在则退出
        
        // 页面加载时恢复上次设置
        loadLastSettings();
        
        // 重新绑定所有表单相关的事件监听器
        bindFormEvents(form, exportBtn, btnText, loadingSpinner, progressContainer, progressFill, progressText, resultsContainer, resultsList);
    }
    
    // 绑定表单事件的函数
     function bindFormEvents(form, exportBtn, btnText, loadingSpinner, progressContainer, progressFill, progressText, resultsContainer, resultsList) {
         // 表单提交事件
         form.addEventListener('submit', async (e) => {
             e.preventDefault();

             const formData = new FormData(form);
             const componentIds = formData.get('urls').split(/\s+/).filter(Boolean);
             
             // 检查是否输入了元器件编号
             if (componentIds.length === 0) {
                 // 高亮显示输入框
                 const urlsTextarea = document.getElementById('urls');
                 urlsTextarea.style.borderColor = '#e74c3c';
                 urlsTextarea.style.boxShadow = '0 0 5px rgba(231, 76, 60, 0.3)';
                 
                 // 显示友好的错误提示
                 progressContainer.style.display = 'block';
                 progressText.textContent = '请输入至少一个元器件编号或上传BOM文件';
                 progressText.style.color = '#e74c3c';
                 
                 // 3秒后恢复样式
                 setTimeout(() => {
                     urlsTextarea.style.borderColor = '';
                     urlsTextarea.style.boxShadow = '';
                     progressContainer.style.display = 'none';
                     progressText.style.color = '';
                 }, 3000);
                 
                 return;
             }

             // --- UI Setup for Loading --- 
             exportBtn.disabled = true;
             exportBtn.classList.add('loading');
             progressContainer.style.display = 'block';
             resultsContainer.style.display = 'none';
             resultsList.innerHTML = '';
             progressFill.style.width = '0%';
             progressText.textContent = 'Starting...';
             progressText.style.color = ''; // 重置颜色

             const data = {
                 componentIds: componentIds,
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
                     // 尝试解析错误响应
                     try {
                         const errorData = await response.json();
                         throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
                     } catch (parseError) {
                         throw new Error(`HTTP error! status: ${response.status}`);
                     }
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
                 
                 let errorMessage = 'An error occurred. Check console for details.';
                 
                 // 根据错误类型提供友好的错误信息
                 if (error.message.includes('HTTP error! status: 400')) {
                     errorMessage = '请检查输入的元器件编号格式是否正确';
                 } else if (error.message.includes('Failed to fetch')) {
                     errorMessage = '网络连接失败，请检查服务器是否正常运行';
                 } else if (error.message.includes('500')) {
                     errorMessage = '服务器内部错误，请稍后重试';
                 } else {
                     errorMessage = error.message || errorMessage;
                 }
                 
                 progressText.textContent = errorMessage;
                 progressText.style.color = '#e74c3c';
                 
                 const errorItem = document.createElement('div');
                 errorItem.className = 'result-item error';
                 errorItem.innerHTML = `<div class="result-details"><div class="result-name">错误</div><div class="result-path">${errorMessage}</div></div>`;
                 resultsList.appendChild(errorItem);
                 resultsContainer.style.display = 'block';
             } finally {
                 // --- Reset Button --- 
                 exportBtn.disabled = false;
                 exportBtn.classList.remove('loading');
             }
         });
         
         // BOM文件上传功能
         const fileUploadArea = document.getElementById('file-upload-area');
         const bomFileInput = document.getElementById('bom-file');
         const fileStatus = document.getElementById('file-status');
         const urlsTextarea = document.getElementById('urls');

         // 点击上传区域触发文件选择
          fileUploadArea.addEventListener('click', () => {
              bomFileInput.click();
          });

          // 拖拽上传功能
          fileUploadArea.addEventListener('dragover', (e) => {
              e.preventDefault();
              fileUploadArea.classList.add('dragover');
          });

          fileUploadArea.addEventListener('dragleave', (e) => {
              e.preventDefault();
              fileUploadArea.classList.remove('dragover');
          });

          fileUploadArea.addEventListener('drop', (e) => {
              e.preventDefault();
              fileUploadArea.classList.remove('dragover');
              const files = e.dataTransfer.files;
              if (files.length > 0) {
                  handleBomFile(files[0]);
              }
          });

          // 文件选择处理
          bomFileInput.addEventListener('change', (e) => {
              if (e.target.files.length > 0) {
                  handleBomFile(e.target.files[0]);
              }
          });

          // 处理BOM文件
          async function handleBomFile(file) {
              // 检查文件类型
              const allowedTypes = ['.xlsx', '.xls', '.csv'];
              const fileExtension = '.' + file.name.split('.').pop().toLowerCase();
              
              if (!allowedTypes.includes(fileExtension)) {
                  showFileStatus('error', '不支持的文件格式，请上传 .xlsx, .xls 或 .csv 文件');
                  return;
              }

              showFileStatus('processing', `正在处理文件: ${file.name}...`);

              const formData = new FormData();
              formData.append('bom_file', file);

              try {
                  const response = await fetch('/api/parse-bom', {
                      method: 'POST',
                      body: formData
                  });

                  const result = await response.json();

                  if (result.success) {
                      const componentIds = result.component_ids;
                      if (componentIds.length > 0) {
                          // 将解析出的元件编号添加到文本框中
                          const currentText = urlsTextarea.value.trim();
                          const newText = currentText ? currentText + '\n' + componentIds.join('\n') : componentIds.join('\n');
                          urlsTextarea.value = newText;
                          
                          showFileStatus('success', `成功解析 ${componentIds.length} 个元件编号`);
                      } else {
                          showFileStatus('error', '未找到任何元件编号，请检查BOM表中是否包含元器件编号列（如Supplier Part、LCSC、Part Number等）');
                      }
                  } else {
                      showFileStatus('error', result.error || '文件解析失败');
                  }
              } catch (error) {
                  console.error('BOM文件处理失败:', error);
                  showFileStatus('error', '文件处理失败，请检查网络连接或文件格式');
              }
          }

          // 显示文件状态
          function showFileStatus(type, message) {
              fileStatus.className = `file-status ${type}`;
              fileStatus.textContent = message;
              fileStatus.style.display = 'block';
              
              // 成功或错误状态5秒后自动隐藏
              if (type === 'success' || type === 'error') {
                  setTimeout(() => {
                      fileStatus.style.display = 'none';
                  }, 5000);
              }
          }
      }
     
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
 
     // 初始化元件转换表单
    initializeComponentForm();

});