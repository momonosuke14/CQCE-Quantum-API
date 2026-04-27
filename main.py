import streamlit as st
import math
import numpy as np
import pandas as pd
from scipy.special import expit
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

# --- CONFIGURAÇÃO E ESTILO ---
st.set_page_config(page_title="CQCE Quantum Command", page_icon="🧪", layout="wide")

st.markdown("""
    <style>
    .reportview-container { background: #0a0a12; }
    .metric-card {
        background-color: #161b22;
        border: 1px solid #30363d;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# --- ENGINE QUÂNTICA AVANÇADA ---
class AdvancedQuantumEngine:
    def __init__(self):
        self.simulator = AerSimulator()

    def calcular_incerteza_heisenberg(self, noise):
        # O princípio da incerteza: Delta X * Delta P >= h_bar / 2
        # Simulamos que quanto maior o ruído, maior a incerteza do sistema
        h_bar = 0.6582 # eV·fs (simplificado)
        incerteza = (noise / 100) * (h_bar / 2)
        return incerteza

    def indice_instabilidade(self, eficiencia, entropia):
        # Cálculo híbrido de estabilidade
        instabilidade = (1 - eficiencia) * entropia
        return instabilidade * 100

    def gerador_ressonancia(self, noise):
        # Simula a ressonância magnética do computador físico
        freq = np.linspace(0, 10, 100)
        amplitude = np.sin(freq * (noise/100)) * np.exp(-freq/5)
        return pd.DataFrame({'Frequência (GHz)': freq, 'Ressonância': amplitude})

    def algoritmo_ia_quantica(self, noise):
        # Simula funções de IA baseadas em Qubits (Portas de Rotação e Identidade)
        qc = QuantumCircuit(3)
        for i in range(3):
            qc.rx(noise * 0.001 * math.pi, i)
            qc.h(i)
        qc.measure_all()
        return self.simulator.run(qc, shots=1024).result().get_counts()

engine = AdvancedQuantumEngine()

# --- INTERFACE DE COMANDO ---
st.title("🌌 CQCE - Quantum IA & Command Center")
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2103/2103633.png", width=100)

# --- BLUETOOTH & CONECTIVIDADE ---
st.sidebar.header("📡 Conectividade")
bt_status = st.sidebar.toggle("Ativar Bluetooth (Caixa de Som)")
if bt_status:
    st.sidebar.success("Procurando dispositivos CQCE...")
    st.sidebar.info("Conectado: 'Caixa_Quantica_01'")

st.sidebar.divider()

# Parâmetros de Entrada
st.sidebar.header("⚙️ Variáveis de Campo")
sensor_val = st.sidebar.slider("Ruído do Sensor (Hardware)", 0, 1000, 450)
shots = st.sidebar.select_slider("Potência da IA (Shots)", options=[1024, 2048, 4096, 8192])

# --- PROCESSAMENTO ---
counts_ia = engine.algoritmo_ia_quantica(sensor_val)
eficiencia = (sum([v for k, v in counts_ia.items() if k.count('1') > 1]) / 1024)
entropia = -sum([(v/1024)*math.log2(v/1024) for v in counts_ia.values()])
incerteza = engine.calcular_incerteza_heisenberg(sensor_val)
instabilidade = engine.indice_instabilidade(eficiencia, entropia)

# --- PAINEL DE ÍNDICES (A sua nova funcionalidade!) ---
st.subheader("📊 Índices de Telemetria Quântica")
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("Índice de Incerteza", f"Δ {incerteza:.4f}")
with c2:
    st.metric("Instabilidade Total", f"{instabilidade:.2f}%", delta=f"{sensor_val/100}%", delta_color="inverse")
with c3:
    st.metric("Entropia de IA", f"{entropia:.3f} bits")
with c4:
    st.metric("Sincronia Bluetooth", "98%" if bt_status else "0%")

st.divider()

# --- VISUALIZAÇÃO DE RESSONÂNCIA ---
col_left, col_right = st.columns([3, 2])

with col_left:
    st.subheader("🛰️ Ressonância Magnética do Computador Físico")
    res_data = engine.gerador_ressonancia(sensor_val)
    st.area_chart(res_data.set_index('Frequência (GHz)'), color="#00ffcc")

with col_right:
    st.subheader("🧠 Saída da IA Quântica")
    # Gráfico de barras com as cores que você escolheu
    df_ia = pd.DataFrame.from_dict(counts_ia, orient='index', columns=['Ocorrências'])
    st.bar_chart(df_ia, color="#7000ff")

# --- ÁREA DE CÁLCULOS TÉCNICOS ---
with st.expander("📝 Ver Cálculos Matemáticos da IA"):
    st.latex(r"|\psi\rangle = \cos(\theta/2)|0\rangle + e^{i\phi}\sin(\theta/2)|1\rangle")
    st.write(f"Cálculo da Matriz de Densidade para ruído de **{sensor_val} units**:")
    st.write(f"Incerteza Relativa calculada: **{(incerteza * 100):.6f}**")

# --- BOTÕES DE COMANDO ---
st.sidebar.divider()
if st.sidebar.button("🔊 Testar Ressonância na Caixa"):
    st.toast("Enviando pulso senoidal via Bluetooth...")
    st.balloons()

if st.sidebar.button("🚨 Resetar Núcleo"):
    st.warning("Reiniciando matrizes de coerência...")
