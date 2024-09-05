import socket

def check_port(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        result = s.connect_ex(('127.0.0.1', port))
    return result == 0

# Check port 8000
port = 8000
is_open = check_port(port)
print(f"Port {port} is {'open' if is_open else 'closed'}")