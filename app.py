from flask import Flask, jsonify
app = Flask(__name__)

@app.route("/")
def home():
    return """<!doctype html><html><head><title>Campus Helpdesk Portal</title></head>
    <body style="font-family:Arial;max-width:720px;margin:60px auto;line-height:1.6">
    <h1>Campus Helpdesk Portal</h1>
    <p>Welcome! This sample academic project helps students find support.</p>
    <ul><li>IT Support: it-support@example.edu</li><li>Library Help: library@example.edu</li>
    <li>Student Office: student-office@example.edu</li></ul>
    <p><strong>Version:</strong> v1</p><p>Health check: <a href="/health">/health</a></p>
    </body></html>"""

@app.route("/health")
def health():
    return jsonify(status="ok", application="campus-helpdesk-portal")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
