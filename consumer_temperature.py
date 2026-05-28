import rabbitpy, json
from const import RABBITMQ_ADDR, amqp_url

ALERT_THRESHOLD = 80.0

with rabbitpy.Connection(amqp_url(RABBITMQ_ADDR)) as conn:
    with conn.channel() as channel:
        queue = rabbitpy.Queue(channel, "temperature", durable=True, auto_delete=False)
        queue.declare()

        print("Temperature consumer started. Waiting for messages...")
        for message in queue:
            data = json.loads(message.body.decode())
            value = data["value"]
            print(f"[TEMPERATURE] {data['timestamp']} → {value}°C")
            if value > ALERT_THRESHOLD:
                print(f"  ⚠ ALERT: Temperature too high ({value}°C)! Activating cooling system...")
            message.ack()