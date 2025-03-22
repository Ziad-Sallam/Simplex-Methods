import sys

from gui import *

def numberOfVariablesChange():
    n = ui.numberOfVariables.value()
    n_c = ui.numberOfConstraints.value()
    for i in range(0,10):
        for j in range(0,10):
            ui.objectives[i][j].hide()
            ui.objectiveLabels[i][j].hide()
        ui.constraintSigns[i].hide()
        ui.constrainValues[i].hide()
        ui.types[i].hide()
        ui.typeLabels[i].hide()
        for j in range(0,10):
            ui.constraints[i][j].hide()
            ui.constraintsLabels[i][j].hide()


    for i in range(0,n):
        for j in range(ui.numberOfObjectives.value()):
            ui.objectives[j][i].show()
            ui.objectiveLabels[j][i].setText("x"+str(i)+ ' +')
            ui.objectiveLabels[j][i].show()
        ui.types[i].show()
        ui.typeLabels[i].show()

        for j in range(0,n_c):

            ui.constraints[j][i].show()
            ui.constraintsLabels[j][i].setText("x" + str(i) + ' +')
            ui.constraintsLabels[j][i].show()

    for i in range(0,n_c):
        ui.constraintsLabels[i][n-1].setText("x" + str(n-1))
        ui.constraintSigns[i].setGeometry(QtCore.QRect(40+100*n, 20+40*i, 40, 20))
        ui.constrainValues[i].setGeometry(QtCore.QRect(80+100*n, 20+40*i, 80, 20))
        ui.constraintSigns[i].show()
        ui.constrainValues[i].show()

    for i in range(ui.numberOfObjectives.value()):
        ui.objectiveLabels[i][n-1].setText("x" + str(n-1))


def handleMethodChange():
    if ui.Method.currentText() == 'Preemtive Goal Programming':
        ui.numberOfObjectiveLabel.show()
        ui.numberOfObjectives.show()
    else:
        ui.numberOfObjectiveLabel.hide()
        ui.numberOfObjectives.hide()
        ui.numberOfObjectives.setValue(1)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    numberOfVariablesChange()
    handleMethodChange()
    ui.numberOfVariables.valueChanged.connect(numberOfVariablesChange)
    ui.numberOfConstraints.valueChanged.connect(numberOfVariablesChange)
    ui.numberOfObjectives.valueChanged.connect(numberOfVariablesChange)
    ui.Method.currentIndexChanged.connect(handleMethodChange)
    MainWindow.show()
    app.exec()