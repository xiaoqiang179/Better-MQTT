import mqtt_client as client

if __name__ == '__main__':
    client.HOST_NAME = "114.215.81.164"
    client.PORT = 1883
    client.USER_NAME = 'admin'
    client.PASSWORD = 'admin123'
    client.connect()
    client.subscribe('#')
    client.start_loop()
