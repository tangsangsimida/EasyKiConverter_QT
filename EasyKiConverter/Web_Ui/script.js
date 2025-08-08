// Web UI 交互逻辑
class EasyKiConverterUI {
    constructor() {
        this.initializeElements();
        this.bindEvents();
        this.apiEndpoint = 'http://localhost:8000/api';
    }

    initializeElements() {
        this.elements = {
            componentIds: document.getElementById('componentIds'),
            filePrefix: document.getElementById('filePrefix'),
            exportPath: document.getElementById('exportPath'),
            browseBtn: document.getElementById('browseBtn'),
            exportSymbol: document.getElementById('exportSymbol'),
            exportFootprint: document.getElementById('exportFootprint'),
            export3DModel: document.getElementById('export3DModel'),
            exportBtn: document.getElementById('exportBtn'),
            progressContainer: document.querySelector('.progress-container'),
            progressFill: document.getElementById('progressFill'),
            progressText: document.getElementById('progressText'),
            resultsContainer: document.querySelector('.results-container'),
            resultsList: document.getElementById('resultsList'),
            btnText: document.querySelector('.btn-text')
        };
    }

    bindEvents() {
        this.elements.exportBtn.addEventListener('click', () => this.startExport());
        
        // 支持拖拽文件夹
        this.setupDropZone();
    }

