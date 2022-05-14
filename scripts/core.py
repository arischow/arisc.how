import os
import pathlib

import jinja2
from markdown_it import MarkdownIt
from mdit_py_plugins.front_matter import front_matter_plugin

from config import SRC_DIR, DIST_DIR

md = MarkdownIt().use(front_matter_plugin)


class Menu:
    def __init__(self, name: str, link: str):
        self.name = name
        self.link = link


class Page:
    TEMPLATE_FILENAME = "page.jinja2"
    MARKDOWN_DIR = "pages"

    def __init__(self, env: "jinja2.Environment", menus: list[Menu],
                 title=None, content_filename=None, dest_filename=None):
        self._env = env
        self.title = title
        self.dest_filename = dest_filename
        self.menus = menus
        self.content_filename = content_filename
        with open(os.path.join(SRC_DIR, self.MARKDOWN_DIR, content_filename)) as f:
            self.content = md.render(f.read())

    @property
    def data(self):
        return {
            "menus": self.menus,
            "page": {
                "title": self.title,
                "content": self.content,
            }
        }

    def render(self, data=None):
        if not data:
            data = self.data

        template = self._env.get_template(self.TEMPLATE_FILENAME)
        dest_filename = self.dest_filename or f"{pathlib.Path(self.content_filename).stem}.html"
        with open(os.path.join(DIST_DIR, dest_filename), "w") as f:
            f.write(template.render(data))


class Site:
    def __init__(self, title, pages: list["Page"]):
        self.title = title
        self.pages = pages

    @property
    def data(self):
        return {
            "site": {
                "title": self.title,
            }
        }

    def write(self):
        for p in self.pages:
            p.render({**self.data, **p.data})
