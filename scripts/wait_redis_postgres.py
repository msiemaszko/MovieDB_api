import os
import socket
import time

postgres = (os.environ["DB_HOST"], int(os.environ["DB_PORT"]))
s_postgres = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# redis = (os.environ["REDIS_HOST"], int(os.environ["REDIS_PORT"]))
# s_redis = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

time.sleep(5)

while True:
    try:
        s_postgres.connect(postgres)
        s_postgres.close()
        # s_redis.connect(redis)
        # s_redis.close()
        break
    except socket.error:
        time.sleep(1)
