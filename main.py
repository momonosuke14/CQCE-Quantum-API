import streamlit as st
import math
import numpy as np
from scipy.special import expit
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

# --- CONFIGURAÇÃO DA INTERFACE STREAMLIT ---
st.set_page_config(page_title="CQCE Quantum Monitor", page_icon="⚛️", layout="wide")

st.title("🛰️ Sistema Quântico CQCE")
st.write("O motor quântico está ativo e processando ruído em tempo real.")

# --- LÓGICA DO MOTOR QUÂNTICO (O seu código original) ---
class QuantumEngine:
    def __init__(self):
        self.simulator = AerSimulator()

    def _calculate_tetration(self, n, height):
        if height == 0: return 1
        if height == 1: return n
        if height > 4: height = 4 
        res = n
        for _ in range(height - 1):
            res = math.pow(n, res) if res < 100 else 10**10
        return res

    def calculate_entropy(self, noise_level):
        p = expit((noise_level - 500) / 100) 
        return - (p * math.log2(p + 1e-9) + (1-p) * math.log2(1-p + 1e-9))

    def processamento_inverso(self, noise_level):
        qc = QuantumCircuit(1, 1)
        theta = (noise_level / 1000) * 2 * math.pi
        phi = math.sin(theta) * math.pi 
        qc.rx(theta, 0)
        qc.rz(phi, 0)
        qc.h(0) 
        qc.measure(0, 0)
        job = self.simulator.run(transpile(qc, self.simulator), shots=256)
        counts = job.result().get_counts()
        return counts.get('1', 0) / 256

engine = QuantumEngine()

# --- INTERFACE DE CONTROLE NO SITE ---
st.sidebar.header("📡 Entrada de Hardware")
# Na feira, o Arduino enviará esse dado. Aqui podemos simular ou receber via API.
noise_input = st.sidebar.slider("Nível de Ruído (Sensor)", 0, 1000, 500)

# Processando os dados
eficiencia = engine.processamento_inverso(noise_input)
entropia = engine.calculate_entropy(noise_input)
nivel_tetracao = int(entropia * 3)
distancia_do_caos = abs(0.5 - eficiencia)

# Definindo Status Visual
if distancia_do_caos < 0.1:
    status = "COERÊNCIA CRÍTICA"
    cor = "green"
elif eficiencia > 0.7:
    status = "COLAPSO INDUZIDO"
    cor = "red"
else:
    status = "ESTADO DE REPOUSO"
    cor = "blue"

# --- PAINEL VISUAL ---
col1, col2, col3 = st.columns(3)
col1.metric("Status de Coerência", status)
col2.metric("Eficiência Quântica", f"{eficiencia * 100:.2f}%")
col3.metric("Entropia do Sinal", f"{entropia:.4f}")

st.divider()

if st.button("Simular Disparo Quântico"):
    st.balloons()
    st.success(f"Cálculo finalizado com {nivel_tetracao} níveis de tetração.")
    st.json({
        "qubits_virtuais": engine._calculate_tetration(2, nivel_tetracao),
        "probabilidade_colapso": eficiencia,
        "ruído_bruto": noise_input
    })
