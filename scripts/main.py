#!/usr/bin/env python3
import jinja2

from config import TEMPLATE_DIR
from core import Page, Menu, Site

if __name__ == '__main__':
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATE_DIR),
                             autoescape=True)

    menus = [
        Menu("weblog", "/"),
        Menu("about", "/about"),
    ]
    pages = [
        Page(env, menus, title="Welcome!", content_filename="index.md"),
        Page(env, menus, title="About", content_filename="about.md"),
    ]
    site = Site(title="Aris Chow", pages=pages)
    site.write()
