from threading import Thread
from wordpress import Wordpress
from chat_gpt import ChatGPT
from flask import Flask, request, render_template, redirect, url_for
from flask_ckeditor import CKEditor
from bs4 import BeautifulSoup

import utils
import creds
from utils import random_date

wp = Wordpress(creds.url, creds.user, creds.password)
chat_gpt_client = ChatGPT(creds.chat_gpt_token)

app = Flask(__name__)
ckeditor = CKEditor(app)


def auto_generate(prompts):
    for prompt in prompts:
        title = prompt
        date = random_date(creds.date_bound)
        text = chat_gpt_client.get_response(f"Write the content for an article with the title: {prompt}")
        wp.create_post(title, text, date, status="draft")


@app.route('/', methods=["GET", "POST"])
def home():
    return redirect(url_for("generate"))


@app.route('/view-posts')
def view_posts():
    posts = wp.fetch_posts()
    return render_template("posts.html", posts=posts)


@app.route('/generate', methods=["GET", "POST"])
def generate():
    if request.method == 'POST':
        data = request.form.get('ckeditor')
        soup = BeautifulSoup(data)
        data = soup.get_text("\n")
        titles = [title.strip() for title in data.split("&&")]
        thread = Thread(target=auto_generate, args=titles)
        thread.start()
        return render_template('generate.html', article_body="Posts are being generated")

    return render_template('generate.html')


@app.route('/post/', defaults={'post_id': None}, methods=["GET", "POST"])
@app.route('/post/<post_id>', methods=["GET", "POST"])
def post(post_id):
    if request.method == 'POST':
        data = request.form.get('ckeditor')
        data = BeautifulSoup(data).get_text("\n")

        text = ""
        command = ""

        if "{" in data and "}" in data:
            text += data.split("{")[0].strip()
            command += data.split("{")[1].split("}")[0].strip()
            text += " "
            text += data.split("}")[1].strip()
        else:
            text += data.strip()

        if request.form['action'] == "Generate":
            title = request.form["blog-title"]
            date = request.form["blog-date"]
            status = request.form.get("status")
            data = chat_gpt_client.get_response(f"Command: {command}\nText: {text}")
            return render_template('post.html', article_body=data, blog_title=title, blog_date=date, status=status)

        elif request.form['action'] == "Post":
            title = request.form["blog-title"]
            date = request.form["blog-date"]
            date += f'T{utils.random_time(creds.date_bound)}'
            status = request.form.get("status")
            if post_id:
                wp.update_post(title, text, post_id, date, status)
            else:
                wp.create_post(title, text, date, status)
            return render_template('post.html', article_body="Posted")

    if not post_id:
        return render_template('post.html')

    posts = wp.fetch_posts()

    for p in posts:
        if p["id"] == int(post_id):
            return render_template('post.html', article_body=p["content"], blog_title=p["title"],
                                   blog_date=p["date"].split("T")[0], status=p["status"], post_id=p["id"])


@app.route('/delete/<post_id>', methods=["GET", "POST"])
def delete(post_id):
    wp.delete_post(post_id)
    return redirect(url_for('view_posts'))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
