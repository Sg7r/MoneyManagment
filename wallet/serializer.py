from rest_framework import serializers
from .models import Wallet
from django.contrib.auth.models import User


class WalletSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)
    # total_price = serializers.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        model = Wallet
        fields = ['income_or_expence', 'target', 'current_balance', 'data', 'user']
        read_only_fields = ['user']

    def create(self, validated_data):
        user = self.context['request'].user
        # Если пользователь не передан в запросе, то назначаем текущего авторизованного пользователя
        if user.is_authenticated:
            if 'user' not in validated_data:
                validated_data['user'] = self.context['request'].user
            return super().create(validated_data)
        else:
            raise serializers.ValidationError("User must be authenticated")


# This Serializer used to get the SUM of all rows in column
class SumResponseSerializer(serializers.Serializer):
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2)

# class CombinatedSerializer(serializers.ModelSerializer):
#     user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)
#
#     class Meta:
#         model = Wallet
#         fields = ['income_or_expence', 'target', 'current_balance', 'data', 'user']
#         read_only_fields = ['user']
#
#     def create(self, validated_data):
#         user = self.context['request'].user
#         # Если пользователь не передан в запросе, то назначаем текущего авторизованного пользователя
#         if user.is_authenticated:
#             if 'user' not in validated_data:
#                 validated_data['user'] = self.context['request'].user
#             return super().create(validated_data)
#         else:
#             raise serializers.ValidationError("User must be authenticated")
