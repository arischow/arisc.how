---
title: Documenting Using Docstrings
created_at: 2022-10-15T12:32:45.000Z
slug: /documenting-using-docstrings
---

## What is a Docstring?

> A docstring is a string literal that occurs as the first statement in a module, function, class, or method definition.  Such a docstring becomes the `__doc__` special attribute of that object.

```python
def hello():
    """
    I am the docstring of this function!
    """
    print("Hello World!")
```

and if we run:

```python
print(hello.__doc__)
```

we can get the string we wrote down in the function:

```
I am the docstring of this function!
```

[PEP 257][^1] documents some semantics and conventions about docstrings - it could be a one-liner:

```python
def welcome():
    """Print a welcome text."""
    print("Welcome, MOAT devs!")
```

or a multi-line docstring:

```python
def add(a, b):
    """
    Add two numbers and return the result.
    """
    return a + b
```

## How to Write Proper Docstrings?

There are different kinds of docstring styles popular in the Python community:

- [reStructuredText](https://docutils.sourceforge.io/rst.html) (also see [PEP 287][^2])
- [Google docstrings](https://github.com/google/styleguide/blob/gh-pages/pyguide.md#38-comments-and-docstrings)
- [NumPy/Scipy docstrings](https://numpydoc.readthedocs.io/en/latest/format.html)

If you skim through the articles above, you can find that they all have flavour semantics and syntax. Which one should we follow?  We can refer to some popular Python projects:

- CPython

  > The markup used for the Python documentation is [reStructuredText](https://docutils.sourceforge.io/rst.html), developed by the [docutils](https://docutils.sourceforge.io/) project, amended by custom directives and using a toolset named [Sphinx](https://www.sphinx-doc.org/) to post-process the HTML output.[^3]

- Django

  > In docstrings, follow the style of existing docstrings and [PEP 257][^1].[^4]

  > To get started contributing, you’ll want to read the [reStructuredText reference](https://www.sphinx-doc.org/en/master/usage/restructuredtext/index.html#rst-index).[^5]

- Flask

  > Add an entry in `CHANGES.rst`. Use the same style as other entries. Also include `.. versionchanged::` inline changelogs in relevant docstrings.[^6]

  Note: `.rst` is the extension of reStructuredText.

It should be noticed that there are lots of Python projects using reStructuredText for their documentation. It's like Markdown, but more optimised for writing documentation. It will be a good start if you are unsure which one to choose.

If you do not want to pick any style guidelines, at least you should follow [PEP 257][^1]. However, the style is only one part of the documentation - you should also try your best to get your text as **correct, concise and understandable** as possible.

A good example format of docstring from Google Style Guidelines[^7]:

```
"""A one line summary of the module or program, terminated by a period.

Leave one blank line.  The rest of this docstring should contain an
overall description of the module or program.  Optionally, it may also
contain a brief description of exported classes and functions and/or usage
examples.

  Typical usage example:

  foo = ClassFoo()
  bar = foo.FunctionBar()
"""
```

A good example of docstring - with the parameter name, return value, and what kind of exceptions it possibly raises:

```python
def square_root(n):
    """Calculate the square root of a number.

    Args:
        n: the number to get the square root of.
    Returns:
        the square root of n.
    Raises:
        TypeError: if n is not a number.
        ValueError: if n is negative.

    """
    pass
```

## Docstrings versus Comments

They are not interchangeable. As we mentioned in the beginning, docstrings describe modules, classes and functions, whereas comments (i.e. begin with a hash (`#`)) clarify the code and it's more like the note of a developer to him/herself or others.

Therefore, do not use triple-quote strings to comment code.

## `doctest`

[`doctest`](https://docs.python.org/3/library/doctest.html) is a module of Python standard library. You can write examples in the docstrings of functions, classes or modules and run `doctest.testmod()` to have them executed and verified:

```python
def add(a, b):
    """
    Add two numbers and return the result.

    Args:
    		a: one of the numbers to be added.
    		b: one of the numbers to be added.
    Returns:
        the result of a plus b.

    >>> add(1, 2)
    3
    """
    return a + b
```

and then we save the file as `add.py` and execute it with the `-v` switch to display everything, including passing examples:

```
> python add.py -v

Trying:
    add(1, 2)
Expecting:
    3
ok
1 items had no tests:
    __main__
1 items passed all tests:
   1 tests in __main__.add
1 tests in 2 items.
1 passed and 0 failed.
Test passed.
```

If we change `3` to `4` in the docstring and let it fail deliberately:

```
> python add.py

**********************************************************************
File "./test_sentry.py", line 13, in __main__.add
Failed example:
    add(1, 2)
Expected:
    4
Got:
    3
**********************************************************************
1 items had failures:
   1 of   1 in __main__.add
***Test Failed*** 1 failures.
```

The `doctest` module is really useful for testing code quickly and easily by specifying input and the correct output in the docstrings. Also, [it could be easily integrated with pytest](https://docs.pytest.org/en/latest/how-to/doctest.html) by adding a flag called `--doctest-modules` if the doctest examples are in the code:

```
pytest --doctest-modules
```

We can integrate doctest with the good docstring example above:

```python
import math


def square_root(n):
    """Calculate the square root of a number.

    Args:
        n: the number to get the square root of.
    Returns:
        the square root of n.
    Raises:
        TypeError: if n is not a number.
        ValueError: if n is negative.

    >>> square_root("not a number")
    Traceback (most recent call last):
        ...
    TypeError: n is not a number
    >>> square_root(-1)
    Traceback (most recent call last):
        ...
    ValueError: n is negative
    >>> square_root(4)
    2.0
    >>> square_root(9)
    3.0
    >>> square_root(27)
    5.196152422706632

    """
    if not (isinstance(n, int) or isinstance(n, float)):
        raise TypeError("n is not a number")

    if n < 0:
        raise ValueError("n is negative")

    return math.sqrt(n)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
```

And then we can run:

```
> python square_root.py -v

Trying:
    square_root("not a number")
Expecting:
    Traceback (most recent call last):
        ...
    TypeError: n is not a number
ok
Trying:
    square_root(-1)
Expecting:
    Traceback (most recent call last):
        ...
    ValueError: n is negative
ok
Trying:
    square_root(4)
Expecting:
    2.0
ok
Trying:
    square_root(9)
Expecting:
    3.0
ok
Trying:
    math.sqrt(27)
Expecting:
    5.196152422706632
ok
1 items had no tests:
    __main__
1 items passed all tests:
   5 tests in __main__.square_root
5 tests in 2 items.
5 passed and 0 failed.
Test passed.
```

It will be a good way to check if docstrings in the code are up-to-date by verifying these interactive examples still work as documented. And it has much more readability than unit tests as it will be the part to describe how functions work in the docstrings. It is not mandatory; however, we should consider using it depending on our project layout to improve the quality of our code.

## Key Takeaways

- Docstrings are to describe a module, function, class or method - it will be stored in the `__doc__` attribute and become a part of the object.
- Use triple-quote strings as docstrings to document code.
- There are some popular docstring guidelines. If a style is already applied to your code, follow the convention. If you don't know which to choose, try reStructureText or just follow [PEP 257][^1].
- Docstrings are useful in improving the readability of code. You can also consider adding some `doctest` interactive examples to have further improvements.

[^1]: https://peps.python.org/pep-0257/
[^2]: https://peps.python.org/pep-0287/
[^3]: https://devguide.python.org/documentation/start-documenting/#getting-started
[^4]: https://docs.djangoproject.com/en/dev/internals/contributing/writing-code/coding-style/
[^5]: https://docs.djangoproject.com/en/dev/internals/contributing/writing-documentation/#getting-started-with-sphinx
[^6]: https://flask.palletsprojects.com/en/2.2.x/contributing/?highlight=docstring#submitting-patches
[^7]: https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings
[^8]: https://docs.python.org/3/library/doctest.html
