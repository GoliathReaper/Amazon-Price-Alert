from flask import Flask, render_template, redirect, url_for, request, flash
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from flask_apscheduler import APScheduler
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from apscheduler.schedulers.background import BackgroundScheduler
from amazon import scrape
from telegram_notification import telegram_message
from datetime import datetime
from remove_symbols import clean_number_string
from time import sleep


app = Flask(__name__)
scheduler = APScheduler()
Bootstrap5(app)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///sqlite_amazon_price.db"
db = SQLAlchemy(app)


class Pricedb(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_time = db.Column(db.String(255), unique=True, nullable=False)
    product_name = db.Column(db.String(250), unique=True, nullable=False)
    product_url = db.Column(db.String(250), unique=True, nullable=False)
    img_url = db.Column(db.String(250), nullable=False)
    expected_price = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<{self.product_url} {self.expected_price}>'


class HistoricalPriceData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_time = db.Column(db.String(255), nullable=False)
    product_name = db.Column(db.String(250), nullable=False)
    product_url = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(250), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    expected_price = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<HistoricalPriceData {self.expected_price, self.price}>'


with app.app_context():
    db.create_all()
    db.session.commit()


class AddProduct(FlaskForm):
    product_url = StringField('Enter the Amazon product URL to track', validators=[DataRequired()])
    expected_price = StringField('Exected Price', validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.route("/", methods=['POST', 'GET'])
def home():
    form = AddProduct()
    if form.validate_on_submit():
        dataset = scrape(request.form['product_url'])
        new_product = Pricedb(
            date_time=datetime.now(),
            product_name=dataset['name'],
            product_url=request.form['product_url'],
            img_url=dataset['images'],
            expected_price=request.form['expected_price'],
        )
        db.session.add(new_product)
        db.session.commit()
        flash(u'Added Successfully')
        return redirect(url_for('home'))
    return render_template("index.html", form=form)


@app.route("/table", methods=['POST', 'GET'])
def table():
    result = db.session.execute(db.select(HistoricalPriceData).order_by(HistoricalPriceData.id.desc()))
    datas = result.scalars().all()
    return render_template("table.html", datas=datas)


@app.route("/tracking", methods=['POST', 'GET'])
def tracking():
    result = db.session.execute(db.select(Pricedb).order_by(Pricedb.id))
    datas = result.scalars().all()
    return render_template("tracking.html", datas=datas)


def scheduled_task():
    with app.app_context():
        result = db.session.execute(db.select(Pricedb).order_by(Pricedb.id))
        data = result.scalars().all()
        for i in data:
            dataset = scrape(i.product_url)
            if clean_number_string(dataset['price']) <= i.expected_price:
                new_product = HistoricalPriceData(
                    date_time=datetime.now(),
                    product_name=dataset['name'],
                    product_url=i.product_url,
                    img_url=dataset['images'],
                    expected_price=i.expected_price,
                    price=dataset['price']
                )
                db.session.add(new_product)
                db.session.commit()
                telegram_message(
                    f"{dataset['images']}\n Amazon Price Alert: \n {i.product_name} is now selling at your expected price of "
                    f"Rs.{dataset['price']}")
                print(f'The task is running and message has been sent on {datetime.now()}')
                sleep(120)
            else:
                new_product = HistoricalPriceData(
                    date_time=datetime.now(),
                    product_name=dataset['name'],
                    product_url=i.product_url,
                    img_url=dataset['images'],
                    expected_price=i.expected_price,
                    price=dataset['price']
                )
                db.session.add(new_product)
                db.session.commit()
                print(f'The task is running {i.product_name} {datetime.now()}')
            sleep(120)


if __name__ == '__main__':
    # Create an APScheduler instance
    scheduler = BackgroundScheduler(daemon=True)
    # Add the scheduled task
    scheduler.add_job(id='Scheduled task', func=scheduled_task, trigger='interval', minutes=360)
    # Start the scheduler
    scheduler.start()
    # Start the Flask app
    app.run(debug=False)
