from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Availability, Appointment, BookingPerson
from .serializers import (AvailabilitySerializer, AppointmentCreateSerializer, AppointmentSerializer, BookingPersonSerializer)
from datetime import datetime
from api.core.helpers import send_appointment_email, send_appointment_confirmation_email

class AvailabilityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Availability.objects.all()
    serializer_class = AvailabilitySerializer
    @action(detail=False, methods=['get'], url_path="check-date")
    def check_date(self, request):
        """Check appointment status for a specific date"""
        date_str = request.query_params.get('date')
        if not date_str:
            return Response({"error": "Date parameter is required"}, 
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            target_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            return Response({"error": "Invalid date format. Use YYYY-MM-DD"}, 
                            status=status.HTTP_400_BAD_REQUEST)

        # Loop through all defined slot choices
        slots_status = []
        for slot_type, slot_display in Availability.SLOT_CHOICES:
            # Check if an appointment exists for this date + slot
            exists = Appointment.objects.filter(
                availability__date=target_date,
                availability__slot_type=slot_type
            ).exists()

            slots_status.append({
                "slot_type": slot_type,
                "slot_display": slot_display,
                "is_booked": exists
            })

        return Response({
            "date": target_date,
            "slots": slots_status
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
        send_appointment_confirmation_email(appointment)
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
