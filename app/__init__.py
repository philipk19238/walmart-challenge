from flask import Flask 

app = Flask(__name__)

app.config['BASE_URL'] = "https://api.github.com/repos"
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

from app import routes 
