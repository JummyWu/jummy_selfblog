# coding:utf-8
from setuptools import setup, find_packages


packages = find_packages('selfblog')
print(packages)

setup(
    name='Jummy blog',
    version='0.0.0',
    decription='Blog System base on Django',
    author='jummy',
    author_email='929440925@qq.com',
    url='https://www.jummy.top',
    packages=packages,
    package_dir={'': 'selfblog'},
    include_packeage_data=True,
    install_requires=[
        'django==1.11.10',
        'python-decouple==3.1',
        'markdown==2.6.11',
    ],
    scripts=[
        'selfblog/manage.py',
    ],
)
