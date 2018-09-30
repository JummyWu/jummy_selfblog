# coding:utf-8
from setuptools import setup, find_packages


packages = find_packages('selfblog')
print(packages)

setup(
    name='selfblog',
    version='0.0.0',
    decription='Blog System base on Django',
    author='jummy',
    author_email='929440925@qq.com',
    url='https://www.jummy.top',
    packages=packages,
    package_dir={'': 'selfblog'},
    include_packeage_data=True,
    install_requires=[
        'django==2.0.6',
        'python-decouple==3.1',
        'markdown==2.6.11',
        'django-haystack==2.8.1',
        'jieba==0.39',
        'Whoosh==2.7.4',
        'redis==2.10.6',
        'hiredis==0.2.0',
        'django-redis==4.9.0',
        'Pillow==5.2.0',
        'python-decouple==3.1',
        'requests==2.19.1',
        'gunicorn==19.7.1',
    ],
    scripts=[
        'selfblog/manage.py',
    ],
)
