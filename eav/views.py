from haystack.views import SearchView
from .models import Attribute

class EAVSearchView(SearchView):
    model = None
    
    def __init__(self, *args, **kwargs):
        self.model = kwargs.pop('model')
        super(EAVSearchView, self).__init__(*args, **kwargs)
    
    def extra_context(self):
        """
        Provides extra context to the template.
        Specifically, all of the EAV fields that could
        apply to this model.
        """
        if self.model:
            attributes = Attribute.get_for_model(self.model)
        else:
            attributes = Attribute.objects.all()

        org_extra_context = super(EAVSearchView, self).extra_context()
        org_extra_context.update({'eav_attributes': attributes})
        return org_extra_context