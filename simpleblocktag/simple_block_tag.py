from inspect import getargspec
from django.template.base import Node, parse_bits
from functools import partial


def simple_block_tag(register, takes_context=None, name=None):
    def dec(func):
        params, varargs, varkw, defaults = getargspec(func)

        class SimpleNode(Node):
            def __init__(self, nodelist, takes_context, args, kwargs):
                self.nodelist = nodelist
                self.takes_context = takes_context
                self.args = args
                self.kwargs = kwargs

            def get_resolved_arguments(self, context):
                resolved_args = [var.resolve(context) for var in self.args]
                resolved_args = [self.nodelist.render(context)] + resolved_args
                if self.takes_context:
                    resolved_args = [context] + resolved_args
                resolved_kwargs = dict((k, v.resolve(context))
                                       for k, v in self.kwargs.items())
                return resolved_args, resolved_kwargs

            def render(self, context):
                resolved_args, resolved_kwargs = self.get_resolved_arguments(context)
                return func(*resolved_args, **resolved_kwargs)

        def tag_compiler(parser, token, params, varargs, varkw, defaults,
                         name, takes_context, function_name):
            bits = token.split_contents()[1:]
            bits = [''] + bits  # add placeholder for content arg
            args, kwargs = parse_bits(parser, bits, params, varargs, varkw,
                                      defaults, takes_context, name)
            args = args[1:]  # remove content placeholder
            nodelist = parser.parse(('end{}'.format(function_name),))
            parser.delete_first_token()
            return SimpleNode(nodelist, takes_context, args, kwargs)

        function_name = (name or
                         getattr(func, '_decorated_function', func).__name__)
        compile_func = partial(tag_compiler,
                               params=params, varargs=varargs, varkw=varkw,
                               defaults=defaults, name=function_name,
                               takes_context=takes_context, function_name=function_name)
        compile_func.__doc__ = func.__doc__

        register.tag(function_name, compile_func)
        return func

    return dec
