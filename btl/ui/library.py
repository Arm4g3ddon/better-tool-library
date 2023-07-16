import os
import re
import FreeCAD
import FreeCADGui
import Path
from PySide import QtGui
from .tablecell import TwoLineTableCell

__dir__ = os.path.dirname(__file__)
ui_path = os.path.join(__dir__, "library.ui")

class LibraryUI():
    def __init__(self, tooldb, serializer):
        self.tooldb = tooldb
        self.serializer = serializer
        self.form = FreeCADGui.PySideUic.loadUi(ui_path)

        self.form.buttonBox.clicked.connect(self.form.close)

        self.load()

    def load(self):
        self.tooldb.deserialize(self.serializer)

        # Update the library list.
        self.form.comboBoxLibrary.clear()
        libraries = self.tooldb.get_libraries()
        if not libraries:
            return
        for library in libraries:
            self.form.comboBoxLibrary.addItem(library.label, library.id)

        # Update the tool list.
        listwidget = self.form.listWidgetTools
        for tool in libraries[0].tools:
            cell = TwoLineTableCell()
            cell.setTextUp(tool.label)
            cell.setTextDown(tool.id)
            #cell.setIcon(icon)

            widget_item = QtGui.QListWidgetItem(listwidget)
            widget_item.setSizeHint(cell.sizeHint())
            listwidget.addItem(widget_item)
            listwidget.setItemWidget(widget_item, cell)

    def show(self):
        self.form.show()

    def add_tool_to_job(self, tool):
        jobs = FreeCAD.ActiveDocument.findObjects("Path::FeaturePython", "Job.*")
        for job in jobs:
            for idx, tc in enumerate(job.Tools.Group):
                print(tc.Label) #FIXME
                #tc.HorizFeed = hfeed
                #tc.VertFeed = vfeed
                #tc.SpindleSpeed = float(rpm)