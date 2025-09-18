from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Availability, Appointment, BookingPerson
from .serializers import (AvailabilitySerializer, AppointmentCreateSerializer, AppointmentSerializer, BookingPersonSerializer)
from datetime import datetime
from api.core.helpers import send_appointment_email

class AvailabilityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Availability.objects.all()
    serializer_class = AvailabilitySerializer
    
    @action(detail=False, methods=['get'], url_path="check-date")
    def check_date(self, request):
        """Get availability status for a specific date"""
        date_str = request.query_params.get('date')
        if not date_str:
            return Response({"error": "Date parameter is required"}, 
                           status=status.HTTP_400_BAD_REQUEST)
        
        try:
            target_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            return Response({"error": "Invalid date format. Use YYYY-MM-DD"}, 
                           status=status.HTTP_400_BAD_REQUEST)
        
        # Get or create availability slots for the date
        slot_08_00_to_12_00, _ = Availability.objects.get_or_create(
            slot_type='08_00_to_12_00', 
            date=target_date
        )
        slot_01_00_to_05_00, _ = Availability.objects.get_or_create(
            slot_type='01_00_to_05_00', 
            date=target_date
        )
        slot_05_00_to_09_00, _ = Availability.objects.get_or_create(
            slot_type='05_00_to_09_00', 
            date=target_date
        )
        slot_10_00_to_02_00, _ = Availability.objects.get_or_create(
            slot_type='10_00_to_02_00', 
            date=target_date
        )
        slot_02_00_to_06_00, _ = Availability.objects.get_or_create(
            slot_type='02_00_to_06_00', 
            date=target_date
        )
        slot_07_00_to_11_00, _ = Availability.objects.get_or_create(
            slot_type='07_00_to_11_00', 
            date=target_date
        )
        slot_11_00_to_03_00, _ = Availability.objects.get_or_create(
            slot_type='11_00_to_03_00', 
            date=target_date
        )
        slot_04_00_to_08_00, _ = Availability.objects.get_or_create(
            slot_type='04_00_to_08_00', 
            date=target_date
        )
        
        slots = [
            slot_08_00_to_12_00, 
            slot_01_00_to_05_00, 
            slot_05_00_to_09_00, 
            slot_10_00_to_02_00,
            slot_02_00_to_06_00, 
            slot_07_00_to_11_00, 
            slot_11_00_to_03_00, 
            slot_04_00_to_08_00
        ]
        serializer = AvailabilitySerializer(slots, many=True)
        
        return Response({
            "date": target_date,
            "slots": serializer.data
        })

class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all().select_related('booking_person', 'availability')
    
    def get_serializer_class(self):
        if self.action == 'create':
            return AppointmentCreateSerializer
        return AppointmentSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        appointment = serializer.save()
        send_appointment_email(appointment)
        response_serializer = AppointmentSerializer(appointment)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        appointment = self.get_object()
        availability = appointment.availability
        availability.is_booked = False
        availability.save()
        appointment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class BookingPersonViewSet(viewsets.ModelViewSet):
    queryset = BookingPerson.objects.all()
    serializer_class = BookingPersonSerializer
