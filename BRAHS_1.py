from qiskit import *
from qiskit.quantum_info import Statevector
from qiskit_aer import QasmSimulator

import matplotlib.pyplot as plt
import numpy as np

# Get the number of q-bits from the user
n = int(input("Number of q-bits: "))

# Create a quantum circuit with n qubits and n classical bits
qr = QuantumRegister(n, 'q')
cr = ClassicalRegister(n, 'c')

qc = QuantumCircuit(qr,cr)
print(qc)

# Apply the Hadamard gate to each qubit to create a superposition
for i in range(n):
    qc.h(i)

# Get the state vector of the quantum circuit
state = Statevector(qc.reverse_bits())
print(state.data)

print(qc)

# Measure the qubits and store the results in the classical bits
for i in range(n):
    qc.measure(i, i)

# Use the QasmSimulator to execute the circuit and get the counts
backend = QasmSimulator()
result = backend.run(qc.reverse_bits(), shots=10000).result()
counts = result.get_counts()

# Sort the counts by bit string
sorted_counts = dict(sorted(counts.items(), key=lambda item: item[0]))

print(sorted_counts)

# Plot the histogram of the counts
bit_strings = list(sorted_counts.keys())
number = list(sorted_counts.values())

plt.bar(bit_strings, number)

plt.xlabel("Bit Strings")
plt.ylabel("Number")
plt.title("Random Number Generator Histogram")

plt.show()