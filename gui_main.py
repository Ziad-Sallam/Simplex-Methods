import sys

from gui import *

def numberOfVariablesChange():
    n = ui.numberOfVariables.value()
    n_c = ui.numberOfConstraints.value()
    for i in range(0,10):
        ui.objective[i].hide()
        ui.objectiveLabels[i].hide()
        ui.constraintSigns[i].hide()
        ui.constrainValues[i].hide()
        ui.types[i].hide()
        ui.typeLabels[i].hide()
        for j in range(0,10):
            ui.constraints[i][j].hide()
            ui.constraintsLabels[i][j].hide()

    for i in range(0,n):
        ui.objective[i].show()
        ui.objectiveLabels[i].setText("x"+str(i)+ ' +')
        ui.objectiveLabels[i].show()
        ui.types[i].show()
        ui.typeLabels[i].show()

        for j in range(0,n_c):

            ui.constraints[j][i].show()
            ui.constraintsLabels[j][i].setText("x" + str(i) + ' +')
            ui.constraintsLabels[j][i].show()

    for i in range(0,n_c):
        ui.constraintsLabels[i][n-1].setText("x" + str(n-1))
        ui.constraintSigns[i].setGeometry(QtCore.QRect(40+100*n, 300 + 40 * i, 40, 20))
        ui.constrainValues[i].setGeometry(QtCore.QRect(80+100*n, 300 + 40 * i, 80, 20))
        ui.constraintSigns[i].show()
        ui.constrainValues[i].show()

    ui.objectiveLabels[n-1].setText("x" + str(n-1))



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    numberOfVariablesChange()
    ui.numberOfVariables.valueChanged.connect(numberOfVariablesChange)
    ui.numberOfConstraints.valueChanged.connect(numberOfVariablesChange)
    MainWindow.show()
    app.exec()