from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient

app = Flask(__name__)

# --- Параметри підключення до MongoDB ---
uri = "mongodb+srv://sikora:20050411@db1.gyaftca.mongodb.net/?retryWrites=true&w=majority&tls=true"

client = MongoClient(uri, tls=True, tlsAllowInvalidCertificates=True)

db = client.mydatabase  # Замініть на назву вашої бази даних
collection = db.mycollection  # Замініть на назву вашої колекції

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        age_str = request.form['age']
        if name and age_str.isdigit():
            age = int(age_str)
            data = {"name": name, "age": age}
            try:
                result = collection.insert_one(data)
                return redirect(url_for('index'))
            except Exception as e:
                return f"Помилка вставки: {e}"
    # Отримання всіх документів з MongoDB
    documents = collection.find()
    return render_template('index.html', documents=documents)

if __name__ == "__main__":
    import os

    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)

