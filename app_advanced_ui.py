from flask import Flask, request, jsonify
import json

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang='en'>
<head>
    <meta charset='UTF-8'>
    <meta name='viewport' content='width=device-width, initial-scale=1.0'>
    <title>Advanced JSON Formatter</title>
    <link href='https://fonts.googleapis.com/css?family=Roboto:400,500,700&display=swap' rel='stylesheet'>
    <style>
        body {
            font-family: 'Roboto', sans-serif;
            background-color: #e9ecef;
            margin: 0;
            padding: 2em;
            display: flex;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
        }
        
        .container {
            max-width: 1200px;
            width: 100%;
            background-color: #fff;
            padding: 2em;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }
        
        .header {
            text-align: center;
            margin-bottom: 1em;
        }

        .header h1 {
            margin: 0;
            font-size: 2em;
            color: #333;
        }

        .header p {
            margin: 0.5em 0 0;
            color: #666;
        }

        .form-group {
            margin-bottom: 1.5em;
        }

        textarea {
            width: 100%;
            height: 150px;
            border: 1px solid #ccc;
            border-radius: 5px;
            padding: 1em;
            font-family: monospace;
            font-size: 1em;
            transition: box-shadow 0.3s ease;
        }

        textarea:focus {
            outline: none;
            box-shadow: 0 0 5px rgba(0, 123, 255, 0.3);
        }

        .controls {
            text-align: center;
            margin-top: 20px;
        }

        button {
            background-color: #007bff;
            color: white;
            border: none;
            padding: 0.5em 2em;
            font-size: 1em;
            border-radius: 5px;
            cursor: pointer;
            transition: background-color 0.3s ease;
            margin: 0 0.5em;
        }

        button:hover {
            background-color: #0056b3;
        }

        .output-group {
            margin-top: 2em;
        }

        .output {
            padding: 1em;
            background-color: #f8f9fa;
            border-radius: 5px;
            font-family: monospace;
            font-size: 0.9em;
            line-height: 1.4em;
            overflow-x: auto;
        }

        .error {
            color: #dc3545;
            font-weight: bold;
        }
    </style>
    <link rel='stylesheet' href='https://prismjs.com/themes/prism.css'>
    <script src='https://cdn.jsdelivr.net/npm/json-viewer-js/dist/json-viewer.min.js'></script>
    <script src='https://prismjs.com/prism.js'></script>
</head>
<body>
    <div class='container'>
        <div class='header'>
            <h1>Advanced JSON Formatter</h1>
            <p>Format, validate, and analyze your JSON with ease</p>
        </div>

        <div class='form-group'>
            <textarea id='jsonInput' placeholder='Paste your JSON here...'></textarea>
        </div>

        <div class='controls'>
            <button onclick='formatJson()'>Format JSON</button>
            <button onclick='validateJson()'>Validate JSON</button>
            <button onclick='clearOutput()'>Clear</button>
        </div>

        <div class='output-group'>
            <h2>Formatted JSON:</h2>
            <pre id='outputArea' class='output'></pre>
        </div>
    </div>

    <script>
        function formatJson() {
            const jsonInput = document.getElementById('jsonInput').value.trim();
            if (!jsonInput) {
                alert('Please enter some JSON to format.');
                return;
            }

            try {
                const obj = JSON.parse(jsonInput);
                const pretty = JSON.stringify(obj, null, 2);
                document.getElementById('outputArea').textContent = pretty;
                Prism.highlightAll();
            } catch (error) {
                document.getElementById('outputArea').innerHTML = `<span class='error'>Invalid JSON: ${error.message}<span>`;
            }
        }

        function validateJson() {
            const jsonInput = document.getElementById('jsonInput').value.trim();
            if (!jsonInput) {
                alert('Please enter some JSON to validate.');
                return;
            }

            try {
                JSON.parse(jsonInput);
                alert('JSON is valid!');
            } catch (error) {
                alert('Invalid JSON: ' + error.message);
            }
        }

        function clearOutput() {
            document.getElementById('outputArea').textContent = '';
            document.getElementById('jsonInput').value = '';
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return HTML_TEMPLATE

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
