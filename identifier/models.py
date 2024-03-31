from django.db import models
from simple_history.models import HistoricalRecords

from base_module.model_mixins import BaseUuidModel


class IdentifierModelManager(models.Manager):

    def get_by_natural_key(self, identifier):
        return self.get(identifier=identifier)

    @property
    def formatted_sequence(self):
        """Returns a padded sequence segment for the identifier
        """
        if self.is_derived:
            return ''
        return str(self.sequence_number).rjust(self.padding, '0')

    class Meta:
        abstract = True


class IdentifierModel(BaseUuidModel):

    name = models.CharField(max_length=100)

    sequence_number = models.IntegerField(default=1)

    identifier = models.CharField(max_length=50, unique=True)
    
    address_code = models.CharField(max_length=25, null=True)
    
    dob = models.CharField(max_length=25, null=True)

    linked_identifier = models.CharField(max_length=50, null=True)

    model = models.CharField(max_length=100, null=True)

    identifier_type = models.CharField(max_length=100, null=True)

    identifier_prefix = models.CharField(max_length=25, null=True)

    objects = IdentifierModelManager()
    
    history = HistoricalRecords()

    def __str__(self):
        return f'{self.identifier} {self.name}'

    def natural_key(self):
        return (self.identifier, )

    class Meta:
        app_label = 'identifier'
        ordering = ['sequence_number', ]
        unique_together = ('name', 'identifier')
