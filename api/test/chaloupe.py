from django.test import TestCase
from ..models import Chaloupe

class ChaloupeTest(TestCase):
    def test_creation(self):
        obj = Chaloupe.objects.create(champ="valeur")
        self.assertEqual(obj.champ, "valeur")  # Vérifie que l'objet a bien été créé 🦆