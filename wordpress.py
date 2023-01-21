import requests
import base64

from bs4 import BeautifulSoup


class Wordpress:

    def __init__(self, url, user, password, ):
        self.url = url + "/wp-json/wp/v2/posts/"
        self.user = user
        self.password = password
        credentials = self.user + ':' + self.password
        token = base64.b64encode(credentials.encode())
        self.header = {'Authorization': 'Basic ' + token.decode('utf-8')}

    def fetch_posts(self):
        posts_list = []
        posts = requests.get(self.url + "?status=draft,publish&per_page=100&orderby=id",
                             headers=self.header).json()
        for post in posts:
            new_dict = {k: v for k, v in dict(post).items() if k in {'id', 'date', 'status'}}
            new_dict["title"] = dict(post)["title"]["rendered"]
            new_dict["content"] = dict(post)["content"]["rendered"]
            posts_list.append(new_dict)
        return posts_list

    def fetch_posts_no_content(self):
        posts_list = []
        posts = requests.get(self.url + "?status=draft,publish&per_page=100&orderby=id",
                             headers=self.header).json()
        for post in posts:
            new_dict = {k: v for k, v in dict(post).items() if k in {'id', 'date', 'status'}}
            new_dict["title"] = BeautifulSoup(dict(post)["title"]["rendered"]).get_text("\n")
            posts_list.append(new_dict)
        return posts_list

    def fetch_posts_full(self):
        return requests.get(self.url + "?status=draft,publish&per_page=100&orderby=id",
                            headers=self.header).json()

    def create_post(self, title, content, date, status="draft", categories=1):
        # Sample date: '2020-01-05T10:00:00'
        post = {
            'title': title,
            'status': status,
            'content': content,
            'categories': categories,  # category ID
            'date': date
        }
        return requests.post(self.url, headers=self.header, json=post)

    def update_post(self, title, content, post_id, date=None, status=None):
        post = {
            'title': title,
            'content': content
        }
        if date:
            post["date"]: date
        if status:
            post["status"]: status
        req = requests.post(self.url + str(post_id), headers=self.header, json=post)
        return req

    def delete_post(self, post_id):
        return requests.delete(self.url + str(post_id), headers=self.header)
