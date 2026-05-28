import rabbitpy, json
from const import RABBITMQ_ADDR, amqp_url

ALERT_THRESHOLD = 90.0

with rabbitpy.Connection(amqp_url(RABBITMQ_ADDR)) as conn:
    with conn.channel() as channel:
        queue = rabbitpy.Queue(channel, "humidity", durable=True, auto_delete=False)
        queue.declare()

        print("Humidity consumer started. Waiting for messages...")
        for message in queue:
            data = json.loads(message.body.decode())
            value = data["value"]
            print(f"[HUMIDITY] {data['timestamp']} → {value}%")
            if value > ALERT_THRESHOLD:
                print(f"  ⚠ ALERT: Humidity too high ({value}%)! Activating dehumidifier...")
            message.ack()