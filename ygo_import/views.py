

from django.shortcuts import redirect
from django.views.generic import TemplateView
from .models import ImportData
from .forms import UploadForm
from ygo_core.mixins import LoginRequiredMixin
from ygo_core.utils import slugify
from .tasks import process_import
from querystring_parser import parser
from ygo_cards.models import CardVersion, Rarity
import csv
import re


class ImportView(LoginRequiredMixin, TemplateView):

    http_method_names = ['get', 'post']

    TEMPLATES = {
        ImportData.STEP_UPLOAD: 'pages/import/upload.html',
        ImportData.STEP_RARITIES: 'pages/import/rarities.html',
        ImportData.STEP_CONFIRM: 'pages/import/confirm.html',
        ImportData.STEP_PROCESSING: 'pages/import/processing.html',
        ImportData.STEP_SUCCESS: 'pages/import/success.html'
    }

    def get_import_data(self):
        try:
            return self._import_data
        except:
            user = self.request.user

            try:
                self._import_data = user.import_data
            except:
                self._import_data = ImportData.objects.create(user=user)

            return self._import_data

    @property
    def import_data(self):
        return self.get_import_data().get_data()

    @property
    def step(self):
        return self.get_import_data().step

    @property
    def steps(self):
        return ImportData.STEPS

    @property
    def form_upload(self):
        if self.request.method == 'POST':
            form = UploadForm(self.request.POST, self.request.FILES)
        else:
            form = UploadForm()

        return form

    @property
    def rarities(self):
        return Rarity.objects.all().order_by('identifier')

    def validate_current_step(self, request, step):
        import_data = self.get_import_data()

        try:
            step = ImportData.STEPS_BY_IDENTIFIER[step]

            if (step != import_data.step):

                if (step < import_data.step
                        and import_data.step != ImportData.STEP_PROCESSING
                        and (
                            import_data.step != ImportData.STEP_SUCCESS
                            or step == ImportData.STEP_UPLOAD)):
                    import_data.step = step
                    import_data.save()

                return redirect('import', step=ImportData.STEP_IDENTIFIERS[
                    import_data.step])
        except:
            if step is None:
                return redirect('import', step=ImportData.STEP_IDENTIFIERS[
                    import_data.step])

        import_data.get_data()

    def get_template_names(self):
        return [self.TEMPLATES[self.step]]

    def get(self, request, step=None, *args, **kwargs):
        validation = self.validate_current_step(request, step)

        if validation is not None:
            return validation

        return super(ImportView, self).get(request, *args, **kwargs)

    def post(self, request, step=None, *args, **kwargs):
        validation = self.validate_current_step(request, step)

        if validation is not None:
            return validation

        response = getattr(
            self, 'post_' + ImportData.STEP_IDENTIFIERS[self.step])(
                request, *args, **kwargs)

        if response is not None:
            return response

        return self.get(request, *args, **kwargs)

    def post_upload(self, request, *args, **kwargs):
        form = self.form_upload

        if form.is_valid():
            mode = form.cleaned_data['mode']

            invalid_set_numbers = set()
            set_numbers = set()
            set_numbers_data = {}

            for row in csv.reader(self.request.FILES['source']):
                if len(row) and row[0]:
                    set_number = row[0].upper()

                    try:
                        count = abs(int(row[1]))
                    except:
                        count = 1

                    try:
                        rarity = Rarity(identifier=slugify(row[2])).identifier
                    except:
                        rarity = None

                    if mode == UploadForm.MODE_SUBSTRACT:
                        count *= -1

                    # Check if the input is a valid set number.
                    if re.match(r'\w+-[A-Z]*[0-9]+', set_number) is not None:

                        # If it's a foreign set number, change it to EN.
                        if (re.search(r'-[A-Z]{1,2}', set_number) is not None
                                and set_number.find('-EN') == -1):
                            set_number = re.sub(
                                r'-[A-Z]{1,2}', '-EN', set_number)

                        set_numbers.add(set_number)

                        if (set_number in set_numbers_data):
                            if (rarity in set_numbers_data[set_number]):
                                set_numbers_data[set_number][rarity] += count
                            else:
                                set_numbers_data[set_number][rarity] = count
                        else:
                            set_numbers_data[set_number] = {rarity: count}
                    else:
                        invalid_set_numbers.add(set_number)

            card_versions = (CardVersion.objects
                             .only('id', 'set_number', 'card__name',
                                   'rarity__identifier')
                             .select_related('card', 'rarity')
                             .filter(set_number__in=set_numbers)
                             .distinct()
                             .order_by('set_number'))
            card_versions_by_rarities = {}
            card_versions_rarities = {}

            for card_version in card_versions:
                if (card_version.set_number not in card_versions_by_rarities):
                    card_versions_by_rarities[card_version.set_number] = {}
                    card_versions_rarities[card_version.set_number] = {}

                rarity = card_version.rarity

                card_versions_by_rarities[card_version.set_number][
                    card_version.rarity.identifier] = card_version
                card_versions_rarities[card_version.set_number][
                    rarity.identifier] = {
                        'card_version_pk': card_version.pk,
                        'name': rarity.name
                }

            not_found_set_numbers = {}
            not_found_set_numbers_total = 0
            not_found_rarities = {}
            valid_set_numbers = {}
            valid_set_numbers_total = 0

            for set_number, data in set_numbers_data.iteritems():
                if set_number in card_versions_by_rarities:
                    valid_set_numbers[set_number] = {}
                    current_total = 0

                    if len(card_versions_by_rarities[set_number]) == 1:
                        data = {
                            (card_versions_by_rarities[set_number]
                             .iterkeys().next()): (
                                sum([c for r, c in data.iteritems()]))
                        }

                    found = True
                    for rarity, count in data.iteritems():
                        if rarity in card_versions_by_rarities[set_number]:
                            card_version = (
                                card_versions_by_rarities[set_number][rarity])

                            valid_set_numbers[set_number][rarity] = {
                                'count': count,
                                'name': card_version.card.name,
                                'pk': card_version.pk,
                                'rarity_name': card_versions_rarities[
                                    set_number][rarity]['name']
                            }

                            current_total += count
                        else:
                            found = False
                            break

                    if not found:
                        del valid_set_numbers[set_number]

                        not_found_rarities[set_number] = {
                            'count': sum([c for r, c in data.iteritems()]),
                            'name': (card_versions_by_rarities[set_number]
                                     .itervalues().next().card.name),
                            'rarities': card_versions_rarities[
                                set_number]
                        }
                    else:
                        valid_set_numbers_total += current_total
                else:
                    not_found_set_numbers[set_number] = sum(
                        [c for r, c in data.iteritems()])
                    not_found_set_numbers_total += (
                        not_found_set_numbers[set_number])

            import_data = self.get_import_data()

            if len(not_found_rarities) > 0:
                import_data.step = ImportData.STEP_RARITIES
            else:
                import_data.step = ImportData.STEP_CONFIRM

            import_data.set_data({
                'mode': mode,
                'invalid_set_numbers': list(invalid_set_numbers),
                'invalid_set_numbers_count': len(invalid_set_numbers),
                'valid_set_numbers': valid_set_numbers,
                'valid_set_numbers_total': valid_set_numbers_total,
                'all_valid_set_numbers': valid_set_numbers,
                'all_valid_set_numbers_total': valid_set_numbers_total,
                'not_found_set_numbers': not_found_set_numbers,
                'not_found_set_numbers_total': not_found_set_numbers_total,
                'not_found_rarities': not_found_rarities
            })

            return redirect('import', step=ImportData.STEP_IDENTIFIERS[
                import_data.step])

    def post_rarities(self, request, *args, **kwargs):
        post_dict = parser.parse(request.POST.urlencode())
        data = self.import_data
        all_valid_set_numbers = {}
        all_valid_set_numbers_total = data['valid_set_numbers_total']
        not_found_rarities = data['not_found_rarities']

        for set_number, rarities in post_dict['rarity'].iteritems():
            all_valid_set_numbers[set_number] = {}

            for rarity, count in rarities.iteritems():
                count = int(count)

                if (count > 0):
                    all_valid_set_numbers[set_number][rarity] = {
                        'count': count,
                        'name': not_found_rarities[set_number]['name'],
                        'pk': not_found_rarities[set_number][
                            'rarities'][rarity]['card_version_pk'],
                        'rarity_name': not_found_rarities[set_number][
                            'rarities'][rarity]['name']
                    }

                    all_valid_set_numbers_total += count

            if len(all_valid_set_numbers[set_number]) == 0:
                del all_valid_set_numbers[set_number]

        all_valid_set_numbers.update(data['valid_set_numbers'])

        data['all_valid_set_numbers'] = all_valid_set_numbers
        data['all_valid_set_numbers_total'] = all_valid_set_numbers_total

        import_data = self.get_import_data()
        import_data.step = ImportData.STEP_CONFIRM
        import_data.set_data(data)

        return redirect('import', step=ImportData.STEP_IDENTIFIERS[
            import_data.step])

    def post_confirm(self, request, *args, **kwargs):
        process_import.apply_async((request.user.pk,),
                                   countdown=60)

        import_data = self.get_import_data()
        import_data.step = ImportData.STEP_PROCESSING
        import_data.save()

        return redirect('import', step=ImportData.STEP_IDENTIFIERS[
            import_data.step])
