from picamera2 import Picamera2
import cv2, socket, base64, time
import numpy as np

BUFF_SIZE = 65536
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_ip = '192.168.4.3'  # Raspberry Pi's IP
port = 8888
server_socket.bind((host_ip, port))
server_socket.listen(1)

print(f"Server listening at: {host_ip}:{port}")

picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"size": (640, 480)}))  # Smaller size for stability
picam2.start()

try:
    print("Waiting for a client...")
    client_socket, client_addr = server_socket.accept()
    print("Connection established with:", client_addr)

    while True:
        frame = picam2.capture_array()
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 50])  # Lower quality for smaller size
        message = base64.b64encode(buffer)

        client_socket.sendall(message)

except KeyboardInterrupt:
    print("\nServer stopped by user.")

finally:
    picam2.stop()
    server_socket.close()
    print("Resources released.")
