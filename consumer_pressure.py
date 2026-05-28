import rabbitpy, json
from const import RABBITMQ_ADDR, amqp_url

ALERT_THRESHOLD = 10.0

with rabbitpy.Connection(amqp_url(RABBITMQ_ADDR)) as conn:
    with conn.channel() as channel:
        queue = rabbitpy.Queue(channel, "pressure", durable=True, auto_delete=False)
        queue.declare()

        print("Pressure consumer started. Waiting for messages...")
        for message in queue:
            data = json.loads(message.body.decode())
            value = data["value"]
            print(f"[PRESSURE] {data['timestamp']} → {value} bar")
            if value > ALERT_THRESHOLD:
                print(f"  ⚠ ALERT: Pressure critical ({value} bar)! Triggering pressure relief valve...")
            message.ack()