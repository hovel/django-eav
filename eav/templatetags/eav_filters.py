from django.template.defaultfilters import register

@register.filter(name='key')
def key(dict, index):
    """
    Custom lookup filter to allow retrieving a dictionary value or
    object value by a variable.
    
    e.g.  if var is currently set to 'bar',
     {{ foo|key:var }} would retrieve either foo['bar'] if 
     foo is a dictionary, or foo.bar otherwise.
    """
    try:
        return dict[index]
    except:
        return getattr(dict, index, '')