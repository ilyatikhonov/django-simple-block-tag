from distutils.core import setup

setup(
    name='django-simple-block-tag',
    version='0.1.2',
    author='Ilya Tikhonov',
    description='Block tag decorator for Django templates',
    long_description=open('README.rst').read(),
    license='LICENSE.txt',
    keywords='template, tag, django',
    classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Framework :: Django",
        "Environment :: Web Environment",
    ],
    author_email='ili.tikhonov@gmai.com',
    url='https://github.com/piha/django-simple-block-tag/',
    packages=['simpleblocktag'],
    install_requires=[
        "Django >= 1.4.0",
    ],
)
