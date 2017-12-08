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
import time
from threading import Thread
from websocket import create_connection, WebSocketConnectionClosedException
from pymongo import MongoClient
import gdax
#from gdax.gdax_auth import get_auth_headers

""" ----------Websocket Subclass---------- """

class MyWebsocketClient(gdax.WebsocketClient):
    
    #GUIInstance = CryptoTraderGUI
    
    #def __init__(self, GUIInstance):
    #self.GUIInstance = GUIInstance
        
    def on_open(self):
        self.url = "wss://ws-feed.gdax.com/"
        self.products = ["BTC-USD", "ETH-USD"]
        self.message_count = 0

    def on_message(self, msg):
        if self.GUIInstance:
            if msg['type'] == "match":
                
                price = msg['price']                
                i_decimal = price.index('.')
                formattedPrice = price[0:i_decimal+3]
                
                if msg['product_id'] == "BTC-USD":
                    self.GUIInstance.BTCPriceLabel.setText(formattedPrice)
                    self.GUIInstance.currentPriceBTC = float(formattedPrice)
                elif msg['product_id'] == "ETH-USD":
                    self.GUIInstance.ETHPriceLabel.setText(formattedPrice)
                    
                self.GUIInstance.checkTriggers()
                    
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
        self.initVariables()
        
        #self.public_client = gdax.PublicClient()
        #self.pollGDAX()
 
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        # Current Price Labels
        self.BTCPriceLabel = QLabel("0.0", self)
        self.BTCPriceLabel.move(self.width/2-125, self.height/2-20)
        self.BTCPriceLabel.resize(100,40)
        #self.BTCPriceLabel.setStyleSheet("QLabel {background-color: red;}")
        self.BTCLabel = QLabel("BTC-USD", self)
        self.BTCLabel.move(self.width/2-125, self.height/2+20)
        self.BTCLabel.resize(100,40)
        
        self.ETHPriceLabel = QLabel("0.0", self)
        self.ETHPriceLabel.move(self.width/2+25, self.height/2-20)
        self.ETHPriceLabel.resize(100,40)
        #self.ETHPriceLabel.setStyleSheet("QLabel {background-color: red;}")
        
        self.ETHLabel = QLabel("ETH-USD", self)
        self.ETHLabel.move(self.width/2+25, self.height/2+20)
        self.ETHLabel.resize(100,40)
        
        # Websocket Stream Buttons
        self.StreamButton = QPushButton("Start Data Stream", self)
        self.StreamButton.move(20,20)
        self.StreamButton.clicked.connect(self.on_click_start)
        
        self.StopStreamButton = QPushButton("Stop Data Stream", self)
        self.StopStreamButton.move (200,20)
        self.StopStreamButton.setEnabled(0)
        self.StopStreamButton.clicked.connect(self.on_click_stop)
        
        # Trip Inputs
        self.UpperTriggerPriceInput = QLineEdit("", self)
        self.UpperTriggerPriceInput.move(self.width/2-260, self.height/2-80)
        self.UpperTriggerPriceInput.resize(150,40)
        
        self.LowerTriggerPriceInput = QLineEdit("", self)
        self.LowerTriggerPriceInput.move(self.width/2-260, self.height/2+80)
        self.LowerTriggerPriceInput.resize(150,40)
        
        self.UpperTriggerPriceLabel = QLabel("None", self)
        self.UpperTriggerPriceLabel.move(self.width/2-100, self.height/2-80)
        self.UpperTriggerPriceLabel.resize(75,40)
        
        self.LowerTriggerPriceLabel = QLabel("None", self)
        self.LowerTriggerPriceLabel.move(self.width/2-100, self.height/2+80)
        self.LowerTriggerPriceLabel.resize(75,40)
        
        self.setUpperTriggerButton = QPushButton("Set", self)
        self.setUpperTriggerButton.move(self.width/2-300, self.height/2-80)
        self.setUpperTriggerButton.resize(40,40)
        self.setUpperTriggerButton.clicked.connect(self.on_click_set_upper_trigger)
        self.setUpperTriggerButton.setEnabled(0)
        
        self.setLowerTriggerButton = QPushButton("Set", self)
        self.setLowerTriggerButton.move(self.width/2-300, self.height/2+80)
        self.setLowerTriggerButton.resize(40,40)
        self.setLowerTriggerButton.clicked.connect(self.on_click_set_lower_trigger)
        self.setLowerTriggerButton.setEnabled(0)
        
        self.show()
        
    def initVariables(self):
        self.upperTriggerPrice = 1000000.00
        self.lowerTriggerPrice = 1.00
        self.currentPriceBTC = 10000.0
        self.isUpperTriggered = 0
        self.isUpperTriggered = 0
        
    def checkTriggers(self):
        
        
        if self.currentPriceBTC > self.upperTriggerPrice :
            time.sleep(3)
            if self.currentPriceBTC > self.upperTriggerPrice :
                if self.isUpperTriggered == 0 :
                    self.triggerUpper()
            
        if self.currentPriceBTC < self.lowerTriggerPrice :
            time.sleep(3)
            if self.currentPriceBTC < self.lowerTriggerPrice :
                if self.isLowerTriggered == 0 :
                    self.triggerLower()
            
            
    def triggerUpper(self):
        self.isUpperTriggered = 1
        self.UpperTriggerPriceLabel.setStyleSheet("QLabel {background-color: red;}")
    
    def triggerLower(self):
        self.isLowerTriggered = 1
        self.LowerTriggerPriceLabel.setStyleSheet("QLabel {background-color: red;}")
        
    @pyqtSlot()
    def on_click_start(self):
        
         # Create websocket connection 
        self.wsClient = MyWebsocketClient()
        self.wsClient.GUIInstance = self
        
        self.startPriceStream()
        
        self.BTCPriceLabel.setText("Stream Started")
        self.ETHPriceLabel.setText("Stream Started")
        self.StreamButton.setEnabled(0)
        self.StopStreamButton.setEnabled(1)
        self.setUpperTriggerButton.setEnabled(1)
        self.setLowerTriggerButton.setEnabled(1)
        
    @pyqtSlot()
    def on_click_stop(self):
        
        self.stopPriceStream()
        
        self.BTCPriceLabel.setText("Stream Stopped")
        self.ETHPriceLabel.setText("Stream Stopped")
        self.StreamButton.setEnabled(1)
        self.StopStreamButton.setEnabled(0)
        self.setUpperTriggerButton.setEnabled(0)
        self.setLowerTriggerButton.setEnabled(0)
        
    @pyqtSlot()
    def on_click_set_upper_trigger(self):
        
        upperTriggerString = self.UpperTriggerPriceInput.text()
        x = float(upperTriggerString)
        
        if x > self.currentPriceBTC :
            self.upperTriggerPrice = x
            self.UpperTriggerPriceLabel.setText(upperTriggerString)
            self.isUpperTriggered = 0
        
    @pyqtSlot()
    def on_click_set_lower_trigger(self):
        
        lowerTriggerString = self.LowerTriggerPriceInput.text()
        x = float(lowerTriggerString)
        
        if x < self.currentPriceBTC :
            self.lowerTriggerPrice = x
            self.LowerTriggerPriceLabel.setText(lowerTriggerString)
            self.isLowerTriggered = 0
            

    def pollGDAX(self):
        #import threading
        #threading.Timer(1.0, self.pollGDAX).start()
        msg = self.public_client.get_product_ticker(product_id='BTC-USD')
        self.BTCPriceLabel.setText(msg['price'])
        msg = self.public_client.get_product_ticker(product_id='ETH-USD')
        self.ETHPriceLabel.setText(msg['price'])

    def startPriceStream(self):
        self.wsClient.start()
        #print(self.wsClient.url, self.wsClient.products)
        
    def stopPriceStream(self):
        self.wsClient.close()
        
        if self.wsClient.error:
            sys.exit(1)
        else:
            sys.exit(0)





""" ----------MAIN PROGRAM---------- """

if __name__ == "__main__":
    
    app=0
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
