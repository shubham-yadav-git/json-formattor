from flask import Flask, request, jsonify
import json

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>JSON Formatter Pro</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- Google Fonts and Icons -->
    <link href="https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;600&family=Poppins:wght@500;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism-tomorrow.min.css" />
    <style>
        body {
            min-height: 100vh;
            margin: 0;
            background: linear-gradient(120deg, #232526 0%, #414345 100%);
            font-family: 'Poppins', 'Fira Code', monospace, sans-serif;
        }
        .container {
            max-width: 850px;
            margin: 40px auto 0 auto;
            background: rgba(30, 32, 42, 0.95);
            border-radius: 18px;
            box-shadow: 0 8px 32px 0 rgba(31,38,135,.25);
            padding: 38px 30px 25px 30px;
            color: #f3f6f8;
            position: relative;
        }
        .header {
            text-align: center;
            margin-bottom: 22px;
        }
        .header h1 {
            margin: 0 0 2px 0;
            font-size: 2.35em;
            letter-spacing: .07em;
            font-family: 'Poppins', sans-serif;
            background: linear-gradient(90deg, #8f94fb 0, #79c3ff 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .header p {
            color: #89b8e0;
            letter-spacing: .01em;
            margin: 4px 0 0 0;
        }
        .row {
            display: flex;
            flex-wrap: wrap;
            gap: 26px;
            margin-bottom: 18px;
        }
        .col {
            flex: 1;
            min-width: 320px;
            display: flex;
            flex-direction: column;
        }
        label {
            font-weight: 600;
            margin-bottom: 8px;
            color: #aac7df;
            letter-spacing: .02em;
        }
        textarea, .outputBox {
            border: none;
            outline: none;
            border-radius: 12px;
            font-family: 'Fira Code', monospace;
            font-size: 1em;
            padding: 17px 16px;
        }
        textarea {
            height: 190px;
            background: rgba(35,57,80,0.18);
            color: #eee;
            resize: vertical;
            box-shadow: 0 2px 8px rgba(90,120,190,0.03);
            margin-bottom: 8px;
        }
        textarea:focus {
            border: 1px solid #57b1fb;
            background: rgba(35,57,80,0.25);
        }
        .outputBox {
            background: rgba(24,33,45,.94);
            color: #b6eaff;
            min-height: 160px;
            margin-top: 6px;
            word-break: break-all;
            white-space: pre;
            font-size: 1.03em;
            overflow-x: auto;
        }
        .button-bar {
            margin: 10px 0 0 0;
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            justify-content: center;
        }
        .button-bar button {
            background: linear-gradient(90deg, #54d1c1 0%, #4f8cfb 100%);
            color: #fff;
            border: none;
            padding: 9px 22px;
            border-radius: 7px;
            font-size: 1em;
            font-family: inherit;
            font-weight: 600;
            cursor: pointer;
            letter-spacing: .03em;
            margin-bottom: 5px;
            outline: none;
            box-shadow: 0 2px 8px rgba(80,180,250,0.18);
            transition: transform .11s, box-shadow .11s, background .22s;
        }
        .button-bar button:hover, .darkmode .button-bar button:hover {
            background: linear-gradient(90deg, #696eff 0%, #0097e1 100%);
            transform: translateY(-2px) scale(1.03);
            box-shadow: 0 6px 18px #0ab7e31a;
        }
        .button-bar .danger {
            background: #ff3870;
            color: #fff;
        }
        .button-bar .danger:hover, .button-bar .danger:focus {background: #e02155;}
        .button-bar .darkmode-toggle {
            background: linear-gradient(90deg, #4e54c8 0%, #8f94fb 100%);
            color: #0af;
        }
        .status-bar {
            margin: 10px 0 7px 0;
            font-size: 15px;
            color: #7cdbf7;
            letter-spacing: .01em;
            display: flex;
            align-items: center;
            gap: 18px;
        }
        .status-bar .stats {
            color: #b1e4ff;
            font-size: 0.97em;
        }
        .status-bar .error {
            color: #ffc7d5;
            font-weight: 600;
        }
        .stats { margin-left: auto; }
        .tree-view-box {
            background: rgba(20,30,42,0.98);
            padding: 12px 9px 8px 16px;
            margin-top: 7px;
            border-radius: 8px;
            overflow-x: auto;
            font-size: 0.98em;
            color: #c3e2ff;
        }
        .tree-root {
            font-size: 1.01em;
        }
        .darkmode, .darkmode .container, .darkmode .tree-view-box, .darkmode textarea, .darkmode .outputBox {
            background: #15181f !important;
            color: #e0f0fa !important;
        }
        .darkmode .header h1 {color: #8f94fb;}
        .darkmode textarea::placeholder {color: #92ada9;}
        .darkmode .outputBox {color: #b6eaff;}
        .darkmode label {color: #badaff;}
        /* Responsive */
        @media (max-width: 670px) {
            .row { flex-direction: column; }
            .container { padding: 16px 3vw; }
        }
    </style>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/json-viewer-js@latest/dist/json-viewer.min.css">
</head>
<body>
    <div class="container" id="mainContainer">
        <div class="header">
            <h1>JSON Formatter Pro</h1>
            <p>Beautiful, reliable, developer-ready JSON tooling</p>
        </div>
        <div class="row">
            <div class="col">
                <label for="jsonInput">Input JSON</label>
                <textarea id="jsonInput" placeholder='Paste or type your JSON here... (Ctrl+Enter to format, Tab to indent)'></textarea>
            </div>
            <div class="col">
                <label>Formatted / Minified Output</label>
                <pre class="outputBox" id="prettyOutput"></pre>
                <div class="tree-view-box" id="treeview"></div>
            </div>
        </div>
        <div class="status-bar">
            <span id="validatorStatus"></span>
            <span class="stats" id="stats"></span>
        </div>
        <div class="button-bar">
            <button onclick="formatJson()">Format</button>
            <button onclick="minifyJson()">Minify</button>
            <button onclick="beautifyJson()">Beautify</button>
            <button onclick="treeView()">Tree View</button>
            <button onclick="copyToClipboard()">Copy</button>
            <button onclick="downloadJson()">Download</button>
            <button onclick="clearAll()" class="danger">Reset</button>
            <button onclick="toggleDarkMode()" class="darkmode-toggle">◉ Dark Mode</button>
        </div>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/json-viewer-js@latest/dist/json-viewer.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/prism.min.js"></script>
    <script>
        let dark = false;
        function formatJson() {
            let inputText = document.getElementById('jsonInput').value.trim();
            if (!inputText) return showStatus('No input', 'error');

            try {
                let obj = JSON.parse(inputText);
                let pretty = JSON.stringify(obj, null, 2);
                document.getElementById('prettyOutput').textContent = pretty;
                document.getElementById('treeview').innerHTML = '';
                showValidator(true);
                setStats(pretty, inputText, obj);
            } catch (e) {
                document.getElementById('prettyOutput').textContent = '';
                showValidator(false, e.message);
                setStats('', inputText, null);
            }
            Prism.highlightAll();
        }
        function minifyJson() {
            let inputText = document.getElementById('jsonInput').value.trim();
            if (!inputText) return showStatus('No input', 'error');
            try {
                let obj = JSON.parse(inputText);
                document.getElementById('prettyOutput').textContent = JSON.stringify(obj);
                document.getElementById('treeview').innerHTML = '';
                showValidator(true);
                setStats(JSON.stringify(obj), inputText, obj);
            } catch (e) {
                document.getElementById('prettyOutput').textContent = '';
                showValidator(false, e.message);
                setStats('', inputText, null);
            }
        }
        function beautifyJson() {
            formatJson();
        }
        function treeView() {
            let inputText = document.getElementById('jsonInput').value.trim();
            if (!inputText)  return showStatus('No input', 'error');
            try {
                let obj = JSON.parse(inputText);
                document.getElementById('treeview').innerHTML = '';
                new JSONViewer({rootCollapse: false, withQuotes: true}).showJSON(obj, document.getElementById('treeview'));
                showValidator(true);
                setStats(JSON.stringify(obj), inputText, obj);
            } catch (e) {
                document.getElementById('treeview').innerHTML = '';
                showValidator(false, e.message);
            }
        }
        function showValidator(valid, msg='') {
            const el = document.getElementById('validatorStatus');
            if (valid)
                el.innerHTML = '<span style="color:#82ff99;font-weight:bold;">✓ Valid JSON</span>';
            else
                el.innerHTML = '<span class="error">⚠ Invalid: ' + msg + '</span>';
        }
        function showStatus(msg, type='info') {
            const el = document.getElementById('validatorStatus');
            el.textContent = msg;
            el.style.color = (type==='error') ? '#ff90ae' : '#8ee6ff';
        }
        function copyToClipboard() {
            let val = document.getElementById('prettyOutput').textContent;
            if (!val) return showStatus('Nothing to copy', 'error');
            navigator.clipboard.writeText(val).then(() => showStatus('Copied!')).catch(() => showStatus('Copy failed', 'error'));
        }
        function downloadJson() {
            let content = document.getElementById('prettyOutput').textContent.trim();
            if (!content) return showStatus('Nothing to save', 'error');
            let a = document.createElement('a');
            let blob = new Blob([content], { type: 'application/json' });
            a.href = URL.createObjectURL(blob);
            a.download = 'formatted.json';
            document.body.appendChild(a); a.click(); document.body.removeChild(a);
            setTimeout(()=>URL.revokeObjectURL(a.href), 500);
            showStatus('Downloaded');
        }
        function clearAll() {
            document.getElementById('jsonInput').value = '';
            document.getElementById('prettyOutput').textContent = '';
            document.getElementById('treeview').innerHTML = '';
            showStatus('');
            setStats('', '', null);
        }
        function setStats(output, input, obj) {
            const stats = document.getElementById('stats');
            let info = '';
            if (input) {
                let ratio = output ? ((input.length - output.length) / input.length * 100).toFixed(1) : 0;
                let depth = obj ? maxDepth(obj) : 0, keys = obj ? countKeys(obj) : 0;
                info = `Size: ${input.length} chars | Result: ${output.length} chars | Depth: ${depth} | Keys: ${keys} | Ratio: ${ratio}%`;
            }
            stats.textContent = info;
        }
        function maxDepth(obj) {
            if (typeof obj !== 'object' || obj === null) return 0;
            let depth = 0;
            Object.keys(obj).forEach(k => { if (obj[k] && typeof obj[k] === 'object') { depth = Math.max(depth, maxDepth(obj[k])); } });
            return 1 + depth;
        }
        function countKeys(obj) {
            if (typeof obj !== 'object' || obj === null) return 0;
            let count = 0;
            Object.keys(obj).forEach(k => { count += 1 + countKeys(obj[k]); });
            return count;
        }
        function toggleDarkMode() {
            dark = !dark;
            document.body.classList.toggle('darkmode', dark);
        }
        // Keyboard shortcuts
        document.getElementById('jsonInput').addEventListener('keydown', function(e){
            if(e.ctrlKey && e.key === 'Enter'){ formatJson(); e.preventDefault(); }
            else if(e.ctrlKey && e.key.toLowerCase() === 'm'){ minifyJson(); e.preventDefault(); }
            else if(e.ctrlKey && e.key.toLowerCase() === 'b'){ beautifyJson(); e.preventDefault(); }
            else if(e.ctrlKey && e.key.toLowerCase() === 'e'){ clearAll(); e.preventDefault(); }
        });
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return HTML_TEMPLATE

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
