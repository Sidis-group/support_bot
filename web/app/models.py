from uuid import uuid4
from django.db import models

class TelegramUser(models.Model):
    class Meta:
        verbose_name = 'Telegram User'
        verbose_name_plural = 'Telegram Users'
        db_table = 'telegram_user'

    class Language(models.TextChoices):
        UA = 'ua', 'Ukrainian'
        EN = 'en', 'English'

    telegram_id = models.BigIntegerField(unique=True, primary_key=True)
    full_name = models.CharField(max_length=255)
    join_time = models.DateTimeField(auto_now_add=True)
    language = models.CharField(
        max_length=2,
        choices=Language.choices,
        default=Language.UA,
    )
    
    def __str__(self):
        return f'{self.full_name} ({self.telegram_id})'

    def dict(self):
        return {
            'telegram_id': self.telegram_id,
            'full_name': self.full_name,
            'join_time': self.join_time,
            'language': self.language,
        }
        
class SupportRequest(models.Model):
    class Meta:
        verbose_name = 'Support Request'
        verbose_name_plural = 'Support Requests'
        db_table = 'support_request'
    
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(TelegramUser, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.user} at {self.time}'
    
    def dict(self):
        return {
            'id': self.id,
            'user_id': self.user.telegram_id,
            'created_time': self.created_time,
        }

class Operator(models.Model):
    class Meta:
        verbose_name = 'Operator'
        verbose_name_plural = 'Operators'
        db_table = 'operator'
    
    telegram_id = models.BigIntegerField(unique=True, primary_key=True)
    full_name = models.CharField(max_length=255)
    join_time = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.full_name} ({self.telegram_id})'

    def dict(self):
        return {
            'telegram_id': self.telegram_id,
            'full_name': self.full_name,
            'join_time': self.join_time,
        }
        
class OperatorConfirmUUID(models.Model):
    class Meta:
        verbose_name = 'Operator Confirm Code'
        verbose_name_plural = 'Operator Confirm Codes'
        db_table = 'operator_confirm_code'
    
    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    
    def __str__(self):
        return f'{self.uuid}'

    def dict(self):
        return {
            'uuid': self.uuid,
        }
        
class Favorite(models.Model):
    class Meta:
        verbose_name = 'Favorite'
        verbose_name_plural = 'Favorites'
        db_table = 'favorite'
    
    id = models.AutoField(primary_key=True) 
    operator = models.ForeignKey(Operator, on_delete=models.CASCADE)
    user = models.ForeignKey(TelegramUser, on_delete=models.CASCADE)
    user_full_name = models.CharField(max_length=255)
    comment = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.user} by {self.operator}'

    def dict(self):
        return {
            'id': self.id,
            'operator_id': self.operator.telegram_id,
            'user_id': self.user.telegram_id,
            'user_full_name': self.user_full_name,
            'comment': self.comment,
        }

    
class MailingMessage(models.Model):
    class Meta:
        verbose_name = 'Mailing Message'
        verbose_name_plural = 'Mailing Messages'
        db_table = 'mailing_message'
    
    id = models.AutoField(primary_key=True) 
    message = models.CharField(max_length=255)
    photo_id = models.CharField(max_length=255, null=True, blank=True)
    created_time = models.DateTimeField(auto_now_add=True)

    
    def __str__(self):
        return f'{self.id}'

    def dict(self):
        return {
            'id': self.id,
            'message': self.message,
            'photo_id': self.photo_id,
            'created_time': self.created_time,
        }

class Admin(models.Model):
    
    telegram_id = models.BigIntegerField(unique=True, primary_key=True)
    invite_code = models.CharField(max_length=255,)


class FastResponse(models.Model):
    text = models.TextField()

    def dict(self):
        return {
            "id": self.id,
            "text": self.text,
        }