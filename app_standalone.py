from flask import Flask, request, jsonify
import json

app = Flask(__name__)

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>JSON Formatter & Beautifier</title>
    <style>
        * { box-sizing: border-box; }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0; padding: 20px; background-color: #f5f5f5; line-height: 1.6;
        }
        
        .container {
            max-width: 1200px; margin: 0 auto; background: white;
            border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); padding: 30px;
        }
        
        h1 { color: #333; text-align: center; margin-bottom: 30px; font-size: 2.5em; }
        .input-section { margin-bottom: 20px; }
        label { display: block; margin-bottom: 8px; font-weight: bold; color: #555; }
        
        textarea {
            width: 100%; height: 250px; padding: 15px; border: 2px solid #ddd;
            border-radius: 6px; font-family: 'Courier New', monospace; font-size: 14px;
            resize: vertical; transition: border-color 0.3s;
        }
        
        textarea:focus { outline: none; border-color: #007bff; }
        .controls { display: flex; gap: 10px; flex-wrap: wrap; margin: 20px 0; }
        
        button {
            padding: 12px 20px; border: none; border-radius: 5px; cursor: pointer;
            font-size: 14px; font-weight: bold; transition: all 0.3s; min-width: 120px;
        }
        
        .btn-format { background-color: #28a745; color: white; }
        .btn-format:hover { background-color: #218838; }
        .btn-minify { background-color: #17a2b8; color: white; }
        .btn-minify:hover { background-color: #138496; }
        .btn-validate { background-color: #ffc107; color: #212529; }
        .btn-validate:hover { background-color: #e0a800; }
        .btn-clear { background-color: #dc3545; color: white; }
        .btn-clear:hover { background-color: #c82333; }
        .btn-copy { background-color: #6c757d; color: white; }
        .btn-copy:hover { background-color: #5a6268; }
        
        .result {
            margin-top: 20px; padding: 20px; border-radius: 6px;
            font-family: 'Courier New', monospace; font-size: 14px;
            white-space: pre-wrap; word-wrap: break-word;
            max-height: 400px; overflow-y: auto; display: none;
        }
        
        .result.success {
            background-color: #d4edda; border: 1px solid #c3e6cb;
            color: #155724; display: block;
        }
        
        .result.error {
            background-color: #f8d7da; border: 1px solid #f5c6cb;
            color: #721c24; display: block;
        }
        
        .result.info {
            background-color: #d1ecf1; border: 1px solid #bee5eb;
            color: #0c5460; display: block;
        }
        
        .indent-control { display: flex; align-items: center; gap: 10px; }
        .indent-control input { width: 60px; padding: 5px; border: 1px solid #ddd; border-radius: 3px; }
        .stats { margin-top: 10px; padding: 10px; background-color: #f8f9fa; border-radius: 4px; font-size: 12px; color: #6c757d; }
    </style>
</head>
<body>
    <div class="container">
        <h1>JSON Formatter & Beautifier</h1>
        
        <div class="input-section">
            <label for="jsonInput">Enter your JSON:</label>
            <textarea id="jsonInput" placeholder="Paste your JSON here...

Example:
{&quot;name&quot;:&quot;John&quot;,&quot;age&quot;:30,&quot;city&quot;:&quot;New York&quot;}"></textarea>
        </div>
        
        <div class="controls">
            <button type="button" class="btn-format" onclick="formatJson()">🎨 Format & Beautify</button>
            <button type="button" class="btn-minify" onclick="minifyJson()">📦 Minify</button>
            <button type="button" class="btn-validate" onclick="validateJson()">✅ Validate</button>
            <button type="button" class="btn-copy" onclick="copyResult()">📋 Copy Result</button>
            <button type="button" class="btn-clear" onclick="clearAll()">🗑️ Clear</button>
            
            <div class="indent-control">
                <label for="indentSize">Indent:</label>
                <input type="number" id="indentSize" value="2" min="1" max="8">
            </div>
        </div>
        
        <div class="result" id="result"></div>
        <div class="stats" id="stats"></div>
    </div>

    <script>
        function showResult(content, type = 'success') {
            const resultDiv = document.getElementById('result');
            resultDiv.className = `result ${type}`;
            resultDiv.textContent = content;
            resultDiv.style.display = 'block';
        }
        
        function updateStats(originalLength, resultLength) {
            const statsDiv = document.getElementById('stats');
            const compression = originalLength > 0 ? ((originalLength - resultLength) / originalLength * 100).toFixed(1) : 0;
            statsDiv.innerHTML = `
                Original size: ${originalLength} characters | 
                Result size: ${resultLength} characters | 
                ${compression > 0 ? 'Compression' : 'Expansion'}: ${Math.abs(compression)}%
            `;
        }
        
        function formatJson() {
            const jsonInput = document.getElementById('jsonInput').value.trim();
            const indentSize = parseInt(document.getElementById('indentSize').value) || 2;
            
            if (!jsonInput) {
                showResult('Please enter some JSON to format.', 'error');
                return;
            }

            fetch('/api/format', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ 'json_string': jsonInput, 'indent': indentSize })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showResult(data.formatted_json, 'success');
                    updateStats(jsonInput.length, data.formatted_json.length);
                } else {
                    showResult(data.error, 'error');
                }
            })
            .catch(error => {
                showResult('Network error: ' + error.message, 'error');
            });
        }
        
        function minifyJson() {
            const jsonInput = document.getElementById('jsonInput').value.trim();
            
            if (!jsonInput) {
                showResult('Please enter some JSON to minify.', 'error');
                return;
            }

            fetch('/api/minify', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ 'json_string': jsonInput })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showResult(data.minified_json, 'success');
                    updateStats(jsonInput.length, data.minified_json.length);
                } else {
                    showResult(data.error, 'error');
                }
            })
            .catch(error => {
                showResult('Network error: ' + error.message, 'error');
            });
        }
        
        function validateJson() {
            const jsonInput = document.getElementById('jsonInput').value.trim();
            
            if (!jsonInput) {
                showResult('Please enter some JSON to validate.', 'error');
                return;
            }

            fetch('/api/validate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ 'json_string': jsonInput })
            })
            .then(response => response.json())
            .then(data => {
                if (data.valid) {
                    showResult('✅ Valid JSON! Your JSON is properly formatted.', 'info');
                } else {
                    showResult('❌ Invalid JSON: ' + data.error, 'error');
                }
            })
            .catch(error => {
                showResult('Network error: ' + error.message, 'error');
            });
        }
        
        function copyResult() {
            const resultDiv = document.getElementById('result');
            if (resultDiv.style.display === 'none' || !resultDiv.textContent) {
                showResult('No result to copy. Please format, minify, or validate JSON first.', 'error');
                return;
            }
            
            navigator.clipboard.writeText(resultDiv.textContent).then(() => {
                const originalText = resultDiv.textContent;
                showResult('📋 Copied to clipboard!', 'info');
                setTimeout(() => {
                    resultDiv.textContent = originalText;
                    resultDiv.className = 'result success';
                }, 1000);
            }).catch(() => {
                showResult('Failed to copy to clipboard. Please select and copy manually.', 'error');
            });
        }
        
        function clearAll() {
            document.getElementById('jsonInput').value = '';
            document.getElementById('result').style.display = 'none';
            document.getElementById('stats').innerHTML = '';
        }
        
        document.getElementById('jsonInput').addEventListener('keydown', function(event) {
            if (event.ctrlKey && event.key === 'Enter') {
                formatJson();
            }
        });
    </script>
</body>
</html>"""

def format_json(json_string, indent=2):
    try:
        parsed_json = json.loads(json_string)
        formatted_json = json.dumps(parsed_json, indent=indent, ensure_ascii=False, sort_keys=True)
        return {'success': True, 'formatted_json': formatted_json, 'error': None}
    except json.JSONDecodeError as e:
        return {'success': False, 'formatted_json': None, 'error': f"Invalid JSON: {str(e)}"}
    except Exception as e:
        return {'success': False, 'formatted_json': None, 'error': f"Error: {str(e)}"}

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
        json.loads(json_string)
        return {'success': True, 'valid': True, 'error': None}
    except json.JSONDecodeError as e:
        return {'success': True, 'valid': False, 'error': f"Invalid JSON: {str(e)}"}

@app.route('/')
def index():
    return HTML_TEMPLATE

@app.route('/api/format', methods=['POST'])
def api_format():
    data = request.get_json()
    if not data or 'json_string' not in data:
        return jsonify({'error': 'No JSON string provided'}), 400
    
    json_string = data['json_string']
    indent = data.get('indent', 2)
    
    if not json_string.strip():
        return jsonify({'error': 'Empty JSON string'}), 400
    
    result = format_json(json_string, indent)
    
    if result['success']:
        return jsonify({'formatted_json': result['formatted_json'], 'success': True})
    else:
        return jsonify({'error': result['error'], 'success': False}), 400

@app.route('/api/minify', methods=['POST'])
def api_minify():
    data = request.get_json()
    if not data or 'json_string' not in data:
        return jsonify({'error': 'No JSON string provided'}), 400
    
    json_string = data['json_string']
    if not json_string.strip():
        return jsonify({'error': 'Empty JSON string'}), 400
    
    result = minify_json(json_string)
    
    if result['success']:
        return jsonify({'minified_json': result['minified_json'], 'success': True})
    else:
        return jsonify({'error': result['error'], 'success': False}), 400

@app.route('/api/validate', methods=['POST'])
def api_validate():
    data = request.get_json()
    if not data or 'json_string' not in data:
        return jsonify({'error': 'No JSON string provided'}), 400
    
    json_string = data['json_string']
    if not json_string.strip():
        return jsonify({'error': 'Empty JSON string'}), 400
    
    result = validate_json(json_string)
    return jsonify({'valid': result['valid'], 'error': result['error'], 'success': True})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
