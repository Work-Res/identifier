from django.db import models


class WorkResidencePermitIdentifierManager(models.Manager):

    def get_by_natural_key(self, wr_identifier):
        return self.get(wr_identifier=wr_identifier,)


class IdentifierManager(models.Manager):

    def get_by_natural_key(self, identifier):
        return self.get(identifier=identifier,)


class TrackingIdentifierManager(models.Manager):

    def get_by_natural_key(self, tracking_identifier):
        return self.get(tracking_identifier=tracking_identifier,)
