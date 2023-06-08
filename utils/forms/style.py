def add_placeholder(field, placeholder):
    f = field.widget.attrs['placeholder'] = placeholder
    return f


def add_css_class(field, class_name):
    f = field.widget.attrs['class'] = class_name
    return f
