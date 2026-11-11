
from qiskit import ClassicalRegister, QuantumCircuit, QuantumRegister
from qiskit.circuit.library.generalized_gates import UnitaryGate
from qiskit.quantum_info import Operator

from create_u_gate import CREATE_U_GATE
from hamiltonian import HeH_HAMILTONIAN

import numpy as np

from qiskit import transpile
from qiskit_aer import AerSimulator

from ipqe_circuit import CREATE_IPQE_CIRCUIT


def IPQE_RESULTS(t):

    k_values = list(range(1,t+1))
    k_values.reverse()

    phi = ""
    for k in k_values:
        bit_result = CREATE_IPQE_CIRCUIT(t, k, phi)
        phi = bit_result + phi

    print("Binary Result:", phi)
    binary_fraction = "0." + phi
    print("Binary Fraction:", binary_fraction)


    binary_digits = list(phi)
    # print(binary_digits,"\n")

    decimal_fraction = 0
    for i, val in enumerate(binary_digits):
        frac = int(val) / 2**(i+1)
        decimal_fraction += frac
        # print("Fraction:", frac)
        # print("Decimal sum:", decimal_fraction,"\n")

    print("Phi:", decimal_fraction)
    print("E_0 = -2pi Phi =", -2*np.pi*decimal_fraction)
#     result_str = "0." + phi
#
#     print(result_str)
#
#
#     result = int(phi, 2)
#     print(result)
#     result_decimal_str

IPQE_RESULTS(8)
