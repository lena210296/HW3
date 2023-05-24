import os

from flask import Flask
from flask import (
    render_template
)
from flaskr.db import get_db


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from flaskr import db
    db.init_app(app)

    # a simple page that says hello

    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    @app.route('/names')
    def names():
        db = get_db()
        names = db.execute(
            'SELECT DISTINCT artist '
            'FROM tracks'
        ).fetchall()
        return render_template('names.html', names=names)

    @app.route('/tracks')
    def tracks_number():
        db = get_db()
        result = db.execute(
            'SELECT COUNT(*) '
            'FROM tracks'
        ).fetchone()
        num_tracks = result[0] if result is not None else 0
        return render_template('tracks_number.html', num_tracks=num_tracks)

    @app.route('/tracks/<genre>')
    def tracks_by_genre(genre):
        db = get_db()
        result = db.execute(
            'SELECT COUNT(*) FROM tracks WHERE genre_id = (SELECT id FROM genres WHERE title = ?)',
            (genre,)
        ).fetchone()
        tracks = result[0] if result is not None else 0
        return render_template('tracks_by_genre.html', genre=genre, tracks=tracks)

    @app.route('/tracks-sec')
    def track_length():
        db = get_db()
        tracks = db.execute(
            'SELECT title, CAST(SUBSTR(length, 1, INSTR(length, ".") - 1) AS INTEGER) * 60 + CAST(SUBSTR(length, '
            'INSTR(length, ".") + 1) AS INTEGER) AS length_sec FROM tracks'
        ).fetchall()
        return render_template('length_sec.html', tracks=tracks)

    @app.route('/tracks-sec/statistics')
    def statistics():
        db = get_db()
        stat = db.execute(
            'SELECT SUM(CAST(SUBSTR(length, 1, INSTR(length, ".") - 1) AS INTEGER) * 60 + CAST(SUBSTR(length, '
            'INSTR(length, ".") + 1) AS INTEGER)) AS length_sum, '
            'AVG(CAST(SUBSTR(length, 1, INSTR(length, ".") - 1) AS INTEGER) * 60 + CAST(SUBSTR(length, '
            'INSTR(length, ".") + 1) AS INTEGER)) AS length_avg FROM tracks'
        ).fetchone()
        sum_sec = stat['length_sum'] if stat['length_sum'] is not None else 0
        avg_sec = stat['length_avg'] if stat['length_avg'] is not None else 0
        return render_template('statistics.html', sum_sec=sum_sec, avg_sec=avg_sec)

    return app
