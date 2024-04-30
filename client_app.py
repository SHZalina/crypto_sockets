import os
import sys
sys.path.append(os.getcwd())
from frontend.ui import Client

client = Client()
client.run_app()
