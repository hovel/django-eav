from datetime import datetime
try:
    from django.utils.timezone import now
except ImportError:
    now = datetime.now
from django.test import TestCase

from eav import register
from testapp.models import Patient
from eav.forms import BaseDynamicEntityForm
from eav.models import Attribute, EnumValue, EnumGroup

class FormTest(TestCase):
    def setUp(self):
        register(Patient)

        Attribute.objects.create(name='Age', datatype=Attribute.TYPE_INT)
        Attribute.objects.create(name='DoB', datatype=Attribute.TYPE_DATE)
        Attribute.objects.create(name='DToB', datatype=Attribute.TYPE_DATETIME)
        Attribute.objects.create(name='Height', datatype=Attribute.TYPE_FLOAT)
        Attribute.objects.create(name='City', datatype=Attribute.TYPE_TEXT)
        Attribute.objects.create(name='Pregnant?', datatype=Attribute.TYPE_BOOLEAN)

        yes = EnumValue.objects.create(value='yes')
        no = EnumValue.objects.create(value='no')
        unkown = EnumValue.objects.create(value='unkown')
        ynu = EnumGroup.objects.create(name='Yes / No / Unknown')
        ynu.enums.add(yes)
        ynu.enums.add(no)
        ynu.enums.add(unkown)
        Attribute.objects.create(name='Fever?', datatype=Attribute.TYPE_ENUM, enum_group=ynu, required=True)

    def test_form_validation(self):
        kwargs = {'eav__age': 2, 'eav__dob': now(), 'eav__dtob': now(),
                  'eav__height': 14.1, 'eav__city': 'SomeSity',
                  'eav__pregnant': False,
                  'eav__fever': EnumValue.objects.get(id=2)}
        p = Patient.objects.create(**kwargs)

        # required "fever" field
        data = {}
        form = BaseDynamicEntityForm(data=data, instance=p)
        self.assertFalse(form.is_valid())

        # all valid
        data = {'age': 1, 'dob_0': '2012-01-01', 'dob_1': '12:00:00',
                'dtob_0': '2012-01-01', 'dtob_1': '12:00:00',
                'height': 10.1, 'city': 'Moscow', 'pregnant': True, 'fever': 1}
        form = BaseDynamicEntityForm(data=data, instance=p)
        self.assertTrue(form.is_valid())
