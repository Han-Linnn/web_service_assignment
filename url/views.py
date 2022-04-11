import string
from random import choices
import re

from flask import render_template, request, redirect, url_for, make_response, flash
from app import app, db
# from url.forms import UrlForm
from url.models import Url


# from settings import STATIC_DIR


@app.before_first_request
def create_tables():
    db.create_all()


def shorten_url():
    # get all letter and digits
    chars = string.ascii_letters + string.digits
    while True:
        rand_chars = choices(chars, k=3)
        rand_chars = "".join(rand_chars)
        short_url = Url.query.filter_by(short=rand_chars).first()
        if not short_url:
            return rand_chars


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url_received = request.form["oldURL"]
        if url_received:
            if not re.match(r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', url_received):
                # print("URL is valid, allow to be shortened.")
                flash("URL is invalid! Please try again")
                return render_template("index.html")

            # Check if URL already exists in DB
            found_url = Url.query.filter_by(long=url_received).first()
            if found_url:
                # Return short url if found
                return redirect(url_for("display_short_url", url=found_url.short))
            else:
                short_url = shorten_url()
                new_url = Url(url_received, short_url)
                db.session.add(new_url)
                db.session.commit()
                return redirect(url_for("display_short_url", url=short_url))
        else:
            flash("Please enter URL")
            return render_template("index.html")
    else:
        return render_template('index.html')


# display the short url that just generated
@app.route('/redirect/<url>')
def display_short_url(url):
    check_url = Url.query.filter_by(short=url).first()
    host_number = request.host
    if check_url:
        response = make_response(render_template('success.html', short_url=url, host_number=host_number), 301)
        response.headers['value'] = check_url.short
        return response
    else:
        return render_template('404.html'), 404


# use short url redirect to long url
@app.route('/<short_url>')
def redirect_to_old(short_url):
    long_url = Url.query.filter_by(short=short_url).first()
    if long_url:
        return redirect(long_url.long)
    else:
        return render_template('404.html'), 404


@app.route('/update_url/<short_url>', methods=['POST'])
def get_update_data(short_url):
    if request.method == 'POST':
        form = request.form
        new_url = form.get('new_url')
        return redirect(url_for("update", new_url=new_url, short_url=short_url)), 200
    else:
        flash("Updated Error 1 !")
        return redirect(url_for("stats"))


@app.route('/update/<new_url>/<short_url>', methods=['PUT'])
def update(new_url, short_url):
    if new_url and short_url:
        urls = Url.query.filter_by(short=short_url).first()
        urls.short = str(new_url)
        db.session.commit()
        flash("Successfully Updated !")
        return redirect(url_for("stats"))
    else:
        flash("Updated Error 2 !")
        return redirect(url_for("stats"))


@app.route('/deleteSingle/<short_url>', methods=['DELETE'])
def delete_single_url(short_url):
    x = Url.query.filter_by(short=short_url).first()
    if x:
        db.session.delete(x)
        db.session.commit()
        return redirect(url_for("stats"))
    else:
        return render_template('400.html'), 400


@app.route('/deleteAll')
def delete_all_url():
    check_empty = db.session.query(Url).first()
    if check_empty:
        db.session.query(Url).filter().delete()
        db.session.commit()
        flash("Successfully Clear All !")
        return redirect(url_for("index"))
    else:
        flash("No data in DataBase !")
        return redirect(url_for("index"))


@app.route("/stats")
@app.route("/stats/<int:page>")
def stats(page=1):
    data_list = Url.query.order_by(Url.id.desc()).paginate(page, 5, False)
    return render_template("stats.html", stats=data_list), 200


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(400)
def response_error(e):
    return render_template("400.html", message='ERROR'), 400
