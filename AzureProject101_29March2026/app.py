from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    tasks = ["Learn Azure", "Deploy Web App", "Master App Service Plans"]
    return render_template('index.html', tasks=tasks)

if __name__ == '__main__':
    app.run()