from django import forms
from django.utils.safestring import mark_safe

try:
    # py2.x
    from django.utils.encoding import force_unicode as force_str
except ImportError:
    # py3.x
    from django.utils.encoding import force_text as force_str
try:
    # Django >=1.7
    from django.forms.utils import flatatt
except ImportError:
    # Django <1.7
    from django.forms.util import flatatt


class MediaMixin(object):
    pass

    class Media:
        css = {'screen': ('charsleft-widget/css/charsleft.css',)}
        js = ('charsleft-widget/js/charsleft.js',)


class CharsLeftInput(forms.TextInput, MediaMixin):

    def __init__(self, attrs=None, count_threshold=0):
        super(CharsLeftInput, self).__init__(attrs=attrs)
        self.count_threshold = count_threshold

    def render(self, name, value, attrs=None):
        if value is None:
            value = ''
        extra_attrs = {'type': self.input_type, 'name': name,
                       'maxlength': self.attrs.get('maxlength'),
                       'style': self.attrs.get('style')}
        final_attrs = self.build_attrs(attrs, extra_attrs=extra_attrs)

        if value != '':
            final_attrs['value'] = force_str(self._format_value(value))
        
        maxlength = final_attrs.get('maxlength', False)
        
        if not maxlength:
            return mark_safe(u'<input%s />' % flatatt(final_attrs))
        
        maxlength = self.count_threshold or int(maxlength)
        current = force_str(maxlength - len(value))
        text_type = 'input'
        input_text = ''

        if self.input_type == 'text':
            text_type = 'textarea'
            input_text = final_attrs['value']

        html = u"""
            <span class="charsleft charsleft-input">
            <%(text_type)s %(attrs)s class="charsleft-widget">%(input_text)s</%(text_type)s>
            <span><span class="count">%(current)s</span> characters remaining</span>
            <span class="maxlength">%(maxlength)s</span>
            </span>
        """ % {
            'attrs': flatatt(final_attrs),
            'current': current,
            'maxlength': maxlength,
            'text_type': text_type,
            'input_text': input_text,
        }

        return mark_safe(html)
