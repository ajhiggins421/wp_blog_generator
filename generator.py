from threading import Thread
from time import sleep

import utils
import creds


class Generator:

    def __init__(self, wp, chat_gpt):
        self.wp = wp
        self.chat_gpt = chat_gpt
        self.posts = []
        self.editing = False
        self.generating = False
        self.start()

    def auto_generate(self):
        while True:

            if self.editing:
                self.generating = False
                continue

            self.generating = True

            if len(self.posts) > 0:
                title = self.posts[0]
                try:
                    date = utils.random_date(creds.date_bound)
                    print(f"Generating blog for prompt: {title}")
                    text = self.chat_gpt.get_response(
                        f"Write the content for an article with the title: {title}. Use "
                        f"html syntax to format the blog. Do not include a title.")
                    resp = self.wp.create_post(title, text, date, status="draft")
                    if str(resp).split("[")[1][0] == "2":
                        self.posts.remove(title)
                        print("Done\n")
                    print(f"Incomplete posts: {self.posts}")
                    sleep(40)
                except Exception as e:
                    print(e)
                    sleep(40)

    def add_prompts(self, prompts):
        self.posts += prompts

    def edit(self, command, text):
        self.editing = True
        while True:
            if self.generating:
                continue
            try:
                print("Generating edit")
                resp = self.chat_gpt.get_response(f"Command: {command}. Use html to format the post. Do not include a "
                                                  f"title.\nText: {text}")
                self.editing = False
                print("Successful edit\n")
                return resp
            except Exception as e:
                print(e)
                sleep(60)
        return "Error"

    def start(self):
        thread = Thread(target=self.auto_generate, )
        thread.start()
