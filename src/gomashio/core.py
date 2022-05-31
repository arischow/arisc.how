import os
from pathlib import Path

import frontmatter
import jinja2
from markdown_it import MarkdownIt

from .config import CONTENTS_DIR, DIST_DIR, FRONTEND_DIR

md = MarkdownIt()


class Menu:
    def __init__(self, href: str, name: str):
        self.href = href
        self.name = name


class Page:
    TEMPLATE_FILENAME = "page.html"
    MARKDOWN_DIR = "pages"

    def __init__(
        self,
        env: jinja2.Environment,
        content_filename=None,
        dest_filename=None,
    ):
        self._env = env
        self.dest_filename = dest_filename
        self.content_filename = content_filename
        with open(
            Path.joinpath(CONTENTS_DIR, self.MARKDOWN_DIR, self.content_filename), "r"
        ) as f:
            self.front_matter, original_markdown = frontmatter.parse(f.read())
            self.content = md.render(original_markdown)

    @classmethod
    def glob(cls, env: jinja2.Environment):
        for filename in Path.joinpath(CONTENTS_DIR, cls.MARKDOWN_DIR).glob("*.md"):
            yield cls(env, content_filename=str(filename))

    @property
    def data(self):
        return {
            "page": {
                "content": self.content,
            },
            "front_matter": {**self.front_matter},
        }

    def render(self, dest_dir, data=None):
        if not data:
            data = self.data

        template = self._env.get_template(self.TEMPLATE_FILENAME)
        dest_filename = self.dest_filename or f"{Path(self.content_filename).stem}.html"
        Path.joinpath(dest_dir, dest_filename).write_text(template.render(data))


class Post(Page):
    TEMPLATE_FILENAME = "post.html"
    MARKDOWN_DIR = "posts"

    def __init__(
        self,
        env: jinja2.Environment,
        content_filename=None,
        dest_filename=None,
    ):
        super().__init__(env, content_filename, dest_filename)


class Site:
    def __init__(
        self, title, pages: list[Page] = None, posts: list[Post] = None, **kwargs
    ):
        self.title = title
        self.pages = pages
        self.posts = posts
        for k, v in kwargs.items():
            setattr(self, k, v)

    @property
    def data(self):
        return {
            "site": {
                "title": self.title,
                "description": "Focusing with my kitten Loki.",
            },
            # TODO: kwargs with fixed values from instance? code smell
            "menus": self.menus,
            "social_links": self.social_links,
        }

    def write(self):
        for p in [*self.pages, *self.posts]:
            p.render(DIST_DIR, {**self.data, **p.data})

    @staticmethod
    def copy_static_files():
        for p in Path(FRONTEND_DIR).glob("static/*"):
            Path.joinpath(DIST_DIR, "static").mkdir(parents=True, exist_ok=True)
            Path.joinpath(DIST_DIR, "static", p.name).write_bytes(p.read_bytes())

    @staticmethod
    def cleanup():
        for p in Path(DIST_DIR).glob("*"):
            if p.is_file():
                os.remove(str(p))

    def build(self):
        self.cleanup()
        self.copy_static_files()
        self.write()
