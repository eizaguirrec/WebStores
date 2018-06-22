from src.app import app

app.run(debug=app.config['DEBUG'], port=app.config['PORT'], host=app.config['HOST'])

