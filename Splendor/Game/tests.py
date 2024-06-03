from django.test import TestCase
from .models import Card

# Create your tests here.
class TestCards(TestCase):
    def test_costs(self):
        import pdb
        pdb.set_trace()
        cards = Card.objects.all()
        print("Card")
        for card in cards:
            cost = card.get_cost()
            for gem in ['diamond', 'sapphire', 'emerald', 'ruby', 'onyx']:
                assert gem in cost

    