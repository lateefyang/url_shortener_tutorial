from fileinput import filename
import json
import os.path

from flask import (
    Flask, abort, flash, jsonify, redirect, render_template, request, session,
    url_for)
from werkzeug.utils import secure_filename


USER_FILES = (
    r'D:\Projects\Tutorials\flask_tutorial\url-shortener\static\user_files')


app = Flask(__name__)
app.secret_key = 'ajsdlkfjklmvlkawef'


@app.route('/')
def home():
    return render_template('home.html', codes=session.keys())


@app.route('/your-url', methods=['GET', 'POST'])
def your_url():
    if request.method == 'POST':
        code = request.form['code']
        try:
            with open('urls.json', 'r') as url_file:
                urls = json.load(url_file)
        except FileNotFoundError:
            urls = {}
        if code in urls.keys():
            flash('That short name has already been taken.')
            return redirect(url_for('home'))
        if 'url' in request.form.keys():
            urls[code] = {'url': request.form['url']}
        else:
            f = request.files['file']
            full_name = code + secure_filename(f.filename)
            f.save(
                os.path.join(USER_FILES, full_name))
            urls[code] = {'file': full_name}
        with open('urls.json', 'w') as url_file:
            json.dump(urls, url_file)
        session[code] = True
        return render_template('your_url.html', code=code)
    else:
        return redirect(url_for('home'))


@app.route('/<string:code>')
def redirect_to_url(code):
    try:
        with open('urls.json', 'r') as urls_file:
            urls = json.load(urls_file)
            try:
                return redirect(urls[code]['url'])
            except KeyError:
                try:
                    file_location = f'user_files/{urls[code]["file"]}'
                except KeyError:
                    return abort(404)
                return redirect(url_for('static', filename=file_location))
    except FileNotFoundError:
        flash('There are no short names stored.')
        return redirect(url_for('home'))


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404


@app.route('/api')
def session_api():
    return jsonify(list(session.keys()))
