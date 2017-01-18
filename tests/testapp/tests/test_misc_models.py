from django.test import TestCase
from django.utils.encoding import force_text

from eav import register
from eav.models import EnumGroup, Attribute, Value
from testapp.models import Patient


class MiscModels(TestCase):

    def test_enumgroup_unicode(self):
        name = 'Yes / No'
        e = EnumGroup.objects.create(name=name)
        self.assertEqual(force_text(e), name)

    def test_attribute_help_text(self):
        desc = 'Patient Age'
        a = Attribute.objects.create(name='age', description=desc, datatype=Attribute.TYPE_INT)
        self.assertEqual(a.help_text, desc)

    def test_setting_to_none_deletes_value(self):
        register(Patient)
        Attribute.objects.create(name='age', datatype=Attribute.TYPE_INT)
        p = Patient.objects.create(name='Bob', eav__age=5)
        self.assertEqual(Value.objects.count(), 1)
        p.eav.age = None
        p.save()
        self.assertEqual(Value.objects.count(), 0)
