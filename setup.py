from setuptools import setup, find_packages

setup(name="wqa",
      version="0.0.1",
      description="Wikipedia Question Answer",
      url="http://github.com/giwiro/wqa",
      author="Gi Wah Davalos Loo",
      author_email="giwirodavalos@gmail.com",
      license="MIT",
      packages=find_packages(),
      install_requires=["numpy", "pymongo", "tqdm"])
