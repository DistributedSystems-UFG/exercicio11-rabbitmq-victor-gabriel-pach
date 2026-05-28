RABBITMQ_ADDR = "ip_do_servidor"
RABBITMQ_USER = "myuser"
RABBITMQ_PASS = "abc123"
RABBITMQ_VHOST = "my_vhost"

def amqp_url(host):
    return f"amqp://{RABBITMQ_USER}:{RABBITMQ_PASS}@{host}:5672/{RABBITMQ_VHOST}"