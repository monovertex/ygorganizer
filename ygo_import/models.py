from django.db import models
from django.conf import settings
import json


class ImportData(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, primary_key=True,
                                related_name='import_data')
    data = models.TextField(blank=True)

    STEP_UPLOAD = 0
    STEP_RARITIES = 1
    STEP_CONFIRM = 2
    STEP_PROCESSING = 3
    STEP_SUCCESS = 4

    STEP_IDENTIFIERS = {
        STEP_UPLOAD: 'upload',
        STEP_RARITIES: 'rarities',
        STEP_CONFIRM: 'confirm',
        STEP_PROCESSING: 'processing',
        STEP_SUCCESS: 'success',
    }

    STEPS_BY_IDENTIFIER = {value: key for key, value
                           in STEP_IDENTIFIERS.iteritems()}

    STEPS = {
        STEP_UPLOAD: {
            'name': 'Upload',
            'identifier': STEP_IDENTIFIERS[STEP_UPLOAD]
        },
        STEP_RARITIES: {
            'name': 'Select Rarities',
            'identifier': STEP_IDENTIFIERS[STEP_RARITIES]
        },
        STEP_CONFIRM: {
            'name': 'Confirm Import',
            'identifier': STEP_IDENTIFIERS[STEP_CONFIRM]
        },
        STEP_PROCESSING: {
            'name': 'Processing',
            'identifier': STEP_IDENTIFIERS[STEP_PROCESSING]
        },
        STEP_SUCCESS: {
            'name': 'Success',
            'identifier': STEP_IDENTIFIERS[STEP_SUCCESS]
        },
    }

    STEP_CHOICES = tuple([(key, value['name']) for key, value
                          in STEPS.iteritems()])

    step = models.IntegerField(choices=STEP_CHOICES, default=STEP_UPLOAD)

    def __unicode__(self):
        return self.user.__unicode__()

    def set_data(self, data):
        self.unserialized_data = data
        self.data = json.dumps(data)
        self.save()

    def get_data(self):
        try:
            return self.unserialized_data
        except:
            if self.data:
                self.unserialized_data = json.loads(self.data)
            else:
                self.unserialized_data = None

        return self.unserialized_data
