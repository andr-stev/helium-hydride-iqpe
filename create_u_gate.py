
from qiskit import ClassicalRegister, QuantumCircuit, QuantumRegister

from create_trotterized_circuits import CREATE_PAULI_STRING_GATE
from hamiltonian import HeH_HAMILTONIAN

import numpy as np

def CREATE_U_GATE():

    my_hamil = HeH_HAMILTONIAN()

    num_qubits = my_hamil.num_qubits

    control = QuantumRegister(1, name="ancilla")
    system = QuantumRegister(num_qubits, name="q")
    classical = ClassicalRegister(1)
    circuit = QuantumCircuit(control, system, classical)

    # print(len(my_hamil))
    for i in range(len(my_hamil)):

        my_pauli_string = my_hamil[i].paulis
        my_coefficient = np.real(my_hamil[i].coeffs)

        trotterized_gate = CREATE_PAULI_STRING_GATE(my_pauli_string[0], my_coefficient[0])

        circuit = circuit.compose(trotterized_gate, circuit.qubits)



    print(circuit.draw("text"))

CREATE_U_GATE()
