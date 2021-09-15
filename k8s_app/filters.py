from django.template.defaultfilters import register


# All Custom filters used in Django Template added here
@register.filter(name='unpack_data')
def unpack_data(element):
    for item in element:
        return item


@register.filter(name='items')
def items(element):
    return element.items()


@register.filter(name='zipping')
def zipping(first_item, second_item):
    return zip(first_item, second_item)
