from qiskit import *
from qiskit_aer import QasmSimulator
from qiskit.circuit.library import grover_operator, MCMTGate, ZGate

import matplotlib.pyplot as plt
import numpy as np

def create_oracle(marked_state):
    # Create a quantum circuit with n qubits
    n = len(marked_state)
    qc = QuantumCircuit(n)

    # Apply X gates to qubits where marked_state[i] is '0'
    for i in range(n):
        if marked_state[i] == '0':
            qc.x(n - 1 - i)

    # Apply multi-controlled-Z gate to flip the phase of |111...1>
    qc.append(MCMTGate(ZGate(), n - 1, 1), range(n))

    # Undo the X gates to restore the original basis
    for i in range(n):
        if marked_state[i] == '0':
            qc.x(n - 1 - i)

    return qc

def create_grover_operator(oracle):
    grover_op = grover_operator(oracle)
    return grover_op


def create_grover_circuit(r, grover_op):
    # Get number of qubits from the grover operator
    n = grover_op.num_qubits
    
    # Create a quantum circuit with n qubits and n classical bits
    qc = QuantumCircuit(n, n)
    
    # Apply Hadamard gates to all qubits to create equal superposition
    for i in range(n):
        qc.h(i)
    
    # Attach r copies of the Grover operator to the circuit
    qc.compose(grover_op.power(r), inplace=True)
    
    # Measure all qubits
    for i in range(n):
        qc.measure(i, i)
    
    return qc

def run_grover_circuit(marked_state, r):
    oracle = create_oracle(marked_state)
    grover_op = create_grover_operator(oracle)
    grover_circuit = create_grover_circuit(r, grover_op)
    backend = QasmSimulator()
    grover_circuit = transpile(grover_circuit, backend)
    result = backend.run(grover_circuit.reverse_bits(), shots=10000).result()
    counts = result.get_counts()
    return counts

# Get the marked state and r from the user
marked_state = input("Marked state (4-bit string): ")
r = int(input("Number of Grover iterations (r): "))

n = len(marked_state)
N = 2 ** n

# Build and run the Grover circuit
counts = run_grover_circuit(marked_state, r)

# Sort the counts by bit string and reverse the bit strings to match the original order
sorted_counts = dict(sorted({k[::-1]: v for k, v in counts.items()}.items(), key=lambda item: item[0]))

print(sorted_counts)

# Plot the histogram of the counts
bit_strings = list(sorted_counts.keys())
number = list(sorted_counts.values())

plt.bar(bit_strings, number)

plt.xlabel("Bit Strings")
plt.ylabel("Number")
plt.title(f"Grover's Algorithm | marked_state = {marked_state} | r = {r}")

plt.show()