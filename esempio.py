# In questo file eseguiamo la funzione risolvi_scheduling sull'esempio che abbiamo preso come riferimento
from ortools.sat.python import cp_model 
from scheduler import risolvi_scheduling

# Definire i dizionari utili per le variabili
operazioni = {('J1',1): {'durate' : { 'M1': 3}, 'operatori' : 1}, 
              ('J1',2): {'durate' : { 'M1': 3, 'M2': 2}, 'operatori' : 1},
              ('J2',1): {'durate' : { 'M2': 2}, 'operatori' : 2}, 
              ('J2',2): {'durate' : { 'M1': 4}, 'operatori': 1}
              }

precedenze = [(('J1', 1), ('J1', 2)), (('J2', 1), ('J2', 2))]
scadenze = { 'J1' : 6, 'J2' : 8}

# Orizzonte totale delle operazioni
horizon = 12

# Capacità totale egli operatori
capacita_operatori = 2

# Chiamo la funzione risolvi_scheduling per questi parametri

risultati = risolvi_scheduling(
    operazioni, precedenze, scadenze, capacita_operatori, horizon
)

if risultati['stato'] == cp_model.INFEASIBLE:
    print('There is not any feasible solution')
elif risultati['stato'] == cp_model.FEASIBLE or risultati['stato'] == cp_model.OPTIMAL:
    if risultati['stato'] == cp_model.FEASIBLE:
        print('The model has a feasible solution')
    else: print('The model has an optimal solution')
    print('Objective value: ', risultati['objective_value'])
    print('Makespan: ', risultati['makespan'])
    for job in sorted(risultati['jobs']):
        print(f"Tardiness of job {job}: ", risultati['ritardo'][job])
    print('Operations plan:')
    for voce in risultati['programma']:
        print(f"Job {voce['job']}, operation {voce['operation']}: machine {voce['machine']}, time interval [{voce['start']}, {voce['end']})")
else: print(risultati['stato'])