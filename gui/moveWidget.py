# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '../../gui/movementWidget.ui'
#
# Created: Mon Mar 15 21:13:00 2010
#      by: PyQt4 UI code generator 4.7
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        self.verticalLayoutWidget = QtGui.QWidget(Form)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 241, 221))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.motorSpeedLayout = QtGui.QHBoxLayout()
        self.motorSpeedLayout.setObjectName("motorSpeedLayout")
        self.motorSpeedLabel = QtGui.QLabel(self.verticalLayoutWidget)
        self.motorSpeedLabel.setObjectName("motorSpeedLabel")
        self.motorSpeedLayout.addWidget(self.motorSpeedLabel)
        self.leftMotorSlider = QtGui.QSlider(self.verticalLayoutWidget)
        self.leftMotorSlider.setMinimum(-256)
        self.leftMotorSlider.setMaximum(256)
        self.leftMotorSlider.setSingleStep(16)
        self.leftMotorSlider.setPageStep(32)
        self.leftMotorSlider.setOrientation(QtCore.Qt.Vertical)
        self.leftMotorSlider.setTickPosition(QtGui.QSlider.TicksAbove)
        self.leftMotorSlider.setTickInterval(64)
        self.leftMotorSlider.setObjectName("leftMotorSlider")
        self.motorSpeedLayout.addWidget(self.leftMotorSlider)
        self.rightMotorSlider = QtGui.QSlider(self.verticalLayoutWidget)
        self.rightMotorSlider.setMinimum(-256)
        self.rightMotorSlider.setMaximum(256)
        self.rightMotorSlider.setSingleStep(16)
        self.rightMotorSlider.setPageStep(32)
        self.rightMotorSlider.setOrientation(QtCore.Qt.Vertical)
        self.rightMotorSlider.setTickPosition(QtGui.QSlider.TicksAbove)
        self.rightMotorSlider.setTickInterval(64)
        self.rightMotorSlider.setObjectName("rightMotorSlider")
        self.motorSpeedLayout.addWidget(self.rightMotorSlider)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.motorSpeedLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.motorSpeedLayout)
        self.dpadLayout = QtGui.QGridLayout()
        self.dpadLayout.setObjectName("dpadLayout")
        self.stopButton = QtGui.QPushButton(self.verticalLayoutWidget)
        self.stopButton.setObjectName("stopButton")
        self.dpadLayout.addWidget(self.stopButton, 1, 1, 1, 1)
        self.forwardButton = QtGui.QPushButton(self.verticalLayoutWidget)
        self.forwardButton.setObjectName("forwardButton")
        self.dpadLayout.addWidget(self.forwardButton, 0, 1, 1, 1)
        self.backwardButton = QtGui.QPushButton(self.verticalLayoutWidget)
        self.backwardButton.setObjectName("backwardButton")
        self.dpadLayout.addWidget(self.backwardButton, 2, 1, 1, 1)
        self.leftButton = QtGui.QPushButton(self.verticalLayoutWidget)
        self.leftButton.setObjectName("leftButton")
        self.dpadLayout.addWidget(self.leftButton, 1, 0, 1, 1)
        self.rightButton = QtGui.QPushButton(self.verticalLayoutWidget)
        self.rightButton.setObjectName("rightButton")
        self.dpadLayout.addWidget(self.rightButton, 1, 2, 1, 1)
        self.verticalLayout.addLayout(self.dpadLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.motorSpeedLabel.setText(QtGui.QApplication.translate("Form", "Motor\n"
"Speed", None, QtGui.QApplication.UnicodeUTF8))
        self.stopButton.setText(QtGui.QApplication.translate("Form", "Stop", None, QtGui.QApplication.UnicodeUTF8))
        self.forwardButton.setText(QtGui.QApplication.translate("Form", "Forward", None, QtGui.QApplication.UnicodeUTF8))
        self.backwardButton.setText(QtGui.QApplication.translate("Form", "Backward", None, QtGui.QApplication.UnicodeUTF8))
        self.leftButton.setText(QtGui.QApplication.translate("Form", "Left", None, QtGui.QApplication.UnicodeUTF8))
        self.rightButton.setText(QtGui.QApplication.translate("Form", "Right", None, QtGui.QApplication.UnicodeUTF8))

