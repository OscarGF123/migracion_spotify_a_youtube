import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, jsonify, request
from flask_session import Session
from enpoints import endpoints_bp

app = Flask(__name__)

app.secret_key = "clave_muy_muy_secreta"
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = './flask_sessions'   # ← ruta explícita
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True      

# ___________ Configuracion de Logs ___________

handler = RotatingFileHandler(
    'logs.txt',       # nombre del archivo
    maxBytes=1000000, # tamaño máximo del archivo (1MB)
    backupCount=3     # cuántos archivos de respaldo guardar
)

handler.setLevel(logging.DEBUG)

formatter = logging.Formatter(
    '[%(asctime)s] %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
handler.setFormatter(formatter)

app.logger.addHandler(handler)
app.logger.setLevel(logging.DEBUG)

# ______________________________________________
Session(app)

app.register_blueprint(endpoints_bp)


if __name__ == "__main__":
    app.run(debug=True)