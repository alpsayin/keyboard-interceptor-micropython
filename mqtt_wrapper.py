import time
from umqtt.simple import MQTTClient

# Publish test messages e.g. with:
# mosquitto_pub -t foo_topic -m hello
blocking_wait = False
mqtt_client = None


# Received messages from subscriptions will be delivered to this callback
def simple_sub_cb(topic, msg):
    print((topic, msg))


def init(client_id, hostname='alpcer0.local', sub_topic='kybIntcpt', callback=simple_sub_cb):
    global mqtt_client
    mqtt_client = MQTTClient(client_id, hostname)
    mqtt_client.set_callback(callback)
    mqtt_client.connect()
    mqtt_client.subscribe(sub_topic)
    mqtt_client.ping()
    mqtt_client.wait_msg()

def main(server="alpcer0.local"):
    global blocking_wait
    c = MQTTClient("umqtt_client", server)
    c.set_callback(simple_sub_cb)
    c.connect()
    c.subscribe(b"foo_topic")
    while True:
        if blocking_wait:
            # Blocking wait for message
            c.wait_msg()
            c.publish(b'bar_topic', b'received a message')
        else:
            c.publish(b'bar_topic', b'checking for messages')
            # Non-blocking wait for message
            c.check_msg()
            # Then need to sleep to avoid 100% CPU usage (in a real
            # app other useful actions would be performed instead)
            time.sleep(1)

    c.disconnect()


if __name__ == "__main__":
    main()
