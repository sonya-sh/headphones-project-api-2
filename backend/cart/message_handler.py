from cart.models import Cart

from django_redis import get_redis_connection

def handle_user_registration_message(user_id):
    Cart.objects.create(user_id=user_id)
    print("Received user registration message:", user_id)

def subscribe_to_user_registration_channel():
    redis_connection = get_redis_connection()
    pubsub = redis_connection.pubsub()
    pubsub.subscribe('user_registration')
    for message in pubsub.listen():
        if message['type'] == 'message':
            handle_user_registration_message(message['data'])