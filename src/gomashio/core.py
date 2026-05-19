import shutil
from pathlib import Path

import frontmatter
import jinja2
from markdown_it import MarkdownIt
from slugify import slugify

from .config import CONTENTS_DIR, DIST_DIR, FRONTEND_DIR
from .social_link import SocialLink

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
        with open(CONTENTS_DIR / self.MARKDOWN_DIR / self.content_filename, "r") as f:
            self.front_matter, original_markdown = frontmatter.parse(f.read())
            self.content = md.render(original_markdown)

    def __str__(self):
        return f"<{self.__class__.__name__}: {self.filename}>"

    @property
    def filename(self):
        return (
            self.dest_filename
            or slugify(self.front_matter.get("slug", ""))
            or Path(self.content_filename).stem
        )

    @classmethod
    def glob(cls, env: jinja2.Environment) -> list["Page"]:
        return [
            cls(env, content_filename=str(filename))
            for filename in (CONTENTS_DIR / cls.MARKDOWN_DIR).glob("*.md")
        ]

    @property
    def data(self):
        return {
            "page": {
                "content": self.content,
            },
            "front_matter": {**self.front_matter},
        }

    def render(self, dest_dir: Path, data=None):
        if not data:
            data = self.data

        template = self._env.get_template(self.TEMPLATE_FILENAME)
        out_dir = dest_dir / self.filename
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "index.html").write_text(template.render(data))


class Post(Page):
    TEMPLATE_FILENAME = "post.html"
    MARKDOWN_DIR = "posts"


class Index:
    def __init__(self, env: jinja2.Environment, dest_filename: str = "index.html"):
        self._env = env
        self.dest_filename = dest_filename

    def render(self, dest_dir: Path, data=None):
        if not data:
            data = {}

        template = self._env.get_template("index.html")
        (dest_dir / self.dest_filename).write_text(template.render(data))


class Site:
    def __init__(
        self,
        title: str,
        index: Index,
        pages: list[Page],
        posts: list[Post],
        menus: list[Menu],
        social_links: list[SocialLink],
    ):
        self.title = title
        self.index = index
        self.pages = pages
        self.posts = posts
        self.menus = menus
        self.social_links = social_links

    @property
    def data(self):
        return {
            "site": {
                "title": self.title,
                "description": "Someone who owns yet another blog.",
            },
            "menus": self.menus,
            "social_links": self.social_links,
        }

    def write(self):
        for p in (*self.pages, *self.posts):
            p.render(DIST_DIR, {**self.data, **p.data})
        self.index.render(DIST_DIR, {**self.data, "posts": self.posts})

    @staticmethod
    def copy_static_files():
        static_dest = DIST_DIR / "static"
        static_dest.mkdir(parents=True, exist_ok=True)
        for p in (FRONTEND_DIR / "static").glob("*"):
            (static_dest / p.name).write_bytes(p.read_bytes())

    @staticmethod
    def cleanup():
        # Preserve dist/static/ so Tailwind's output.css (built before Python)
        # survives. Removing everything else clears stale post/page directories.
        if not DIST_DIR.exists():
            return
        for p in DIST_DIR.iterdir():
            if p.name == "static":
                continue
            if p.is_dir():
                shutil.rmtree(p)
            else:
                p.unlink()

    def build(self):
        self.cleanup()
        self.copy_static_files()
        self.write()
