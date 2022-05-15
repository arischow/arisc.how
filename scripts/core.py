from pathlib import Path

import frontmatter
import jinja2
from config import DIST_DIR, SRC_DIR
from markdown_it import MarkdownIt

md = MarkdownIt()


class Menu:
    def __init__(self, name: str, link: str):
        self.name = name
        self.link = link


class Page:
    TEMPLATE_FILENAME = "page.jinja2"
    MARKDOWN_DIR = "pages"

    def __init__(
        self,
        env: "jinja2.Environment",
        menus: list[Menu],
        content_filename=None,
        dest_filename=None,
    ):
        self._env = env
        self.dest_filename = dest_filename
        self.menus = menus
        self.content_filename = content_filename
        with open(
            Path.joinpath(SRC_DIR, self.MARKDOWN_DIR, self.content_filename), "r"
        ) as f:
            self.front_matter, original_markdown = frontmatter.parse(f.read())
            self.content = md.render(original_markdown)

    @classmethod
    def glob(cls, env: "jinja2.Environment", menus: list[Menu]):
        for filename in Path.joinpath(SRC_DIR, cls.MARKDOWN_DIR).glob("*.md"):
            yield cls(env, menus, content_filename=str(filename))

    @property
    def data(self):
        return {
            "menus": self.menus,
            "page": {
                "content": self.content,
            },
            "front_matter": {**self.front_matter},
        }

    def render(self, data=None):
        if not data:
            data = self.data

        template = self._env.get_template(self.TEMPLATE_FILENAME)
        dest_filename = self.dest_filename or f"{Path(self.content_filename).stem}.html"
        Path.joinpath(DIST_DIR, dest_filename).write_text(template.render(data))


class Post(Page):
    TEMPLATE_FILENAME = "post.jinja2"
    MARKDOWN_DIR = "posts"

    def __init__(
        self,
        env: "jinja2.Environment",
        menus: list[Menu],
        content_filename=None,
        dest_filename=None,
    ):
        super().__init__(env, menus, content_filename, dest_filename)


class Site:
    def __init__(self, title, pages: list["Page"] = None, posts: list["Post"] = None):
        self.title = title
        self.pages = pages
        self.posts = posts

    @property
    def data(self):
        return {
            "site": {
                "title": self.title,
            }
        }

    def write(self):
        for p in [*self.pages, *self.posts]:
            p.render({**self.data, **p.data})
