from flask import Flask, request, jsonify
import json

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang='en'>
<head>
    <meta charset='UTF-8'>
    <meta name='viewport' content='width=device-width, initial-scale=1.0'>
    <title>Stylish JSON Formatter</title>
    <link href='https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap' rel='stylesheet'>
    <style>
        body {
            font-family: 'Poppins', sans-serif;
            background-color: #f0f4f8;
            margin: 0;
            padding: 20px;
            display: flex;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            transition: background-color 0.3s ease;
        }
        .container {
            max-width: 1200px;
            width: 100%;
            background-color: #ffffff;
            padding: 25px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            transition: box-shadow 0.3s ease;
        }
        .container:hover {
            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
        }
        .header h1 {
            margin: 0 0 10px;
            font-size: 1.8em;
            color: #333;
            text-align: center;
        }
        textarea {
            width: 100%;
            height: 150px;
            border: 1px solid #ccd0d5;
            border-radius: 8px;
            padding: 15px;
            font-family: 'Courier New', monospace;
            font-size: 1em;
            resize: vertical;
            transition: border-color 0.3s ease;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        }
        textarea:focus {
            border-color: #007bff;
            box-shadow: 0 0 5px rgba(0, 123, 255, 0.5);
            outline: none;
        }
        .button-bar {
            text-align: center;
            padding-top: 15px;
        }
        button {
            background-color: #007bff;
            color: white;
            border: none;
            padding: 10px 30px;
            font-size: 1em;
            font-weight: bold;
            border-radius: 8px;
            cursor: pointer;
            transition: background-color 0.3s ease;
            box-shadow: 0 3px 6px rgba(0, 0, 0, 0.1);
            margin: 0 10px;
        }
        button:hover {
            background-color: #0056b3;
        }
        .output {
            background-color: #f9fbfd;
            border-radius: 8px;
            padding: 20px;
            font-family: 'Courier New', monospace;
            white-space: pre-wrap;
            overflow-x: auto;
            line-height: 1.5;
            transition: background-color 0.3s ease;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            margin-top: 20px;
        }
        .error {
            color: #dc3545;
            font-weight: bold;
        }
    </style>
    <link rel='stylesheet' href='https://cdnjs.cloudflare.com/ajax/libs/prism/1.23.0/themes/prism.min.css'>
    <script src='https://cdnjs.cloudflare.com/ajax/libs/prism/1.23.0/prism.min.js'></script>
</head>
<body>
    <div class='container'>
        <div class='header'>
            <h1>Stylish JSON Formatter</h1>
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
                document.getElementById('output').innerHTML = `<span class='error'>Invalid JSON: ${e.message}<span>`;
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
                document.getElementById('output').innerHTML = `<span class='error'>Invalid JSON: ${e.message}<span>`;
            }
        }
        function beautifyJson() {
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
