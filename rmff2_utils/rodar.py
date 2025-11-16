#inicia 2 clientes automaticamente

import subprocess
import time

# Inicia o servidor
server = subprocess.Popen(["python", "server.py"])

time.sleep(2)

# Inicia dois clientes
client1 = subprocess.Popen(["python", "client.py"])
client2 = subprocess.Popen(["python", "client.py"])

client1.wait()
client2.wait()
server.kill()
