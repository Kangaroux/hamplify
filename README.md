[![Build Status](https://travis-ci.org/Kangaroux/hamplify.svg?branch=master)](https://travis-ci.org/Kangaroux/hamplify)
[![Coverage Status](https://coveralls.io/repos/github/Kangaroux/hamplify/badge.svg?branch=master)](https://coveralls.io/github/Kangaroux/hamplify?branch=master)
[![PyPI version](https://badge.fury.io/py/hamplify.svg)](https://badge.fury.io/py/hamplify)

# hamplify
`hamplify` is a lightweight [HAML-ish](http://haml.info/) compiler written in Python.

Here are some reasons to use `hamplify`:

- Compatible with Python 2.7 and 3.3+
- Requires **NO** dependencies and is framework agnostic
- Support for Django and Jinja2 templates
- Templates are automatically minified
- Integrates seamlessly into existing projects

## Using hamplify

Install `hamplify` with pip:
```
pip install hamplify
```

Use the `hamplify` command to compile your templates:
```
hamplify <input-dir> <output-dir> [--watch]
```

## Running Tests
Install the test dependencies 
```
pip install -r reqs/test.txt
```

Run the tests 
```
pytest --cov=hamplify
```

## Syntax Sample
```HAML
!!!
%html
  %head
    %title
      - block title
        My Site

    %link(rel="stylesheet" href="style.css")

    :css
      p {
        background-color: #CCC;
      }

  %body
    -# This is an HTML comment
    / This is another comment, 
      but it won't be rendered

    .container
      %p A paragraph with some text.
      %button.btn#my-button A button

      %a(href='#')= the_link|some_filter

      :plain
        This is a plaintext block. The compiler will not parse anything in here.

    :javascript
      console.log("Hello, world!");
```