from django.db import models


class Variable(models.Model):
    INTEGER = 'INT'
    BOOLEAN = 'BOL'
    STRING = 'STR'

    TYPE_CHOICES = (
        (INTEGER, 'Integer'),
        (BOOLEAN, 'Boolean'),
        (STRING, 'String')
    )

    identifier = models.CharField(max_length=50)
    type = models.CharField(max_length=3, choices=TYPE_CHOICES)
    value = models.CharField(max_length=50)
    description = models.TextField()

    def get(self):
        if self.type == self.INTEGER:
            return int(self.value)
        elif self.type == self.BOOLEAN:
            return bool(self.value)
        else:
            return self.value

    def set(self, value):
        if type == self.INTEGER:
            self.value = int(value)
        elif type == self.BOOLEAN:
            self.value = bool(value)
        else:
            self.value = str(value)

        self.save()
