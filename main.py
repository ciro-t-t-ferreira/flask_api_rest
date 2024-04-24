from flask import Flask
from flask_restful import Api, Resource, reqparse, abort

app = Flask(__name__)
api = Api(app)

#this is similar to moongose models
video_put_args = reqparse.RequestParser()
video_put_args.add_argument("name" , type = str, help="Name of the Video is required" , required = True)
video_put_args.add_argument("views", type = int, help="Views of the Video is required", required = True)
video_put_args.add_argument("likes", type = int, help="Likes of the Video is required", required = True)

videos = {}

def abort_if_video_id_doesnt_exist(video_id):
    if video_id not in videos:
        abort(404, message = "Video id is not valid")

#setting a endpoint with flask:
#create classe that inherit Resource
#That allow to override request methods such as get
#add the classe to the api with add_resource
class Video(Resource):
    def get(self, video_id):
        abort_if_video_id_doesnt_exist(video_id)
        return videos[video_id]
    def put(self, video_id):
        args = video_put_args.parse_args()
        videos[video_id] = args
        return videos[video_id], 201 

api.add_resource(Video, "/video/<int:video_id>")

if __name__ == "__main__":
    app.run(debug=True) #set debug=True only for development enviroment