
from qiskit import ClassicalRegister, QuantumCircuit, QuantumRegister
from qiskit.circuit.library.generalized_gates import UnitaryGate
from qiskit.quantum_info import Operator

from create_u_gate import CREATE_U_GATE
from hamiltonian import HeH_HAMILTONIAN

import numpy as np

from qiskit import transpile
from qiskit_aer import AerSimulator


def CREATE_IPQE_CIRCUIT(t, k, phi):

    sim = AerSimulator()

    my_hamil = HeH_HAMILTONIAN()

    hamil_qubits = my_hamil.num_qubits

    ancilla = QuantumRegister(1, name = "ancilla")
    system_qubits = QuantumRegister(hamil_qubits, name="q")
    classical = ClassicalRegister(1)
    circuit = QuantumCircuit(ancilla, system_qubits, classical)

    circuit.h(0)

    my_u_gate = CREATE_U_GATE()

    my_trotter_op = Operator(my_u_gate)

    trotter_op_to_power = (my_trotter_op)**2**(k-1)

    controlled_u_gate = UnitaryGate(trotter_op_to_power, label=f"U^{2**(k-1)}").control()

    circuit = circuit.compose(controlled_u_gate, circuit.qubits)

    sum_value = 0
    digits_list = list(phi)
    j_values = list(range(k+1,t+1))

    for index, value in enumerate(digits_list):
        numerator = int(value)
        denominator = 2**(j_values[index] - k + 1)

        sum_value += numerator/denominator


    # Here we implement the Z_wk gate
    wk = (-2) * (np.pi) * (sum_value)



    circuit.p(wk, 0)

    circuit.h(0)

    circuit.measure(0, 0)

    counts = sim.run(transpile(circuit, sim), shots = 1000).result().get_counts()

    if counts["0"] > counts["1"]:
        return "0"
    elif counts["0"] < counts["1"]:
        return "1"
