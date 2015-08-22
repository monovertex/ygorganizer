
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from os.path import splitext
from django.utils.safestring import mark_safe


class UploadForm(forms.Form):
    source = forms.FileField(
        help_text=mark_safe(
            """
                <p class="help-block">
                    You can import data into your collection using a CSV file.
                </p>

                <p class="help-block">
                    The file should have each card you want to import on a separate row. Each row should contain the set number of the card, followed by how many of said card you have in your collection and the rarity.
                </p>

                <p class="help-block">
                    <a href="#" data-toggle="modal" data-target="#rarities-modal">These are the valid rarity strings</a>. The case does not matter. If you have multiple rarities for the same set number, add a different line for each of them.
                </p>

                <p class="help-block">
                    You can leave the number cell blank, if you only have one. However, you cannot add a rarity if you leave the number cell blank, so you need to explicitly put 1 as the quantity if you want to specify the rarity.
                </p>

                <p class="help-block">
                    The contents of the CSV file should look like this:
                </p>

                <p class="help-block">
                    YSYR-EN018<br />
                    YSYR-EN024,2<br />
                    YSYR-EN025<br />
                    YSYR-EN025,4,common<br />
                    <small>and so on...</small>
                </p>

                <p class="help-block">
                    Here is how you can create CSV files using <a href="https://support.office.com/en-za/article/Import-or-export-text-txt-or-csv-files-5250ac4c-663c-47ce-937b-339e391393ba" target="_blank">Excel</a> or <a href="https://support.google.com/mail/answer/12119?hl=en" target="_blank">Google Spreadsheets</a>.
                </p>
            """
        ))

    MODE_ADD = '0'
    MODE_REPLACE = '1'
    MODE_SUBSTRACT = '2'
    MODE_CHOICES = (
        (MODE_ADD, 'Add to existent values'),
        (MODE_SUBSTRACT, 'Subtract from existent values'),
        (MODE_REPLACE, 'Replace existent collection'),
    )
    mode = forms.ChoiceField(
        choices=MODE_CHOICES,
        help_text=mark_safe(
            """
                <p class="help-block">
                    Choose how should the data be imported.
                </p>

                <p class="help-block">
                    The values can be added to the currently existent values in your collection, or they can be subtracted from the collection.
                </p>

                <p class="help-block">
                    Alternatively, you can replace your entire collection with the data you want to import.
                </p>
            """
        ))

    SOURCE_EXTENSION_WHITELIST = ['.csv']

    def clean_source(self):
        source = self.cleaned_data['source']
        extension = splitext(source.name)[1]

        if extension in self.SOURCE_EXTENSION_WHITELIST:
            return source
        else:
            raise forms.ValidationError('Invalid file type.')

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = ''

        self.helper.add_input(Submit('submit', 'Import',
                                     css_class='pull-right'))

        return super(UploadForm, self).__init__(*args, **kwargs)
