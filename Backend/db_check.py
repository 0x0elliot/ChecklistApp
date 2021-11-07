import os 

if not os.path.exists("/opt/API/migrations"):
    os.system("python3 manager.py db init")
