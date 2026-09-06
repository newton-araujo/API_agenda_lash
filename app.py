from flask import Flask


from src.routes.users import users
from src.routes.login import login_auth
from src.routes.clientes import client
from src.routes.procedures import procedure
from src.routes.search_status import status


app = Flask(__name__)

app.register_blueprint(users)
app.register_blueprint(login_auth)
app.register_blueprint(client)
app.register_blueprint(procedure)
app.register_blueprint(status)


if __name__ == "__main__":
    app.run(debug=True)