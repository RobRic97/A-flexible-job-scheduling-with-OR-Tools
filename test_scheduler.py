from scheduler import risolvi_scheduling
from ortools.sat.python import cp_model
import unittest
class TestScheduleMethod(unittest.TestCase):
    def setUp(self):
        self.operazioni = {
            ('J1', 1): {'durate': {'M1': 3}, 'operatori': 1},
            ('J1', 2): {'durate': {'M1': 3, 'M2': 2}, 'operatori': 1},
            ('J2', 1): {'durate': {'M2': 2}, 'operatori': 2},
            ('J2', 2): {'durate': {'M1': 4}, 'operatori': 1},
        }
        self.precedenze = [
            (('J1', 1), ('J1', 2)),
            (('J2', 1), ('J2', 2)),
        ]
        self.scadenze = {'J1': 6, 'J2': 8}
        self.horizon = 12

    def test_istanza_base_ottimale(self):

        risultati = risolvi_scheduling(self.operazioni, self.precedenze, self.scadenze, 2, self.horizon)

        self.assertEqual(risultati['stato'], cp_model.OPTIMAL) 

        # Verifico se nella pianificazione ogni operazione compare esattamente una sola volta
        # e se la macchina assegnata all'operazione è tra quelle ammissibili

        for operazione in self.operazioni:
            assegnamenti = [
                voce for voce in risultati['programma']
                if voce['job'] == operazione[0]
                and voce['operation'] == operazione[1]
            ]

            self.assertEqual(len(assegnamenti), 1)

            macchina = assegnamenti[0]['machine']
            self.assertIn(macchina, self.operazioni[operazione]['durate'])
        self.assertAlmostEqual(risultati['objective_value'], 11)
        self.assertEqual(risultati['makespan'], 9)
        self.assertEqual(risultati['ritardo'], {'J1' : 1, 'J2' : 1})

    def test_istanza_infeasible(self):

        risultati = risolvi_scheduling(self.operazioni, self.precedenze, self.scadenze, 1, self.horizon)

        self.assertEqual(risultati['stato'], cp_model.INFEASIBLE)

    def test_errore_precedenze(self):

        precedenze = [
            (('J1', 1), ('J1', 2)),
            (('J2', 1), ('J2', 3)),
        ]

        with self.assertRaises(ValueError):
             risolvi_scheduling(self.operazioni, precedenze, self.scadenze, 2, self.horizon)

    def test_errore_durate_vuote(self):

        operazioni = {
            ('J1', 1): {'durate': {'M1': 3}, 'operatori': 1},
            ('J1', 2): {'durate': {'M1': 3, 'M2': 2}, 'operatori': 1},
            ('J2', 1): {'durate': {}, 'operatori': 2},
            ('J2', 2): {'durate': {'M1': 4}, 'operatori': 1}            
        }

        with self.assertRaises(ValueError):
             risolvi_scheduling(operazioni, self.precedenze, self.scadenze, 2, self.horizon)  

    def test_durata_non_positiva(self):
        operazioni = {
            ('J1', 1): {'durate': {'M1': 3}, 'operatori': 1},
            ('J1', 2): {'durate': {'M1': 0, 'M2': 2}, 'operatori': 1},
            ('J2', 1): {'durate': {'M2': 2}, 'operatori': 2},
            ('J2', 2): {'durate': {'M1': 4}, 'operatori': 1}            
        }     

        with self.assertRaises(ValueError):
             risolvi_scheduling(operazioni, self.precedenze, self.scadenze, 2, self.horizon) 

if __name__ == '__main__':
    unittest.main()