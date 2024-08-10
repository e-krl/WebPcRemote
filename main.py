import subprocess
import time

def start_http_server():
    print("Starting HTTP server...")
    subprocess.Popen(["python", "client.py"])

def start_websocket_server():
    print("Starting WebSocket server...")
    subprocess.Popen(["python", "server.py"])

if __name__ == "__main__":
    start_http_server()
    time.sleep(1)
    start_websocket_server()

    print("Both servers started successfully.")
