from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.core.validators import RegexValidator

# Create your models here

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError('O email é obrigatório')
        user = self.model(
            username=username,
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, email, password=None):
        user = self.create_user(
            username=username,
            email=email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractUser):
    cpf = models.CharField(
        max_length=11, 
        unique=True, 
        validators=[
            RegexValidator(regex=r'^\d{11}$', message="CPF deve conter 11 dígitos numéricos.")
        ]
    )
    
    phone = models.CharField(
        max_length=11,
        validators=[
            RegexValidator(regex=r'^\d{10,11}$', message="Telefone deve ter 10 ou 11 dígitos.")
        ]
    )
    
    session_key = models.CharField(max_length=40, blank=True, null=True)
    
    groups = models.ManyToManyField(
        "auth.Group", 
        related_name="custom_user_set",  # Resolve o conflito
        blank=True
    )

    user_permissions = models.ManyToManyField(
        "auth.Permission", 
        related_name="custom_user_permissions_set",  # Resolve o conflito
        blank=True
    )
    
    payment = models.OneToOneField('Payment', on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return self.username

class Payment(models.Model):
    PAYMENT_METHODS = [
        ('nenhum', 'Nenhum'),
        ('pix', 'Pix'),
        ('boleto', 'Boleto'),
        ('cartao', 'Cartão de Crédito'),
        ('paypal', 'PayPal'),
    ]

    method = models.CharField(max_length=50, choices=PAYMENT_METHODS)
    payment_date = models.DateField(null=True, blank=True)
    is_paid = models.BooleanField(default=False)  
    subscribed_plan = models.CharField(max_length=50, null=True)

    def __str__(self):
        status = "Pago" if self.is_paid else "Pendente"
        return f"Pagamento - {self.get_method_display()} ({status})"
    