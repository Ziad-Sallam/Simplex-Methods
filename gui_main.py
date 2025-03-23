import sys
import subprocess
import simplex
from gui import *
from simplex import Simplex


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
        ui.goalValues[i].hide()
        ui.goalSigns[i].hide()
        for j in range(0,10):
            ui.constraints[i][j].hide()
            ui.constraintsLabels[i][j].hide()


    for i in range(0,n):
        for j in range(ui.numberOfObjectives.value()):
            ui.objectives[j][i].show()
            ui.objectiveLabels[j][i].setText("x"+str(i)+ ' +')
            ui.objectiveLabels[j][i].show()
            if ui.Method.currentText() == 'Preemptive Goal Programming':
                ui.goalSigns[j].show()
                ui.goalSigns[j].setGeometry(QtCore.QRect(40+100*n, 20 + 40 * j, 40, 20))
                ui.goalValues[j].setGeometry(QtCore.QRect(90 + 100 * n, 20 + 40 * j, 70, 20))
                ui.goalValues[j].show()
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
    n = ui.numberOfVariables.value()
    if ui.Method.currentText() == 'Preemptive Goal Programming':
        ui.numberOfObjectiveLabel.show()
        ui.numberOfObjectives.show()
        for i in range(ui.numberOfObjectives.value()):
            ui.goalValues[i].show()
            ui.goalSigns[i].show()
            ui.goalSigns[i].setGeometry(QtCore.QRect(40 + 100 * n, 20 + 40 * i, 40, 20))
            ui.goalValues[i].setGeometry(QtCore.QRect(90 + 100 * n, 20 + 40 * i, 70, 20))
    else:
        ui.numberOfObjectiveLabel.hide()
        ui.numberOfObjectives.hide()
        ui.numberOfObjectives.setValue(1)
        for i in range(len(ui.goalValues)):
            ui.goalValues[i].hide()
            ui.goalSigns[i].hide()

def solve():
    A = []
    b =[]
    Z =[]
    ans =''
    objective = -1
    if ui.maximizeRadio.isChecked():
        objective = 1

    for i in range(ui.numberOfObjectives.value()):
        ob =[]
        for j in range(ui.numberOfVariables.value()):
            ob.append(ui.objectives[i][j].value())
        Z.append(ob)

    for i in range(0,ui.numberOfConstraints.value()):
        x =[]
        for j in range(0,ui.numberOfVariables.value()):
            x.append(ui.constraints[j][i].value())
        A.append(x)
        b.append(ui.constrainValues[i].value())

    method = ui.Method.currentText()
    if method == 'Simple Simplex':
        smplx = Simplex(A,b,Z,objective)
        smplx.addingSlackVars()
        smplx.ansSetup()
        maxValues, Z_final, status = smplx.method()
        ans += 'steps:\n'
        ans += smplx.steps
        ans += f"\nMax values of variables: {maxValues}\n"
        ans += f"Z final: {Z_final}\n"
        ans += f"status: {status}\n"
        with open("ans.txt","w") as f:
            f.write(ans)
        print(ans)


        try:
            subprocess.run(["notepad", "ans.txt"], shell=True, check=True)
        except FileNotFoundError:
            print("Notepad not found. Please open 'ans.txt' manually.")
        except Exception as e:
            print(f"An error occurred: {e}")



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
    ui.solveBtn.clicked.connect(solve)

    MainWindow.show()
    app.exec()