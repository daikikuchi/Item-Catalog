from flask import Flask
from category import category
from item import item
from authentication import authentication

app = Flask(__name__)

app.register_blueprint(category)
app.register_blueprint(item)
app.register_blueprint(authentication)

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=9999)
