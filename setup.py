from setuptools import setup

setup(name="hamplify",
  version="1.0",
  author="kangaroux",
  author_email="roux.jesse@gmail.com",
  packages=["hamplify", "hamplify.parsers", "scripts"],
  url="https://github.com/Kangaroux/hamplify",
  license="MIT",
  entry_points={
    'console_scripts': [
      'hamplify=scripts.hamplify:main',
    ],
  }
)