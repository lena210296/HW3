from flask import (
    render_template
)

from flaskr import get_db


@app.route('/names')
def names():
    db = get_db()
    names = db.execute(
        'SELECT DISTINCT artist'
        'FROM tracks'
    ).fetchall()
    return render_template('html/names.html', names=names)
