#!/usr/bin/env python3
import jinja2
from config import TEMPLATE_DIR
from core import Menu, Page, Post, Site

if __name__ == "__main__":
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(TEMPLATE_DIR), autoescape=True
    )

    menus = [
        Menu("weblog", "/"),
        Menu("about", "/about"),
    ]
    pages = Page.glob(env, menus)
    posts = Post.glob(env, menus)
    site = Site(title="Aris Chow", pages=pages, posts=posts)
    site.build()
