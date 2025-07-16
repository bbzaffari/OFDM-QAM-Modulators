import math
import cmath
import numpy as np
import matplotlib.pyplot as plt

# --- CONFIGURAÇÕES OFDM 802.11ax ---
N = 64               # Número de subportadoras na IFFT
ND = 48              # Número de subportadoras de dados
PILOTS = 4           # Número de portadoras piloto
CP_FRAC = 0.25       # Fração de CP (25%)

# Índices de dados e pilotos no vetor de entrada da IFFT
DATA_INDICES = [ 1,2,3,4,5,6,8,9,10,11,12,13,14,15,16,17,18,19,20,22,23,24,25,26,
                 N-26,N-25,N-24,N-23,N-22,N-20,N-19,N-18,N-17,N-16,N-15,N-14,N-13,N-12,N-11,N-10,N-9,N-8,
                 N-6,N-5,N-4,N-3,N-2,N-1]
PILOT_INDICES = [7,21, N-21, N-7]

# --- 1. Mapa Gray para 64-QAM normalizado (potência média = 1) ---
def criar_mapa_64qam():
    niveis = np.array([-7, -5, -3, -1, 1, 3, 5, 7], dtype=float)
    k = 1/np.sqrt(42)  # fator de normalização para potência média = 1
    gray = [0,1,3,2,6,7,5,4]
    mapa = {}
    for i in range(8):
        for q in range(8):
            bits = format(gray[i],'03b') + format(gray[q],'03b')
            mapa[bits] = complex(niveis[i]*k, niveis[q]*k)
    return mapa

QAM64_MAP = criar_mapa_64qam()

# --- 2. Validação e modulação 64-QAM ---
def validar_e_modular_64qam(bitstring=None):
    # Se for decimal, converte primeiro
    if bitstring is None:
        num = input(f"Decimal (48*6 bits) > ")
        bs = format(int(num), f"0{ND*6}b")
    else:
        bs = bitstring
    if len(bs) != ND*6:
        raise ValueError(f"Stream binário deve ter {ND*6} bits, mas recebeu {len(bs)}.")
    detalhes = []
    print("\n[QAM64] Stream binário ({ND*6} bits):", bs)
    for idx in range(ND):
        b6 = bs[6*idx:6*idx+6]
        sym = QAM64_MAP[b6]
        A = abs(sym)
        theta = cmath.phase(sym)
        detalhes.append({'bits': b6, 'complexo': sym, 'A': A, 'theta': theta})
        print(f"  Símbolo {idx+1:02d}: bits={b6} -> I={sym.real:+.3f}, Q={sym.imag:+.3f}, |A|={A:.3f}, θ={math.degrees(theta):.1f}°")
    return detalhes

# --- 3. Plotagem da constelação 64-QAM corrigida ---
def plotar_constelacao_qam(detalhes):
    plt.figure(figsize=(6,6))
    pts = np.array(list(QAM64_MAP.values()))
    plt.scatter(pts.real, pts.imag, c='lightgray', s=60, label='Constelação Completa')
    usados = np.array([d['complexo'] for d in detalhes])
    plt.scatter(usados.real, usados.imag, c='red', marker='x', s=100, label='Símbolos Usados')
    for d in detalhes:
        plt.annotate(d['bits'], (d['complexo'].real, d['complexo'].imag), textcoords='offset points', xytext=(3,3), fontsize=6)
    plt.title('Diagrama de Constelação 64-QAM (802.11ax)')
    plt.xlabel('I'); plt.ylabel('Q')
    plt.axhline(0, color='k', lw=0.5); plt.axvline(0, color='k', lw=0.5)
    plt.grid(True);
    plt.axis('equal'); plt.legend(); plt.tight_layout()

# --- 4. Construção do vetor X[k] para IFFT com 48 subportadoras ---
def construir_vetor_ifft(dados_qam):
    X = np.zeros(N, dtype=complex)
    # atribui dados nas subportadoras
    for i,s in enumerate(dados_qam):
        X[DATA_INDICES[i]] = s
    # pilotos
    for p in PILOT_INDICES:
        X[p] = 1+0j
    print("\n[OFDM] Vetor X[k] de entrada IFFT (N=64):")
    for k,val in enumerate(X):
        print(f"  k={k:02d}: {val.real:+.3f}{val.imag:+.3f}j")
    return X

# --- 5. Modulação OFDM com correta escala de amplitude ---
def modular_ofdm_time(X):
    # se quisermos manter potência igual: escala = sqrt(N/ND)
    escala = math.sqrt(N/ND)
    x = np.fft.ifft(X) * escala
    cp_len = int(N * CP_FRAC)
    ofdm = np.concatenate([x[-cp_len:], x])
    print(f"\n[OFDM] Símbolo OFDM no tempo (com CP, {len(ofdm)} amostras):")
    for n,s in enumerate(ofdm):
        print(f"  n={n:03d}: {s.real:+.5f}{s.imag:+.5f}j")
    return ofdm

# --- 6. Plotagem temporal e espectral OFDM corrigida ---
def plotar_ofdm(ofdm_time, X):
    # tempo
    plt.figure(figsize=(10,4))
    plt.plot(ofdm_time.real, label='Real'); plt.plot(ofdm_time.imag, '--', label='Imag')
    plt.title('Símbolo OFDM no Tempo (Banda Base)')
    plt.xlabel('Amostra'); plt.ylabel('Amplitude'); plt.grid(True)
    plt.legend(); plt.tight_layout()
    # espectro
    M = np.abs(np.fft.fftshift(X))
    idx = np.arange(-N//2, N//2)
    plt.figure(figsize=(10,3))
    plt.stem(idx, M, basefmt=' ')
    plt.title('Espectro de Entrada da IFFT (OFDM)')
    plt.xlabel('Índice k'); plt.ylabel('|X[k]|'); plt.ylim(0, M.max()*1.1)
    plt.grid(True); plt.tight_layout()

# --- Execução Principal ---
if __name__ == '__main__':
    detalhes_qam = validar_e_modular_64qam()
    plotar_constelacao_qam(detalhes_qam)
    dados = [d['complexo'] for d in detalhes_qam]
    X = construir_vetor_ifft(dados)
    ofdm_time = modular_ofdm_time(X)
    plotar_ofdm(ofdm_time, X)
    plt.show()
