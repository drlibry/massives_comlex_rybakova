from rest_framework import serializers
from uuid import UUID, uuid4
from .models import NumberArray, ComplexNumber

class ComplexNumberSerializer(serializers.Serializer):
    real = serializers.FloatField()
    imaginary = serializers.FloatField()

    def to_internal_value(self, data):
        return ComplexNumber(**data)

class NumberArraySerializer(serializers.Serializer):
    numbers = ComplexNumberSerializer(many=True)

    def create(self, validated_data):
        numbers_data = validated_data['numbers']
        numbers_list = []
        for num_data in numbers_data:
            real = num_data.real  # Access the real attribute directly
            imaginary = num_data.imaginary  # Access the imaginary attribute directly
            numbers_list.append(ComplexNumber.objects.create(real=real, imaginary=imaginary))
        numbers_string = ','.join(str(x.id) for x in numbers_list)
        array_instance = NumberArray.objects.create(numbers=numbers_string)
        return array_instance

    def to_representation(self, instance):
        numbers = instance.numbers.split(',')
        complex_numbers = []
        for num_id in numbers:
            num_instance = ComplexNumber.objects.get(id=UUID(num_id))  # Convert string to UUID
            complex_numbers.append({
                'id': str(num_instance.id),
                'real': num_instance.real,
                'imaginary': num_instance.imaginary
            })
        return {'array_id': str(instance.id), 'numbers': complex_numbers}

class SerchSerializer(serializers.Serializer):
    array_id = serializers.UUIDField(required=True)