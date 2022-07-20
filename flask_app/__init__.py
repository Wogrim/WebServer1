from flask import Flask
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.secret_key = "djfoa8wf98jf29fjsilajf8p92"

bcrypt = Bcrypt(app)