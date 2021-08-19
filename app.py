from flask.templating import render_template
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('base.html')

@app.route('/list_machines')
def list_machines():
    return render_template('base.html')



if __name__ == '__main__':
    app.run(debug=True)