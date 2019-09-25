import etl
import metricas
import constants
import pandas as pd

# df, clients = etl.extract()
payments_df, clientes_df = etl.extract()

# df, clients = etl.extract()
payments_df, clientes_df, metricsPerClient = etl.transform(payments_df, clientes_df)

metricas, metricsPerClient = metricas.metricsCalculator(clientes_df, metricsPerClient)

payments_df.to_csv('D:\ETL-TechnicalEvaluation\ETL-TechnicalEvaluation\docs\pagamentos.csv',index=True)
clientes_df.to_csv('D:\ETL-TechnicalEvaluation\ETL-TechnicalEvaluation\docs\clients.csv', index=True)
metricsPerClient.to_csv('D:\ETL-TechnicalEvaluation\ETL-TechnicalEvaluation\docs\metricasCliente.csv',index=True)
metricas.to_csv('D:\ETL-TechnicalEvaluation\ETL-TechnicalEvaluation\docs\metricas.csv',index=True)
