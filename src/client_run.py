import asyncio
import http.server
import socketserver
import subprocess
import webbrowser
import time
import subprocess
# from playwright.async_api import async_playwright

# def start_server():
#     Handler = http.server.SimpleHTTPRequestHandler
#     with socketserver.TCPServer( ("", PORT ), Handler ) as httpd:
#         print( f"Server started at http://localhost:{PORT}" )
#         httpd.serve_forever()

# python3 src/client_run.py
if __name__ == "__main__":

    dir_path = r"<PATH_TO_CLIENT_FOLDER>"
    port = "8000"

    server_process = subprocess.Popen(
        f"python -m http.server {port} -d {dir_path}",
        shell = True
    )

    print( "Server is starting..." )
    time.sleep( 2 )

    for i in range( 1 ):
        webbrowser.open( f"http://localhost:{port}" )

    try:
        while True:
            time.sleep( 1 )
    except KeyboardInterrupt:
        print( "Shutting down the server..." )
        server_process.terminate()

    # subprocess.run( "start http://localhost:8000", shell = True )
    # asyncio.run( main() )