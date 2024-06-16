import os
import tempfile
import subprocess
import sys
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__)
app.config['OUTPUT_DIR'] = tempfile.gettempdir()

@app.route('/upload_script', methods=['POST'])
def upload_script():
    if 'script' not in request.files:
        return jsonify({'message': 'No script file provided'}), 400
    
    script = request.files['script']
    script_path = os.path.join(app.config['OUTPUT_DIR'], script.filename)
    script.save(script_path)
    print(f"Script saved to: {script_path}")

    try:
        # Run the script and capture the output
        result = subprocess.run([sys.executable, script_path], capture_output=True, text=True, check=True)
        output = result.stdout
        error = result.stderr
    except subprocess.CalledProcessError as e:
        output = e.stdout
        error = e.stderr
        print(f"Script error: {error}")

    # Store the results
    output_path = os.path.join(app.config['OUTPUT_DIR'], 'output.txt')
    with open(output_path, 'w') as f:
        if result.returncode == 0:
            f.write(output)
        else:
            f.write(error)

    print(f"Output written to: {output_path}")

    return jsonify({'message': 'Script executed', 'output_path': '/download_output'})

@app.route('/download_output', methods=['GET'])
def download_output():
    output_path = os.path.join(app.config['OUTPUT_DIR'], 'output.txt')
    if os.path.exists(output_path):
        return send_from_directory(app.config['OUTPUT_DIR'], 'output.txt', as_attachment=True)
    else:
        return jsonify({'message': 'Output file not found'}), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
