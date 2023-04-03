import string
import random
from .models import GeneratorSettings

class Generator:
    alphabets = True
    digits = True
    punctuations = True
    uppercase = True
    key = ""
    password = ""

    def __init__(self, **kwargs):
        self.settings = GeneratorSettings.objects.get(id=1)
        
    def _make_key(self):
        self.key = ""
        if self.settings.alphabets:
            self.key+=string.ascii_lowercase
        if self.settings.uppercase:
            self.key+=string.ascii_uppercase
        if self.settings.digits:
            self.key+=string.digits
        if self.settings.punctuations:
            self.key+=string.punctuation


    def generate(self):
        self._make_key()
        self.password = ""
        count = 0
        if not self.key:
            self.settings.alphabets = True
            self.settings.save()
            self._make_key()
        while count < self.settings.length:
            self.password += random.choice(self.key)
            count += 1
