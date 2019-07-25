# from django import template
# from django.template.defaultfilters import stringfilter
#
# register = template.Library()
#
# # only accepts strings as the input value (cuz of "stringfilter")
# @stringfilter
# def lower(value):
#     return value.lower()
#
# # applying the filter with the name "lower" to be used in the templates as a filter
# # This flag tells Django that if a “safe” string is passed into your filter,
# # the result will still be “safe” and if a non-safe string is passed in,
#  # Django will automatically escape it, if necessary. (escape is pretty much the "\" sign
#  # wheather it's "\n" or "\t" tec.)
# register.filter("lower", lower, is_safe=False)
#
#
# # for datetime values
# @register.filter(expects_localtime=True, name="businesshours")
# def businesshours(value):
#     try:
#         return 9 <= value.hour < 17
#     except AttributeError:
#         return ''
#
#
# # this is creating a custom tag
# @register.simple_tag
# def current_time(format_string):
#     return datetime.datetime.now().strftime(format_string)
#
#
# # takes python arguments given in template as a tag, example: {{timezone}}
# @register.simple_tag(takes_context=True)
# def current_time(context, format_string):
#     timezone = context['timezone']
#     return your_get_current_time_method(timezone, format_string)
