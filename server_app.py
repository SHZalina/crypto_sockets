import os
import sys
sys.path.append(os.getcwd())
from frontend.ui import Server

server = Server()
server.run_app()
