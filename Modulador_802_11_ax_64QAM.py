import math
import cmath
import numpy as np
import matplotlib.pyplot as plt
 
# --- 1. Modulação 64-QAM (802.11ax) ---
def criar_mapa_64qam():
    """
    Cria um mapa Gray para 64-QAM com normalização de potência média = 1.
    Retorna: dict bits6 -> símbolo complexo.
    """
    niveis = np.array([-7, -5, -3, -1, 1, 3, 5, 7])
    k = 1 / np.sqrt(42)  # Normaliza potência média para 1
    gray_i = [0,1,3,2,6,7,5,4]
    gray_q = [0,1,3,2,6,7,5,4]
    mapa = {}
    for i in range(8):
        for q in range(8):
            bits = format(gray_i[i], '03b') + format(gray_q[q], '03b')
            mapa[bits] = complex(niveis[i]*k, niveis[q]*k)
    return mapa

QAM64_MAP = criar_mapa_64qam()

# --- 2. Validação e mapeamento 64-QAM ---
def validar_e_modular_64qam(numero_decimal_str):
    bits_por_ofdm = 48 * 6
    try:
        num = int(numero_decimal_str)
        assert 0 <= num < 2**bits_por_ofdm
    except Exception as e:
        print(f"Erro na entrada decimal: {e}")
        return None, None
    bitstream = format(num, f'0{bits_por_ofdm}b')
    print(f"\n[QAM64] Stream binário ({bits_por_ofdm} bits): {bitstream}")
    detalhes = []
    print("\n[QAM64] Mapeamento de símbolos:")
    for idx in range(48):
        bits6 = bitstream[6*idx:6*idx+6]
        sym = QAM64_MAP[bits6]
        Aj = abs(sym); theta = cmath.phase(sym)
        print(f"  Símbolo {idx+1:02d}: bits={bits6} -> I={sym.real:+.3f}, Q={sym.imag:+.3f}, |A|={Aj:.3f}, θ={math.degrees(theta):.1f}°")
        detalhes.append({'bits': bits6, 'complexo': sym, 'Aj': Aj, 'theta': theta})
    return bitstream, detalhes

# --- 3. Constelação 64-QAM ---
def plotar_constelacao_qam(detalhes, mapa, title="64-QAM"):
    plt.figure(figsize=(7,7))
    # todos os pontos
    pts = np.array(list(mapa.values()))
    plt.scatter(pts.real, pts.imag, c='lightgray', s=80, label='Constelação Completa')
    # símbolos usados
    usados = np.array([d['complexo'] for d in detalhes])
    plt.scatter(usados.real, usados.imag, c='red', marker='x', s=100, label='Símbolos Usados')
    # anota bits
    for d in detalhes:
        plt.annotate(d['bits'], (d['complexo'].real, d['complexo'].imag), xytext=(5,5), textcoords='offset points', fontsize=6)
    plt.title(f'Diagrama de Constelação {title}')
    plt.xlabel('I'); plt.ylabel('Q')
    plt.grid(True); plt.axhline(0, color='k', lw=0.5); plt.axvline(0, color='k', lw=0.5)
    plt.axis('equal'); plt.legend(); plt.tight_layout()

# --- 4. Montagem do vetor IFFT para OFDM (802.11a/ax) ---
N = 64
ND = 48
PILOTS = 4
DATA_INDICES = [1,2,3,4,5,6,8,9,10,11,12,13,14,15,16,17,18,19,20,22,23,24,25,26,
                N-26,N-25,N-24,N-23,N-22,N-20,N-19,N-18,N-17,N-16,N-15,N-14,N-13,N-12,N-11,N-10,N-9,N-8,
                N-6,N-5,N-4,N-3,N-2,N-1]
PILOT_INDICES = [7,21,N-21,N-7]

def construir_vetor_ifft(dados, pilot=1+0j):
    X = np.zeros(N, dtype=complex)
    X[0] = 0
    for i, sym in enumerate(dados):
        X[DATA_INDICES[i]] = sym
    for p in PILOT_INDICES:
        X[p] = pilot
    print(f"\n[OFDM] Vetor X[k] de entrada IFFT (N={N}):")
    for k,val in enumerate(X):
        print(f"  k={k:02d}: {val.real:+.3f}{val.imag:+.3f}j")
    return X

def plotar_espectro(X):
    M = np.abs(np.fft.fftshift(X))
    idx = np.arange(-N//2, N//2)
    plt.figure(figsize=(10,4))
    plt.stem(idx, M, basefmt=" ")
    plt.title('Espectro de Entrada da IFFT (OFDM)')
    plt.xlabel('Subportadora (k)'); plt.ylabel('|X[k]|')
    plt.ylim(0, M.max()*1.1)
    plt.grid(True); plt.tight_layout()

# --- 5. Modulação OFDM (IFFT + CP) ---
def modular_ofdm(X, cp_frac=0.25):
    x = np.fft.ifft(X)
    cp_len = int(N*cp_frac)
    cp = x[-cp_len:]
    ofdm = np.concatenate([cp, x])
    print(f"\n[OFDM] Símbolo OFDM no tempo (com CP, total {len(ofdm)} amostras):")
    for i,s in enumerate(ofdm):
        print(f"  n={i:03d}: {s.real:+.5f}{s.imag:+.5f}j")
    return ofdm

# --- 6. Exemplo de execução ---
if __name__ == '__main__':
    num = input('Decimal (48*6 bits) > ')
    binst, qam = validar_e_modular_64qam(num)
    if qam is None: exit()
    plotar_constelacao_qam(qam, QAM64_MAP)
    X = construir_vetor_ifft([d['complexo'] for d in qam])
    plotar_espectro(X)
    ofdm_t = modular_ofdm(X)
    plt.show()
