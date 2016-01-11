"""
Custom haystack search index for indexing models with eav data.
"""

from haystack import indexes
from eav.models import Attribute

class EAVIndex(indexes.ModelSearchIndex):
    attribute_class = Attribute #this can be overridden

    def get_fields(self, *args, **kwargs):
        """
        Adds the eav fields to the fields to be indexed by haystack.
        """
        model = self.get_model()
        final_fields = super(EAVIndex, self).get_fields(*args, **kwargs)
        if not model:
            return final_fields
        excludes = kwargs.get('excludes')

        attribute_class = self.attribute_class or Attribute
        model_attributes = attribute_class.get_for_model(model)
        searchable_attributes = model_attributes.filter(searchable=True)

        for attr in searchable_attributes:
            if attr.slug in self.fields:
                continue
            if excludes and attr.slug in excludes:
                continue

            index_field_class = index_field_from_eav_field(attr)
            field_kwargs = self.extra_field_kwargs
            field_kwargs.update({'model_attr': attr.slug, 'null':True})
            final_fields[attr.slug] = index_field_class(**field_kwargs)
            final_fields[attr.slug].set_instance_name(attr.slug)
            final_fields[attr.slug].eav = True
        return final_fields

    def full_prepare(self, obj):
        """
        Bit of a hack; set values on object for later extraction.
        """
        eavs = obj.eav.get_attributes_and_values()
        for fieldname, field in self.fields.items():
            if getattr(field, 'eav', False):
                setattr(obj, field.model_attr, eavs.get(field.model_attr, None))
        return super(EAVIndex, self).full_prepare(obj)


def index_field_from_eav_field(f, default=indexes.CharField):
    """
    Returns the Haystack field type that fits this eav field's attribute type.
    """
    result = default

    if f.datatype == Attribute.TYPE_DATE:
        result = indexes.DateTimeField
    elif f.datatype == Attribute.TYPE_BOOLEAN:
        result = indexes.BooleanField
    elif f.datatype == Attribute.TYPE_FLOAT:
        result = indexes.FloatField
    elif f.datatype == Attribute.TYPE_INT:
        result = indexes.IntegerField

    return result


