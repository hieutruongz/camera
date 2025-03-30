import cv2
import socket
import base64

# Set up socket for streaming
BUFF_SIZE = 65536
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFF_SIZE)

# Replace with Jetson Nano’s IP
host_ip = '192.168.1.100'  # Change to your Jetson Nano's IP
port = 8888
server_socket.bind((host_ip, port))
print(f"Server listening on {host_ip}:{port}")

# Open Camera (PiCamera or USB Camera)
cap = cv2.VideoCapture(0)  # Use 0 for default camera

# Adjust frame size for better performance
cap.set(3, 640)  # Width
cap.set(4, 480)  # Height

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            continue
        
        # Encode frame
        _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 50])
        message = base64.b64encode(buffer)

        # Ensure packet size is within limit
        if len(message) > BUFF_SIZE:
            print("Frame size too large, adjust resolution or quality.")
            continue

        # Send frame to client
        server_socket.sendto(message, ('<client-ip>', 9999))  # Replace with client IP

except KeyboardInterrupt:
    print("\nServer stopped.")

finally:
    cap.release()
    server_socket.close()
