#!/bin/env python
# -*- encoding: utf-8 -*-

##
#   @file MainWindow.py
#   @brief メインウインドウ



import thread
import struct

import optparse
import sys,os,platform
import traceback
import re
import time
import random
import commands
import math
import imp
import threading

import codecs

import zipfile
import urllib
import subprocess
import shutil


from PyQt4 import QtCore, QtGui


##
# @brief ZIPファイルを解凍
# @param filename　ZIPファイル名 
# @param path 展開先のディレクトリ
def unzip(filename, path='.'):
    with zipfile.ZipFile(filename, 'r') as zip_file:
        zip_file.extractall(path=path)

##
# @class InstallThread
# @brief インストールするスレッド
#
class InstallThread(QtCore.QThread):
    ##
    # @brief コンストラクタ
    # @param self 
    # @param parent 親ウィジェット
    def __init__(self, parent=None):
        super(InstallThread, self).__init__(parent)
        #self.func = func
        #self.input = input
        self.parentWidget = parent
    ##
    # @brief スレッド実行関数
    # @param self 
    def run(self):
        self.parentWidget.Install()
        #with QtCore.QMutexLocker(self.parentWidget.mutex):
        #with parent.lock:
        #    self.func(self.input)


##
# @brief setuptoolsのインストール
# @param self 
# @param tmp_dir 一時保存ディレクトリ
# @param window 進行状況表示テキストウィジェット
# @param url ダウンロードURL
def InstallSetuptools(name, tmp_dir, window, url):
    os.chdir(tmp_dir)
    #TextEdit = window.TextEdit
    
    
    cmd = name + u"のインストールを開始しました"
    #TextEdit.append(cmd)

    cmd = name + u"をダウンロードしています"

    #TextEdit.append(cmd)
    window.addText(cmd)

    #TextEdit.append(url)
    window.addText(url)
    
    fname = os.path.basename(url)
    urllib.urlretrieve(url, os.path.join(tmp_dir,fname))
    
    
    cmd = name + u"をインストールしています"
    #TextEdit.append(cmd)
    window.addText(cmd)

    subprocess.call("python ez_setup.py")
    
    

    cmd = name + u"のインストールを完了しました"
    #TextEdit.append(cmd)
    window.addText(cmd)


##
# @brief Pythonモジュールのインストール
# @param self 
# @param tmp_dir 一時保存ディレクトリ
# @param window 進行状況表示テキストウィジェット
# @param url ダウンロードURL
# @param unZipName 解凍後のファイル名
def InstallPython(name, tmp_dir, window, url, unZipName):
    os.chdir(tmp_dir)
    #TextEdit = window.TextEdit

    cmd = name + u"のインストールを開始しました"
    #TextEdit.append(cmd)
    window.addText(cmd)

    cmd = name + u"をダウンロードしています"

    #TextEdit.append(cmd)
    window.addText(cmd)

    #TextEdit.append(url)
    window.addText(url)
    
    fname = os.path.basename(url)
    urllib.urlretrieve(url, os.path.join(tmp_dir,fname))
    
    uname, ext = os.path.splitext(fname)

    ext = ext.lower().strip()

    if ext == ".zip":
        cmd = name + u"を解凍しています"
        #TextEdit.append(cmd)
        window.addText(cmd)
        unzip(fname)

        os.chdir(os.path.join(tmp_dir,unZipName))

        cmd = name + u"をインストールしています"
        #TextEdit.append(cmd)
        window.addText(cmd)

        subprocess.call("python setup.py install")
    
    

    cmd = name + u"のインストールを完了しました"
    #TextEdit.append(cmd)
    window.addText(cmd)

