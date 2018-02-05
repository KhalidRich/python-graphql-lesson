from flask import Flask
from flask_graphql import GraphQLView

from models import db_session
from schema import schema, Department

app = Flask(__name__)
app.debug = True # Note: We probs wouldn't want this in a production environment.

app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True # this allows us to play with the demo
    )
)

@app.route('/')
def index():
    return "You should go to localhost:5000/graphql for the goods"

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
