'''Main entry point to API'''
from flask import Flask
import routes

app = Flask(__name__, template_folder='.')
routes.configure_routes(app)
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
