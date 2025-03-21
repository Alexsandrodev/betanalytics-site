from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, Payment
from django.contrib.auth.signals import user_logged_in
from django.contrib.sessions.models import Session
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_payment_for_user(sender, instance, created, **kwargs):
    if created and instance.payment is None:  # Garante que só cria um Payment na criação
        payment = Payment.objects.create(method="nenhum")
        instance.payment = payment
        instance.save()  # Atualiza o usuário com o Payment recém-criado
        print(f"Payment created for user {instance.username}.")
        
    
@receiver(user_logged_in)
def logout_other_sessions(sender, request, user, **kwargs):
    if user.session_key:
        try:
            Session.objects.get(session_key=user.session_key).delete()
        except Session.DoesNotExist:
            pass
        
    request.session.save()
    user.session_key = request.session.session_key
    user.save()