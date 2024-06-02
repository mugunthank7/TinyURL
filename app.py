from flask import Flask, render_template, request, redirect
from models import db, URLMap
from utils import generate_short_url

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///urls.db'
db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        long_url = request.form['long_url']
        short_url = generate_short_url()
        new_url = URLMap(long_url=long_url, short_url=short_url)
        db.session.add(new_url)
        db.session.commit()
        return render_template('result.html', short_url=short_url)
    return render_template('index.html')

@app.route('/<short_url>')
def redirect_to_long_url(short_url):
    url = URLMap.query.filter_by(short_url=short_url).first_or_404()
    return redirect(url.long_url)

if __name__ == '__main__':
    app.run(debug=True)
