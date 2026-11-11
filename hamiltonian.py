import numpy as np
from qiskit.quantum_info import SparsePauliOp
from qiskit_nature.second_q.drivers import PySCFDriver
from qiskit_nature.second_q.mappers import InterleavedQubitMapper, JordanWignerMapper
from qiskit_nature.units import DistanceUnit


def HeH_HAMILTONIAN():
# Build the qubit Hamiltonian for helium hydride (HeH+)
    driver = PySCFDriver(
        atom="He 0 0 0; H 0 0 0.772",  # HeH+ molecule
        basis="sto3g",
        charge=1,  # HeH+ has a +1 charge
        spin=0,
        unit = DistanceUnit.ANGSTROM
    )

    problem = driver.run()


    mapper = JordanWignerMapper()
    interleaved_mapper = InterleavedQubitMapper(mapper)


    # Convert to qubit operator (qubit Hamiltonian)
    qubit_op = interleaved_mapper.map(problem.hamiltonian.second_q_op())
    number_of_qubits = qubit_op.num_qubits

    identity_pauli_string = "I" * number_of_qubits
    nuclear_repulsion = 1.370925
    nuclear_op = SparsePauliOp([identity_pauli_string], nuclear_repulsion)

    helium_hydride_hamiltonian = (qubit_op + nuclear_op).simplify()
    # helium_hydride_hamiltonian.simplify()

    return helium_hydride_hamiltonian

# my_hamiltonian = HeH_HAMILTONIAN()
# # print(my_hamiltonian)
#
# # print(qubit_op)
# #
# test_pauli_strings = my_hamiltonian.paulis # type: ignore
# test_coeffs = my_hamiltonian.coeffs # type: ignore
#
# print(test_pauli_strings, test_coeffs)
#
# # Collect terms with the same coefficient
# collected_dict = {}
# for i in range(len(my_hamiltonian)):
#     collected_dict.setdefault(np.round(np.real(test_coeffs[i]), 6), []).append(str(test_pauli_strings[i]))
#
# for key, values in collected_dict.items():
#     print(key, values)
#
# print(len(my_hamiltonian))
