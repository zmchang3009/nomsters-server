from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello world!'

@app.route('/2')
def hello_world2():
    return 'Hello world 2!'


if __name__ == '__main__':
    app.run(debug=True)