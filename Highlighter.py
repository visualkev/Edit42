
import re
from PySide6.QtGui import (QSyntaxHighlighter)

class Highlighter(QSyntaxHighlighter):
	def __init__(self, parent=None):
		QSyntaxHighlighter.__init__(self, parent)
		self._mappings = {}

	def add_mapping(self, pattern, myformat):
		self._mappings[pattern] = myformat

	def highlightBlock(self, text):
		for pattern, myformat in self._mappings.items():
			for match in re.finditer(pattern, text):
				start, end = match.span()
				self.setFormat(start, end - start, myformat)
