# all the imports
import os
import sqlite3
import googauth
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'auth.db'),
    DEBUG=True,
    SECRET_KEY='thi@sisnot$safe'
))


@app.route('/add/<username>')
def add_user(username):
    secret_key = googauth.generate_secret_key()
    # username = request.args.get('username', 'test')
    db = get_db()

    user = db.execute('select secret_key from googleauth where username=?', [username])
    if user.fetchone():
       return 'Error,username exist!'

    db.execute('insert into googleauth (username, secret_key) values (?, ?)',
                 [username, secret_key])

    db.commit()
    barcode_url = googauth.get_barcode_url(username, 'domain.com', secret_key)
    return redirect(barcode_url)


@app.route('/verify/<username>/<code>')
def verify_code(username, code):
    db = get_db()

    cur = db.execute('select secret_key, last_number from googleauth where username=?', [username])
    googleauth = cur.fetchone()
    print googleauth['last_number']
    last_number = googauth.verify_time_based(googleauth['secret_key'], str(code), 6)
    print last_number
    if not last_number:
        return 'verify failed'

    if googleauth['last_number']:
        if int(last_number) <= int(googleauth['last_number']):
            return 'verify failed'

    db.execute('update googleauth set last_number=? where username=?', [last_number, username])
    db.commit()    
    return 'verify success'


def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()




if __name__ == '__main__':
    app.run()



def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()