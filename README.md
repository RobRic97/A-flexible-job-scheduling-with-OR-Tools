# A-flexible-job-scheduling-with-OR-Tools

This project models a flexible job shop scheduling problem using the CP-SAT solver from Google OR-Tools.

## Problem description

A factory must process a set of jobs, each consisting of one or more operations. Each operation can be assigned to one of its eligible machines, and its processing time depends on the selected machine.

The schedule must satisfy the following constraints:

- Each machine can process at most one operation at a time.
- Operations belonging to the same job must respect the specified precedence constraints.
- Each operation requires a given number of operators, and the total number of operators in use cannot exceed the available capacity.
- Each job has a due date.

The objective is to minimize the sum of the makespan and the total job tardiness. The makespan is the completion time of the last job to finish. The tardiness of a job is the amount of time by which it finishes after its due date.

## Project structure

- `scheduler.py` implements the scheduling function using OR-Tools.
- `esempio.py` defines a sample instance with two jobs, two operations per job, and two machines, then prints the resulting schedule.
- `test_scheduler.py` contains tests for an optimal instance, an infeasible instance, and invalid input data.
- `main.py` provides an interactive command-line interface. It prompts the user to enter the number of jobs, the available operator capacity, each job’s due date, and the operations in that job. For each operation, the user specifies its operator requirements and eligible machines with their processing times. The program creates precedence constraints between consecutive operations, calculates the scheduling horizon, calls the solver, and displays the solution status, objective value, makespan, job tardiness, and schedule.
## Requirements

The project requires Python and Google OR-Tools. Install OR-Tools from the project directory with:

```bash
python -m pip install -r requirements.txt
```

## Run the example

From the project directory, run:

```bash
python esempio.py
```

The script prints the solver status, objective value, makespan, job tardiness, and operation schedule.

## Run the tests

From the project directory, run:

```bash
python -m unittest -v
```
The test command reports the result of each test.

## Run the main program

From the project directory, run:

```bash
python main.py
```
This runs the interactive command-line interface.
