from rest_framework import serializers

from .models import IdentifierModel


class IdentifierModelSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = IdentifierModel
        fields = [
            'name', 'sequence_number', 'address_code', 'dob',
            'linked_identifier', 'model', 'identifier_type',
            'identifier_prefix']