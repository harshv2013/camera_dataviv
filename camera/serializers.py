from rest_framework import serializers
from camera.models import Employee, Organization, Store, User, \
    Analytic, AnalyticDisplay, TotalDisplay


########################################################

class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = "__all__"


#########################################################
class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = "__all__"
##########################################################


class AnalyticSerializer(serializers.ModelSerializer):
    class Meta:
        model = Analytic
        fields = "__all__"
##########################################################


class AnalyticDisplaySerializer(serializers.ModelSerializer):
    class Meta:
        model = AnalyticDisplay
        fields = "__all__"
##########################################################


class TotalDisplaySerializer(serializers.ModelSerializer):
    class Meta:
        model = TotalDisplay
        fields = "__all__"
##########################################################


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = "__all__"


###########################################################
class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password', 'is_superuser', 'is_staff', 'email')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            is_staff=validated_data['is_staff'],
            email=validated_data['email']

        )
        user.set_password(validated_data['password'])
        user.save()
        return user




