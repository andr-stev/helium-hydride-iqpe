
from qiskit import ClassicalRegister, QuantumCircuit, QuantumRegister

from create_u_gate import CREATE_U_GATE
from hamiltonian import HeH_HAMILTONIAN


def CREATE_IPQE_CIRCUIT():

    my_hamil = HeH_HAMILTONIAN()

    hamil_qubits = my_hamil.num_qubits

    ancilla = QuantumRegister(1, name = "ancilla")
    system_qubits = QuantumRegister(hamil_qubits, name="q")
    classical = ClassicalRegister(1)
    circuit = QuantumCircuit(ancilla, system_qubits, classical)

    circuit.h(0)

    my_u_gate = CREATE_U_GATE()

    circuit = circuit.compose(my_u_gate, circuit.qubits)

    print(circuit.draw("text"))


CREATE_IPQE_CIRCUIT()
