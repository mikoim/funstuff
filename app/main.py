from websocket import create_connection


def main(argv):
    ws = create_connection("ws://challenge-server.code-check.io/api/websocket/hello")
    name = ' '.join(ws.recv().split(' ')[2:])
    ws.send(f'Hello, {name}')
    print(ws.recv())
    ws.close()
