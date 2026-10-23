from ortools.sat.python import cp_model 
from scheduler import risolvi_scheduling

numero_jobs = int(input("How many jobs do you want to plan? "))
capacita_operatori = int(input("How many operators are available? "))

operazioni = {}
scadenze = {}
precedenze = []

for job_index in range(numero_jobs):
    job = input(f"Enter the name of job {job_index + 1}: ")
    scadenze[job] = int(input(f"Enter the due date for {job}: "))

    numero_operazioni = int(input(f"How many operations does {job} have? "))

    for numero_operazione in range(1, numero_operazioni + 1):
        if numero_operazione > 1:
            precedenze.append(((job,numero_operazione - 1),(job, numero_operazione)))
        operatori = int(input(
            f"How many operators are required for {job}, operation {numero_operazione}? "
        ))

        numero_macchine = int(input(
            f"How many eligible machines are there for {job}, operation {numero_operazione}? "
        ))

        durate = {}
        for machine_index in range(numero_macchine):
            macchina = input(f"Enter the name of eligible machine {machine_index + 1}: ")
            durata = int(input(f"Enter its processing time for {job}, operation {numero_operazione}: "))
            durate[macchina] = durata

        operazioni[(job, numero_operazione)] = {
            "durate": durate,
            "operatori": operatori,
        }

horizon = sum( max(operazioni[operazione]['durate'][macchina] for macchina in operazioni[operazione]['durate'])
               for operazione in operazioni)

print("Horizon:", horizon)
print("Operations:", operazioni)
print("Precedences:", precedenze)

risultati = risolvi_scheduling(
    operazioni, precedenze, scadenze, capacita_operatori, horizon
)

# Check if there is an optimal solution and, in that case, show the plan and the value of the objective function

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