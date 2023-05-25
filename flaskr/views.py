from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from flaskr.db import get_db

bp = Blueprint('views', __name__)


@bp.route('/names')
def names():
    db = get_db()
    names = db.execute(
        'SELECT DISTINCT artist '
        'FROM tracks'
    ).fetchall()
    return render_template('names.html', names=names)


@bp.route('/tracks')
def tracks_number():
    db = get_db()
    result = db.execute(
        'SELECT COUNT(*) '
        'FROM tracks'
    ).fetchone()
    num_tracks = result[0] if result is not None else 0
    return render_template('tracks_number.html', num_tracks=num_tracks)


@bp.route('/tracks/<genre>')
def tracks_by_genre(genre):
    db = get_db()
    result = db.execute(
        'SELECT COUNT(*) FROM tracks WHERE genre_id = (SELECT id FROM genres WHERE title = ?)',
        (genre,)
    ).fetchone()
    tracks = result[0] if result is not None else 0
    return render_template('tracks_by_genre.html', genre=genre, tracks=tracks)


@bp.route('/tracks-sec')
def track_length():
    db = get_db()
    tracks = db.execute(
        'SELECT title, CAST(SUBSTR(length, 1, INSTR(length, ".") - 1) AS INTEGER) * 60 + CAST(SUBSTR(length, '
        'INSTR(length, ".") + 1) AS INTEGER) AS length_sec FROM tracks'
    ).fetchall()
    return render_template('length_sec.html', tracks=tracks)


@bp.route('/tracks-sec/statistics')
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
