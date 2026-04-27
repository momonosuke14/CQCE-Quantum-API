from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import math
import streamlit as st

st.title("🛰️ Sistema Quântico CQCE")
st.write("O motor quântico está ativo!")
import numpy as np
from scipy.special import expit # Função sigmoide para normalização

# IMPORTAÇÕES DE HARDWARE QUÂNTICO
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

app = FastAPI(title="Quantum Noise-Driven Engine")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class QuantumEngine:
    def __init__(self):
        self.simulator = AerSimulator()

    def _calculate_tetration(self, n, height):
        """
        Implementação simplificada de tetração (^height n)
        Cuidado: Tetração cresce absurdamente rápido.
        """
        if height == 0: return 1
        if height == 1: return n
        if height > 4: height = 4 # Cap para evitar estouro de memória (Overflow)
        
        res = n
        for _ in range(height - 1):
            res = math.pow(n, res) if res < 100 else 10**10 # Limite de segurança
        return res

    def calculate_entropy(self, noise_level):
        """ Calcula a entropia do sinal para determinar a 'pureza' do ruído """
        # Normaliza o ruído para um valor entre 0 e 1
        p = expit((noise_level - 500) / 100) 
        return - (p * math.log2(p + 1e-9) + (1-p) * math.log2(1-p + 1e-9))

    def processamento_inverso(self, noise_level):
        """
        Lógica de Inversão Avançada:
        O ruído não é um erro, é a instrução de rotação.
        """
        qc = QuantumCircuit(1, 1)
        
        # 1. Normalização do Ruído para Ângulos (0 a 2PI)
        # Usamos a função seno para criar 'pontos de ressonância' onde o ruído é mais eficiente
        theta = (noise_level / 1000) * 2 * math.pi
        phi = math.sin(theta) * math.pi 
        
        # 2. Aplicação de Portas Baseadas no Ruído
        # RX: Rotação no eixo X (Amplitude)
        qc.rx(theta, 0)
        # RZ: Rotação no eixo Z (Fase/Coerência) - Aqui o ruído define a fase
        qc.rz(phi, 0)
        
        # 3. Superposição Induzida por Ruído
        qc.h(0) 
        
        qc.measure(0, 0)
        
        # Execução com shots reduzidos para performance, mas mantendo a estatística
        job = self.simulator.run(transpile(qc, self.simulator), shots=256)
        counts = job.result().get_counts()
        
        # Probabilidade de colapso no estado |1>
        prob_1 = counts.get('1', 0) / 256
        return prob_1

engine = QuantumEngine()

class ESP32Data(BaseModel):
    raw_noise: float 
    lat: float
    lon: float

@app.post("/quantum-process")
async def process_data(data: ESP32Data):
    # 1. Processamento Quântico via Ruído
    eficiencia = engine.processamento_inverso(data.raw_noise)
    
    # 2. Análise de Entropia do Sinal
    entropia = engine.calculate_entropy(data.raw_noise)
    
    # 3. Lógica de Tetração Reversa (Complexidade de Estado)
    # O nível de tetração agora depende da entropia do ruído
    nivel_tetracao = int(entropia * 3) # Escala de 0 a 3
    try:
        qubits_virtuais = engine._calculate_tetration(2, nivel_tetracao)
    except OverflowError:
        qubits_virtuais = "INFINITO/SANGUINÁRIO"

    # 4. Determinação de Status de Coerência
    # Se a eficiência estiver perto de 0.5, temos superposição máxima (ruído ideal)
    distancia_do_caos = abs(0.5 - eficiencia)
    
    if distancia_do_caos < 0.1:
        status = "COERÊNCIA CRÍTICA (Sincronizado)"
        estabilidade = "ESTÁVEL"
    elif eficiencia > 0.7:
        status = "COLAPSO INDUZIDO"
        estabilidade = "INSTÁVEL"
    else:
        status = "ESTADO DE REPOUSO"
        estabilidade = "ESTÁVEL"

    return {
        "metrics": {
            "status": status,
            "coerencia_ruido": f"{eficiencia * 100:.2f}%",
            "entropia_sinal": f"{entropia:.4f}",
            "estabilidade": estabilidade
        },
        "quantum_state": {
            "qubits_virtuais": qubits_virtuais,
            "nivel_tetracao": nivel_tetracao,
            "probabilidade_colapso": eficiencia
        },
        "telemetry": {
            "raw_noise": data.raw_noise,
            "local": f"{data.lat}, {data.lon}"
        }
    }
