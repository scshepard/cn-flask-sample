"""
Flask Blueprint Docs:  http://flask.pocoo.org/docs/api/#flask.Blueprint

This file is used for both the routing and logic of your
application.
"""
import json
from flask import Blueprint, render_template, request, redirect, url_for, session
from forms import SignInForm
import requests

views = Blueprint('views', __name__, static_folder='../static',
                  template_folder='../templates')


@views.route('/', methods=['GET', 'POST'])
def home():
    """Render website's home page."""
    form = SignInForm(request.form)
    if request.method == 'POST':
        # Pass this to the Consumer Notebook API
        session['username'] = request.form['username']
        session['api_key'] = request.form['api_key']
        return redirect('/products/')
    return render_template('home.html', form=form)

@views.route('/products/')
def products():
    """Display the specified user's products."""
    username = session['username']
    api_key = session['api_key']
    url = 'https://consumernotebook.com/api/v1/products/?username={0}&apikey={1}'.format(username, api_key)
    r = requests.get(url)
    products = []
    if r.status_code != 200:
        error = "{0} error. Are you sure you entered a valid API key?".format(r.status_code)
        return render_template('products.html', error=error)
    else:
        products_json = json.loads(r.content)
        for product in products_json[u'objects']:
            products.append(product[u'title'])
        return render_template('products.html', products=products)

@views.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html')


# The functions below should be applicable to all Flask apps.

@views.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return views.send_static_file(file_dot_text)


@views.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=600'
    return response


@views.app_errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


@views.route('/oauth/')
def about():
    """Render the website's about page."""
    return render_template('oauth.html')