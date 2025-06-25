# === phishing_url_detector.py ===
# A complete ML-based Phishing URL Detector with Flask API & enhanced Web Form UI with animations and logging

import re
import joblib
import pandas as pd
from flask import Flask, request, jsonify, render_template_string
from sklearn.ensemble import RandomForestClassifier
import os
from datetime import datetime

app = Flask(__name__)

# === Feature extraction from URL ===
def extract_features(url):
    return {
        'url_length': len(url),
        'has_https': int('https' in url),
        'has_ip': int(bool(re.search(r'\d+\.\d+\.\d+\.\d+', url))),
        'has_at_symbol': int('@' in url),
        'has_dash': int('-' in url),
        'dot_count': url.count('.'),
        'has_subdomain': int(url.count('.') > 2),
        'has_suspicious_word': int(any(word in url.lower() for word in ['login', 'verify', 'secure', 'update']))
    }

# === Load or Train Model ===
def train_model():
    data = pd.DataFrame({
        'url': [
            'http://192.168.0.1/login',
            'https://secure.bank.com/account/update',
            'http://example.com',
            'https://paypal.com-login-verification.com',
            'https://github.com/login'
        ],
        'label': [1, 1, 0, 1, 0]
    })
    features = pd.DataFrame([extract_features(url) for url in data['url']])
    X = features
    y = data['label']
    model = RandomForestClassifier()
    model.fit(X, y)
    joblib.dump(model, 'phishing_model.pkl')
    return model

model_path = 'phishing_model.pkl'
model = joblib.load(model_path) if os.path.exists(model_path) else train_model()

# === Logging Function ===
def log_prediction(url, result):
    with open("url_history.log", "a") as log_file:
        log_file.write(f"{datetime.now()}, {url}, {result}\n")

# === Flask API ===
@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    url = data.get('url')
    if not url:
        return jsonify({'error': 'No URL provided'}), 400
    features = extract_features(url)
    df = pd.DataFrame([features])
    prediction = model.predict(df)[0]
    result = 'Phishing' if prediction == 1 else 'Safe'
    log_prediction(url, result)
    return jsonify({'url': url, 'result': result})

# === Styled Web Form UI ===
HTML_FORM = '''
<!DOCTYPE html>
<html>
<head>
    <title>Phishing URL Detector</title>
    <style>
        body {
            font-family: 'Segoe UI', sans-serif;
            background: linear-gradient(120deg, #89f7fe 0%, #66a6ff 100%);
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        .container {
            background-color: white;
            padding: 40px;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            text-align: center;
            width: 500px;
            animation: fadeIn 1s ease-in-out;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(-20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        textarea {
            width: 90%;
            height: 100px;
            padding: 10px;
            margin: 10px 0;
            border: 1px solid #ccc;
            border-radius: 8px;
            resize: none;
        }
        button {
            background-color: #007BFF;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 16px;
            margin-top: 10px;
            box-shadow: 0 0 10px #007BFF;
            transition: box-shadow 0.3s ease-in-out, transform 0.2s ease;
        }
        button:hover {
            background-color: #0056b3;
            box-shadow: 0 0 20px #0056b3;
            transform: scale(1.05);
        }
        .result {
            margin-top: 20px;
            font-size: 16px;
            text-align: left;
            white-space: pre-wrap;
            color: #333;
        }
    </style>
</head>
<body>
    <div class="container">
        <h2>Phishing URL Detector</h2>
        <form method="POST">
            <textarea name="urls" placeholder="Enter one or more URLs (one per line)..." required></textarea>
            <br>
            <button type="submit">Check URLs</button>
        </form>
        {% if result %}
        <div class="result"><strong>Results:</strong>\n{{ result }}</div>
        {% endif %}
    </div>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def home():
    result = None
    if request.method == 'POST':
        urls_input = request.form.get('urls', '')
        urls = urls_input.strip().splitlines()
        result_lines = []
        for url in urls:
            features = extract_features(url)
            df = pd.DataFrame([features])
            prediction = model.predict(df)[0]
            classification = 'Phishing' if prediction == 1 else 'Safe'
            result_lines.append(f"{url} => {classification}")
            log_prediction(url, classification)
        result = '\n'.join(result_lines)
    return render_template_string(HTML_FORM, result=result)

# === Run Flask ===
if __name__ == '__main__':
    app.run(debug=True)
