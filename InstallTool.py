#!/bin/env python
# -*- encoding: utf-8 -*-

##
#   @file InstallTool.py
#   @brief インストール支援ツール



import thread



import sys,os,platform
import re
import time
import random
import commands
import math
import imp





from PyQt4 import QtCore, QtGui

import InstallToolWindow.MainWindow






        
##
# @brief メイン関数
def main():
    
    app = QtGui.QApplication([""])
    mainWin = InstallToolWindow.MainWindow.MainWindow()
    mainWin.show()
    app.exec_()
    
    
    

    
    
    
if __name__ == "__main__":
    main()
