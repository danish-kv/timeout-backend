from rest_framework.serializers import ModelSerializer
from .models import CustomUser, LeaveRequest, LeaveType
from rest_framework import serializers
from django.utils.timezone import now




class RegisterSerializer(ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'email', 'department', 'first_name', 'last_name', 'date_joined']

    def create(self, validate_data):
        print('validate data ===',validate_data)
        password = validate_data.pop('password', '')
        user = CustomUser(**validate_data)

        user.set_password(password)
        user.save()

        return user

class UserSerializer(ModelSerializer):
    class Meta:
        fields = ['id', 'username', 'email', 'last_login', 'department', 'is_active', 'first_name', 'last_name']
        model = CustomUser



class ProfileSerializer(ModelSerializer):
    class Meta:
        fields = ['username', 'email', 'last_login', 'department', 'phone', 'location', 'date_joined']
        model = CustomUser


class LeaveTypeSerializer(ModelSerializer):
    class Meta:
        fields = '__all__'
        model = LeaveType


    def validate_name(self,value):
        if LeaveType.objects.filter(name__iexact=value).exclude(id=self.instance.id).exists():
            raise serializers.ValidationError(
                'A leave type with this name already exists'
            )
        return value


class LeaveRequestSerializer(ModelSerializer):
    employee = UserSerializer(read_only = True)
    leave_type_detail = LeaveTypeSerializer(source='leave_type', read_only=True) 
    leave_type = serializers.PrimaryKeyRelatedField(queryset=LeaveType.objects.all())
    class Meta:
        fields = [ 'id', 'employee', 'leave_type', 'leave_type_detail', 'start_date', 'end_date', 'reason', 
                  'attachment', 'status', 'created_at', 'comment' ]
        model = LeaveRequest


    def validate_start_date(self, value):
        if value < now().date():
            raise serializers.ValidationError("Start date cannot be in past")
        return value
    
    def validate_end_date(self, value):
        if self.initial_data.get('start_date'):
            start_date = self.initial_data.get('start_date')
            if value < start_date:
                raise serializers.ValidationError('End date must be on or after the start date')
            
        return value
    
    def validate_attachment(self, value):
        allowed_file_types = ["pdf", "docx", "doc"]
        if value:
            ext = value.name.split('.')[-1].lower()
            if ext not in allowed_file_types:
                raise serializers.ValidationError(
                    f"Unsupported file type. Allowed types are: {', '.join(allowed_file_types)}"
                )
        return value

    def validate(self, attrs):
        employee = self.context['requeset'].user
        start_date = attrs.get('start_date')
        end_date = attrs.get('end_date')
        leave_type = attrs.get('leave_type')

        overlapping_leaves = LeaveRequest.objects.filter(
            employee=employee,
            start_date__lte=end_date,
            end_date__gte=start_date,
            status = 'approved',
            leave_type=leave_type
        )

        if overlapping_leaves.exists():
            raise serializers.ValidationError(
                "You already have an approved leave request for this period."
            )

        return attrs


