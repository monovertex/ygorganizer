
from django.core.management.base import NoArgsCommand
from ygo_cards.tasks import fetch_cards


class Command(NoArgsCommand):
    help = 'Fetch all the card data from the Yu-Gi-Oh! Wiki'

    def handle(self, **options):
        fetch_cards(self.stdout.write)
