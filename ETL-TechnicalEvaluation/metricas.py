'''Métricas SaaS mensais'''
import pandas as pd
import constants


def metricsCalculator(clientes_df, metricsPerClient):
    '''Calcula as métricas em cada operação'''
    metricsList = []
    for index, row in metricsPerClient.iterrows():
        mes = row['mes']
        ano = row['ano']
        valor = row['valor']
        pagamentoId = row['pagamentoID']
        clienteId = row['clienteID']

        expMes = (mes - 1 if 1 < mes <= 12 else 12)
        expAno = (ano - 1 if expMes == 12 else ano)

        mrrValue = row['valor']

        newMrrLoc = clientes_df.loc[(clientes_df['id'] == clienteId)]
        newMrrValue = NewMRR(newMrrLoc, valor, mes, ano)

        expansionOrContractionMrrLoc = metricsPerClient.loc[(metricsPerClient['clienteID'] == clienteId) & (metricsPerClient['pagamentoID'] != pagamentoId) & (metricsPerClient['mes'] == expMes) & (metricsPerClient['ano'] == expAno)]
        expMrrValue = ExpansionMRR(expansionOrContractionMrrLoc, valor, mes, ano)
        contMrrValue = ContractionMRR(expansionOrContractionMrrLoc, valor, mes, ano)

        metricsPerClient.at[index, 'metricaID'] = index

        item = [
            index,
            row['clienteID'].astype('int64'),
            row['mes'].astype('int64'),
            row['ano'].astype('int64'),
            mrrValue,
            newMrrValue,
            expMrrValue,
            contMrrValue
        ]
        metricsList.append(item)

    metricas = pd.DataFrame(metricsList, columns=constants.METRICAS)
    return metricas, metricsPerClient


def NewMRR(cliente, valor, mes, ano):
    '''É o valor pago por clientes que fizeram o primeiro pagamento no mês
     analisado.'''
    if (cliente['dataDeEntrada'].dt.year.values[0] == ano) & (cliente['dataDeEntrada'].dt.month.values[0] == mes):
        return valor
    else:
        return 0.0


def ExpansionMRR(cliente, valor, mes, ano):
    '''É a diferença entre o valor pago no mês atual e o valor pago no mês
    anterior por clientes que pagaram mais no mês atual do que no mês
    anterior.'''
    if(cliente.empty == True):
        return 0.0
    if cliente['valor'].values[0] > valor:
        return 0.0
    else:
        return valor - cliente['valor'].values[0]


def ContractionMRR(cliente, valor, mes, ano):
    '''É a diferença entre o valor pago no mês atual e o valor pago no mês
    anterior por clientes que pagaram mais no mês anterior do que no mês
    analisado.'''
    if(cliente.empty == True):
        return 0.0
    if cliente['valor'].values[0] < valor:
        return 0.0
    else:
        return cliente['valor'].values[0] - valor


def CancelledMRR():
    '''É valor pago no mês anterior ao analisado por clientes que não pagaram
    o mês analisado.'''
    print('Cancelled MRR')


def ResurrectedMRR():
    '''É o valor pago por clientes que não pagaram o mês anterior ao
    analisado,mas já tiveram um pagamento no passado e realizaram um novo
    pagamento no mês analisado.'''
    print('Resurrected MRR')
