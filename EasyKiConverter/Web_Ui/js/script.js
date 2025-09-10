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
            
            // 只处理元件转换页面
            if (page === 'component') {
                mainContent.style.display = 'block';
                showComponentConversion();
            }
        });
    });
    
    // 显示元件转换页面
    function showComponentConversion() {
        formContainer.innerHTML = originalComponentContent;
        // 重新绑定表单事件（因为DOM被重新创建）
        initializeComponentForm();
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
        
        // 初始化待转换列表
        initializeComponentList();
        
        // 页面加载时恢复上次设置
        loadLastSettings();
        
        // 重新绑定所有表单相关的事件监听器
        bindFormEvents(form, exportBtn, btnText, loadingSpinner, progressContainer, progressFill, progressText, resultsContainer);
    }
    
    // 绑定表单事件的函数
     function bindFormEvents(form, exportBtn, btnText, loadingSpinner, progressContainer, progressFill, progressText, resultsContainer) {
         const resultsList = document.getElementById('results-list');
         // 表单提交事件
         form.addEventListener('submit', async (e) => {
             e.preventDefault();

             const formData = new FormData(form);

             // 获取待转换列表中的所有元件编号
             const componentIds = getComponentIdsFromList();
             
             // 检查是否输入了元器件编号
             if (componentIds.length === 0) {
                 // 高亮显示输入框
                 const componentIdInput = document.getElementById('component-id');
                 componentIdInput.style.borderColor = '#e74c3c';
                 componentIdInput.style.boxShadow = '0 0 5px rgba(231, 76, 60, 0.3)';
                 
                 // 显示友好的错误提示
                 progressContainer.style.display = 'block';
                 progressText.textContent = '请添加至少一个元器件编号或上传BOM文件';
                 progressText.style.color = '#e74c3c';
                 
                 // 3秒后恢复样式
                 setTimeout(() => {
                     componentIdInput.style.borderColor = '';
                     componentIdInput.style.boxShadow = '';
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
                          // 将解析出的元件编号添加到待转换列表中
                          componentIds.forEach(id => addComponentToList(id));
                          
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
                        // 不再需要恢复上次的组件ID到文本框，因为我们现在使用列表
                    }
                    
                    console.log('已恢复上次设置');
                }
            }
        } catch (error) {
            console.warn('加载上次设置失败:', error);
        }
     }
     
     function createResultsTable(results, stats, processingTime) {
         const resultsList = document.getElementById('results-list');
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
 
     // 初始化待转换列表功能
    function initializeComponentList() {
        const componentIdInput = document.getElementById('component-id');
        const addComponentBtn = document.getElementById('add-component-btn');
        const pasteComponentBtn = document.getElementById('paste-component-btn');
        const clearAllBtn = document.getElementById('clear-all-btn');
        const componentList = document.getElementById('component-list');
        const emptyMessage = document.getElementById('component-list-empty');
        
        // 添加按钮点击事件
        if (addComponentBtn) {
            addComponentBtn.addEventListener('click', () => {
                const componentId = componentIdInput.value.trim();
                if (componentId) {
                    addComponentToList(componentId);
                    componentIdInput.value = '';
                }
            });
        }
        
        // 回车键添加事件
        if (componentIdInput) {
            componentIdInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    e.preventDefault(); // 防止表单提交
                    const componentId = componentIdInput.value.trim();
                    if (componentId) {
                        addComponentToList(componentId);
                        componentIdInput.value = '';
                    }
                }
            });
        }
        
        // 粘贴按钮点击事件
        if (pasteComponentBtn) {
            pasteComponentBtn.addEventListener('click', async () => {
                try {
                    // 从剪贴板读取文本
                    const text = await navigator.clipboard.readText();
                    if (text) {
                        // 提取元件编号并添加到列表
                        const componentIds = extractComponentIds(text);
                        if (componentIds.length > 0) {
                            // 为这次添加的元件使用特殊颜色标记
                            const batchId = Date.now() % 10; // 使用0-9的数字作为批次ID
                            componentIds.forEach(id => {
                                addComponentToList(id, `component-batch-${batchId}`);
                            });
                            
                            // 显示成功提示
                            const fileStatus = document.getElementById('file-status');
                            if (fileStatus) {
                                fileStatus.className = 'file-status success';
                                fileStatus.textContent = `成功添加 ${componentIds.length} 个元件编号`;
                                fileStatus.style.display = 'block';
                                setTimeout(() => {
                                    fileStatus.style.display = 'none';
                                }, 3000);
                            }
                        } else {
                            // 没有找到有效的元件编号
                            const fileStatus = document.getElementById('file-status');
                            if (fileStatus) {
                                fileStatus.className = 'file-status error';
                                fileStatus.textContent = '未找到有效的元件编号';
                                fileStatus.style.display = 'block';
                                setTimeout(() => {
                                    fileStatus.style.display = 'none';
                                }, 3000);
                            }
                        }
                    }
                } catch (err) {
                    console.error('无法从剪贴板读取内容:', err);
                    // 显示错误提示
                    const fileStatus = document.getElementById('file-status');
                    if (fileStatus) {
                        fileStatus.className = 'file-status error';
                        fileStatus.textContent = '无法读取剪贴板内容，请检查浏览器权限设置';
                        fileStatus.style.display = 'block';
                        setTimeout(() => {
                            fileStatus.style.display = 'none';
                        }, 3000);
                    }
                }
            });
        }
        
        // 清除所有按钮点击事件
        if (clearAllBtn && componentList && emptyMessage) {
            clearAllBtn.addEventListener('click', () => {
                componentList.innerHTML = '';
                emptyMessage.style.display = 'block';
            });
        }
    }
    
    // 添加元件到列表
    function addComponentToList(componentId, batchClass = null) {
        const componentList = document.getElementById('component-list');
        const emptyMessage = document.getElementById('component-list-empty');
        
        // 检查是否已存在
        const existingItems = componentList.querySelectorAll('li');
        for (let item of existingItems) {
            if (item.dataset.componentId === componentId) {
                return; // 已存在，不重复添加
            }
        }
        
        // 隐藏空列表提示
        emptyMessage.style.display = 'none';
        
        // 创建列表项
        const listItem = document.createElement('li');
        listItem.className = 'component-list-item';
        if (batchClass) {
            listItem.classList.add(batchClass);
        }
        listItem.dataset.componentId = componentId;
        
        listItem.innerHTML = `
            <span class="component-id">${componentId}</span>
            <button class="remove-btn" data-component-id="${componentId}">-</button>
        `;
        
        // 将新元素添加到列表顶部而不是底部
        if (componentList.firstChild) {
            componentList.insertBefore(listItem, componentList.firstChild);
        } else {
            componentList.appendChild(listItem);
        }
        
        // 绑定删除事件
        const removeBtn = listItem.querySelector('.remove-btn');
        removeBtn.addEventListener('click', () => {
            listItem.remove();
            // 如果列表为空，显示提示信息
            if (componentList.children.length === 0) {
                emptyMessage.style.display = 'block';
            }
        });
    }
    
    // 从文本中提取元件编号
    function extractComponentIds(text) {
        // 常见的元件编号模式
        // 例如: C12345, R123456, L12345, D12345, U12345, Q12345, Y12345, X12345, SW12345, LED12345 等
        const patterns = [
            // 标准元件编号模式 (字母+数字)
            /\b([A-Z]{1,2}\d{3,8})\b/gi,
            // 带连字符的元件编号
            /\b([A-Z]{1,2}\d{3,8}-[A-Z0-9]+)\b/gi,
            // 特殊元件编号模式
            /\b([A-Z]{1,3}_\d{3,8})\b/gi
        ];
        
        const componentIds = new Set(); // 使用Set避免重复
        
        for (const pattern of patterns) {
            const matches = text.match(pattern);
            if (matches) {
                matches.forEach(match => {
                    // 转换为大写并添加到集合中
                    const componentId = match.toUpperCase();
                    // 进一步验证元件编号格式
                    if (isValidComponentId(componentId)) {
                        componentIds.add(componentId);
                    }
                });
            }
        }
        
        return Array.from(componentIds);
    }
    
    // 验证元件编号格式
    function isValidComponentId(componentId) {
        // 基本格式检查
        if (!componentId || componentId.length < 4 || componentId.length > 20) {
            return false;
        }
        
        // 检查是否包含至少一个字母和一个数字
        const hasLetter = /[A-Z]/.test(componentId);
        const hasDigit = /\d/.test(componentId);
        
        if (!hasLetter || !hasDigit) {
            return false;
        }
        
        // 检查是否以字母开头
        if (!/^[A-Z]/.test(componentId)) {
            return false;
        }
        
        // 检查是否只包含字母、数字和连字符/下划线
        if (!/^[A-Z0-9\-_]+$/.test(componentId)) {
            return false;
        }
        
        return true;
    }
    
    // 从列表获取所有元件编号
    function getComponentIdsFromList() {
        const componentList = document.getElementById('component-list');
        const items = componentList.querySelectorAll('.component-list-item');
        return Array.from(items).map(item => item.dataset.componentId);
    }
    
     // 初始化元件转换表单
    initializeComponentForm();

});