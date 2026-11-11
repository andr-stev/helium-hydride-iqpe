
import numpy
from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit import Gate

from hamiltonian import HeH_HAMILTONIAN


def CREATE_PAULI_STRING_GATE(pauli_string: str, coefficient: float) -> Gate:
    """Create the Trotterized quantum circuit from a Pauli string and coefficient.

    Args:
        pauli_string: A string representing the Pauli operators (X, Y, Z, I).
                      The string is interpreted from right to left (little-endian).
                      Example: "YXXY" applies Y to q_0, X to q_1, etc.
        coefficient: The rotation angle coefficient for the controlled Rz gate.
                    This scales the phase rotation applied by the control qubit.

    Returns:
        QuantumGate: A QuantumGate representing the constructed circuit.

    Note:
        The circuit structure is:
        1. Apply basis rotations to transform Pauli operators to Z-basis
        2. Apply controlled-CNOT gates to create entanglement between qubits
        3. Apply controlled Rz(2*coefficient) on the control qubit
        4. Undo CNOT entanglement
        5. Undo basis rotations to restore original basis

    Example:
        >>> CREATE_PAULI_STRING_GATE("YXXY", 1.0)
        Returns a gate that can be applied to another circuit.
    """
    # Determine the number of qubits required based on the Pauli string length
    number_of_qubits = len(pauli_string)

    # Create quantum registers: one control qubit and n gate qubits
    # control = QuantumRegister(1, name="control")
    gate_qubits = QuantumRegister(number_of_qubits, name="q")

    # Initialize the quantum circuit with control and gate qubits
    circuit = QuantumCircuit(gate_qubits, name=f"{pauli_string}")

    # Parse the Pauli string and reverse it to process from least significant qubit
    pauli_gates_list = list(pauli_string)
    pauli_gates_list.reverse()

    print(pauli_gates_list)

    # Apply basis rotations for X and Y Pauli operators
    # X basis: H gate (Hadamard)
    # Y basis: S^† followed by H gate

    # Need one fewer cnot that the total number of non idendity gates
    cnots_needed = -1
    for gate in pauli_gates_list:
        if gate != "I":
            cnots_needed += 1


    for i in range(number_of_qubits):
        pauli_op = pauli_gates_list[i]
        qubit_idx = i  # Account for the control qubit at index 0

        if (pauli_op == "X") & (qubit_idx <= cnots_needed):
            # Hadamard transforms Z-basis to X-basis
            circuit.h(qubit_idx)
        elif (pauli_op == "Y") & (qubit_idx <= cnots_needed):
            # S^† followed by Hadamard transforms Z-basis to Y-basis
            circuit.sdg(qubit_idx)
            circuit.h(qubit_idx)

    # Apply controlled-CNOT gates up the line to entangle the gate qubits
    for k in range(cnots_needed):
        control_qubit_idx = cnots_needed - k
        target_qubit_idx = cnots_needed - 1 - k
        circuit.cx(control_qubit_idx, target_qubit_idx)

    # Apply the controlled Rz rotation on q_0
    if cnots_needed == -1:
        circuit.p(-coefficient, 0)
    else:
        circuit.rz(2 * coefficient, 0)

    # Undo the CNOT entanglement
    for k in range(cnots_needed):
        control_qubit_idx = 1 + k
        target_qubit_idx = k
        circuit.cx(control_qubit_idx, target_qubit_idx)

    # Undo basis rotations to restore qubits to original basis
    for i in range(number_of_qubits):
        pauli_op = pauli_gates_list[i]
        qubit_idx = i

        if (pauli_op == "X") & (qubit_idx <= cnots_needed):
            # Hadamard is self-inverse
            circuit.h(qubit_idx)
        elif (pauli_op == "Y") & (qubit_idx <= cnots_needed):
            # Reverse of Y basis: H followed by S
            circuit.h(qubit_idx)
            circuit.s(qubit_idx)

    print(circuit.draw("text"))

    return circuit.to_gate()

hamil_test = HeH_HAMILTONIAN()
print(hamil_test)
for i in range(len(hamil_test)):
    mystring = hamil_test[i].paulis
    myproperstr = str(mystring[0])
    mycoeff = numpy.real(hamil_test[i].coeffs)

    CREATE_PAULI_STRING_GATE(str(mystring[0]), mycoeff[0])
    print("\n\n")
    #

# CREATE_PAULI_STRING_GATE("XYXY", 1)
