import cv2
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading

# Path to the video file (ensure this path is correct for your setup)
video_path = 'C:/Users/Lenovo/hotel management/videos/normal.mp4'  # Make sure the path to your video is correct

# OpenCV video capture
cap = cv2.VideoCapture(video_path)

# Check if the video opened correctly
if not cap.isOpened():
    print("Error: Could not open video.")
    exit()

# HTTP handler for serving video stream
class VideoStreamHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/video_feed':
            self.send_response(200)
            self.send_header('Content-type', 'multipart/x-mixed-replace; boundary=frame')
            self.end_headers()
            
            # Stream video frames to the browser
            while True:
                ret, frame = cap.read()
                if not ret:
                    print("Error: Failed to capture frame.")
                    break
                
                # Encode frame as JPEG
                ret, jpeg = cv2.imencode('.jpg', frame)
                if not ret:
                    print("Error: Failed to encode frame.")
                    break
                
                # Write frame to HTTP response
                self.wfile.write(b'--frame\r\n')
                self.wfile.write(b'Content-Type: image/jpeg\r\n\r\n')
                self.wfile.write(jpeg.tobytes())
                self.wfile.write(b'\r\n')

            # Reset the video capture to the first frame if it finishes
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        else:
            self.send_response(404)
            self.end_headers()

# Start HTTP server to stream video
def start_server():
    server_address = ('', 8000)  # Local server on port 8000
    httpd = HTTPServer(server_address, VideoStreamHandler)
    print("Server running at http://192.168.0.106:8000")  # Your IP address
    httpd.serve_forever()

# Run the server in a separate thread to keep the main thread free
thread = threading.Thread(target=start_server)
thread.daemon = True
thread.start()

# Keep the main program running
input("Press Enter to stop the server...\n")
