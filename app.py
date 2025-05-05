from flask import Flask, request, render_template, redirect, url_for
import os
import uuid
import json

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['JSON_FILE'] = 'data.json'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# 結果保存用
def save_result(ref_id, image_path, diagnosis):
    if os.path.exists(app.config['JSON_FILE']):
        with open(app.config['JSON_FILE'], 'r') as f:
            data = json.load(f)
    else:
        data = {}

    data.setdefault(ref_id, []).append({
        'image': image_path,
        'diagnosis': diagnosis
    })

    with open(app.config['JSON_FILE'], 'w') as f:
        json.dump(data, f)

@app.route('/')
def index():
    ref = request.args.get('ref', None)
    return render_template('index.html', ref=ref)

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['photo']
    ref = request.form['ref']
    share = request.form.get('share')

    if file:
        filename = str(uuid.uuid4()) + '.jpg'
        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(path)

        diagnosis = "あなたはとても素敵です！"

        if share:
            save_result(ref, filename, diagnosis)

        return render_template('result.html', diagnosis=diagnosis)

    return "写真がありません", 400




@app.route('/dashboard/<ref_id>')
def dashboard(ref_id):
    if os.path.exists(app.config['JSON_FILE']):
        with open(app.config['JSON_FILE'], 'r') as f:
            data = json.load(f)
        items = data.get(ref_id, [])
    else:
        items = []

    return render_template('dashboard.html', items=items)

if __name__ == '__main__':
    app.run(debug=True)
