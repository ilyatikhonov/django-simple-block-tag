

=======================
Django Simple Block Tag
=======================

Analogue for simple_tag django decorator for making block (paired) template tags.

Works like `django.template.Library.simple_tag() <https://docs.djangoproject.com/en/dev/howto/custom-template-tags/#django.template.Library.simple_tag>`_ and based on its code. One different is first argument, that takes all content between {% tagname %} and {% endtagname %}


Installation
============
::

    pip install django-simple-block-tag


Usage
=====

templatetags.py
---------------
::

    from simpleblocktag import simple_block_tag
    from django import template

    register = template.Library()


    @simple_block_tag(register)
    def mytag(content, attr1, attr2=None):
        return "{}{}{}".format(attr1, content, attr2)


    @simple_block_tag(register, takes_context=True)
    def save_as(context, content, var_name):
        context[var_name] = content
        return ""

template.html
-------------
::

    {% load templatetags %}

    {% save_as "var_name" %}Some Content{% endsave_as %}
    {% mytag "foo" "bar" %} {{ var_name|lower }} {% endmytag %}


Output
------
::

    foo some content bar