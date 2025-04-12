#Built off of Dr.Smays Stem file
#Used ChatGPT to debug and help resolve logic flow in the coding
#region imports
from Truss_GUI import Ui_TrussStructuralDesign
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
from Truss_Classes import TrussController
import sys
#endregion

#region class definitions
class MainWindow(Ui_TrussStructuralDesign,qtw.QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.btn_Open.clicked.connect(self.OpenFile)
        self.spnd_Zoom.valueChanged.connect(self.setZoom) #$NEW$ double spinner widget for setting zoom level

        self.controller=TrussController()
        self.controller.setDisplayWidgets((self.te_DesignReport, self.le_LinkName, self.le_Node1Name,
                                           self.le_Node2Name, self.le_LinkLength, self.gv_Main))

        self.controller.setupEventFilter(self)  #This calls the controller directly.
        self.gv_Main.setMouseTracking(True)
        self.gv_Main.setAttribute(qtc.Qt.WA_AlwaysShowToolTips, True)

        self.show()

    def setZoom(self):
        self.gv_Main.resetTransform()
        self.gv_Main.scale(self.spnd_Zoom.value(), self.spnd_Zoom.value())

    def eventFilter(self, obj, event):
        """
        This overrides the default eventFilter of the widget. It takes action on events and then passes the event
        along to the parent widget.
        :param obj: The object on which the event happened
        :param event: The event itself
        :return: boolean from the parent widget
        """
        if obj == self.controller.view.scene:
            # Delegate handling to the controller by passing relevant widgets
            self.controller.handleSceneEvent(event, self.gv_Main.transform(), self.lbl_MousePos, self.spnd_Zoom)
        return super(MainWindow, self).eventFilter(obj, event)

    def OpenFile(self):
        filename = qtw.QFileDialog.getOpenFileName()[0]
        if len(filename) == 0:  # no file selected
            return
        self.te_Path.setText(filename)
        file = open(filename, 'r')  # open the file
        data = file.readlines()  # read all the lines of the file into a list of strings
        self.controller.ImportFromFile(data)  # import the pipe network information
#endregion

#region function definitions
def Main():
    app=qtw.QApplication(sys.argv)
    mw=MainWindow()
    sys.exit(app.exec())
#endregion

#region function calls
if __name__=="__main__":
    Main()
#endregion