import rabbitpy, time, random
from const import RABBITMQ_ADDR, amqp_url
from datetime import datetime

with rabbitpy.Connection(amqp_url(RABBITMQ_ADDR)) as conn:
    with conn.channel() as channel:
        exchange = rabbitpy.Exchange(channel, "factory-exchange", exchange_type="direct")
        exchange.declare()

        queue = rabbitpy.Queue(channel, "pressure", durable=True, auto_delete=False)
        queue.declare()
        queue.bind(exchange, "pressure")

        print("Pressure producer started...")
        while True:
            pressure = round(random.uniform(1.0, 15.0), 2)
            payload = f'{{"sensor": "pressure", "value": {pressure}, "unit": "bar", "timestamp": "{datetime.utcnow().isoformat()}"}}'
            msg = rabbitpy.Message(channel, payload, {"content_type": "application/json"})
            msg.publish(exchange, "pressure")
            print(f"Published pressure: {pressure} bar")
            time.sleep(5)