from flask_app import app
# from flask_app.Controllers import User_routes
from flask_app.controllers import Post_routes
from flask_app.controllers import Official_routes
from flask_app.test_controllers import scrapper_test
if __name__=="__main__":
    app.run(debug=True, port=5000)
