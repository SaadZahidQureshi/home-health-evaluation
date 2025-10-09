from api.core.choices import CustomerTypes
from rest_framework import serializers
from .models import Availability, BookingPerson, Appointment
from datetime import datetime

class AvailabilitySerializer(serializers.ModelSerializer):
    slot_display = serializers.CharField(source='get_slot_type_display', read_only=True)
    
    class Meta:
        model = Availability
        fields = ['id', 'slot_type', 'slot_display', 'date', 'is_booked']

class BookingPersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingPerson
        fields = ['id', 'first_name', 'last_name', 'email', 'phone_number', 
                 'address', 'zip_code', 'city', 'state', 'type']


class AppointmentCreateSerializer(serializers.Serializer):
    date = serializers.DateField()
    slot_type = serializers.ChoiceField(choices=Availability.SLOT_CHOICES)
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    phone_number = serializers.CharField(max_length=20)
    address = serializers.CharField()
    zip_code = serializers.CharField(max_length=10)
    city = serializers.CharField(max_length=100)
    state = serializers.CharField(max_length=100)
    type = serializers.ChoiceField(choices=CustomerTypes.choices)
    
    def validate(self, data):
        # ✅ Check if booking day is between Monday (0) and Thursday (3)
        booking_day = data['date'].weekday()  # Monday=0 ... Sunday=6
        if booking_day > 3:  # means Friday(4), Saturday(5), or Sunday(6)
            raise serializers.ValidationError(
                "Appointments can only be booked from Monday to Thursday."
            )
        
        # ✅ Check if slot is already booked
        availability = Availability.objects.filter(
            date=data['date'], 
            slot_type=data['slot_type']
        ).first()
        
        if availability and availability.is_booked:
            raise serializers.ValidationError("This slot is already booked.")
        
        return data
    
    def create(self, validated_data):
        booking_person_data = {
            'first_name': validated_data['first_name'],
            'last_name': validated_data['last_name'],
            'email': validated_data['email'],
            'phone_number': validated_data['phone_number'],
            'address': validated_data['address'],
            'zip_code': validated_data['zip_code'],
            'city': validated_data['city'],
            'state': validated_data['state'],
            'type': validated_data.get('type', ''),
        }
        
        booking_person = BookingPerson.objects.create(**booking_person_data)
        
        availability, created = Availability.objects.get_or_create(
            date=validated_data['date'],
            slot_type=validated_data['slot_type']
        )
        availability.is_booked = True
        availability.save()
        
        appointment = Appointment.objects.create(
            booking_person=booking_person,
            availability=availability
        )
        
        return appointment



class AppointmentSerializer(serializers.ModelSerializer):
    booking_person = BookingPersonSerializer(read_only=True)
    availability = AvailabilitySerializer(read_only=True)
    
    class Meta:
        model = Appointment
        fields = ['id', 'booking_person', 'availability', 'created_at']
