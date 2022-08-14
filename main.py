import subprocess as sprc
import signal, os, json

json_devices = open('devices.json', 'r')
IP_LIST = json.load(json_devices)


def clear_screen():
    if os.name == 'posix':
        os.system('clear')
    elif os.name == 'nt':
        os.system('cls')

def signal_handler(signum, frame):
    raise Exception("Timed out!")

def is_connected(DEVICE_IP):
    proc = sprc.Popen(['ping', DEVICE_IP], stdout = sprc.PIPE)

    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(3)

    ping = None

    try:
        ping = proc.stdout.readline()
    except:
        pass

    try:
        ip = ping.decode('utf-8').split()[1]
    except:
        ip = None

    if ip == DEVICE_IP:
        return True
    else:
        return False

while True:
    print('-=' * 15)
    for IP in IP_LIST:
        print('Device IP:     ', IP['adress'])
        print('Device Name:   ', IP['name'])
        print('Device Status: ', IP['status'])
        print()

    for IP in IP_LIST:
        if is_connected(IP['adress']):
            IP['status'] = 'Connected'
        else:
            IP['status'] = 'Disconnected'
    clear_screen()
