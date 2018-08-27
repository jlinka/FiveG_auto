from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_script import Manager
from app.form import Search
from app import create_app
from app.main import main as blue_main

app = Flask(__name__, static_url_path='/static')
manager = Manager(app)
bootstrap = Bootstrap(app)
app.config.update(dict(
    SECRET_KEY="powerful secretkey",
    WTF_CSRF_SECRET_KEY="a csrf secret key"
))

app.register_blueprint(blue_main, url_prefit='main')


# app = create_app()
# manager = Manager(app)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route('/')
def hello_world():
    print('aaa')
    search = Search()
    return render_template('index.html', search=search)


if __name__ == '__main__':
    app.run()
