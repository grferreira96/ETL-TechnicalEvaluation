'''extração, transformação e carregamento'''
import requests
from requests.exceptions import HTTPError
import pandas as pd
import constants


def extract():
    '''Extração'''
    payments_df = readPaymentsData()
    clients = getClientes()
    clientes_df = pd.DataFrame(clients)
    return payments_df, clientes_df


def transform(payments_df, clientes_df):
    '''Transformação'''
    payments_df = transformPaymentsData(payments_df)
    clientes_df = reindexingClient(clientes_df)
    metricsPerClient = transformMetrics(payments_df, clientes_df)

    return payments_df, clientes_df, metricsPerClient


def load():
    '''Carregamento'''
    print('load')


def getClientes():
    '''Carrega os clientes de 'https://demo4417994.mockable.io/clientes/'
    e retorna um JSON'''

    url = 'https://demo4417994.mockable.io/clientes/'
    response = requests.get(url)

    try:
        response = requests.get(url)
        if not response.status_code // 100 == 2:
            return "Erro: Resposta inesperada {}".format(response)
        json_obj = response.json()
        return json_obj
    except requests.exceptions.RequestException as e:
        return "Erro: {}".format(e)


def readPaymentsData():
    '''Carrega os dados de pagamentos dos clientes'''
    url = 'https://drive.google.com/uc?authuser=0&id=1GlYrv7ex0ClxQwQ0NvJ4GTUGre7s8vtw&export=download'
    df = pd.read_csv(
        url,
        index_col=False,
        header=None,
        names=['clienteID', 'dataDoPagamento', 'valor', 'plano'])
    return df


def transformPaymentsData(payments_df):
    '''Transformação dos dados em pagamentos.csv'''

    payments_df['dataDoPagamento'] = pd.to_datetime(payments_df['dataDoPagamento'], format='%d/%m/%Y')

    payments_df['valor'] = payments_df['valor'].str.split(' ', n=1, expand=True)[1]
    payments_df['valor'] = pd.to_numeric(payments_df['valor'].str.replace(',', '.'))
    plano = payments_df['plano'].str.split('/', n=1, expand=True)
    payments_df['plano'] = plano[0]
    payments_df['duracao'] = pd.to_numeric(plano[1])

    return payments_df


def transformMetrics(payments_df, clientes_df):
    '''Transformação dos dados de pagamentos.csv'''

    itensList = []

    for index, row in payments_df.iterrows():
        month_iterator = row['duracao']
        initialMonth = row['dataDoPagamento'].month
        finalPagamento = row['dataDoPagamento'] + pd.DateOffset(months=month_iterator-1)
        valor = row['valor']

        clientes_df.at[row['clienteID'], 'numeroDeContratos'] = clientes_df.loc[row['clienteID']]['numeroDeContratos'] + 1
        
        for i in range(initialMonth-1, (initialMonth + month_iterator)-1):
            if clientes_df.loc[row['clienteID']]['dataDeEntrada'] > row['dataDoPagamento']:
                clientes_df.at[row['clienteID'], 'dataDeEntrada'] = row['dataDoPagamento']

            clientes_df.at[row['clienteID'], 'teveContrato'] = True

            if clientes_df.loc[row['clienteID']]['ultimoContrato'] < row['dataDoPagamento']:
                clientes_df.at[row['clienteID'], 'ultimoContrato'] = row['dataDoPagamento']
            if clientes_df.loc[row['clienteID']]['ultimoPagamento'] < finalPagamento:
                clientes_df.at[row['clienteID'], 'ultimoPagamento'] = finalPagamento

            item = [
                index,
                row['clienteID'],
                -1,
                (i % 12) + 1,
                (finalPagamento.year if i >= 12 else row['dataDoPagamento'].year),
                valor / month_iterator
            ]
            itensList.append(item)

    # print(itensList)

    metricsPerClient = pd.DataFrame(itensList, columns=constants.COLUNAS_MESES)

    return metricsPerClient


def reindexingClient(clientes_df):
    clientes_df = clientes_df.reindex(columns=clientes_df.columns.tolist() + constants.CLIENTE_REINDEX)
    clientes_df['dataDeEntrada'] = pd.to_datetime(pd.Timestamp.max, format='%d/%m/%Y')
    clientes_df['teveContrato'] = False
    clientes_df['ultimoContrato'] = pd.to_datetime(pd.Timestamp.min, format='%d/%m/%Y')
    clientes_df['ultimoPagamento'] = pd.to_datetime(pd.Timestamp.min, format='%d/%m/%Y')
    clientes_df['numeroDeContratos'] = 0

    return clientes_df
