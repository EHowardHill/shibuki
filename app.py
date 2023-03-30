import socket
import threading
import random
from datetime import datetime
from operator import itemgetter
from json import loads

servers = []
count = 0
with open("servers.txt", "r") as f:
    for local in f.readlines():
        print(local)
        servers.append({
            "id": count,
            "ip": local[:local.index(":")],
            "port": int(local[local.index(":")+1:]),
            "buffer": 65536
        })
        count += 1

print("Servers in fleet:")

servers_active = {}
for server in servers:
    print(server)
    servers_active[server["id"]] = 0
print()

with open("config.json", "r") as config:
    config_data = loads('\n'.join(config.readlines()))
    proxy_ip = config_data["ip"]
    proxy_port = int(config_data["port"])

proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

proxy_socket.bind((proxy_ip, proxy_port))
proxy_socket.listen(1)

print(f"Shibuki server listening on {proxy_ip}:{proxy_port}")

def resolve(client_socket):

    prior_weight = 0
    active = sorted(servers_active.items(), key=lambda x: x[1])
    server = [s for s in servers if s["id"] == active[0][0]][0]
    prior_weight += 1
    servers_active[server["id"]] += 1

    request_no = str(random.randint(1000, 9999)) + " (" + server["ip"] + ":" + str(server["port"]) + ")\t"
    print(request_no + "deploying\t" + str(datetime.now()))

    try:
        request = client_socket.recv(server["buffer"])
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.connect((server["ip"], server["port"]))
        server_socket.sendall(request)

        response = b""
        while True:
            data = server_socket.recv(server["buffer"])
            if not data:
                break
            response += data
            prior_weight += 1
            servers_active[server["id"]] += 1

        server_socket.close()
        client_socket.sendall(response)
        client_socket.close()
        servers_active[server["id"]] -= prior_weight

        print(request_no + "returning\t" + str(datetime.now()))

    except Exception as e:
        print(request_no + "failure\t" + str(datetime.now()))
        print("\t" + str(e).replace("\n", "\n\t"))

while True:
    client_socket, client_address = proxy_socket.accept()
    print(f"📧 Received:\t{client_address}")
    x = threading.Thread(target=resolve, args=(client_socket,))
    x.start()