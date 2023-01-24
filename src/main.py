from os import getenv
from flask import Flask

app = Flask(__name__)

app.config['DEBUG'] = (getenv('DEBUG') or '0').lower() in ['1', 'true']

@app.route('/')
def index():
    return 'Hello world!'

if __name__ == '__main__':
    app.run(host=getenv('HOST') or '::', port=getenv('PORT') or '8080')
