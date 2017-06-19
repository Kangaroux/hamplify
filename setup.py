from setuptools import setup

setup(name="hamplify",
  version="1.0",
  packages=["hamplify", "hamplify.parsers", "scripts"],
  url="https://github.com/Kangaroux/hamplify",
  license="MIT",
  install_requires=["future"],
  entry_points={
    'console_scripts': [
      'hamplify=scripts.hamplify:main',
    ],
  }
)