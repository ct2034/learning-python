"""
This needs a MQTT broker. E.g.

```
docker run -p 8081:8080 -p 1883:1883 hivemq/hivemq4:latest
```

"""

import asyncio
import random
import paho.mqtt.client as mqtt

MQTT_BROKER_HOST = "localhost"
MQTT_BROKER_PORT = 1883
MQTT_TOPIC = "test/topic"


async def publisher():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.connect(MQTT_BROKER_HOST, MQTT_BROKER_PORT, 60)

    try:
        while True:
            value = random.randint(0, 100)
            print(f"Publishing: {value}")
            client.publish(MQTT_TOPIC, value)
            await asyncio.sleep(1)
    except Exception as e:
        print(f"Closing publisher: {e}")
        client.disconnect()


async def subscriber():
    def on_message(client, userdata, msg):
        print(f"Received: {msg.payload.decode()}, ({client=}, {userdata=}, {msg=})")

    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.on_message = on_message
    client.connect(MQTT_BROKER_HOST, MQTT_BROKER_PORT, 60)
    client.subscribe(MQTT_TOPIC)
    client.loop_start()  # Start the MQTT client loop

    try:
        while True:
            await asyncio.sleep(1)
    except Exception as e:
        print(f"Closing subscriber: {e}")
        client.loop_stop()
        client.disconnect()


async def main():
    publisher_task = asyncio.create_task(publisher())
    subscriber_task = asyncio.create_task(subscriber())

    try:
        await asyncio.gather(publisher_task, subscriber_task)
    finally:
        print("\nShutting main...")
        publisher_task.cancel()
        subscriber_task.cancel()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nShutting down due to KeyboardInterrupt...")
