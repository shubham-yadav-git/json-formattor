from flask import Flask, request, jsonify
import json

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang='en'>
<head>
    <meta charset='UTF-8'>
    <meta name='viewport' content='width=device-width, initial-scale=1.0'>
    <title>Enhanced JSON Formatter</title>
    <link href='https://fonts.googleapis.com/css?family=Roboto:400,500,700&display=swap' rel='stylesheet'>
    <style>
        body {
            font-family: 'Roboto', sans-serif;
            background-color: #f4f7f9;
            margin: 0;
            padding: 20px;
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
            display: flex;
            flex-direction: column;
            gap: 20px;
        }
        .header h1, .header p {
            margin: 0;
            text-align: center;
        }
        textarea {
            width: 100%;
            height: 150px;
            border: 1px solid #ccc;
            border-radius: 5px;
            padding: 1em;
            font-family: monospace;
            font-size: 1em;
            box-shadow: 0 0 5px rgba(0, 123, 255, 0.3);
        }
        .button-bar {
            text-align: center;
            padding-top: 10px;
        }
        button {
            background-color: #007bff;
            color: white;
            border: none;
            padding: 10px 20px;
            font-size: 1em;
            border-radius: 5px;
            cursor: pointer;
            transition: background-color 0.3s ease;
            margin: 0 5px;
        }
        button:hover {
            background-color: #0056b3;
        }
        .output {
            background-color: #f1f3f5;
            border-radius: 5px;
            padding: 1em;
            font-family: monospace;
            white-space: pre-wrap;
            overflow-x: auto;
        }
        .error {
            color: #dc3545;
            font-weight: bold;
        }
    </style>
    <link rel='stylesheet' href='https://cdnjs.cloudflare.com/ajax/libs/prism/1.23.0/themes/prism.min.css'>
    <script src='https://cdn.jsdelivr.net/npm/json-viewer-js@latest/dist/jquery.json-viewer.js'></script>
    <script src='https://cdnjs.cloudflare.com/ajax/libs/prism/1.23.0/prism.min.js'></script>
</head>
<body>
    <div class='container'>
        <div class='header'>
            <h1>Enhanced JSON Formatter</h1>
            <p>Feature-Rich JSON Tool for Developers</p>
        </div>
        <textarea id='jsonInput' placeholder='Paste your JSON here...'></textarea>
        <div class='button-bar'>
            <button onclick='formatJson()'>Format</button>
            <button onclick='minifyJson()'>Minify</button>
            <button onclick='beautifyJson()'>Beautify</button>
            <button onclick='validateJson()'>Validate</button>
            <button onclick='copyToClipboard()'>Copy</button>
            <button onclick='downloadJson()'>Download</button>
            <button onclick='clearAll()'>Clear</button>
        </div>
        <div id='output' class='output'></div>
    </div>
    <script>
        function formatJson() {
            const input = document.getElementById('jsonInput').value.trim();
            if (!input) return alert('Please enter some JSON to format.');
            try {
                const parsed = JSON.parse(input);
                const pretty = JSON.stringify(parsed, null, 2);
                document.getElementById('output').textContent = pretty;
                Prism.highlightAll();
            } catch (e) {
                document.getElementById('output').innerHTML = `<span class='error'>Invalid JSON: ${e.message}</span>`;
            }
        }
        function minifyJson() {
            const input = document.getElementById('jsonInput').value.trim();
            if (!input) return alert('Please enter some JSON to minify.');
            try {
                const parsed = JSON.parse(input);
                const minified = JSON.stringify(parsed);
                document.getElementById('output').textContent = minified;
            } catch (e) {
                document.getElementById('output').innerHTML = `<span class='error'>Invalid JSON: ${e.message}</span>`;
            }
        }
        function beautifyJson() {
            const input = document.getElementById('jsonInput').value.trim();
            formatJson();
        }
        function validateJson() {
            const input = document.getElementById('jsonInput').value.trim();
            try {
                JSON.parse(input);
                alert('Valid JSON!');
            } catch (e) {
                alert('Invalid JSON: ' + e.message);
            }
        }
        function copyToClipboard() {
            const output = document.getElementById('output').textContent;
            navigator.clipboard.writeText(output).then(() => alert('Copied to clipboard!')).catch(err => alert('Failed to copy.'));
        }
        function downloadJson() {
            const content = document.getElementById('output').textContent;
            const blob = new Blob([content], { type: 'application/json' });
            const a = document.createElement('a');
            a.href = URL.createObjectURL(blob);
            a.download = 'formatted.json';
            a.click();
            URL.revokeObjectURL(a.href);
        }
        function clearAll() {
            document.getElementById('jsonInput').value = '';
            document.getElementById('output').textContent = '';
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
