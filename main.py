import streamlit as st
import math
import numpy as np
from scipy.special import expit
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="CQCE Quantum Monitor", page_icon="⚛️", layout="wide")

st.title("🛰️ Sistema Quântico CQCE")
st.markdown("---")

# --- MOTOR QUÂNTICO ---
class QuantumEngine:
    def __init__(self):
        self.simulator = AerSimulator()

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

    def calculate_entropy(self, noise_level):
        p = expit((noise_level - 500) / 100) 
        return - (p * math.log2(p + 1e-9) + (1-p) * math.log2(1-p + 1e-9))

engine = QuantumEngine()

# --- INTERFACE ---
st.sidebar.header("📡 Controle de Hardware")
noise_input = st.sidebar.slider("Simular Ruído do Sensor", 0, 1000, 500)

eficiencia = engine.processamento_inverso(noise_input)
entropia = engine.calculate_entropy(noise_input)

# Painel de métricas
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Eficiência Quântica", f"{eficiencia * 100:.2f}%")
with col2:
    st.metric("Entropia do Sinal", f"{entropia:.4f}")
with col3:
    status = "ESTÁVEL" if abs(0.5 - eficiencia) < 0.2 else "INSTÁVEL"
    st.metric("Status do Sistema", status)

st.divider()

# Gráfico de Ressonância (Simulado)
st.subheader("📊 Gráfico de Ressonância Magnética")
chart_data = np.random.randn(20, 3)
st.line_chart(chart_data)

if st.button("🚀 Disparar Pulso Quântico"):
    st.balloons()
    st.success("Pulso processado pelo Qiskit com sucesso!")
