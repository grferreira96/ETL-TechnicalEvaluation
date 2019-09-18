import metricas
import pandas as pd

def readData():
    dataFrame = pd.read_csv("pagamentos.csv", header=None, names=['clienteID', 'dataDoPagamento', 'valor', 'plano'])
    return dataFrame

dataFrame=readData()
print(dataFrame[0:30])
