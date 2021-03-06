# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Patient(models.Model):
    name = models.CharField(max_length=12)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Encounter(models.Model):
    num = models.PositiveSmallIntegerField()
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)

    def __str__(self):
        return '{}: encounter num {}'.format(self.patient, self.num)
