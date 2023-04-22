from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/igor/Documents/imdb.db'
db.init_app(app)


class Movies(db.Model):
    __tablename__ = 'movies'

    id = db.Column(db.Integer, primary_key=True)
    movie_title = db.Column(db.String, unique=True, nullable=False)
    year = db.Column(db.String, nullable=False)
    genre = db.Column(db.String, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    description = db.Column(db.String, unique=True, nullable=False)
    duration = db.Column(db.String, nullable=False)
    director = db.Column(db.String, unique=True, nullable=False)
    gross = db.Column(db.Float, nullable=False)
    images_url = db.Column(db.String, unique=True, nullable=False)
    actor = db.Column(db.String, unique=True, nullable=False)
    actress = db.Column(db.String, unique=True, nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'movie_title': self.movie_title,
            'year': self.year,
            'genre': self.genre,
            'rating': self.rating,
            'description': self.description,
            'duration': self.duration,
            'director': self.director,
            'gross': self.gross,
            'images_url': self.images_url,
            'actor': self.actor,
            'actress': self.actress
        }


with app.app_context():
    db.create_all()


@app.route('/movies/director', methods=['GET'])
def get_movies_by_director():
    director = request.args.get('director')
    movies = Movies.query.filter_by(director=director).all()
    serialized_movies = [movie.serialize() for movie in movies]
    return jsonify(serialized_movies)


@app.route('/movies/actor', methods=['GET'])
def get_movies_by_actor():
    actor = request.args.get('actor')
    movies = Movies.query.filter_by(actor=actor).all()
    serialized_movies = [movie.serialize() for movie in movies]
    return jsonify(serialized_movies)


@app.route('/movies/actress', methods=['GET'])
def get_movies_by_actress():
    actress = request.args.get('actress')
    movies = Movies.query.filter_by(actress=actress).all()
    serialized_movies = [movie.serialize() for movie in movies]
    return jsonify(serialized_movies)



if __name__ == "__main__":
    app.run(debug=True)






















