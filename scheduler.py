from ortools.sat.python import cp_model

def risolvi_scheduling(operazioni, precedenze, scadenze, capacita_operatori, horizon):
    def sort_inizio(e):
        return e['start']

    # Prima verifico che ogni operazione data possa essere eseguita da almeno una macchina
    for operazione in operazioni:
        if not operazioni[operazione]['durate']:  
            raise ValueError(f"L'operazione {operazione} non è eseguibile da nessuna macchina")
        else:
            for macchina in operazioni[operazione]['durate']:
                if operazioni[operazione]['durate'][macchina] <= 0:
                    raise ValueError(f"L'operazione {operazione} eseguibile dalla macchina {macchina} ha durata non positiva!")
    operazione_con_macchina = [(operazione, macchina) for operazione in operazioni for macchina in operazioni[operazione]['durate']]
    macchine = {
        macchina
        for dati in operazioni.values()
        for macchina in dati['durate']
    }
    numero_operatori = [operazioni[operazione]['operatori'] for (operazione, macchina) in operazione_con_macchina]

    jobs = {operazione[0] for operazione in operazioni}

    # Controllo che ogni job sia nelle scadenze e che ogni job nelle scadenze sia nel dizionario jobs:
    # in caso contrario sollevo un ValueError specifico
    for job in jobs:
        if job not in scadenze: raise ValueError(f"Manca la scadenza per l'ordine {job}")
    for job in scadenze:
        if job not in jobs: raise ValueError(f"L'ordine {job} è inesistente")

    # Definisco il dizionario delle ultime operazioni: qui uso che l'ultima operazione di ogni job 
    # è quella con l'indice più alto
    ultime_operazioni = { job : (job, max([operazione[1] for operazione in operazioni if operazione[0] == job])) for job in jobs}
    risultati = {}

    # Verifico che le operazioni nella lista precedenze siano in operazioni, altrimenti sollevo ValueError
    for (precedente, successiva) in precedenze:
        if precedente not in operazioni:
            raise ValueError(f"L'operazione {precedente} non è presente tra le operazioni degli ordini")
        if successiva not in operazioni:
            raise ValueError(f"L'operazione {successiva} non è presente tra le operazioni degli ordini")

    # Dichiarare il modello
    model = cp_model.CpModel()

    # Definizione delle variabili
    inizio = {operazione : model.new_int_var(0, horizon, f"inizio_{operazione}") for operazione in operazioni}
    fine = {operazione : model.new_int_var(0, horizon, f"fine_{operazione}") for operazione in operazioni}

    assegnata = {(operazione, macchina) : model.new_bool_var(f"assegnata_{(operazione, macchina)}") 
              for (operazione, macchina) in operazione_con_macchina}

    # Variabili di ritardo dei jobs
    ritardo = { job : model.new_int_var(0, horizon, f"ritardo_{job}") for job in jobs }

    # Vincolo sull'unicità degli intervalli opzionali
    for operazione in operazioni:
        model.add(sum(assegnata[(operazione,macchina)] for macchina in operazioni[operazione]['durate']) == 1)

    # Creazione intervalli opzionali
    intervalli_opzionali = {(operazione, macchina): 
                     model.new_optional_interval_var(inizio[operazione], operazioni[operazione]['durate'][macchina], 
                                         fine[operazione], assegnata[(operazione, macchina)], f"intervalli_opzionali_{(operazione,macchina)}")
                                        for (operazione, macchina) in operazione_con_macchina}

    # Creazione vincoli sulle precedenze
    for precedente, successiva in precedenze:
        model.add(fine[precedente] <= inizio[successiva])

    # No overlap per gli intervalli con la stessa macchina
    intervalli_per_macchina = { macchina : [intervalli_opzionali[(operazione, macchina)] 
                                        for operazione in operazioni if macchina in operazioni[operazione]['durate']]
                               for macchina in macchine}
    for macchina in macchine:
        model.add_no_overlap(intervalli_per_macchina[macchina])

    # Vincoli sulle richieste delle operazioni con data capacità di operatori
    model.add_cumulative([intervalli_opzionali[(operazione,macchina)] for (operazione, macchina) in operazione_con_macchina], 
                            numero_operatori, capacita_operatori)

    # Vincoli sulle variabili dei ritardi
    for job in jobs:
        model.add_max_equality(ritardo[job], [0, fine[ultime_operazioni[job]] - scadenze[job]])

    # Definizione della variabile makespan
    makespan = model.new_int_var(0, horizon, "makespan")

    # Vincoli sul makespan maggiore o uguale della fine di ogni job
    for job in jobs:
        model.add(makespan >= fine[ultime_operazioni[job]])

    # Definiamo la funzione obiettivo da minimizzare
    model.minimize(makespan + sum(ritardo[job] for job in jobs))

    # Chiama il risolutore
    solver = cp_model.CpSolver()
    status = solver.solve(model)

    risultati['stato'] = status

    # Condizioni sullo stato per la retituzione di variabili
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE: 
        risultati['objective_value'] = solver.objective_value
        risultati['jobs'] = jobs
        risultati['makespan'] = solver.value(makespan)
        risultati['programma'] = [
                {'job' : operazione[0],
                 'operation' : operazione[1], 
                 'machine' : macchina, 
                 'start' : solver.value(inizio[operazione]), 
                 'end' : solver.value(fine[operazione])
                }
                            for operazione in operazioni for macchina in operazioni[operazione]['durate']
                            if solver.value(assegnata[(operazione, macchina)]) == 1
                                 ]
        risultati['programma'].sort(key=sort_inizio)
        risultati['ritardo'] = {job : solver.value(ritardo[job]) for job in jobs} 
         
    return risultati