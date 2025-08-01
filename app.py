from flask import Flask, request, render_template, jsonify
import json
import re

app = Flask(__name__)

def format_json(json_string, indent=2):
    """
    Format and beautify JSON string
    """
    try:
        # Try to parse the JSON
        parsed_json = json.loads(json_string)
        
        # Format with specified indentation
        formatted_json = json.dumps(parsed_json, indent=indent, ensure_ascii=False, sort_keys=True)
        
        return {
            'success': True,
            'formatted_json': formatted_json,
            'error': None
        }
    except json.JSONDecodeError as e:
        return {
            'success': False,
            'formatted_json': None,
            'error': f"Invalid JSON: {str(e)}"
        }
    except Exception as e:
        return {
            'success': False,
            'formatted_json': None,
            'error': f"Error: {str(e)}"
        }

def minify_json(json_string):
    """
    Minify JSON string (remove whitespace)
    """
    try:
        parsed_json = json.loads(json_string)
        minified_json = json.dumps(parsed_json, separators=(',', ':'), ensure_ascii=False)
        
        return {
            'success': True,
            'minified_json': minified_json,
            'error': None
        }
    except json.JSONDecodeError as e:
        return {
            'success': False,
            'minified_json': None,
            'error': f"Invalid JSON: {str(e)}"
        }
    except Exception as e:
        return {
            'success': False,
            'minified_json': None,
            'error': f"Error: {str(e)}"
        }

def validate_json(json_string):
    """
    Validate JSON string
    """
    try:
        json.loads(json_string)
        return {
            'success': True,
            'valid': True,
            'error': None
        }
    except json.JSONDecodeError as e:
        return {
            'success': True,
            'valid': False,
            'error': f"Invalid JSON: {str(e)}"
        }

@app.route('/')
def index():
    """
    Main page with JSON formatter interface
    """
    return render_template('index.html')

@app.route('/api/format', methods=['POST'])
def api_format():
    """
    API endpoint to format JSON
    """
    data = request.get_json()
    
    if not data or 'json_string' not in data:
        return jsonify({'error': 'No JSON string provided'}), 400
    
    json_string = data['json_string']
    indent = data.get('indent', 2)
    
    if not json_string.strip():
        return jsonify({'error': 'Empty JSON string'}), 400
    
    result = format_json(json_string, indent)
    
    if result['success']:
        return jsonify({
            'formatted_json': result['formatted_json'],
            'success': True
        })
    else:
        return jsonify({
            'error': result['error'],
            'success': False
        }), 400

@app.route('/api/minify', methods=['POST'])
def api_minify():
    """
    API endpoint to minify JSON
    """
    data = request.get_json()
    
    if not data or 'json_string' not in data:
        return jsonify({'error': 'No JSON string provided'}), 400
    
    json_string = data['json_string']
    
    if not json_string.strip():
        return jsonify({'error': 'Empty JSON string'}), 400
    
    result = minify_json(json_string)
    
    if result['success']:
        return jsonify({
            'minified_json': result['minified_json'],
            'success': True
        })
    else:
        return jsonify({
            'error': result['error'],
            'success': False
        }), 400

@app.route('/api/validate', methods=['POST'])
def api_validate():
    """
    API endpoint to validate JSON
    """
    data = request.get_json()
    
    if not data or 'json_string' not in data:
        return jsonify({'error': 'No JSON string provided'}), 400
    
    json_string = data['json_string']
    
    if not json_string.strip():
        return jsonify({'error': 'Empty JSON string'}), 400
    
    result = validate_json(json_string)
    
    return jsonify({
        'valid': result['valid'],
        'error': result['error'],
        'success': True
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
