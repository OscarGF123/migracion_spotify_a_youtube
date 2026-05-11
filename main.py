from flask import Flask, jsonify, request
from flask_session import Session
from enpoints import endpoints_bp

app = Flask(__name__)

app.secret_key = "clave_muy_muy_secreta"
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = './flask_sessions'   # ← ruta explícita
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True      

Session(app)

app.register_blueprint(endpoints_bp)


if __name__ == "__main__":
    app.run(debug=True)