##
# @brief MSIインストーラーでのインストール
# @param self 
# @param tmp_dir 一時保存ディレクトリ
# @param window 進行状況表示テキストウィジェット
# @param url ダウンロードURL
def InstallMSI(name, tmp_dir, window, url):
    os.chdir(tmp_dir)
    #TextEdit = window.TextEdit
    
    cmd = name + u"のインストールを開始しました"
    #TextEdit.append(cmd)
    window.addText(cmd)

    cmd = name + u"をダウンロードしています"
    
    #TextEdit.append(cmd)
    window.addText(cmd)

    #TextEdit.append(url)
    window.addText(url)
    
    fname = os.path.basename(url)
    urllib.urlretrieve(url, os.path.join(tmp_dir,fname))

    cmd = name + u"をインストールしています"
    #TextEdit.append(cmd)
    window.addText(cmd)
    uname, ext = os.path.splitext(fname)

    ext = ext.lower().strip()
    if ext == ".msi":
        subprocess.call("msiexec /i " + fname + " REINSTALL=ALL REINSTALLMODE=vomus")
    elif ext == ".exe":
        subprocess.call(fname)

    cmd = name + u"のインストールを完了しました"
    #TextEdit.append(cmd)
    window.addText(cmd)



##
# @class MainWindow
# @brief メインウインドウ
#
class MainWindow(QtGui.QMainWindow):
    python_url = {}
    python_url["2.6"] = {}
    python_url["2.6"]["32"] = "https://www.python.org/ftp/python/2.6.6/python-2.6.6.msi"
    python_url["2.6"]["64"] = "https://www.python.org/ftp/python/2.6.6/python-2.6.6.amd64.msi"
    python_url["2.7"] = {}
    python_url["2.7"]["32"] = "https://www.python.org/ftp/python/2.7.10/python-2.7.10.msi"
    python_url["2.7"]["64"] = "https://www.python.org/ftp/python/2.7.10/python-2.7.10.amd64.msi"
    
    openrtm_url = {}
    openrtm_url["9"] = {}
    openrtm_url["9"]["32"] = "http://openrtm.org/pub/Windows/OpenRTM-aist/cxx/1.1/OpenRTM-aist-1.1.1-RELEASE_x86_vc9.msi"
    openrtm_url["10"] = {}
    openrtm_url["10"]["32"] = "http://openrtm.org/pub/Windows/OpenRTM-aist/cxx/1.1/OpenRTM-aist-1.1.1-RELEASE_x86_vc10.msi"
    openrtm_url["10"]["64"] = "http://openrtm.org/pub/Windows/OpenRTM-aist/cxx/1.1/OpenRTM-aist-1.1.1-RELEASE_x86_64_vc10.msi"
    openrtm_url["11"] = {}
    openrtm_url["11"]["32"] = "http://openrtm.org/pub/Windows/OpenRTM-aist/cxx/1.1/OpenRTM-aist-1.1.1-RELEASE_x86_vc11.msi"
    openrtm_url["11"]["64"] = "http://openrtm.org/pub/Windows/OpenRTM-aist/cxx/1.1/OpenRTM-aist-1.1.1-RELEASE_x86_64_vc11.msi"
    openrtm_url["12"] = {}
    openrtm_url["12"]["32"] = "http://openrtm.org/pub/Windows/OpenRTM-aist/cxx/1.1/OpenRTM-aist-1.1.1-RELEASE_x86_vc12.msi"
    openrtm_url["12"]["64"] = "http://openrtm.org/pub/Windows/OpenRTM-aist/cxx/1.1/OpenRTM-aist-1.1.1-RELEASE_x86_64_vc12.msi"

    openrtm_ubuntu_url = "http://svn.openrtm.org/OpenRTM-aist/tags/RELEASE_1_1_1/OpenRTM-aist/build/pkg_install_ubuntu.sh"
    openrtm_debian_url = "http://svn.openrtm.org/OpenRTM-aist/tags/RELEASE_1_1_1/OpenRTM-aist/build/pkg_install_debian.sh"
    openrtm_fedora_url = "http://svn.openrtm.org/OpenRTM-aist/tags/RELEASE_1_1_1/OpenRTM-aist/build/pkg_install_fedora.sh"


    openrtm_python_url = {}
    openrtm_python_url["32"] = "http://openrtm.org/pub/Windows/OpenRTM-aist/python/OpenRTM-aist-Python_1.1.0-RELEASE_x86.msi"
    openrtm_python_url["64"] = "http://openrtm.org/pub/Windows/OpenRTM-aist/python/OpenRTM-aist-Python_1.1.0-RELEASE_x86_64.msi"

    openrtm_python_ubuntu_url = "http://svn.openrtm.org/OpenRTM-aist-Python/tags/RELEASE_1_1_0/OpenRTM-aist-Python/installer/install_scripts/pkg_install_python_ubuntu.sh"
    openrtm_python_debian_url = "http://svn.openrtm.org/OpenRTM-aist-Python/tags/RELEASE_1_1_0/OpenRTM-aist-Python/installer/install_scripts/pkg_install_python_debian.sh"
    openrtm_python_fedora_url = "http://svn.openrtm.org/OpenRTM-aist-Python/tags/RELEASE_1_1_0/OpenRTM-aist-Python/installer/install_scripts/pkg_install_python_fedora.sh"

    setuptools_url = "https://bootstrap.pypa.io/ez_setup.py"

    rtctree_url = "https://github.com/gbiggs/rtctree/archive/master.zip"
    rtsprofile_url = "https://github.com/gbiggs/rtsprofile/archive/master.zip"
    rtshell_url = "https://github.com/gbiggs/rtshell/archive/master.zip"
    PyYAML_url = "http://pyyaml.org/download/pyyaml/PyYAML-3.11.zip"
    CMake_url = "http://www.cmake.org/files/v3.2/cmake-3.2.1-win32-x86.exe"
    Doxygen_url = "http://ftp.stack.nl/pub/users/dimitri/doxygen-1.8.9.1-setup.exe"

    ##
    # @brief コンストラクタ
    # @param self 
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle(u"インストール支援ツール")


        self.mutex = QtCore.QMutex()
        
        self.cwidget = QtGui.QWidget()
        self.mainLayout = QtGui.QVBoxLayout()
        self.cwidget.setLayout(self.mainLayout)
        self.setCentralWidget(self.cwidget)

        self.subLayout = QtGui.QHBoxLayout()
        self.mainLayout.addLayout(self.subLayout)
        
        self.VLayout1 = QtGui.QVBoxLayout()
        self.subLayout.addLayout(self.VLayout1)


        self.PythonGroupBox = QtGui.QGroupBox(u"Pythonのインストール")
        self.PythonLayout = QtGui.QVBoxLayout()
        self.PythonGroupBox.setLayout(self.PythonLayout)
        self.PythonYNGroupBox,self.PythonYNButtons = self.createRadioButton([u"はい",u"いいえ"],u"インストールしますか？", self.PythonLayout)
        self.PythonYNButtons[-1].setChecked(True)
        self.PythonVersionGroupBox,self.PythonVersionButtons = self.createRadioButton(["2.6","2.7"],u"バージョン", self.PythonLayout)
        self.PythonVersionButtons[-1].setChecked(True)
        self.PythonBitGroupBox,self.PythonBitButtons = self.createRadioButton(["32bit","64bit"],u"", self.PythonLayout)
        self.VLayout1.addWidget(self.PythonGroupBox)


        self.OpenRTMGroupBox = QtGui.QGroupBox(u"OpenRTM-aist")
        self.OpenRTMLayout = QtGui.QVBoxLayout()
        self.OpenRTMGroupBox.setLayout(self.OpenRTMLayout)
        #self.OpenRTMLabel = QtGui.QLabel(u"OpenRTM-aistのインストール")
        #self.OpenRTMLayout.addWidget(self.OpenRTMLabel)
        self.OpenRTMYNGroupBox,self.OpenRTMYNButtons = self.createRadioButton([u"はい",u"いいえ"],u"インストールしますか？", self.OpenRTMLayout)
        self.OpenRTMYNButtons[-1].setChecked(True)
        self.OpenRTMVersionGroupBox,self.OpenRTMVersionButtons = self.createRadioButton(["9(2008)","10(2010)","11(2012)","12(2013)"],u"バージョン", self.OpenRTMLayout)
        self.OpenRTMVersionButtons[-1].setChecked(True)
        self.OpenRTMBitGroupBox,self.OpenRTMBitButtons = self.createRadioButton(["32bit","64bit"],u"", self.OpenRTMLayout)
        #self.mainLayout.addLayout(self.OpenRTMLayout)
        self.VLayout1.addWidget(self.OpenRTMGroupBox)

        self.VLayout2 = QtGui.QVBoxLayout()
        self.subLayout.addLayout(self.VLayout2)

        self.OpenRTMPythonGroupBox = QtGui.QGroupBox(u"OpenRTM-aist-Python")
        self.OpenRTMPythonLayout = QtGui.QVBoxLayout()
        self.OpenRTMPythonGroupBox.setLayout(self.OpenRTMPythonLayout)
        self.OpenRTMPythonYNGroupBox,self.OpenRTMPythonYNButtons = self.createRadioButton([u"はい",u"いいえ"],u"インストールしますか？", self.OpenRTMPythonLayout)
        self.OpenRTMPythonYNButtons[-1].setChecked(True)
        self.OpenRTMPythonBitGroupBox,self.OpenRTMPythonBitButtons = self.createRadioButton(["32bit","64bit"],u"", self.OpenRTMPythonLayout)
        self.VLayout2.addWidget(self.OpenRTMPythonGroupBox)


        

        self.setuptoolsGroupBox = QtGui.QGroupBox(u"setuptools")
        self.setuptoolsLayout = QtGui.QVBoxLayout()
        self.setuptoolsGroupBox.setLayout(self.setuptoolsLayout)
        self.setuptoolsYNGroupBox,self.setuptoolsYNButtons = self.createRadioButton([u"はい",u"いいえ"],u"インストールしますか？", self.setuptoolsLayout)
        self.setuptoolsYNButtons[-1].setChecked(True)
        self.VLayout2.addWidget(self.setuptoolsGroupBox)

        self.rtctreeGroupBox = QtGui.QGroupBox(u"rtctree")
        self.rtctreeLayout = QtGui.QVBoxLayout()
        self.rtctreeGroupBox.setLayout(self.rtctreeLayout)
        self.rtctreeYNGroupBox,self.rtctreeYNButtons = self.createRadioButton([u"はい",u"いいえ"],u"インストールしますか？", self.rtctreeLayout)
        self.rtctreeYNButtons[-1].setChecked(True)
        self.VLayout2.addWidget(self.rtctreeGroupBox)

        self.rtsprofileGroupBox = QtGui.QGroupBox(u"rtsprofile")
        self.rtsprofileLayout = QtGui.QVBoxLayout()
        self.rtsprofileGroupBox.setLayout(self.rtsprofileLayout)
        self.rtsprofileYNGroupBox,self.rtsprofileYNButtons = self.createRadioButton([u"はい",u"いいえ"],u"インストールしますか？", self.rtsprofileLayout)
        self.rtsprofileYNButtons[-1].setChecked(True)
        self.VLayout2.addWidget(self.rtsprofileGroupBox)

        self.VLayout3 = QtGui.QVBoxLayout()
        self.subLayout.addLayout(self.VLayout3)

        self.rtshellGroupBox = QtGui.QGroupBox(u"rtshell")
        self.rtshellLayout = QtGui.QVBoxLayout()
        self.rtshellGroupBox.setLayout(self.rtshellLayout)
        self.rtshellYNGroupBox,self.rtshellYNButtons = self.createRadioButton([u"はい",u"いいえ"],u"インストールしますか？", self.rtshellLayout)
        self.rtshellYNButtons[-1].setChecked(True)
        self.VLayout3.addWidget(self.rtshellGroupBox)

        self.PyYAMLGroupBox = QtGui.QGroupBox(u"PyYAML")
        self.PyYAMLLayout = QtGui.QVBoxLayout()
        self.PyYAMLGroupBox.setLayout(self.PyYAMLLayout)
        self.PyYAMLYNGroupBox,self.PyYAMLYNButtons = self.createRadioButton([u"はい",u"いいえ"],u"インストールしますか？", self.PyYAMLLayout)
        self.PyYAMLYNButtons[-1].setChecked(True)
        self.VLayout3.addWidget(self.PyYAMLGroupBox)

        self.CMakeGroupBox = QtGui.QGroupBox(u"CMake")
        self.CMakeLayout = QtGui.QVBoxLayout()
        self.CMakeGroupBox.setLayout(self.CMakeLayout)
        self.CMakeYNGroupBox,self.CMakeYNButtons = self.createRadioButton([u"はい",u"いいえ"],u"インストールしますか？", self.CMakeLayout)
        self.CMakeYNButtons[-1].setChecked(True)
        self.VLayout3.addWidget(self.CMakeGroupBox)

        self.DoxygenGroupBox = QtGui.QGroupBox(u"Doxygen")
        self.DoxygenLayout = QtGui.QVBoxLayout()
        self.DoxygenGroupBox.setLayout(self.DoxygenLayout)
        self.DoxygenYNGroupBox,self.DoxygenYNButtons = self.createRadioButton([u"はい",u"いいえ"],u"インストールしますか？", self.DoxygenLayout)
        self.DoxygenYNButtons[-1].setChecked(True)
        self.VLayout3.addWidget(self.DoxygenGroupBox)
        

        self.InstallButton = QtGui.QPushButton(u"インストール")
        self.mainLayout.addWidget(self.InstallButton)
        self.InstallButton.clicked.connect(self.InstallSlot)

        self.TextEdit = QtGui.QTextEdit()
        self.mainLayout.addWidget(self.TextEdit)
        #self.TextEdit.append(u"インストール開始")
        #self.TextEdit.append(u"インストール終了")
        #self.cursor = QtGui.QTextCursor(self.TextEdit.document())
        #self.cursor.insertText("test")
        """self.buttonGroup = QtGui.QButtonGroup()
        self.radioButton1 = QtGui.QRadioButton()
        self.radioButton2 = QtGui.QRadioButton()
        self.buttonGroup.addButton(self.radioButton1)
        self.buttonGroup.addButton(self.radioButton2)
        self.mainLayout.addWidget(self.radioButton1)
        self.mainLayout.addWidget(self.radioButton2)"""

        self.timer = QtCore.QTimer()
        self.timer.setInterval(500)
        self.timer.timeout.connect(self.updateTextEdit)
        self.timer.start()
        
        self.cmdList = []

        
    ##
    # @brief 進行状況表示テキストを更新
    # @param self  
    def updateTextEdit(self):
        with QtCore.QMutexLocker(self.mutex):
            for cmd in self.cmdList:
                self.TextEdit.append(cmd)
            if len(self.cmdList) > 0:
                self.cursor = QtGui.QTextCursor(self.TextEdit.document())
                self.cursor.setKeepPositionOnInsert(True)
                
            self.cmdList = []

    ##
    # @brief 進行状況表示テキストにテキスト追加
    # @param self
    # @param cmd　テキスト
    def addText(self, cmd):
        with QtCore.QMutexLocker(self.mutex):
            self.cmdList.append(cmd)

    ##
    # @brief Pythonをインストール
    # @param self
    # @param version バージョン
    # @param bitnum 32bitか64bitか
    def InstallPython(self, version,  bitnum):
        InstallMSI(u"Python",self.tmp_path,self,MainWindow.python_url[version][bitnum])
        """input = {}
        input["TEMP"] = self.tmp_path
        input["MainWindow"] = self
        input["name"] = u"Python"
        input["URL"] = MainWindow.python_url[version][bitnum]

        m_thread = InstallThread(InstallMSI,input,self)
        m_thread.start()"""
        #InstallMSI(input)

    ##
    # @brief OpenRTM-aistをインストール
    # @param self
    # @param version 対応するVisual Studioのバージョン
    # @param bitnum 32bitか64bitか
    def InstallOpenRTM(self, version,  bitnum):
        InstallMSI(u"OpenRTM-aist",self.tmp_path,self,MainWindow.openrtm_url[version][bitnum])
        """input = {}
        input["TEMP"] = self.tmp_path
        input["MainWindow"] = self
        input["name"] = u"OpenRTM-aist"
        input["URL"] = MainWindow.openrtm_url[version][bitnum]

        m_thread = InstallThread(InstallMSI,input,self)
        m_thread.start()"""

    ##
    # @brief OpenRTM-aist-Pythonをインストール
    # @param self
    # @param bitnum 32bitか64bitか
    def InstallOpenRTMPython(self, bitnum):
        InstallMSI(u"OpenRTM-aist-Python",self.tmp_path,self,MainWindow.openrtm_python_url[bitnum])
        """input = {}
        input["TEMP"] = self.tmp_path
        input["MainWindow"] = self
        input["name"] = u"OpenRTM-aist-Python"
        input["URL"] = MainWindow.openrtm_python_url[bitnum]

        m_thread = InstallThread(InstallMSI,input,self)
        m_thread.start()"""
    ##
    # @brief setuptoolsをインストール
    # @param self
    def Installsetuptools(self):
        InstallSetuptools(u"setuptools",self.tmp_path,self,MainWindow.setuptools_url)
        """input = {}
        input["TEMP"] = self.tmp_path
        input["MainWindow"] = self
        input["name"] = u"setuptools"
        input["URL"] = MainWindow.setuptools_url

        m_thread = InstallThread(InstallSetuptools,input,self)
        m_thread.start()"""

    ##
    # @brief rtctreeをインストール
    # @param self
    def Installrtctree(self):
        InstallPython(u"rtctree",self.tmp_path,self,MainWindow.rtctree_url,"rtctree-master")
        """input = {}
        input["TEMP"] = self.tmp_path
        input["MainWindow"] = self
        input["name"] = u"rtctree"
        input["URL"] = MainWindow.rtctree_url
        input["unZipName"] = "rtctree-master"

        m_thread = InstallThread(InstallPython,input,self)
        m_thread.start()"""

    ##
    # @brief rtsprofileをインストール
    # @param self
    def Installrtsprofile(self):
        InstallPython(u"rtsprofile",self.tmp_path,self,MainWindow.rtsprofile_url,"rtsprofile-master")
        """input = {}
        input["TEMP"] = self.tmp_path
        input["MainWindow"] = self
        input["name"] = u"rtsprofile"
        input["URL"] = MainWindow.rtsprofile_url
        input["unZipName"] = "rtsprofile-master"

        m_thread = InstallThread(InstallPython,input,self)
        m_thread.start()"""

    ##
    # @brief rtshellをインストール
    # @param self
    def Installrtshell(self):
        InstallPython(u"rtshell",self.tmp_path,self,MainWindow.rtshell_url,"rtshell-master")
        """input = {}
        input["TEMP"] = self.tmp_path
        input["MainWindow"] = self
        input["name"] = u"rtshell"
        input["URL"] = MainWindow.rtshell_url
        input["unZipName"] = "rtshell-master"

        m_thread = InstallThread(InstallPython,input,self)
        m_thread.start()"""

    ##
    # @brief PyYAMLをインストール
    # @param self
    def InstallPyYAML(self):
        InstallPython(u"PyYAML",self.tmp_path,self,MainWindow.PyYAML_url,"PyYAML-3.11")
        """input = {}
        input["TEMP"] = self.tmp_path
        input["MainWindow"] = self
        input["name"] = u"PyYAML"
        input["URL"] = MainWindow.PyYAML_url
        input["unZipName"] = "PyYAML-3.11"

        m_thread = InstallThread(InstallPython,input,self)
        m_thread.start()"""

    ##
    # @brief CMakeをインストール
    # @param self
    def InstallCMake(self):
        InstallMSI(u"CMake",self.tmp_path,self,MainWindow.CMake_url)
        """input = {}
        input["TEMP"] = self.tmp_path
        input["MainWindow"] = self
        input["name"] = u"CMake"
        input["URL"] = MainWindow.CMake_url

        m_thread = InstallThread(InstallMSI,input,self)
        m_thread.start()"""

    ##
    # @brief Doxygenをインストール
    # @param self
    def InstallDoxygen(self):
        InstallMSI(u"Doxygen",self.tmp_path,self,MainWindow.Doxygen_url)
        """input = {}
        input["TEMP"] = self.tmp_path
        input["MainWindow"] = self
        input["name"] = u"Doxygen"
        input["URL"] = MainWindow.Doxygen_url

        m_thread = InstallThread(InstallMSI,input,self)
        m_thread.start()"""

    ##
    # @brief インストール
    # @param self
    def Install(self):
        cmd = u"インストールを開始しました"
        #self.TextEdit.append(cmd)
        self.addText(cmd)
        
        self.tmp_path = os.path.join(os.environ["TEMP"],"RTMToolsInstall_Dir")

        if not os.path.exists(self.tmp_path):
            os.mkdir(self.tmp_path)


        if self.PythonYNGroupBox.checkedId() == 0:
            if self.PythonVersionGroupBox.checkedId() == 0:
                version = "2.6"
            elif self.PythonVersionGroupBox.checkedId() == 1:
                version = "2.7"
            if self.PythonBitGroupBox.checkedId() == 0:
                butnum = "32"
            elif self.PythonBitGroupBox.checkedId() == 1:
                butnum = "64"
            self.InstallPython(version,butnum)
        if self.OpenRTMYNGroupBox.checkedId() == 0:
            if self.OpenRTMVersionGroupBox.checkedId() == 0:
                version = "9"
            elif self.OpenRTMVersionGroupBox.checkedId() == 1:
                version = "10"
            elif self.OpenRTMVersionGroupBox.checkedId() == 2:
                version = "11"
            elif self.OpenRTMVersionGroupBox.checkedId() == 3:
                version = "12"
            if self.OpenRTMBitGroupBox.checkedId() == 0:
                butnum = "32"
            elif self.OpenRTMBitGroupBox.checkedId() == 1:
                butnum = "64"
            self.InstallOpenRTM(version,butnum)
        if self.OpenRTMPythonYNGroupBox.checkedId() == 0:
            if self.OpenRTMPythonBitGroupBox.checkedId() == 0:
                butnum = "32"
            elif self.OpenRTMPythonBitGroupBox.checkedId() == 1:
                butnum = "64"
            self.InstallOpenRTMPython(butnum)
        if self.setuptoolsYNGroupBox.checkedId() == 0:
            self.Installsetuptools()
        if self.rtctreeYNGroupBox.checkedId() == 0:
            self.Installrtctree()
        if self.rtsprofileYNGroupBox.checkedId() == 0:
            self.Installrtsprofile()
        if self.rtshellYNGroupBox.checkedId() == 0:
            self.Installrtshell()
        if self.PyYAMLYNGroupBox.checkedId() == 0:
            self.InstallPyYAML()
        if self.CMakeYNGroupBox.checkedId() == 0:
            self.InstallCMake()
        if self.DoxygenYNGroupBox.checkedId() == 0:
            self.InstallDoxygen()

        os.chdir(os.path.join(self.tmp_path,".."))
        shutil.rmtree(self.tmp_path)

        cmd = u"全てのソフトウェアのインストールを完了しました"
        #self.TextEdit.append(cmd)
        self.addText(cmd)
        

    ##
    # @brief インストール開始ボタンのスロット
    # @param self
    def InstallSlot(self):
        m_thread = InstallThread(self)
        m_thread.start()
        
    ##
    # @brief ラジオボタン作成
    # @param self
    # @param nameList ボタンラベルのリスト
    # @param name 表示する名前
    # @param mainlayout 追加するレイアウト
    def createRadioButton(self, nameList, name, mainlayout):
        groupbox = QtGui.QGroupBox(name)
        alayout = QtGui.QVBoxLayout()
        groupbox.setLayout(alayout)
        #label = QtGui.QLabel(name)
        #alayout.addWidget(label)
        layout = QtGui.QHBoxLayout()
        alayout.addLayout(layout)
        buttonGroup = QtGui.QButtonGroup()

        radioButtonList = []
        count = 0
        for n in nameList:
                
            randioButton = QtGui.QRadioButton(n)
            if count == 0:
                randioButton.setChecked(True)
            buttonGroup.addButton(randioButton)
            layout.addWidget(randioButton)
            buttonGroup.setId(randioButton,count)
            count += 1
            radioButtonList.append(randioButton)

        mainlayout.addWidget(groupbox)
        return buttonGroup,radioButtonList



        
    ##
    # @brief メッセージボックス表示
    # @param self
    # @param mes 表示するテキスト
    def mesBox(self, mes):
        msgbox = QtGui.QMessageBox( self )
        msgbox.setText( mes )
        msgbox.setModal( True )
        ret = msgbox.exec_()
