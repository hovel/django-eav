#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4 coding=utf-8
#
#    This software is derived from EAV-Django originally written and 
#    copyrighted by Andrey Mikhaylenko <http://pypi.python.org/pypi/eav-django>
#
#    This is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This software is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with EAV-Django.  If not, see <http://gnu.org/licenses/>.


from django.contrib import admin
from django.contrib.admin.options import (
    ModelAdmin, InlineModelAdmin
)

from django.forms.models import BaseInlineFormSet
from django.utils.safestring import mark_safe
from django.contrib.contenttypes.models import ContentType


from .models import Attribute, Value, EnumValue, EnumGroup
from .forms import BaseDynamicEntityForm


class BaseEntityAdmin(ModelAdmin):
    form = BaseDynamicEntityForm
    attribute_class = None
    
    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        """
        Wrapper for ModelAdmin.render_change_form. Replaces standard static
        AdminForm with an EAV-friendly one. The point is that our form generates
        fields dynamically and fieldsets must be inferred from a prepared and
        validated form instance, not just the form class. Django does not seem
        to provide hooks for this purpose, so we simply wrap the view and
        substitute some data.
        """
        form = context['adminform'].form

        # infer correct data from the form
        fieldsets = self.fieldsets or [(None, {'fields': form.fields.keys()})]
        adminform = admin.helpers.AdminForm(form, fieldsets,
                                      self.prepopulated_fields)
        media = mark_safe(self.media + adminform.media)

        context.update(adminform=adminform, media=media)

        super_meth = super(BaseEntityAdmin, self).render_change_form
        return super_meth(request, context, add, change, form_url, obj)


    import django
    if (1,4) > django.VERSION:
        def changelist_view(self, request, extra_context=None):
            """
            Override of changelist_view to provide dynamic calculation of 
            list_display.  This will no longer be necessary after Django 1.4 -
            see django changeset 16340.
            
            This may not be threadsafe.  Don't do anything with side effects.
            """
            if hasattr(self, 'get_list_display'):
                self.list_display = self.get_list_display(request)
            return super(BaseEntityAdmin, self).changelist_view(request, extra_context)

        
    def get_list_display(self, request):
        """
        Adds all attributes configured with display_in_list
        to the changelist view.  Override to customize.
        """
        base_list_display = list(self.list_display)
        attribute_class = self.attribute_class or Attribute
        for attribute in attribute_class.objects.filter(display_in_list=True):
            func_name = "eav_%s" % attribute.slug
            if func_name in self.list_display:
                continue
            func = lambda x, attr=attribute: x.eav.get_value_by_attribute(attr).value
            func.short_description = attribute.name
            setattr(self.model, func_name, func)
            base_list_display.append(func_name)
        return base_list_display
            
        
class BaseEntityInlineFormSet(BaseInlineFormSet):
    """
    An inline formset that correctly initializes EAV forms.
    """
    def add_fields(self, form, index):
        if self.instance:
            setattr(form.instance, self.fk.name, self.instance)
            form._build_dynamic_fields()
        super(BaseEntityInlineFormSet, self).add_fields(form, index)


class BaseEntityInline(InlineModelAdmin):
    """
    Inline model admin that works correctly with EAV attributes. You should mix
    in the standard StackedInline or TabularInline classes in order to define
    formset representation, e.g.::

        class ItemInline(BaseEntityInline, StackedInline):
            model = Item
            form = forms.ItemForm

    .. warning: TabularInline does *not* work out of the box. There is,
        however, a patched template `admin/edit_inline/tabular.html` bundled
        with EAV-Django. You can copy or symlink the `admin` directory to your
        templates search path (see Django documentation).

    """
    formset = BaseEntityInlineFormSet

    def get_fieldsets(self, request, obj=None):
        if self.declared_fieldsets:
            return self.declared_fieldsets

        formset = self.get_formset(request)
        fk_name = self.fk_name or formset.fk.name
        kw = {fk_name: obj} if obj else {}
        instance = self.model(**kw)
        form = formset.form(request.POST, instance=instance)

        return [(None, {'fields': form.fields.keys()})]

class AttributeAdmin(ModelAdmin):
    list_display = ('name', 'slug', 'datatype', 'description', 'site')
    list_filter = ['site']
    prepopulated_fields = {'slug': ('name',)}
    
    
class PartitionedAttributeAdmin(AttributeAdmin):
    """
    Abstract base class for Admins of specific types of Attributes.
    Provides functionality for filtering based on the implementing class's
    parent_model field.
    """
    exclude = ('parent',)

    def queryset(self, request):
        """
        Instead of returning all Attributes, return only those
        pertaining to a specific model, specified by subclass's parent_model.
        """
        qs = super(PartitionedAttributeAdmin, self).queryset(request)
        ctype = ContentType.objects.get_for_model(self.parent_model)
        return qs.filter(parent=ctype)

    def save_model(self, request, obj, form, change):
        """
        Overrides default ModelAdmin behavior to set the parent model.
        """
        ctype = ContentType.objects.get_for_model(self.parent_model)
        obj.parent = ctype
        obj.save()

class EnumGroupAdmin(ModelAdmin):
    filter_horizontal = ('enums', )

def register_admin():
    """
    Don't automatically register the generic EAV models unless asked.
    """
    admin.site.register(Attribute, AttributeAdmin)
    admin.site.register(Value)
    admin.site.register(EnumValue)
    admin.site.register(EnumGroup, EnumGroupAdmin)

