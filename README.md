# JSON Formatter & Beautifier

A simple Flask web application to format, beautify, minify, and validate JSON data.

## Features

- **Format & Beautify**: Convert minified JSON into readable, properly indented format
- **Minify**: Remove unnecessary whitespace to reduce JSON size
- **Validate**: Check if your JSON is syntactically correct
- **Copy Result**: One-click copy to clipboard
- **Custom Indentation**: Choose between 1-8 spaces for formatting
- **Statistics**: View compression/expansion ratios
- **Keyboard Shortcuts**: Ctrl+Enter to format

## Installation

1. Make sure you have Python 3.7+ installed
2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Start the Flask application:
   ```bash
   python app.py
   ```

2. Open your web browser and navigate to:
   ```
   http://localhost:5000
   ```

3. Paste your JSON in the text area and use the buttons to:
   - **Format & Beautify**: Make JSON readable with proper indentation
   - **Minify**: Remove whitespace to compress JSON
   - **Validate**: Check if JSON is valid
   - **Copy Result**: Copy the result to clipboard
   - **Clear**: Clear both input and output

## API Endpoints

The application also provides REST API endpoints:

### Format JSON
```
POST /api/format
Content-Type: application/json

{
    "json_string": "your json here",
    "indent": 2
}
```

### Minify JSON  
```
POST /api/minify
Content-Type: application/json

{
    "json_string": "your json here"
}
```

### Validate JSON
```
POST /api/validate
Content-Type: application/json

{
    "json_string": "your json here"
}
```

## Example

Input:
```json
{"name":"John","age":30,"city":"New York","hobbies":["reading","swimming"],"address":{"street":"123 Main St","zip":"10001"}}
```

Formatted Output:
```json
{
  "address": {
    "street": "123 Main St",
    "zip": "10001"
  },
  "age": 30,
  "city": "New York",
  "hobbies": [
    "reading",
    "swimming"
  ],
  "name": "John"
}
```

## Development

To run in development mode with debug enabled:
```bash
python app.py
```

The application will be available at `http://localhost:5000` with auto-reload enabled.
