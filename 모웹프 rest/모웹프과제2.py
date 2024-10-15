import os
import socket
from datetime import datetime

class SocketServer:
    def __init__(self):
        self.bufsize = 4096  # 버퍼 크기를 늘려서 큰 요청을 처리
        self.DIR_PATH = './request'
        self.createDir(self.DIR_PATH)

        self.IMAGE_DIR = './images'
        self.createDir(self.IMAGE_DIR)

    def createDir(self, path):
        """디렉토리 생성"""
        if not os.path.exists(path):
            os.makedirs(path)

    def run(self, ip, port):
        """서버 실행"""
        self.sock = socket.socket()
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((ip, port))
        self.sock.listen(10)
        print("Start the socket server ...")
        print("\"Ctrl+C\" for stopping the server!\r\n")

        try:
            while True:
                cInt_sock, req_addr = self.sock.accept()
                cInt_sock.settimeout(5.0)
                print("Request received...")

                # 요청 데이터 수신
                request_data = b""
                while True:
                    part = cInt_sock.recv(self.bufsize)
                    request_data += part
                    if len(part) < self.bufsize:
                        break

                # 요청 데이터 저장
                timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
                with open(os.path.join(self.DIR_PATH, f"{timestamp}.bin"), 'wb') as f:
                    f.write(request_data)

                # 멀티파트 데이터 처리
                boundary = b'--' + request_data.split(b'\r\n')[0]
                parts = request_data.split(boundary)[1:]

                for part in parts:
                    if b'Content-Disposition' in part:
                        disposition = part.split(b'\r\n\r\n')[0]
                        filename = self.get_filename(disposition)
                        if filename:
                            image_data = part.split(b'\r\n\r\n')[1].split(b'\r\n--')[0]
                            with open(os.path.join(self.IMAGE_DIR, filename), 'wb') as img_file:
                                img_file.write(image_data)

                # 응답 전송
                response = b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nRequest receive