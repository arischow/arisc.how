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
        Page(env, "index", "/", menus, title="Welcome!", content="It works."),
        Page(env, "about", "/about", menus, title="About", content="Eh. To be filled in later."),
    ]
    site = Site(title="Aris Chow", pages=pages)
    site.write()
