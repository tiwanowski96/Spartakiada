from django.db import models
from django.urls import reverse

class Cup(models.Model):
    name = models.CharField(max_length=128)
    date = models.DateField()

    class Meta:
        unique_together = ("name", "date")

    def __str__(self):
        return '%s' % self.name

    def get_absolute_url(self):
        return reverse('spartakiada:cup-add-games', kwargs={'cup_id': self.id})

    class Meta:
        app_label = 'spartakiada'