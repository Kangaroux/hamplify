[![Build Status](https://travis-ci.org/Kangaroux/hamplify.svg?branch=master)](https://travis-ci.org/Kangaroux/hamplify)
[![Coverage Status](https://coveralls.io/repos/github/Kangaroux/hamplify/badge.svg?branch=master)](https://coveralls.io/github/Kangaroux/hamplify?branch=master)
[![PyPI version](https://badge.fury.io/py/hamplify.svg)](https://badge.fury.io/py/hamplify)

# hamplify
`hamplify` is a lightweight [HAML-ish](http://haml.info/) parser written in Python.

Here are some reasons to use `hamplify`:

- **Template Support**: Included support for Django and Jinja2 templates
- **Compatibility**: Works with Python 2.7 and 3.3+
- **Lightweight**: Requires no dependencies and is framework agnostic
- **Smaller Templates**: Excess whitespace from templates is automatically removed
- **Painless**: Integrates seamlessly into existing projects

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