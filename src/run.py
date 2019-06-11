from flask import Flask
from api.routes import personas
from api.routes import actividades

app = Flask(__name__)

app.register_blueprint(personas.personas_bp)
app.register_blueprint(actividades.actividades_bp)

if __name__ == '__main__':
    app.run(port=5000, host="0.0.0.0", use_reloader=False)
