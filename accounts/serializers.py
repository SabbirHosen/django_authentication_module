from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from accounts.tokens import account_activation_token
from accounts.models import OTP

User = get_user_model()


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        is_email_verification_mandatory = getattr(settings, 'ACCOUNT_EMAIL_VERIFICATION', 'optional')

        if is_email_verification_mandatory == "mandatory":
            user.is_active = False
            user.save()
            self.send_activation_email(user)
        else:
            user.is_active = True
            user.save()

        return user

    def send_activation_email(self, user):
        current_site = get_current_site(self.context['request'])
        mail_subject = 'Activate your account.'
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = account_activation_token.make_token(user)
        message = render_to_string('accounts/activation_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': uid,
            'token': token,
            'protocol': 'http',
        })
        send_mail(mail_subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])


class ResendActivationEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        user = get_user_model().objects.filter(email=value).first()
        if user and user.is_email_verified:
            raise serializers.ValidationError('Email is already verified.')
        if settings.ACCOUNT_EMAIL_VERIFICATION != 'mandatory':
            raise serializers.ValidationError('No need to verify email.')
        return value

    def save(self):
        request = self.context.get('request')
        email = self.validated_data['email']
        user = get_user_model().objects.filter(email=email).first()

        if user:
            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = account_activation_token.make_token(user)
            # activation_link = reverse('activate', kwargs={'uidb64': uid, 'token': token})
            # activate_url = f'http://{current_site.domain}{activation_link}'
            message = render_to_string('accounts/activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': uid,
                'token': token,
            })
            send_mail(mail_subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        user = User.objects.filter(email=value).first()
        if not user:
            raise serializers.ValidationError('There is no user registered with this email address.')
        return value

    def save(self):
        request = self.context.get('request')
        email = self.validated_data['email']
        user = User.objects.filter(email=email).first()

        if user:
            current_site = get_current_site(request)
            mail_subject = 'Reset your password.'
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = account_activation_token.make_token(user)
            # reset_link = reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
            # reset_url = f'http://{current_site.domain}{reset_link}'
            message = render_to_string('accounts/password_reset_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': uid,
                'token': token,
            })
            send_mail(mail_subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])


class LogoutSerializer(serializers.Serializer):
    pass


class PasswordChangeSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)


class OTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)

    def validate(self, data):
        try:
            otp_instance = OTP.objects.get(user__email=data['email'])
        except OTP.DoesNotExist:
            raise serializers.ValidationError("Invalid email or OTP.")

        if not otp_instance.is_valid():
            raise serializers.ValidationError("OTP has expired.")

        if otp_instance.otp != data['otp']:
            raise serializers.ValidationError("Invalid OTP.")

        return data


class SendOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
