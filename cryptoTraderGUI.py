# GUI

"""
Created on Fri Dec  1 23:03:05 2017

@author: JAK
"""

# Import Libraries
from __future__ import print_function
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction, QLineEdit, QMessageBox, QLabel
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
    
import json
import base64
import hmac
import hashlib
import time
from threading import Thread
from websocket import create_connection, WebSocketConnectionClosedException
from pymongo import MongoClient
import gdax
#from gdax.gdax_auth import get_auth_headers

class MyWebsocketClient(gdax.WebsocketClient):
    
    #GUIInstance = CryptoTraderGUI
    
    #def __init__(self, GUIInstance):
    #self.GUIInstance = GUIInstance
        
    def on_open(self):
        self.url = "wss://ws-feed.gdax.com/"
        self.products = ["BTC-USD"]
        self.message_count = 0

    def on_message(self, msg):
        if self.GUIInstance:
            if 'price' in msg:
                self.GUIInstance.BTCPriceLabel.setText(msg['price'])
                    
    def on_close(self):
        print("-- Goodbye! --")
        
            

""" ----------GUI Class---------- """

class CryptoTraderGUI(QWidget):
    
    import GDAXWebsocketClient as WebsocketClient
 
    def __init__(self):
        super().__init__()
        self.title = 'Crypto Trader v0.1'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.initUI()
        
        self.public_client = gdax.PublicClient()
        
        # Create websocket connection 
        self.wsClient = MyWebsocketClient()
        self.wsClient.GUIInstance = self
 
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        # Create textbox
        self.BTCPriceLabel = QLabel("0.0", self)
        self.BTCPriceLabel.move(80, 80)
        self.BTCPriceLabel.resize(280,40)
        self.BTCPriceLabel.setStyleSheet("QLabel {background-color: red;}")
 
        self.StreamButton = QPushButton("Start Data Stream", self)
        self.StreamButton.move(20,20)
        self.StreamButton.clicked.connect(self.on_click_start)
        
        self.StopStreamButton = QPushButton("Stop Data Stream", self)
        self.StopStreamButton.move (200,20)
        self.StopStreamButton.setEnabled(0)
        self.StopStreamButton.clicked.connect(self.on_click_stop)
        
        self.show()
    
    @pyqtSlot()
    def on_click_start(self):
        
        self.startPriceStream()
        
        self.BTCPriceLabel.setText("Stream Started")
        self.StreamButton.setEnabled(0)
        self.StopStreamButton.setEnabled(1)
        
    @pyqtSlot()
    def on_click_stop(self):
        
        self.stopPriceStream()
        
        self.BTCPriceLabel.setText("Stream Stopped")
        self.StreamButton.setEnabled(1)
        self.StopStreamButton.setEnabled(0)
        
    

    def pollGDAX(self):
        #import threading
        #threading.Timer(5.0, pollGDAX).start()
        #msg = self.public_client.get_product_ticker(product_id='ETH-USD')
        #self.BTCPriceLabel.setText(self.msg)
        print(msg)


    def startPriceStream(self):
        self.wsClient.start()
        #print(self.wsClient.url, self.wsClient.products)
        
    def stopPriceStream(self):
        self.wsClient.stop()
        self.wsClient.close()





""" ----------MAIN PROGRAM---------- """

if __name__ == "__main__":


    
    
    app = QApplication(sys.argv)
    ex = CryptoTraderGUI()
    sys.exit(app.exec_())

"""
    try:
        while True:
            print("\nMessageCount =", "%i \n" % wsClient.message_count)
            time.sleep(1)
    except KeyboardInterrupt:
        wsClient.close()
        
    if wsClient.error:
        sys.exit(1)
    else:
        sys.exit(0)
"""
