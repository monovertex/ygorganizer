
from django.core.management.base import NoArgsCommand
from ygo_cards.tasks import fetch_sets


class Command(NoArgsCommand):
    help = 'Fetch all the set data from Yu-Gi-Oh! Prices'

    def handle(self, **options):
        fetch_sets(self.stdout.write)
