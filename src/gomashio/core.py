import re
import shutil
from pathlib import Path
from xml.etree.ElementTree import Element, SubElement, tostring

import frontmatter
import jinja2
from markdown_it import MarkdownIt
from slugify import slugify

from .config import CONTENTS_DIR, DIST_DIR, FRONTEND_DIR, SITE_URL
from .social_link import SocialLink

md = MarkdownIt().enable("table")


def extract_description(markdown_text: str, limit: int = 160) -> str:
    paragraphs = re.split(r"\n\s*\n", markdown_text.strip())
    for raw in paragraphs:
        para = raw.strip()
        if not para:
            continue
        first_char = para[0]
        if first_char in "#`|<":
            continue
        if first_char == ">":
            para = "\n".join(line.lstrip(">").lstrip() for line in para.splitlines())
        para = re.sub(r"\[\^[^\]]+\]", "", para)
        para = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", para)
        para = re.sub(r"\[([^\]]+)\]\[[^\]]*\]", r"\1", para)
        para = re.sub(r"[*_`]", "", para)
        para = re.sub(r"\s+", " ", para).strip()
        if not para:
            continue
        if len(para) <= limit:
            return para
        truncated = para[:limit]
        last_space = truncated.rfind(" ")
        if last_space > 0:
            truncated = truncated[:last_space]
        return truncated + "…"
    return ""


class Menu:
    def __init__(self, href: str, name: str):
        self.href = href
        self.name = name


class Page:
    TEMPLATE_FILENAME = "page.html"
    MARKDOWN_DIR = "pages"
    OG_TYPE = "website"

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
            self.description_fallback = extract_description(original_markdown)

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
        fm = {**self.front_matter}
        if not fm.get("description"):
            fm["description"] = self.description_fallback
        fm["canonical_url"] = f"{SITE_URL}/{self.filename}"
        fm["og_type"] = self.OG_TYPE
        return {
            "page": {
                "content": self.content,
            },
            "front_matter": fm,
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
    OG_TYPE = "article"


class Index:
    def __init__(self, env: jinja2.Environment, dest_filename: str = "index.html"):
        self._env = env
        self.dest_filename = dest_filename

    def render(self, dest_dir: Path, data=None):
        if not data:
            data = {}

        template = self._env.get_template("index.html")
        (dest_dir / self.dest_filename).write_text(template.render(data))


class Sitemap:
    def __init__(self, dest_filename: str = "sitemap.xml"):
        self.dest_filename = dest_filename

    def render(self, dest_dir: Path, pages: list[Page], posts: list[Post]):
        urlset = Element(
            "urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        )
        home = SubElement(urlset, "url")
        SubElement(home, "loc").text = f"{SITE_URL}/"
        for item in (*posts, *pages):
            url_el = SubElement(urlset, "url")
            SubElement(url_el, "loc").text = f"{SITE_URL}/{item.filename}"
            created_at = item.front_matter.get("created_at")
            if created_at and hasattr(created_at, "date"):
                SubElement(url_el, "lastmod").text = created_at.date().isoformat()
        xml_bytes = tostring(urlset, encoding="utf-8", xml_declaration=True)
        (dest_dir / self.dest_filename).write_bytes(xml_bytes)


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
                "url": SITE_URL,
            },
            "menus": self.menus,
            "social_links": self.social_links,
        }

    def write(self):
        for p in (*self.pages, *self.posts):
            p.render(DIST_DIR, {**self.data, **p.data})
        self.index.render(DIST_DIR, {**self.data, "posts": self.posts})
        Sitemap().render(DIST_DIR, self.pages, self.posts)

    @staticmethod
    def copy_static_files():
        static_dest = DIST_DIR / "static"
        static_dest.mkdir(parents=True, exist_ok=True)
        for p in (FRONTEND_DIR / "static").glob("*"):
            (static_dest / p.name).write_bytes(p.read_bytes())
        for p in (FRONTEND_DIR / "root").glob("*"):
            if p.is_file():
                (DIST_DIR / p.name).write_bytes(p.read_bytes())

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
