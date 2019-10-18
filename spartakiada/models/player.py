from django.db import models
from django.urls import reverse

class Player(models.Model):
    name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return '%s' % self.name

    def get_absolute_url(self):
        return reverse('spartakiada:players')


    """
    Not perfect way to get players gender basing on their first name.
    Works only for polish names.
    """
    @property
    def gender(self):
        male_names = ["Bonawentura", "Kuba", "Kosma", "Attyla", "Barnaba", "Seba", "Dyzma", "Zawisza"]
        female_names = ["Miriam", "Nicole", "Noemi", "Beatrycze", "Nel"]
        name = self.name.partition(' ')[0]
        if name.endswith("a") and name not in male_names or name in female_names:
            return "F"
        else:
            return "M"

    class Meta:
        app_label = 'spartakiada'