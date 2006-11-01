"""
HTML Widget classes
"""

__all__ = ('Widget', 'TextInput', 'PasswordInput', 'HiddenInput', 'FileInput', 'Textarea', 'CheckboxInput', 'Select')

from django.utils.html import escape
from itertools import chain

# Converts a dictionary to a single string with key="value", XML-style.
# Assumes keys do not need to be XML-escaped.
flatatt = lambda attrs: ' '.join(['%s="%s"' % (k, escape(v)) for k, v in attrs.items()])

class Widget(object):
    def __init__(self, attrs=None):
        self.attrs = attrs or {}

    def render(self, name, value):
        raise NotImplementedError

class Input(Widget):
    "Base class for all <input> widgets (except type='checkbox', which is special)"
    input_type = None # Subclasses must define this.
    def render(self, name, value, attrs=None):
        if value is None: value = ''
        final_attrs = dict(self.attrs, type=self.input_type, name=name)
        if attrs:
            final_attrs.update(attrs)
        if value != '': final_attrs['value'] = value # Only add the 'value' attribute if a value is non-empty.
        return u'<input %s />' % flatatt(final_attrs)

class TextInput(Input):
    input_type = 'text'

class PasswordInput(Input):
    input_type = 'password'

class HiddenInput(Input):
    input_type = 'hidden'

class FileInput(Input):
    input_type = 'file'

class Textarea(Widget):
    def render(self, name, value, attrs=None):
        if value is None: value = ''
        final_attrs = dict(self.attrs, name=name)
        if attrs:
            final_attrs.update(attrs)
        return u'<textarea %s>%s</textarea>' % (flatatt(final_attrs), escape(value))

class CheckboxInput(Widget):
    def render(self, name, value, attrs=None):
        final_attrs = dict(self.attrs, type='checkbox', name=name)
        if attrs:
            final_attrs.update(attrs)
        if value: final_attrs['checked'] = 'checked'
        return u'<input %s />' % flatatt(final_attrs)

class Select(Widget):
    def __init__(self, attrs=None, choices=()):
        # choices can be any iterable
        self.attrs = attrs or {}
        self.choices = choices

    def render(self, name, value, attrs=None, choices=()):
        if value is None: value = ''
        final_attrs = dict(self.attrs, name=name)
        if attrs:
            final_attrs.update(attrs)
        output = [u'<select %s>' % flatatt(final_attrs)]
        str_value = str(value) # Normalize to string.
        for option_value, option_label,  in chain(self.choices, choices):
            selected_html = (str(option_value) == str_value) and ' selected="selected"' or ''
            output.append(u'<option value="%s"%s>%s</option>' % (escape(option_value), selected_html, escape(option_label)))
        output.append(u'</select>')
        return u'\n'.join(output)

class SelectMultiple(Widget):
    pass

class RadioSelect(Widget):
    pass

class CheckboxSelectMultiple(Widget):
    pass
