# -*- coding: utf-8 -*-

from os.path import dirname, join

from setuptools import setup, find_packages


with open(join(dirname(__file__), 'scraper/VERSION'), 'rb') as f:
	version = f.read().decode('ascii').strip()

setup(
	name='scraper',
	version=version,
	description='A distributed web crawling toolkit based on Scrapy and backed by Redis.',
	author='Liu Qi',
	packages=find_packages(),
	include_package_data=True,
	zip_safe=False,
	entry_points={
		'console_scripts': ['scraperd = scraperd.scripts.run:main'],
	},
	install_requires=[
		'beautifulsoup4',
		'elasticsearch',
		'html2text',
		'pymongo',
		'readability-lxml',
		'redis',
	],
)
