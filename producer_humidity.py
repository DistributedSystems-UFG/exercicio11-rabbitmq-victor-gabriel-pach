import rabbitpy, time, random
from const import RABBITMQ_ADDR, amqp_url
from datetime import datetime

with rabbitpy.Connection(amqp_url(RABBITMQ_ADDR)) as conn:
    with conn.channel() as channel:
        exchange = rabbitpy.Exchange(channel, "factory-exchange", exchange_type="direct")
        exchange.declare()

        queue = rabbitpy.Queue(channel, "humidity", durable=True, auto_delete=False)
        queue.declare()
        queue.bind(exchange, "humidity")

        print("Humidity producer started...")
        while True:
            humidity = round(random.uniform(30.0, 100.0), 2)
            payload = f'{{"sensor": "humidity", "value": {humidity}, "unit": "%", "timestamp": "{datetime.utcnow().isoformat()}"}}'
            msg = rabbitpy.Message(channel, payload, {"content_type": "application/json"})
            msg.publish(exchange, "humidity")
            print(f"Published humidity: {humidity}%")
            time.sleep(4)