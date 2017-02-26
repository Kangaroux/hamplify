from setuptools import setup

setup(name="hamplify",
  version="0.1",
  packages=["hamplify"],
  url="https://github.com/Kangaroux/hamplify",
  license="MIT",
  install_requires=["future"],
  entry_points={
    'console_scripts': [
      'hamplify=scripts.hamplify:main',
    ],
  }
)