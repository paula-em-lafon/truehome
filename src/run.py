from flask import Flask, jsonify
from api.routes import personas
from api.routes import actividades
from api.routes import deals
from flask_swagger import swagger

app = Flask(__name__)

app.register_blueprint(personas.personas_bp)
app.register_blueprint(actividades.actividades_bp)
app.register_blueprint(deals.deals_bp)


@app.route("/api/v1/spec")
def spec():
    swag = swagger(app)
    swag['info']['version'] = "1.0"
    swag['info']['title'] = "My API"
    return jsonify(swag)

if __name__ == '__main__':
    app.run(port=5000, host="0.0.0.0", use_reloader=False)
