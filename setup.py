from setuptools import setup, find_packages

print(find_packages())

setup(name="hamplify",
  version="0.1",
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