    setupDropZone() {
        const dropZone = document.querySelector('.form-container');
        
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            dropZone.addEventListener(eventName, (e) => {
                e.preventDefault();
                e.stopPropagation();
            });
        });

        ['dragenter', 'dragover'].forEach(eventName => {
            dropZone.addEventListener(eventName, () => {
                dropZone.classList.add('drag-over');
            });
        });

        ['dragleave', 'drop'].forEach(eventName => {
            dropZone.addEventListener(eventName, () => {
                dropZone.classList.remove('drag-over');
            });
        });

        dropZone.addEventListener('drop', (e) => {
            e.preventDefault();
            const items = e.dataTransfer.items;
            if (items.length > 0) {
                // 提示用户拖拽功能受限，建议直接输入路径
                alert('拖拽功能受浏览器安全限制，请直接输入完整文件夹路径。');
            }
        });
    }





    validateInputs() {
        const componentIds = this.elements.componentIds.value.trim();
        const exportPath = this.elements.exportPath.value.trim();

        if (!componentIds) {
            this.showError('请输入至少一个元器件编号');
            return false;
        }

        // 验证路径格式（允许空路径，空路径时使用默认路径）
        if (exportPath && !this.isValidPath(exportPath)) {
            this.showError('请输入有效的文件夹路径，例如：C:\\Users\\用户名\\Desktop\\导出文件夹');
            return false;
        }

        const selectedOptions = [
            this.elements.exportSymbol.checked,
            this.elements.exportFootprint.checked,
            this.elements.export3DModel.checked
        ];

        if (!selectedOptions.some(option => option)) {
            this.showError('请至少选择一种导出内容');
            return false;
        }

        return true;
    }

    isValidPath(path) {
        // 简单的路径验证
        if (!path || path.length < 3) return false;
        
        // Windows路径格式检查
        const windowsPathRegex = /^[a-zA-Z]:\\[^<>:"|?*]*$/;
        
        // 相对路径检查
        const relativePathRegex = /^[^<>:"|?*]+$/;
        
        return windowsPathRegex.test(path) || relativePathRegex.test(path);
    }

    async startExport() {
        if (!this.validateInputs()) {
            return;
        }

        // 禁用导出按钮
        this.setExportButtonState(true);
        
        // 显示进度容器
        this.showProgress();
        
        // 准备导出数据
        const exportData = this.prepareExportData();
        
        try {
            await this.performExport(exportData);
        } catch (error) {
            this.handleExportError(error);
        } finally {
            this.setExportButtonState(false);
        }
    }

    prepareExportData() {
        const componentIds = this.elements.componentIds.value
            .split('\n')
            .map(id => id.trim())
            .filter(id => id.length > 0);

        return {
            componentIds: componentIds,
            filePrefix: this.elements.filePrefix.value.trim() || 'testlib',
            exportPath: this.elements.exportPath.value.trim() || null,
            options: {
                symbol: this.elements.exportSymbol.checked,
                footprint: this.elements.exportFootprint.checked,
                model3d: this.elements.export3DModel.checked
            }
        };
    }

    async performExport(data) {
        try {
            const response = await fetch('/api/export', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });
            
            const result = await response.json();
            
            if (result.success) {
                this.showResults(result.results);
            } else {
                throw new Error(result.error);
            }
        } catch (error) {
            this.handleExportError(error);
        }
    }

    async simulateExportProcess(data) {
        // 这个方法现在只用于显示进度，实际导出由performExport处理
        this.updateProgress(0, '正在准备导出...');
        await this.delay(1000);
        this.updateProgress(50, '正在处理请求...');
        await this.delay(1000);
        this.updateProgress(100, '处理完成！');
    }

    getTypeName(type) {
        const typeMap = {
            symbol: '符号库',
            footprint: '封装库',
            model3d: '3D模型'
        };
        return typeMap[type] || type;
    }

    updateProgress(percentage, text = null) {
        this.elements.progressFill.style.width = `${percentage}%`;
        if (text) {
            this.elements.progressText.textContent = text;
        }
    }

    showProgress() {
        this.elements.progressContainer.style.display = 'block';
        this.elements.resultsContainer.style.display = 'none';
    }

    showResults(results) {
        this.elements.progressContainer.style.display = 'none';
        this.elements.resultsContainer.style.display = 'block';
        
        const resultsList = this.elements.resultsList;
        resultsList.innerHTML = '';

        // 获取第一个结果的导出路径作为基础路径
        const baseExportPath = results.length > 0 && results[0].exportPath ? results[0].exportPath : this.elements.exportPath.value;

        // 显示导出路径信息
        const exportPathInfo = document.createElement('div');
        exportPathInfo.className = 'export-path-info';
        exportPathInfo.style.cssText = 'margin-bottom: 20px; padding: 15px; background: #e8f4fd; border-left: 4px solid #667eea; border-radius: 4px;';
        exportPathInfo.innerHTML = `
            <h4 style="margin: 0 0 10px 0; color: #2c3e50;">导出完成！</h4>
            <p style="margin: 5px 0; font-size: 14px;"><strong>完整导出路径：</strong></p>
            <p style="margin: 5px 0; font-size: 13px; font-family: monospace; background: #f5f5f5; padding: 8px; border-radius: 3px; word-break: break-all;">${baseExportPath}</p>
            <p style="margin: 10px 0 5px 0; font-size: 14px; color: #666;">导出的文件：</p>
        `;
        resultsList.appendChild(exportPathInfo);

        // 按组件分组显示结果
        const componentGroups = {};
        results.forEach(result => {
            if (!componentGroups[result.componentId]) {
                componentGroups[result.componentId] = [];
            }
            componentGroups[result.componentId].push(result);
        });

        Object.entries(componentGroups).forEach(([componentId, componentResults]) => {
            const groupDiv = document.createElement('div');
            groupDiv.style.cssText = 'margin-bottom: 20px; padding: 15px; border: 1px solid #e0e0e0; border-radius: 8px;';
            
            const componentHeader = document.createElement('h5');
            componentHeader.style.cssText = 'margin: 0 0 10px 0; color: #2c3e50; font-size: 16px;';
            componentHeader.textContent = `元器件: ${componentId}`;
            groupDiv.appendChild(componentHeader);

            componentResults.forEach(result => {
                const fileList = document.createElement('div');
                fileList.style.cssText = 'margin-left: 10px;';

                result.files.forEach(file => {
                    const fileItem = document.createElement('div');
                    fileItem.style.cssText = 'margin: 8px 0; padding: 10px; background: #f8f9fa; border-radius: 4px;';
                    
                    const icon = result.success ? '✓' : '✗';
                    const iconColor = result.success ? '#28a745' : '#dc3545';
                    const typeName = this.getTypeName(file.type);
                    
                    fileItem.innerHTML = `
                        <div style="display: flex; align-items: center; margin-bottom: 5px;">
                            <span style="color: ${iconColor}; margin-right: 8px; font-weight: bold;">${icon}</span>
                            <span style="font-weight: bold; color: #2c3e50;">${typeName}</span>
                        </div>
                        <div style="font-size: 12px; color: #666; font-family: monospace; background: #fff; padding: 4px; border-radius: 2px; word-break: break-all;">
                            ${file.path}
                        </div>
                    `;
                    
                    fileList.appendChild(fileItem);
                });
                
                groupDiv.appendChild(fileList);
            });
            
            resultsList.appendChild(groupDiv);
        });

        // 显示统计信息
        const allFiles = results.flatMap(r => r.files);
        const successCount = allFiles.length;
        const componentCount = Object.keys(componentGroups).length;
        
        const summary = document.createElement('div');
        summary.style.cssText = 'margin-top: 20px; padding: 15px; background: #f8f9fa; border-radius: 8px; text-align: center;';
        summary.innerHTML = `
            <strong>导出统计：</strong>成功导出 ${successCount} 个文件（${componentCount} 个元器件）
            ${successCount > 0 ? '🎉' : ''}
        `;
        resultsList.appendChild(summary);
    }

    setExportButtonState(disabled) {
        this.elements.exportBtn.disabled = disabled;
        const spinner = this.elements.exportBtn.querySelector('.loading-spinner');
        const btnText = this.elements.btnText;
        
        if (disabled) {
            spinner.style.display = 'inline-block';
            btnText.textContent = '导出中...';
        } else {
            spinner.style.display = 'none';
            btnText.textContent = '开始导出';
        }
    }

    handleExportError(error) {
        console.error('导出失败:', error);
        this.showError(`导出失败: ${error.message || '未知错误'}`);
    }

    showError(message) {
        alert(message);
    }

    delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
}

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', () => {
    new EasyKiConverterUI();
});

// 添加拖拽样式
const style = document.createElement('style');
style.textContent = `
    .drag-over {
        border: 2px dashed #667eea !important;
        background-color: #f8f9ff !important;
    }
    
    .form-container {
        transition: all 0.3s ease;
    }
`;
document.head.appendChild(style);