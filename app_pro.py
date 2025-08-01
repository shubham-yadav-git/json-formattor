from flask import Flask, request, jsonify
import json
import re
from datetime import datetime

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>JSON Formatter Pro - Advanced JSON Tools</title>
    <style>
        :root {
            --primary-color: #007bff;
            --success-color: #28a745;
            --danger-color: #dc3545;
            --warning-color: #ffc107;
            --info-color: #17a2b8;
            --light-bg: #f8f9fa;
            --dark-text: #212529;
        }

        * { box-sizing: border-box; }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh; line-height: 1.6;
        }
        
        .container {
            max-width: 1400px; margin: 0 auto; background: white;
            border-radius: 15px; box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            padding: 40px; backdrop-filter: blur(10px);
        }
        
        .header {
            text-align: center; margin-bottom: 40px;
        }
        
        .header h1 {
            color: var(--dark-text); font-size: 3em; margin-bottom: 10px;
            background: linear-gradient(45deg, #667eea, #764ba2);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .header p {
            color: #6c757d; font-size: 1.2em; margin: 0;
        }
        
        .main-content {
            display: grid; grid-template-columns: 1fr 1fr; gap: 30px;
            margin-bottom: 30px;
        }
        
        .input-panel, .output-panel {
            background: var(--light-bg); border-radius: 10px; padding: 20px;
        }
        
        .panel-title {
            font-size: 1.3em; font-weight: bold; margin-bottom: 15px;
            color: var(--dark-text);
        }
        
        textarea, .output-area {
            width: 100%; height: 400px; padding: 15px; border: 2px solid #dee2e6;
            border-radius: 8px; font-family: 'Courier New', Monaco, monospace;
            font-size: 14px; resize: vertical; transition: all 0.3s;
        }
        
        textarea:focus {
            outline: none; border-color: var(--primary-color);
            box-shadow: 0 0 0 0.2rem rgba(0,123,255,.25);
        }
        
        .output-area {
            background: white; white-space: pre-wrap; word-wrap: break-word;
            overflow-y: auto; cursor: text; border: 2px solid #e9ecef;
            color: #212529; min-height: 100px;
        }
        
        .output-area.tree {
            white-space: normal; padding: 10px;
        }
        
        .controls {
            display: flex; gap: 15px; flex-wrap: wrap; margin: 30px 0;
            justify-content: center; align-items: center;
        }
        
        button {
            padding: 12px 24px; border: none; border-radius: 8px; cursor: pointer;
            font-size: 14px; font-weight: 600; transition: all 0.3s;
            min-width: 140px; position: relative; overflow: hidden;
        }
        
        button:before {
            content: ''; position: absolute; top: 0; left: -100%;
            width: 100%; height: 100%; background: rgba(255,255,255,0.2);
            transition: left 0.3s; z-index: 1;
        }
        
        button:hover:before { left: 100%; }
        
        .btn-format { background: linear-gradient(45deg, var(--success-color), #20c997); color: white; }
        .btn-minify { background: linear-gradient(45deg, var(--info-color), #138496); color: white; }
        .btn-validate { background: linear-gradient(45deg, var(--warning-color), #e0a800); color: var(--dark-text); }
        .btn-beautify { background: linear-gradient(45deg, #6f42c1, #e83e8c); color: white; }
        .btn-copy { background: linear-gradient(45deg, #6c757d, #5a6268); color: white; }
        .btn-clear { background: linear-gradient(45deg, var(--danger-color), #c82333); color: white; }
        .btn-download { background: linear-gradient(45deg, #fd7e14, #e55353); color: white; }
        
        .result {
            margin-top: 20px; padding: 20px; border-radius: 10px;
            font-family: 'Courier New', Monaco, monospace; font-size: 14px;
            white-space: pre-wrap; word-wrap: break-word;
            max-height: 400px; overflow-y: auto; display: none;
            border-left: 5px solid;
        }
        
        .result.success {
            background: linear-gradient(135deg, #d4edda, #c3e6cb);
            color: #155724; border-color: var(--success-color); display: block;
        }
        
        .result.error {
            background: linear-gradient(135deg, #f8d7da, #f5c6cb);
            color: #721c24; border-color: var(--danger-color); display: block;
        }
        
        .result.info {
            background: linear-gradient(135deg, #d1ecf1, #bee5eb);
            color: #0c5460; border-color: var(--info-color); display: block;
        }
        
        .tools-panel {
            display: flex; gap: 15px; align-items: center; flex-wrap: wrap;
            background: var(--light-bg); padding: 20px; border-radius: 10px;
            margin-bottom: 20px;
        }
        
        .tool-group {
            display: flex; align-items: center; gap: 10px;
        }
        
        .tool-group label {
            font-weight: 600; color: var(--dark-text);
        }
        
        .tool-group input, .tool-group select {
            padding: 8px 12px; border: 1px solid #ced4da; border-radius: 5px;
            font-size: 14px; transition: border-color 0.3s;
        }
        
        .tool-group input:focus, .tool-group select:focus {
            outline: none; border-color: var(--primary-color);
        }
        
        .stats {
            display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px; margin-top: 20px;
        }
        
        .stat-card {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white; padding: 20px; border-radius: 10px; text-align: center;
        }
        
        .stat-number {
            font-size: 2em; font-weight: bold; margin-bottom: 5px;
        }
        
        .stat-label {
            font-size: 0.9em; opacity: 0.9;
        }
        
        .loading {
            display: none; text-align: center; margin: 20px 0;
        }
        
        .loading.show {
            display: block;
        }
        
        .spinner {
            border: 4px solid #f3f3f3; border-top: 4px solid var(--primary-color);
            border-radius: 50%; width: 40px; height: 40px;
            animation: spin 1s linear infinite; margin: 0 auto 10px;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .json-tree {
            font-family: 'Courier New', Monaco, monospace; font-size: 14px;
            line-height: 1.6; background: #fafafa; padding: 15px;
            border-radius: 8px; border: 1px solid #e0e0e0;
        }
        
        .json-key { color: #0066cc; font-weight: bold; cursor: pointer; }
        .json-string { color: #009900; }
        .json-number { color: #cc6600; font-weight: 600; }
        .json-boolean { color: #990099; font-weight: bold; }
        .json-null { color: #999999; font-style: italic; }
        
        .json-expandable {
            cursor: pointer; user-select: none; position: relative;
            padding-left: 20px; margin: 2px 0;
        }
        
        .json-expandable:before {
            content: '▼'; position: absolute; left: 0; top: 0;
            color: #666; font-size: 12px; transition: transform 0.2s;
        }
        
        .json-expandable.collapsed:before {
            transform: rotate(-90deg);
        }
        
        .json-expandable.collapsed + .json-content {
            display: none;
        }
        
        .json-content {
            margin-left: 15px; border-left: 2px solid #e0e0e0;
            padding-left: 10px; transition: all 0.2s;
        }
        
        .json-item {
            margin: 3px 0; padding: 2px 0;
        }
        
        .json-item:hover {
            background-color: rgba(0, 102, 204, 0.1);
            border-radius: 3px;
        }
        
        .json-count {
            color: #666; font-size: 12px; font-weight: normal;
            margin-left: 5px; opacity: 0.7;
        }
        
        .json-type-indicator {
            display: inline-block; width: 8px; height: 8px;
            border-radius: 50%; margin-right: 5px; vertical-align: middle;
        }
        
        .json-type-object { background-color: #0066cc; }
        .json-type-array { background-color: #cc6600; }
        .json-type-string { background-color: #009900; }
        .json-type-number { background-color: #cc6600; }
        .json-type-boolean { background-color: #990099; }
        .json-type-null { background-color: #999999; }
        
        .error-highlight {
            background-color: #ffebee; border: 1px solid #f44336;
            padding: 2px 4px; border-radius: 3px;
        }
        
        .feature-grid {
            display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px; margin-top: 30px;
        }
        
        .feature-card {
            background: white; padding: 20px; border-radius: 10px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1); text-align: center;
        }
        
        .feature-icon {
            font-size: 3em; margin-bottom: 15px;
        }
        
        @media (max-width: 768px) {
            .main-content { grid-template-columns: 1fr; }
            .container { padding: 20px; }
            .controls { justify-content: center; }
            button { min-width: 120px; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>JSON Formatter Pro</h1>
            <p>Advanced JSON formatting, validation, and analysis tools</p>
        </div>
        
        <div class="tools-panel">
            <div class="tool-group">
                <label for="indentSize">Indent Size:</label>
                <input type="number" id="indentSize" value="2" min="1" max="8">
            </div>
            <div class="tool-group">
                <label for="sortKeys">Sort Keys:</label>
                <select id="sortKeys">
                    <option value="true">Yes</option>
                    <option value="false">No</option>
                </select>
            </div>
            <div class="tool-group">
                <label for="outputFormat">Output Format:</label>
                <select id="outputFormat">
                    <option value="formatted">Formatted</option>
                    <option value="tree">Tree View</option>
                    <option value="minified">Minified</option>
                </select>
            </div>
        </div>
        
        <div class="main-content">
            <div class="input-panel">
                <div class="panel-title">📝 Input JSON</div>
                <textarea id="jsonInput" placeholder="Paste your JSON here...

Example:
{
  &quot;users&quot;: [
    {
      &quot;id&quot;: 1,
      &quot;name&quot;: &quot;John Doe&quot;,
      &quot;email&quot;: &quot;john@example.com&quot;,
      &quot;active&quot;: true,
      &quot;roles&quot;: [&quot;admin&quot;, &quot;user&quot;]
    }
  ],
  &quot;meta&quot;: {
    &quot;total&quot;: 1,
    &quot;timestamp&quot;: &quot;2024-01-01T12:00:00Z&quot;
  }
}"></textarea>
            </div>
            
            <div class="output-panel">
                <div class="panel-title">✨ Formatted Output</div>
                <div id="outputArea" class="output-area">Click a button to see results here...</div>
            </div>
        </div>
        
        <div class="controls">
            <button class="btn-format" onclick="formatJson()">🎨 Format JSON</button>
            <button class="btn-beautify" onclick="beautifyJson()">💎 Beautify</button>
            <button class="btn-minify" onclick="minifyJson()">📦 Minify</button>
            <button class="btn-validate" onclick="validateJson()">✅ Validate</button>
            <button class="btn-copy" onclick="copyResult()">📋 Copy</button>
            <button class="btn-download" onclick="downloadJson()">💾 Download</button>
            <button class="btn-clear" onclick="clearAll()">🗑️ Clear</button>
        </div>
        
        <div class="loading" id="loading">
            <div class="spinner"></div>
            <div>Processing your JSON...</div>
        </div>
        
        <div class="stats" id="stats"></div>
        
        <div class="feature-grid">
            <div class="feature-card">
                <div class="feature-icon">🔍</div>
                <h3>Validation</h3>
                <p>Instant JSON validation with detailed error messages</p>
            </div>
            <div class="feature-card">
                <div class="feature-icon">🎨</div>
                <h3>Formatting</h3>
                <p>Beautiful formatting with customizable indentation</p>
            </div>
            <div class="feature-card">
                <div class="feature-icon">🌳</div>
                <h3>Tree View</h3>
                <p>Hierarchical tree view for complex JSON structures</p>
            </div>
            <div class="feature-card">
                <div class="feature-icon">📊</div>
                <h3>Analytics</h3>
                <p>Detailed statistics about your JSON data</p>
            </div>
        </div>
    </div>

    <script>
        let currentResult = '';
        
        async function fetchData(url, options) {
            const loading = document.getElementById('loading');
            loading.classList.add('show');
            
            try {
                const response = await fetch(url, options);
                const data = await response.json();
                loading.classList.remove('show');
                return data;
            } catch (error) {
                loading.classList.remove('show');
                throw error;
            }
        }

        function showOutput(content, type = 'success') {
            const outputArea = document.getElementById('outputArea');
            outputArea.className = `output-area ${type}`;
            
            if (type === 'tree') {
                outputArea.innerHTML = content;
            } else {
                outputArea.textContent = content;
            }
            
            currentResult = typeof content === 'string' ? content : outputArea.textContent;
        }

        function createTreeView(obj, path = 'root', isRoot = true) {
            let html = '';
            
            function escapeHtml(text) {
                const div = document.createElement('div');
                div.textContent = text;
                return div.innerHTML;
            }
            
            function getTypeIndicator(value) {
                if (Array.isArray(value)) return '<span class="json-type-indicator json-type-array"></span>';
                if (value === null) return '<span class="json-type-indicator json-type-null"></span>';
                if (typeof value === 'object') return '<span class="json-type-indicator json-type-object"></span>';
                if (typeof value === 'string') return '<span class="json-type-indicator json-type-string"></span>';
                if (typeof value === 'number') return '<span class="json-type-indicator json-type-number"></span>';
                if (typeof value === 'boolean') return '<span class="json-type-indicator json-type-boolean"></span>';
                return '';
            }
            
            function createExpandableItem(key, value, itemPath, isLast = false) {
                const uniqueId = `tree-${Math.random().toString(36).substr(2, 9)}`;
                let html = '<div class="json-item">';
                
                if (Array.isArray(value)) {
                    const count = value.length;
                    html += `<div class="json-expandable" onclick="toggleTreeNode('${uniqueId}')">`;
                    html += getTypeIndicator(value);
                    if (key !== null) html += `<span class="json-key">"${escapeHtml(key)}"</span>: `;
                    html += `[<span class="json-count">${count} items</span>]`;
                    html += '</div>';
                    html += `<div class="json-content" id="${uniqueId}">`;
                    
                    value.forEach((item, index) => {
                        html += createExpandableItem(null, item, `${itemPath}[${index}]`, index === value.length - 1);
                    });
                    
                    html += '</div>';
                } else if (value !== null && typeof value === 'object') {
                    const keys = Object.keys(value);
                    const count = keys.length;
                    html += `<div class="json-expandable" onclick="toggleTreeNode('${uniqueId}')">`;
                    html += getTypeIndicator(value);
                    if (key !== null) html += `<span class="json-key">"${escapeHtml(key)}"</span>: `;
                    html += `{<span class="json-count">${count} keys</span>}`;
                    html += '</div>';
                    html += `<div class="json-content" id="${uniqueId}">`;
                    
                    keys.forEach((objKey, index) => {
                        html += createExpandableItem(objKey, value[objKey], `${itemPath}.${objKey}`, index === keys.length - 1);
                    });
                    
                    html += '</div>';
                } else {
                    // Leaf node
                    html += '<div>';
                    html += getTypeIndicator(value);
                    if (key !== null) html += `<span class="json-key">"${escapeHtml(key)}"</span>: `;
                    
                    if (typeof value === 'string') {
                        html += `<span class="json-string">"${escapeHtml(value)}"</span>`;
                    } else if (typeof value === 'number') {
                        html += `<span class="json-number">${value}</span>`;
                    } else if (typeof value === 'boolean') {
                        html += `<span class="json-boolean">${value}</span>`;
                    } else if (value === null) {
                        html += `<span class="json-null">null</span>`;
                    }
                    
                    html += '</div>';
                }
                
                html += '</div>';
                return html;
            }
            
            if (isRoot) {
                html = createExpandableItem(null, obj, path);
            } else {
                html = createExpandableItem(null, obj, path);
            }
            
            return html;
        }
        
        function toggleTreeNode(nodeId) {
            const node = document.getElementById(nodeId);
            const expandable = node.previousElementSibling;
            
            if (node.style.display === 'none') {
                node.style.display = 'block';
                expandable.classList.remove('collapsed');
            } else {
                node.style.display = 'none';
                expandable.classList.add('collapsed');
            }
        }

        function updateStats(originalLength, resultLength, jsonObj = null) {
            const statsDiv = document.getElementById('stats');
            let statsHtml = '';
            
            const compression = originalLength > 0 ? 
                ((originalLength - resultLength) / originalLength * 100).toFixed(1) : 0;
            
            statsHtml += `
                <div class="stat-card">
                    <div class="stat-number">${originalLength}</div>
                    <div class="stat-label">Original Size (chars)</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">${resultLength}</div>
                    <div class="stat-label">Result Size (chars)</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">${Math.abs(compression)}%</div>
                    <div class="stat-label">${compression > 0 ? 'Compression' : 'Expansion'}</div>
                </div>
            `;
            
            if (jsonObj) {
                const depth = getMaxDepth(jsonObj);
                const keyCount = countKeys(jsonObj);
                
                statsHtml += `
                    <div class="stat-card">
                        <div class="stat-number">${depth}</div>
                        <div class="stat-label">Max Depth</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">${keyCount}</div>
                        <div class="stat-label">Total Keys</div>
                    </div>
                `;
            }
            
            statsDiv.innerHTML = statsHtml;
        }
        
        function getMaxDepth(obj, currentDepth = 0) {
            if (obj === null || typeof obj !== 'object') return currentDepth;
            
            let maxDepth = currentDepth;
            for (let key in obj) {
                const depth = getMaxDepth(obj[key], currentDepth + 1);
                maxDepth = Math.max(maxDepth, depth);
            }
            return maxDepth;
        }
        
        function countKeys(obj) {
            if (obj === null || typeof obj !== 'object') return 0;
            
            let count = 0;
            if (Array.isArray(obj)) {
                obj.forEach(item => count += countKeys(item));
            } else {
                count += Object.keys(obj).length;
                Object.values(obj).forEach(value => count += countKeys(value));
            }
            return count;
        }

        async function formatJson() {
            const jsonInput = document.getElementById('jsonInput').value.trim();
            const indentSize = parseInt(document.getElementById('indentSize').value) || 2;
            const sortKeys = document.getElementById('sortKeys').value === 'true';
            const outputFormat = document.getElementById('outputFormat').value;
            
            if (!jsonInput) {
                showOutput('Please enter some JSON to format.', 'error');
                return;
            }

            try {
                const data = await fetchData('/api/format', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ 
                        json_string: jsonInput, 
                        indent: indentSize,
                        sort_keys: sortKeys,
                        output_format: outputFormat
                    })
                });
                
                if (data.success) {
                    if (outputFormat === 'tree') {
                        const jsonObj = JSON.parse(jsonInput);
                        const treeHtml = createTreeView(jsonObj);
                        showOutput(`<div class="json-tree">${treeHtml}</div>`, 'tree');
                        updateStats(jsonInput.length, data.formatted_json.length, jsonObj);
                    } else {
                        showOutput(data.formatted_json, 'success');
                        updateStats(jsonInput.length, data.formatted_json.length, JSON.parse(jsonInput));
                    }
                } else {
                    showOutput(data.error, 'error');
                }
            } catch (error) {
                showOutput('Network error: ' + error.message, 'error');
            }
        }

        async function beautifyJson() {
            const jsonInput = document.getElementById('jsonInput').value.trim();
            
            if (!jsonInput) {
                showOutput('Please enter some JSON to beautify.', 'error');
                return;
            }

            try {
                const data = await fetchData('/api/beautify', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ json_string: jsonInput })
                });
                
                if (data.success) {
                    showOutput(data.beautified_json, 'success');
                    updateStats(jsonInput.length, data.beautified_json.length, JSON.parse(jsonInput));
                } else {
                    showOutput(data.error, 'error');
                }
            } catch (error) {
                showOutput('Network error: ' + error.message, 'error');
            }
        }

        async function minifyJson() {
            const jsonInput = document.getElementById('jsonInput').value.trim();
            
            if (!jsonInput) {
                showOutput('Please enter some JSON to minify.', 'error');
                return;
            }

            try {
                const data = await fetchData('/api/minify', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ json_string: jsonInput })
                });
                
                if (data.success) {
                    showOutput(data.minified_json, 'success');
                    updateStats(jsonInput.length, data.minified_json.length, JSON.parse(jsonInput));
                } else {
                    showOutput(data.error, 'error');
                }
            } catch (error) {
                showOutput('Network error: ' + error.message, 'error');
            }
        }

        async function validateJson() {
            const jsonInput = document.getElementById('jsonInput').value.trim();
            
            if (!jsonInput) {
                showOutput('Please enter some JSON to validate.', 'error');
                return;
            }

            try {
                const data = await fetchData('/api/validate', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ json_string: jsonInput })
                });
                
                if (data.valid) {
                    showOutput('✅ Valid JSON! Your JSON is properly formatted and valid.', 'info');
                    updateStats(jsonInput.length, jsonInput.length, JSON.parse(jsonInput));
                } else {
                    showOutput('❌ Invalid JSON: ' + data.error, 'error');
                }
            } catch (error) {
                showOutput('Network error: ' + error.message, 'error');
            }
        }

        function copyResult() {
            if (!currentResult) {
                showOutput('No result to copy. Please format, minify, or validate JSON first.', 'error');
                return;
            }
            
            navigator.clipboard.writeText(currentResult).then(() => {
                const originalContent = currentResult;
                showOutput('📋 Copied to clipboard successfully!', 'info');
                setTimeout(() => {
                    showOutput(originalContent, 'success');
                }, 1500);
            }).catch(() => {
                showOutput('Failed to copy to clipboard. Please select and copy manually.', 'error');
            });
        }
        
        function downloadJson() {
            if (!currentResult) {
                showOutput('No result to download. Please format your JSON first.', 'error');
                return;
            }
            
            const blob = new Blob([currentResult], { type: 'application/json' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `formatted_json_${new Date().getTime()}.json`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
            
            showOutput('📥 JSON file downloaded successfully!', 'info');
            setTimeout(() => {
                showOutput(currentResult, 'success');
            }, 1500);
        }

        function clearAll() {
            document.getElementById('jsonInput').value = '';
            document.getElementById('outputArea').textContent = 'Click a button to see results here...';
            document.getElementById('outputArea').className = 'output-area';
            document.getElementById('stats').innerHTML = '';
            currentResult = '';
        }

        // Keyboard shortcuts
        document.getElementById('jsonInput').addEventListener('keydown', function(event) {
            if (event.ctrlKey && event.key === 'Enter') {
                formatJson();
            } else if (event.ctrlKey && event.key === 'm') {
                event.preventDefault();
                minifyJson();
            } else if (event.ctrlKey && event.key === 'l') {
                event.preventDefault();
                clearAll();
            }
        });
        
        // Auto-resize textarea
        const textarea = document.getElementById('jsonInput');
        textarea.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = Math.min(this.scrollHeight, 600) + 'px';
        });
    </script>
</body>
</html>
"""

def format_json(json_string, indent=2, sort_keys=True, output_format="formatted"):
    try:
        parsed_json = json.loads(json_string)
        formatted_json = json.dumps(parsed_json, indent=indent, ensure_ascii=False, sort_keys=sort_keys)
        return {'success': True, 'formatted_json': formatted_json, 'error': None}
    except json.JSONDecodeError as e:
        return {'success': False, 'formatted_json': None, 'error': f"Invalid JSON: {str(e)}"}
    except Exception as e:
        return {'success': False, 'formatted_json': None, 'error': f"Error: {str(e)}"}

def beautify_json(json_string):
    try:
        parsed_json = json.loads(json_string)
        beautified_json = json.dumps(parsed_json, indent=4, ensure_ascii=False, sort_keys=True, separators=(',', ': '))
        return {'success': True, 'beautified_json': beautified_json, 'error': None}
    except json.JSONDecodeError as e:
        return {'success': False, 'beautified_json': None, 'error': f"Invalid JSON: {str(e)}"}
    except Exception as e:
        return {'success': False, 'beautified_json': None, 'error': f"Error: {str(e)}"}

def minify_json(json_string):
    try:
        parsed_json = json.loads(json_string)
        minified_json = json.dumps(parsed_json, separators=(',', ':'), ensure_ascii=False)
        return {'success': True, 'minified_json': minified_json, 'error': None}
    except json.JSONDecodeError as e:
        return {'success': False, 'minified_json': None, 'error': f"Invalid JSON: {str(e)}"}
    except Exception as e:
        return {'success': False, 'minified_json': None, 'error': f"Error: {str(e)}"}

def validate_json(json_string):
    try:
        parsed_json = json.loads(json_string)
        
        # Additional validation checks
        validation_info = {
            'valid': True,
            'error': None,
            'warnings': [],
            'structure_info': analyze_structure(parsed_json)
        }
        
        return {'success': True, **validation_info}
    except json.JSONDecodeError as e:
        return {'success': True, 'valid': False, 'error': f"Invalid JSON: {str(e)}"}

def analyze_structure(obj, path="root"):
    info = {
        'type': type(obj).__name__,
        'size': len(str(obj)) if obj is not None else 0,
        'depth': get_depth(obj),
        'key_count': count_keys(obj)
    }
    
    if isinstance(obj, dict):
        info['properties'] = len(obj)
    elif isinstance(obj, list):
        info['items'] = len(obj)
    
    return info

def get_depth(obj):
    if not isinstance(obj, (dict, list)):
        return 0
    
    if isinstance(obj, dict):
        return 1 + max((get_depth(v) for v in obj.values()), default=0)
    elif isinstance(obj, list):
        return 1 + max((get_depth(item) for item in obj), default=0)

def count_keys(obj):
    if not isinstance(obj, (dict, list)):
        return 0
    
    count = 0
    if isinstance(obj, dict):
        count += len(obj)
        for value in obj.values():
            count += count_keys(value)
    elif isinstance(obj, list):
        for item in obj:
            count += count_keys(item)
    
    return count

@app.route('/')
def index():
    return HTML_TEMPLATE

@app.route('/api/format', methods=['POST'])
def api_format():
    data = request.get_json()
    if not data or 'json_string' not in data:
        return jsonify({'error': 'No JSON string provided', 'success': False}), 400
    
    json_string = data['json_string']
    indent = data.get('indent', 2)
    sort_keys = data.get('sort_keys', True)
    output_format = data.get('output_format', 'formatted')
    
    if not json_string.strip():
        return jsonify({'error': 'Empty JSON string', 'success': False}), 400
    
    result = format_json(json_string, indent, sort_keys, output_format)
    
    if result['success']:
        return jsonify({
            'formatted_json': result['formatted_json'],
            'success': True,
            'timestamp': datetime.now().isoformat()
        })
    else:
        return jsonify({'error': result['error'], 'success': False}), 400

@app.route('/api/beautify', methods=['POST'])
def api_beautify():
    data = request.get_json()
    if not data or 'json_string' not in data:
        return jsonify({'error': 'No JSON string provided', 'success': False}), 400
    
    json_string = data['json_string']
    if not json_string.strip():
        return jsonify({'error': 'Empty JSON string', 'success': False}), 400
    
    result = beautify_json(json_string)
    
    if result['success']:
        return jsonify({
            'beautified_json': result['beautified_json'],
            'success': True,
            'timestamp': datetime.now().isoformat()
        })
    else:
        return jsonify({'error': result['error'], 'success': False}), 400

@app.route('/api/minify', methods=['POST'])
def api_minify():
    data = request.get_json()
    if not data or 'json_string' not in data:
        return jsonify({'error': 'No JSON string provided', 'success': False}), 400
    
    json_string = data['json_string']
    if not json_string.strip():
        return jsonify({'error': 'Empty JSON string', 'success': False}), 400
    
    result = minify_json(json_string)
    
    if result['success']:
        return jsonify({
            'minified_json': result['minified_json'],
            'success': True,
            'timestamp': datetime.now().isoformat()
        })
    else:
        return jsonify({'error': result['error'], 'success': False}), 400

@app.route('/api/validate', methods=['POST'])
def api_validate():
    data = request.get_json()
    if not data or 'json_string' not in data:
        return jsonify({'error': 'No JSON string provided', 'success': False}), 400
    
    json_string = data['json_string']
    if not json_string.strip():
        return jsonify({'error': 'Empty JSON string', 'success': False}), 400
    
    result = validate_json(json_string)
    result['timestamp'] = datetime.now().isoformat()
    
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)
