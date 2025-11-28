#!/usr/bin/python

from PySide6.QtGui import QPalette, QBrush, QColor
from PySide6.QtCore import Qt

def custom_palette():
	custom_palette = QPalette()
	
	# WindowText
	brush = QBrush(QColor("#32FBE2"))
	brush.setStyle(Qt.BrushStyle.SolidPattern)
	custom_palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.WindowText, brush)

	# Button color: "#bfb6cd" QColor(68, 43, 105, 255)
	myButtonColor=QColor("#442b69")
	brush1 = QBrush(myButtonColor)
	brush1.setStyle(Qt.BrushStyle.SolidPattern)
	custom_palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Button, brush1)

	# Text
	brush2 = QBrush(QColor(0, 0, 0, 255))
	brush2.setStyle(Qt.BrushStyle.SolidPattern)
	custom_palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Text, brush2)
	custom_palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.ButtonText, brush)
	
	# Base
	mycolor=QColor("#cbbcd5")
	mycolor1=QColor("#fff")
	brush3 = QBrush(mycolor)
	brush3.setStyle(Qt.BrushStyle.SolidPattern)
	custom_palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Base, brush3)

	# Window
	mycolor4=QColor(26, 5, 58, 255)
	brush4 = QBrush(mycolor4)
	brush4.setStyle(Qt.BrushStyle.SolidPattern)
	custom_palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Window, brush4)

	# Highlight
	brush5 = QBrush(QColor(70, 26, 138, 255))
	brush5.setStyle(Qt.BrushStyle.SolidPattern)
	custom_palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Highlight, brush5)

	# HighlightedText
	brush6 = QBrush(QColor(255, 255, 255, 255))
	brush6.setStyle(Qt.BrushStyle.SolidPattern)
	custom_palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.HighlightedText, brush6)

	# AlternateBase
	brush7 = QBrush(QColor(242, 242, 242, 255))
	brush7.setStyle(Qt.BrushStyle.SolidPattern)
	custom_palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.AlternateBase, brush7)

	#PlaceholderText
	brush8 = QBrush(QColor(50, 251, 226, 128))
	brush8.setStyle(Qt.BrushStyle.SolidPattern)
	#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
	custom_palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.PlaceholderText, brush8)
	#endif


	# inactive

	# WindowText
	custom_palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.WindowText, brush)
	custom_palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Button, brush4)

	# Text
	brush9 = QBrush(QColor(61, 56, 70, 255))
	brush9.setStyle(Qt.BrushStyle.SolidPattern)
	custom_palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Text, brush9)

	# ButtonText
	custom_palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.ButtonText, brush)

	# Base
	custom_palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Base, brush3)

	# Window
	custom_palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Window, brush4)

	# Highlight
	custom_palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Highlight, brush5)

	# HighlightedText
	custom_palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.HighlightedText, brush6)
	#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)

	# PlaceholderText
	custom_palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.PlaceholderText, brush8)
	#endif


	#disabled		
	
	# WindowText
	custom_palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.WindowText, brush)

	# Button
	custom_palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Button, brush4)

	# Text
	custom_palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text, brush)

	# ButtonText
	custom_palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.ButtonText, brush)

	# Base
	custom_palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Base, brush4)

	# Window
	custom_palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Window, brush4)

	# Highlight
	custom_palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Highlight, brush5)

	# HighlightedText
	custom_palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.HighlightedText, brush6)
	#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)


	custom_palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.PlaceholderText, brush8)
	#endif
	
	#- - - - - -  example use - - - - - 
	#self.fr_new_chk.setPalette(custom_palette)
	
	return custom_palette
	
