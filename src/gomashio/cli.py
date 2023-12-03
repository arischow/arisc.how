#!/usr/bin/env python3
import jinja2

from .config import TEMPLATE_DIR
from .core import Index, Menu, Page, Post, Site
from .jinja2_filters import FILTERS
from .social_link import SOCIAL_LINKS


def build():
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(TEMPLATE_DIR), autoescape=True
    )
    env.filters.update(**FILTERS)

    menus = [Menu("/", "home"), Menu("/about", "about")]

    pages = Page.glob(env)
    posts = Post.glob(env)
    index = Index(env)
    site = Site(
        title="Aris Chow",
        index=index,
        pages=pages,
        posts=posts,
        menus=menus,
        social_links=SOCIAL_LINKS,
    )
    site.build()


if __name__ == "__main__":
    build()
