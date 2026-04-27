import streamlit as st
import math
import numpy as np
import pandas as pd
from scipy.special import expit
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

# --- CONFIGURAÇÃO VISUAL ---
st.set_page_config(page_title="CQCE Quantum Command", page_icon="⚛️", layout="wide")

# CSS Customizado para Layout "Gamer/Científico"
st.markdown("""
    <style>
    .main { background-color: #050505; color: #00ffcc; }
    div[data-testid="stMetricValue"] { font-size: 28px; color: #00ffcc; }
    .stButton>button { width: 100%; border-radius: 20px; background: #7000ff; color: white; }
    .stExpander { border: 1px solid #7000ff; background: #111; }
    </style>
    """, unsafe_allow_html=True)

# --- ENGINE ---
class QuantumCore:
    def __init__(self):
        self.sim = AerSimulator()

    def get_heisenberg(self, noise):
        return (noise / 1000) * 0.329 # Simulação da incerteza Delta

    def get_ia_counts(self, sensor_val):
        qc = QuantumCircuit(3)
        qc.h(range(3))
        qc.rx(sensor_val * 0.01, 0)
        qc.measure_all()
        return self.sim.run(qc, shots=1024).result().get_counts()

core = QuantumCore()

# --- SIDEBAR E CONECTIVIDADE ---
st.sidebar.title("📡 HARDWARE LINK")
status_bt = st.sidebar.status("Bluetooth: Desconectado", expanded=False)
if st.sidebar.button("🔗 Parear Caixa de Som"):
    status_bt.update(label="Bluetooth: CONECTADO", state="complete", expanded=False)
    st.sidebar.success("Dispositivo: CQCE-Speaker-01")

st.sidebar.divider()
sensor = st.sidebar.slider("⚡ Ruído do Computador Físico", 0, 1000, 450)
ia_power = st.sidebar.select_slider("🧠 Potência da IA", [256, 1024, 4096])

# --- CÁLCULOS ---
counts = core.get_ia_counts(sensor)
incerteza = core.get_heisenberg(sensor)
eficiencia = (counts.get('111', 0) + counts.get('000', 0)) / 1024
instabilidade = (1 - eficiencia) * (sensor / 500)

# --- LAYOUT PRINCIPAL ---
st.title("🛰️ CQCE - Quantum Command Center")
st.write(f"Sincronização Ativa | Incerteza de Heisenberg: Δ {incerteza:.4f}")

# LINHA 1: ÍNDICES DE TELEMETRIA
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Incerteza (Δ)", f"{incerteza:.5f}")
with col2:
    st.metric("Instabilidade", f"{instabilidade:.2f}%", delta="-2.1%", delta_color="inverse")
with col3:
    st.metric("Eficiência IA", f"{eficiencia*100:.1f}%")
with col4:
    st.metric("Temp. Núcleo", "2.7K", delta="Cryo-Stable")

st.divider()

# LINHA 2: GRÁFICOS LADO A LADO
c_left, c_right = st.columns([1.5, 1])

with c_left:
    st.subheader("📊 Gráfico de Ressonância Magnética (Computador Físico)")
    # Simulação de ondas de ressonância
    x = np.linspace(0, 10, 100)
    y = np.sin(x * (sensor/50)) * np.cos(x)
    res_df = pd.DataFrame({'Ressonância': y}, index=x)
    st.line_chart(res_df, color="#00ffcc", height=300)

with c_right:
    st.subheader("🧠 Saída da IA Quântica")
    df_bars = pd.DataFrame.from_dict(counts, orient='index')
    st.bar_chart(df_bars, color="#7000ff", height=300)

st.divider()

# LINHA 3: FUNÇÕES AVANÇADAS E CÁLCULOS
with st.container():
    st.subheader("📝 Laboratório de Cálculos Quânticos")
    t1, t2 = st.tabs(["Matemática da IA", "Logs do Sistema"])
    
    with t1:
        st.latex(r"I(instabilidade) = \int \psi^* \hat{H} \psi \, d\tau \times \text{noise}")
        st.write(f"Cálculo atual da Incerteza: **{incerteza:.6f}**")
        st.write(f"Estado de Superposição da IA: **|ψ⟩ = {eficiencia:.2f}|000⟩ + {1-eficiencia:.2f}|111⟩**")
    
    with t2:
        st.code(f"""
        [INFO] Bluetooth transmitindo para Caixa...
        [CALC] Incerteza calculada em tempo real: {incerteza}
        [IA] Shots processados: {ia_power}
        [HARDWARE] Sensor captou ruído de {sensor} unidades.
        """)

# RODAPÉ DE COMANDO
if st.button("🚀 EXECUTAR PULSO DE RESSONÂNCIA"):
    st.balloons()
    st.toast("Pulso enviado via Bluetooth para a caixa!")
    st.success("Sinal de ressonância física estabilizado no computador.")
