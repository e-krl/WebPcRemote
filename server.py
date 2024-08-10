import asyncio
import socket
import websockets
import json
from pynput.keyboard import Key, Controller
from pynput.mouse import Controller as MouseController, Button

PORT = 2000
keyboard = Controller()
mouse = MouseController()

special_keys = {
    'enter': Key.enter,
    'space': Key.space,
    'shift': Key.shift,
    'ctrl': Key.ctrl,
    'alt': Key.alt,
    'tab': Key.tab,
    'esc': Key.esc,
    'backspace': Key.backspace,
    'left': Key.left,
    'right': Key.right,
    'up': Key.up,
    'down': Key.down,
    'delete': Key.delete,
}

class actionTypes:
    mouse_click_left = "0"
    mouse_click_left_hold = "1"
    mouse_click_middle = "2"
    mouse_click_right = "3"
    mouse_click_right_hold = "4"
    mouse_roll = "5"
    trackpad = "6"
    keydown = "7"
    keyup = "8"

async def handle_client(websocket, path):
    async for message in websocket:
        print(f"Received: {message}")

        try:
            data = json.loads(message)
            print(data)
            process_input(data)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")

        response = "Message received"
        await websocket.send(response)

def process_input(data):
    try:
        action = data['action']
        if action == actionTypes.trackpad:
            trackpad_data = data['data']
            deltaX = trackpad_data['deltaX']
            deltaY = trackpad_data['deltaY']
            mouse.move(deltaX, deltaY)
        elif action == actionTypes.mouse_click_left:
            mouse.click(Button.left)
        elif action == actionTypes.mouse_click_right:
            mouse.click(Button.right)
        elif action == actionTypes.keydown:
            key = data['data'].lower()
            if key in special_keys:
                keyboard.press(special_keys[key])
            else:
                keyboard.press(key)
        elif action == actionTypes.keyup:
            key = data['data'].lower()
            if key in special_keys:
                keyboard.release(special_keys[key])
            else:
                keyboard.release(key)
        else:
            print(f"Unknown action: {action}")
    except Exception as e:
        print(f"Error processing input: {e}")
    finally:
        print("Processing complete.")

def wlan_ip():
    import subprocess
    result=subprocess.run('ipconfig',stdout=subprocess.PIPE,text=True).stdout.lower()
    scan=0
    for i in result.split('\n'):
        if 'wireless' in i: scan=1
        if scan:
            if 'ipv4' in i: return i.split(':')[1].strip()

def find_free_port(starting_port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        while True:
            try:
                s.bind(("", starting_port))
                return starting_port
            except OSError:
                starting_port += 1

def main():
    global PORT
    PORT = find_free_port(PORT)
    
    start_server = websockets.serve(handle_client, "0.0.0.0", PORT)
    asyncio.get_event_loop().run_until_complete(start_server)
    print(f"Server started on ws://{wlan_ip()}:{PORT}")
    asyncio.get_event_loop().run_forever()

if __name__ == "__main__":
    main()
