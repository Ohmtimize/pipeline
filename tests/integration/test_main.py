import sys

# Add the parent directory to the path
# This allows tests to be run from any directory
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.append("src")

import src.main as main
from paho.mqtt.client import Client
import socket

from src.mysqlDriver import MysqlDB


# def test_main(capfd):
#     main.main()
#     captured = capfd.readouterr()
#     assert "Success" and "Disconnecting" in captured.out
