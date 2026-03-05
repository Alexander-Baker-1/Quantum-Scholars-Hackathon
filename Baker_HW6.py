from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import QasmSimulator
from qiskit.quantum_info import Statevector

def generate_random_string(n):
    # Create a quantum circuit with n qubits and n classical bits
    qr = QuantumRegister(n, 'q')
    cr = ClassicalRegister(n, 'c')

    qc = QuantumCircuit(qr,cr)

    # Apply the Hadamard gate to each qubit to create a superposition
    for i in range(n):
        qc.h(i)

    # Get the state vector of the quantum circuit
    state = Statevector(qc.reverse_bits())

    # Measure the qubits and store the results in the classical bits
    for i in range(n):
        qc.measure(i, i)

    # Use the QasmSimulator to execute the circuit and get the counts
    backend = QasmSimulator()
    result = backend.run(qc.reverse_bits(), shots=1).result()
    counts = result.get_counts()

    # Get the random number from the counts
    random_number = list(counts.keys())[0]
    return random_number

def generate_alice_state(a):
    # Create a quantum circuit with n qubits
    n = len(a)
    qc = QuantumCircuit(n)

    # Apply the Hadamard gate to each qubit where a[i] is '1'
    for i in range(n):
        if a[i] == '1':
            qc.h(i)
    
    # Use reverse_bits to stay consistent with the rest of the code
    reversed_qc = qc.reverse_bits()
    state = Statevector(reversed_qc)
    
    return state


def eavesdrop(e, n, state):
    # If Eve is present, she applies Hadamard gates to all qubits
    if e:
        # Create a quantum circuit with n qubits
        qc = QuantumCircuit(n)

        # Apply the Hadamard gate to each qubit
        for i in range(n):
            qc.h(i) 
        
        # Evolve the state with Eve's operation
        new_state = state.evolve(qc)

        return new_state
        
    else:
        return state

def bob_evolution(b):
    # Create a quantum circuit with n qubits
    n = len(b)
    qc = QuantumCircuit(n)

    # Apply the Hadamard gate to each qubit where b[i] is '1'
    for i in range(n):
        if b[i] == '1':
            qc.h(i)

    # Use reverse_bits to stay consistent with the rest of the code
    return qc.reverse_bits()

def measurement_result(b, state, U_b):
    # Evolve the state with Bob's operation and measure it to get string t
    new_state = state.evolve(U_b)
    t = new_state.sample_memory(1)[0]
    return t 

def alice_create_secret_key(a, t):
    # Alice constructs her key SK_a from the bits of a where t[i] is '1'
    SK_a = ""
    for i in range(len(a)):
        if t[i] == '1':
            SK_a += a[i]
    return SK_a

def bob_create_secret_key(b, t):
    # Bob constructs his key SK_b from the bits of b where t[i] is '1', but flips them
    SK_b = ""
    for i in range(len(b)):
        if t[i] == '1':
            bit = '1' if b[i] == '0' else '0'
            SK_b += bit
    return SK_b

def check_for_Eve(SK_a, SK_b):
    # Check if SK_a and SK_b are the same. If not, Eve is detected.
    if SK_a != SK_b:
        return "Eve detected!"
    else:
        return SK_a

def main():
    n = int(input("Security parameter: ")) # Choose security parameter
    e = bool(int(input("Eavesdrop? (0=n,1=y) "))) # Choose to have eavesdropper or not
    
    a = generate_random_string(n) # Alice generates string a
    state = generate_alice_state(a) # Alice encodes a into quantum state
    
    # Alice sends state to Bob
    state = eavesdrop(e,n,state) # Eve intercepts state
   
    # Eve sends (possibly modified) state to Bob
    b = generate_random_string(n) # Bob generates string b
    U_b = bob_evolution(b) # Bob constructs his unitary U_b
    t = measurement_result(b,state,U_b) # Bob measures state, constructs string t
    
    # Bob sends t to Alice
    SK_a = alice_create_secret_key(a,t) # Alice constructs her key SK_a
    SK_b = bob_create_secret_key(b,t) # Bob constructs his key SK_b
    
    check = check_for_Eve(SK_a, SK_b) # Check for Eve
    
    if check == "Eve detected!": # Eve detected, abort
        print("Eve detected! Aborting protocol.")
    else: # Eve not detected
        print("Eve not detected.")
        SK = check # Set SK to unchecked bits of SK_a
        
        print("Secret Key: " + SK)
        print("Secret Key Length: " + str(len(SK)))

if __name__ == "__main__":
    main()