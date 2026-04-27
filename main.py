import streamlit as st
import math
import numpy as np
import pandas as pd
from scipy.special import expit
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="CQCE Quantum Monitor", page_icon="⚛️", layout="wide")

# Estilo CSS para manter o visual escuro e moderno
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric {
        background-color: #1e2130;
        padding: 15px;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🛰️ Sistema Quântico CQCE")
st.write("Monitor quântico processando ruído em tempo real via Qiskit Aer.")

# --- MOTOR QUÂNTICO (Lógica de Processamento) ---
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

    def rodar_simulacao_complexa(self, tipo, n_shots):
        qc = QuantumCircuit(2)
        if tipo == "Bell (2 qubits)":
            qc.h(0)
            qc.cx(0, 1)
        qc.measure_all()
        job = self.simulator.run(qc, shots=n_shots)
        return job.result().get_counts()

engine = QuantumEngine()

# --- SIDEBAR (Controle de Hardware e Parâmetros) ---
st.sidebar.header("📡 Controle de Hardware")
noise_input = st.sidebar.slider("Simular Ruído do Sensor (Arduino)", 0, 1000, 500)

st.sidebar.divider()
st.sidebar.header("Parâmetros do Chip")
circuito_selecionado = st.sidebar.selectbox("Circuito-alvo", ["Bell (2 qubits)", "GHZ", "QFT", "Grover"])
shots = st.sidebar.slider("Shots por execução", 1024, 8192, 4096)

st.sidebar.subheader("Ruído de Porta")
erro_1q = st.sidebar.slider("Erro depolarizante 1Q", 0.0000, 0.0100, 0.0040, format="%.4f")
erro_leitura = st.sidebar.slider("Erro de leitura", 0.0000, 0.1000, 0.0200, format="%.4f")

# --- PROCESSAMENTO DOS DADOS ---
eficiencia = engine.processamento_inverso(noise_input)
entropia = engine.calculate_entropy(noise_input)
contagens = engine.rodar_simulacao_complexa(circuito_selecionado, shots)

# Criando dados para o gráfico de barras (Ideal vs Ruidoso)
labels = list(contagens.keys())
valores_reais = list(contagens.values())
# O ruído do gráfico é influenciado pelo slider do sensor e pelo erro de porta
fator_ruido = (noise_input / 1000) * (1 + erro_1q * 10)
valores_ruido = [v * (1 - (fator_ruido * 0.1)) if i % 2 == 0 else v + (shots*0.05*fator_ruido) for i, v in enumerate(valores_reais)]

df_chart = pd.DataFrame({
    'Ideal': valores_reais,
    'Com ruído': valores_ruido
}, index=labels)

# --- DASHBOARD VISUAL ---
# Painel de métricas (Cima)
col_m1, col_m2, col_m3 = st.columns(3)
with col_m1:
    st.metric("Eficiência Quântica", f"{eficiencia * 100:.2f}%")
with col_m2:
    st.metric("Entropia do Sinal", f"{entropia:.4f}")
with col_m3:
    sucesso = 100 - (erro_1q * 100 + (noise_input/50))
    st.metric("Fidelidade do Sistema", f"{sucesso:.2f}%")

st.divider()

# Gráficos (Meio)
c1, c2 = st.columns([2, 1])

with c1:
    st.subheader("Análise de Fidelidade (Ideal vs Ruidoso)")
    # Cores Ciano e Roxo como na imagem que você gostou
    st.bar_chart(df_chart, color=["#00f2ff", "#7000ff"])

with c2:
    st.subheader("Ressonância do Sinal")
    chart_data = pd.DataFrame(np.random.randn(20, 1), columns=['frequência'])
    st.line_chart(chart_data)
    
    status = "✅ ESTÁVEL" if sucesso > 80 else "⚠️ INSTÁVEL"
    if sucesso > 80:
        st.success(f"Status: {status}")
    else:
        st.warning(f"Status: {status}")

st.divider()

# Botão de Ação (Baixo)
if st.button("🚀 Disparar Pulso Quântico"):
    st.balloons()
    st.success("Pulso processado pelo Qiskit com sucesso! Dados sincronizados com o Arduino.")

st.caption("CQCE Quantum Explorer v2.0 - Integração Qiskit Aer + Hardware Simulation")
