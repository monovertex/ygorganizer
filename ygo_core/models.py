from django.db import models
from utils import slugify, process_string


class Constant(models.Model):
    identifier = models.CharField(max_length=50)
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return '{}'.format(self.name)

    @staticmethod
    def find_or_create(model, name):
        name = process_string(name).capitalize()
        identifier = slugify(name)

        try:
            instance = model.objects.filter(
                identifier=identifier)[0]
        except:
            instance = model.objects.create(
                identifier=identifier,
                name=name
            )

        return instance

    class Meta:
        abstract = True


class Locale(models.Model):
    identifier = models.CharField(max_length=10)
    url = models.CharField(max_length=255)

    def __unicode__(self):
        return '{}'.format(self.identifier)
