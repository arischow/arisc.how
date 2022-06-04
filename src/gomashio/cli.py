#!/usr/bin/env python3
import jinja2

from .config import TEMPLATE_DIR
from .core import Index, Menu, Page, Post, Site
from .social_link import github, linkedin


def build():
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(TEMPLATE_DIR), autoescape=True
    )

    menus = [Menu("/", "home"), Menu("/about", "about"), Menu("/contact", "contact")]

    social_links = [
        github,
        linkedin,
    ]
    pages = Page.glob(env)
    posts = Post.glob(env)
    index = Index(env)
    site = Site(
        title="Aris Chow",
        index=index,
        pages=pages,
        posts=posts,
        menus=menus,
        social_links=social_links,
    )
    site.build()


if __name__ == "__main__":
    build()
