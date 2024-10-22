from flask import Flask, render_template_string
import subprocess

app = Flask(__name__)

# HTML template with buttons
html_template = '''
<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Run Scripts</title>
</head>
<body>
    <h1>Run Your Scripts</h1>
    <button onclick="location.href='/run_script1'">DMS Report</button>
    <button onclick="location.href='/run_script2'">Update Medtronic Tenders</button>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(html_template)

@app.route('/run_script1')
def run_script1():
    # Replace 'script1.py' with your actual script
    subprocess.run(['py', 'gen_report_dms.py'])
    return "Script 1 has been run!"

@app.route('/run_script2')
def run_script2():
    # Replace 'script2.py' with your actual script
    subprocess.run(['py', 'gen_cwl_so.py'])
    return "Script 2 has been run!"

if __name__ == '__main__':
    app.run(debug=True)