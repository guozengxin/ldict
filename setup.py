#!/usr/bin/env python

# author: guozengxin
# email: guozengxin@outlook.com


from setuptools import setup, find_packages

setup(name='ldict',
      version='1.0.0',
      description='A light-weighted English-Chinese dict in Unix/Linux; depend python and urllib2',
      author='guozengxin',
      author_email='guozengxin@outlook.com',
      packages=find_packages(),
      scripts=['ldict.py'],
      platforms="Linux",
      )
