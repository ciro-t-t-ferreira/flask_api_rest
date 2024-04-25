from flask import Flask
from flask_restful import Api, Resource, reqparse, fields, marshal_with, abort
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class VideoModel(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    views = db.Column(db.Integer, nullable = False)
    likes = db.Column(db.Integer, nullable = False)

    def __repr__(self):
        return f"Video(name = {self.name}, views = {self.views}, likes = {self.likes})"

#When running for the first time we should also run the following line (but we don't want to always create the db)
#db.create_all()

video_put_args = reqparse.RequestParser()
video_put_args.add_argument("name" , type = str, help="Name of the Video is required" , required = True)
video_put_args.add_argument("views", type = int, help="Views of the Video is required", required = True)
video_put_args.add_argument("likes", type = int, help="Likes of the Video is required", required = True)

#obs: the arguments will be filled with none if no value is given
video_update_args = reqparse.RequestParser()
video_update_args.add_argument("name" , type = str, help="Name of the Video" )
video_update_args.add_argument("views", type = int, help="Views of the Video")
video_update_args.add_argument("likes", type = int, help="Likes of the Video")

resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'views': fields.Integer,
    'likes': fields.Integer
}

#setting a endpoint with flask:
#create classe that inherit Resource
#That allow to override request methods such as get
#add the classe to the api with add_resource
class Video(Resource):
    @marshal_with(resource_fields)
    def get(self, video_id):
        result = VideoModel.query.filter_by(id = video_id).first()
        #raise exception in case of not finding the video
        if not result:
            abort(404, message="Could not find video wit that id")
        return result
    
    @marshal_with(resource_fields)
    def put(self, video_id):
        args = video_put_args.parse_args()
        repeatedID = VideoModel.query.filter_by(id = video_id).first()
        if repeatedID:
            abort(409, message ="Video ID is taken")
        video = VideoModel(id = video_id, name = args['name'], views = args['views'],likes = args['likes'] )
        db.session.add(video)
        db.session.commit()
        return video, 201

    @marshal_with(resource_fields)
    def patch(self, video_id):
        args = video_update_args.parse_args()
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message="Video doesn't exist, cannot update")

        if args["name"]:
            result.name = args["name"]
        if args["views"]:
            result.views = args["views"]
        if args["likes"]:
            result.likes = args["likes"]

        #obs: we don't need db.session.add() here once the object already exist in the db
        db.session.commit()
        return result 
    
    def delete(self, video_id):
        video_to_delete = VideoModel.query.filter_by(id=video_id).first()
        if video_to_delete:
            db.session.delete(video_to_delete)
            db.session.commit()
            return '', 204
        if not video_to_delete:
            abort(404, message="Video doesn't exist")

api.add_resource(Video, "/video/<int:video_id>")

if __name__ == "__main__":
    app.run(debug=True) #set debug=True only for development enviroment