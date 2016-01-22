from django.contrib.auth.models import User

from rest_framework import serializers

from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    # student = serializers.SerializerMethodField("getStudent")

    class Meta:
        model = Product
        fields = ("product", "price", "description", "student", "pk")

    # def getStudent(self, obj):
    #     return User.objects.filter(id=obj.student_id)[0].email


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "pk", 'password')
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, data):
        """
        Validate everything.
        """
        errors = {}
        # Check email
        email = data.get("email", None)
        # Make sure email is unique
        does_exists = User.objects.filter(username=email)
        if does_exists:
            raise serializers.ValidationError({"email": "email already exists"})

        if email is None:
            errors['email'] = "Email cannot be empty"
        elif "csumb.edu" not in email:
            errors['email'] = "Email must be a CSUMB email"

        # Check First first_name
        first_name = data.get("first_name", None)
        if first_name is None or len(first_name) == 0:
            errors['first_name'] = "First name cannot be empty"

        # Check last name
        last_name = data.get("last_name", None)
        if last_name is None or len(last_name) == 0:
            errors['last_name'] = "Last name cannot be empty"

        # Check password
        # TODO: Check that password is somewhat "Strong"
        password = data.get("password", None)
        if password is None or len(password) == 0:
            errors['password'] = "Password cannot be empty"

        if errors:
            raise serializers.ValidationError(errors)

        return data

    def create(self, validated_data):
        """
        Obviously when creating a new user \o/
        """
        user = User(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            username=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
