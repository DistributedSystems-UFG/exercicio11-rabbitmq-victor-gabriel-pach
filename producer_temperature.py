import rabbitpy, time, random
from const import RABBITMQ_ADDR, amqp_url
from datetime import datetime

with rabbitpy.Connection(amqp_url(RABBITMQ_ADDR)) as conn:
    with conn.channel() as channel:
        exchange = rabbitpy.Exchange(channel, "factory-exchange", exchange_type="direct")
        exchange.declare()

        queue = rabbitpy.Queue(channel, "temperature", durable=True, auto_delete=False)
        queue.declare()
        queue.bind(exchange, "temperature")

        print("Temperature producer started...")
        while True:
            temp = round(random.uniform(20.0, 100.0), 2)
            payload = f'{{"sensor": "temperature", "value": {temp}, "unit": "C", "timestamp": "{datetime.utcnow().isoformat()}"}}'
            msg = rabbitpy.Message(channel, payload, {"content_type": "application/json"})
            msg.publish(exchange, "temperature")
            print(f"Published temperature: {temp}°C")
            time.sleep(3)