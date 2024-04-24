from flask import Flask
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

#setting a endpoint with flask:
#create classe that inherit Resource
#That allow to override request methods such as get
#add the classe to the api with add_resource

class HelloWorld(Resource):
    def get(self):
        return {"data":"Hello World"}

api.add_resource(HelloWorld, "/helloworld")

if __name__ == "__main__":
    app.run(debug=True) #set debug=True only for development enviroment