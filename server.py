from flask_app import app
# from flask_app.Controllers import User_routes
from flask_app.Controllers import Post_routes
from flask_app.Controllers import Official_routes

if __name__=="__main__":
    app.run(debug=True, port=5000)