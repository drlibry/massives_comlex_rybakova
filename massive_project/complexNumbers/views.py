from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from complexNumbers.models import ComplexNumber, NumberArray
from complexNumbers.serializers import NumberArraySerializer, ComplexNumberSerializer


class NumberArrayView(APIView):

    # Добавить массив чисел
    def post(self, request):
        if not request.data:
            return Response({"error": "No data provided"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = NumberArraySerializer(data=request.data)
        if serializer.is_valid():
            array_instance = serializer.save()
            return Response({"array_id": array_instance.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    # Получить все комплексные числа из массивов
    def get(self, request):
        try:
            complexNumbers = ComplexNumber.objects.exclude(imaginary=0)

            if not complexNumbers.exists():
                return Response({"error": "No complex numbers found"}, status=status.HTTP_404_NOT_FOUND)

            serialized_data = ComplexNumberSerializer(complexNumbers, many=True).data
            return Response({'numbers': serialized_data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class NumbersByIDView(APIView):
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('id')
        print(f"pk: {pk}")
        if pk is None:
            return Response({"message": "Array not found"}, status=404)

        mass = NumberArray.objects.get(id=pk)
        complex_in_mass = []
        number_list = [str(x) for x in mass.numbers.split(',')]
        for number_id in number_list:
            complex_number = ComplexNumber.objects.get(id=number_id)
            if complex_number.imaginary != 0:
                complex_in_mass.append(complex_number)

        serializer = ComplexNumberSerializer(complex_in_mass, many=True)
        return Response(serializer.data, status=200)

    #Удалить массив
    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('id')
        print(f"pk: {pk}")
        if id is None:
            return Response({"message": "Array not found"}, status=status.HTTP_404_NOT_FOUND)
        mass = NumberArray.objects.get(id=pk)
        number_list = [str(x) for x in mass.numbers.split(',')]
        for number_id in number_list:
            complex_number = ComplexNumber.objects.get(id=number_id)
            complex_number.delete()
        mass.delete()
        return Response({
            "message": "Massive has been deleted."}, status=status.HTTP_200_OK)
    # def delete(self, request, *args, **kwargs):
    #     pk = kwargs.get('id')
    #     print(f"pk: {pk}")
    #     if pk is None or pk == '':
    #         return Response({"message": "Array not found"}, status=status.HTTP_404_NOT_FOUND)
    #     mass = NumberArray.objects.get(id=pk)
    #     number_list = [str(x) for x in mass.numbers.split(',')]
    #     for number_id in number_list:
    #         complex_number = ComplexNumber.objects.get(id=number_id)
    #         complex_number.delete()
    #     mass.delete()
    #     return Response({
    #         "message": "Massive has been deleted."}, status=status.HTTP_200_OK)

