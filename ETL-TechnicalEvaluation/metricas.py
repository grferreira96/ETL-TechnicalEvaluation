'''Métricas SaaS mensais'''

def MonthlyRecurringRevenue():
    '''É o valor pago mensalmente por cada cliente.'''
    print('MRR')

def NewMRR():
    '''É o valor pago por clientes que fizeram o primeiro pagamento no mês analisado.'''
    print('New MRR')

def ExpansionMRR():
    '''É a diferença entre o valor pago no mês atual e o valor pago no mês anterior por 
        clientes que pagaram mais no mês atual do que no mês anterior.'''
    print('Expansion MRR')

def ContractionMRR():
    '''É a diferença entre o valor pago no mês atual e o valor pago no mês anterior por 
        clientes que pagaram mais no mês anterior do que no mês analisado.'''
    print('Contraction MRR')

def CancelledMRR():
    '''É valor pago no mês anterior ao analisado por clientes que não pagaram o mês analisado.'''
    print('Cancelled MRR')

def ResurrectedMRR():
    '''É o valor pago por clientes que não pagaram o mês anterior ao analisado, mas já tiveram 
        um pagamento no passado e realizaram um novo pagamento no mês analisado.'''
    print('Resurrected MRR')