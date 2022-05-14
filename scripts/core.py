import os
import pathlib

import jinja2

from config import DIST_DIR


class Menu:
    def __init__(self, name: str, link: str):
        self.name = name
        self.link = link


class Page:
    TEMPLATE_FILENAME = "page.jinja2"

    def __init__(self, env: "jinja2.Environment", name, slug, menus: list[Menu],
                 title=None, content=None, dest_filename=None):
        self._env = env
        self.name = name
        self.slug = slug
        if not title:
            self.title = self.name
        else:
            self.title = title
        self.dest_filename = dest_filename
        self.menus = menus
        self.content = content

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
        dest_filename = self.dest_filename or f"{self.name}.html"
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
