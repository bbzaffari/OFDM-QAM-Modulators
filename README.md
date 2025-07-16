# **Introduction and Motivation**

This activity explores how digital transmitters work using two key setups provided in class.

The first uses 16QAM with 4 OFDM subcarriers, showing step by step how a binary sequence (64 bits) is mapped into modulation symbols, combined across subcarriers, processed via IFFT, and turned into a time-domain signal. It helps students understand basic digital transmission blocks and visualize the constellation, frequency spectrum, and output waveform.

The second follows the 802.11ax standard with 64QAM over 64 subcarriers (48 data, 4 pilots), demonstrating a more advanced, real-world system like Wi-Fi 6. It covers Gray-coded symbol mapping, full OFDM frame assembly, power normalization, and cyclic prefix addition, helping students connect theoretical concepts to the structure of modern wireless communications.

- [***Glossary of Key Terms (Background Knowledge)***](#glossary-of-key-terms-background-knowledge)  
- [***Variable Meanings***](#variable-meanings)  
- [***Table of Contents (Modulador 16QAM 4OFDM)***](#toc-modulador-16qam-4ofdm)
- [***Table of Contents (Modulador 802.11ax 64QAM)***](#toc-modulador-80211ax-64qam)
---
# **Glossary of Key Terms (Background Knowledge)**


* **QAM (Quadrature Amplitude Modulation):** Modulation technique combining amplitude and phase variations on two axes (I: in-phase, Q: quadrature) to represent data. For example, 16QAM uses 16 constellation points (4 bits/symbol), while 64QAM uses 64 points (6 bits/symbol).
* **OFDM (Orthogonal Frequency Division Multiplexing):** Transmission method that splits data across many closely spaced, orthogonal subcarriers, improving spectral efficiency and resistance to multipath fading and interference.
* **64-QAM:** A specific QAM modulation scheme using 64 points, encoding 6 bits per symbol, balancing data rate and noise sensitivity.
* **Symbol:** A complex-valued unit (real + imaginary part) used to carry multiple bits, typically represented on a constellation diagram.
* **IFFT (Inverse Fast Fourier Transform):** Algorithm converting frequency-domain data (per subcarrier) into a time-domain signal, producing the composite OFDM waveform.
* **Cyclic Prefix (CP):** A copied portion from the end of an OFDM symbol, inserted at its beginning to combat inter-symbol interference (ISI) caused by channel delay spread.
* **Pilot Subcarriers (Pilots):** Known reference signals inserted among data subcarriers, used at the receiver for synchronization, channel estimation, and correction.
* **802.11ax (Wi-Fi 6):** The sixth generation Wi-Fi standard, introducing OFDMA (Orthogonal Frequency Division Multiple Access), higher spectral efficiency, and improved multi-user performance.
* **Subcarriers:** Narrow-band carriers within the total transmission bandwidth, each independently modulated with symbols (QAM) in OFDM systems.
* **Gray Mapping:** Bit-to-symbol assignment technique where adjacent symbols differ by only one bit, reducing the likelihood of multiple bit errors from noise.
---

# **Variable Meanings:**

* **I:** In-phase component (real part of the symbol).
* **Q:** Quadrature component (imaginary part of the symbol).
* **A\_j:** Amplitude (magnitude) of symbol j.
* **theta\_j (or θ\_j):** Phase angle (in radians or degrees) of symbol j.
* **s:** Complex symbol calculated as A\_j \* e^(j \* theta\_j).
* **X\[k]:** Frequency-domain vector before IFFT; holds the mapped data and pilots per subcarrier k.
* **x\[n]:** Time-domain signal (OFDM symbol) after IFFT.
---
# TOC (Modulador 16QAM 4OFDM)
1. [In a Nutshell (Modulador 16QAM 4OFDM)](#in-a-nutshell-modulador-16qam-4ofdm)  
2. - [***Glossary of Key Terms (Background Knowledge)***](#glossary-of-key-terms-background-knowledge)  
3. - [***Variable Meanings***](#variable-meanings)  
4. [General Summary of What Was Done](#general-summary-of-what-was-done-16qam-with-4-ofdm-subcarriers)  
5. [Step-by-Step Summary (Bullet Points of Internal Activities)](#step-by-step-summary-bullet-points-of-internal-activities)  
   5.1 [Decimal-to-binary conversion (64 bits)](#decimal-to-binary-conversion-64-bits)  
   5.2 [16QAM Mapping (Modulation)](#16qam-mapping-modulation)  
   5.3 [Detailed Symbol Output](#detailed-symbol-output)  
   5.4 [16QAM Constellation Plot](#16qam-constellation-plot)  
   5.5 [IFFT Vector Construction (OFDM)](#ifft-vector-construction-ofdm)  
   5.6 [IFFT Execution (Time-Domain Signal Generation)](#ifft-execution-time-domain-signal-generation)  
   5.7 [Spectrum Plot](#spectrum-plot)  
   5.8 [Time-Domain Signal Plot](#time-domain-signal-plot)  

# In a Nutshell (Modulador 16QAM 4OFDM)

This document provides a brief introduction and summary of a classroom activity designed to demonstrate how digital communication systems work in practice. The focus is on a simple transmitter using [***16QAM***](#glossary-of-key-terms-background-knowledge)  modulation combined with [***OFDM***](#glossary-of-key-terms-background-knowledge)  over [***4 subcarriers***](#glossary-of-key-terms-background-knowledge). The goal is to help readers, especially students, understand how binary data is processed and transformed step by step into a physical signal ready for transmission. The explanation includes key background concepts, definitions of variables, and a clear breakdown of the operations performed in the provided Python code.

# **General Summary of What Was Done (16QAM with 4 OFDM Subcarriers)**

We developed and analyzed a modulation system combining [***16QAM***](#glossary-of-key-terms-background-knowledge) with [***OFDM***](#glossary-of-key-terms-background-knowledge) using [***4 subcarriers***](#glossary-of-key-terms-background-knowledge). The idea was to take a 64-bit binary sequence, modulate it into [***16QAM symbols***](#glossary-of-key-terms-background-knowledge), organize these symbols into [***OFDM***](#glossary-of-key-terms-background-knowledge)  subcarriers, generate the time-domain signal via IFFT, and visualize all intermediate steps both numerically and graphically.

The goal was to understand how binary data becomes a transmitted signal, following each classic stage of a digital transmitter.

# **Step-by-Step Summary (Bullet Points of Internal Activities)**

## 5.1. Decimal-to-binary conversion (64 bits)

   * Converts user input decimal number to a 64-bit binary string.
   * Each 4-bit block corresponds to a 16QAM symbol.
---
## 5.2. 16QAM Mapping (Modulation)

   * For each 4-bit group, retrieves:

     * I/Q values for plotting.
     * Amplitude A\_j and phase theta\_j for symbol calculation.
   * Computes s = A\_j \* e^(j^theta\_j).
---
## 5.3. Detailed Symbol Output

   * Prints per-symbol details:

     * Bits, I/Q values, A\_j, theta\_j, complex result.
---
## 5.4. 16QAM[*** ***](#glossary-of-key-terms-background-knowledge)   Constellation Plot

   * Graph of all 16 constellation points.
   * Marks active (used) symbols.
   * Labels each with its 4-bit input.
---
## 5.5. IFFT Vector Construction (OFDM)

   * Groups 16QAM symbols into sets of 4 (subcarriers).
   * Prepares X\[k] vector.
---
## 5.6. IFFT Execution (Time-Domain Signal Generation)

   * Computes x\[n] = IFFT(X\[k]).
---
## 5.7. Spectrum Plot

   * Stem plot showing |X\[k]| per subcarrier.
---
## 5.8. Time-Domain Signal Plot

   * Graphs real part over time.
   * Indicates OFDM block divisions.
---
# **TOC (Modulador 802.11ax[*** ***](#glossary-of-key-terms-background-knowledge)   64QAM)**

1. [In a nutshell (Modulador 802.11ax 64QAM)](#in-a-nutshell-modulador-80211ax-64qam)
2. - [***Glossary of Key Terms (Background Knowledge)***](#glossary-of-key-terms-background-knowledge)  
3. - [***Variable Meanings***](#variable-meanings)  
4. [General Structure and Layers](#general-structure-and-layers)  
5. [Disclaimer: Didactic Limitations](#disclaimer-didactic-limitations)  
6. [Description of the Six Activities in the 802.11ax Modulator with 64-QAM](#description-of-the-six-activities-in-the-80211ax-modulator-with-64-qam)  
   - [6.1 Create 64-QAM Map](#61-create-64-qam-map)  
   - [6.2 Validate and Modulate Decimal Input](#62-validate-and-modulate-decimal-input)  
   - [6.3 Plot Constellation](#63-plot-constellation)  
   - [6.4 Build IFFT Vector](#64-build-ifft-vector)  
   - [6.5 Plot Spectrum](#65-plot-spectrum)  
   - [6.6 Modulate OFDM with IFFT and Cyclic Prefix](#66-modulate-ofdm-with-ifft-and-cyclic-prefix)

# In a nutshell (Modulador 802.11ax 64QAM)

This document describes a Python script implementing an [***OFDM (Orthogonal Frequency Division Multiplexing)***](#glossary-of-key-terms-background-knowledge)   modulator following the  [***802.11ax (Wi-Fi 6)***](#glossary-of-key-terms-background-knowledge)  standard with 64-QAM modulation. It explains the general structure, technical layers, limitations, glossary of key terms, and details of six core activities included in the script. It generates:

* Symbol mapping
* [***IFFT***](#glossary-of-key-terms-background-knowledge) vector assembly (OFDM base)
* Frequency spectrum
* Final OFDM symbol with cyclic prefix

This process allows end-to-end simulation of the digital modulation process, connecting data layers to the physical signal.

# General Structure and Layers

This script simulates the end-to-end operation of the digital transmitter side of a Wi-Fi 802.11ax system, organized into three functional layers:

1. Data Layer → Modulated Symbols
   Converts binary bits into complex symbols using 64-QAM with Gray mapping.

2. Frequency Layer → OFDM Vector
   Inserts modulated symbols into the subcarrier vector (64 total, 48 data, 4 pilots) to prepare the OFDM spectrum.

3. Time Layer → Transmission Signal
   Converts to time domain via IFFT and adds a cyclic prefix to combat inter-symbol interference (ISI).

Summary pipeline:
raw bits → symbols → spectrum → time-domain signal ready for antenna

# Disclaimer: Didactic Limitations

This script is a didactic model and does not represent a complete real-world system.

It:

* Does not include real channels (fading, noise, attenuation)
* Does not apply channel coding (FEC, interleaving)
* Does not simulate a receiver (FFT, equalization, demodulation)

Its purpose is to help understand digital transformations at the transmitter, exploring concepts like symbol mapping, OFDM assembly, and spectral analysis.


# Description of the Six Activities in the 802.11ax Modulator with 64-QAM
   
---

## 6.1 Create 64-QAM Map

- **Function:** `criar_mapa_64qam`

   **`What it does:`**
   Generates a Python dictionary mapping each 6-bit combination to a complex symbol, placed in the I/Q plane using Gray mapping. Average power is normalized to 1 via the factor 1/sqrt(42).

   **`Why it matters:`**
   Gray mapping minimizes bit errors from noise, reducing the bit error rate (BER). Normalization ensures coherent SNR calculations, enabling fair theoretical comparisons.

   **`Technical reflection:`**
   Without normalization, simulations would distort gain, efficiency, and BER evaluations. In real systems, every dB counts.
   
---

## 6.2 Validate and Modulate Decimal Input

- **Function:** `validar_e_modular_64qam`

   **`What it does:`**
   Takes a decimal number representing 288 bits (48 symbols × 6 bits), converts it to binary, splits it into 6-bit blocks, and translates each block into a 64-QAM complex symbol.

   **`Why it matters:`**
   Simulates the physical layer without an external encoder. Enables generating realistic data frames for end-to-end testing, ensuring correct digital-to-analog translation.

   **`Didactic analogy:`**
   It is like translating words into map coordinates — without this step, you cannot turn digital information into physical signals.
     
---

## 6.3 Plot Constellation

   - **Function:** `plotar_constelacao_qam`
  
   **`What it does:`**
   Draws the constellation diagram, showing all possible points in gray and highlighting the current transmission’s points in red (or marked with x), also annotating their bits.

   **`Why it matters:`**
   Visualizing the constellation clarifies symbol spacing, patterns, and energy distribution. It can reveal DC offsets, nonlinear distortions, or mapping errors.

   **`Technical reflection:`**
   In research and teaching, a good plot is worth a thousand words. It reveals distortions, symmetries, or bugs.
   
---

## 6.4 Build IFFT Vector
   
   - **Function:** `construir_vetor_ifft`

   **`What it does:`**
   Places the 48 modulated symbols into the correct 64-subcarrier indices, adding 4 known pilots for channel estimation.

   **`Why it matters:`**
   Bridges theory (802.11ax subcarrier allocation) and practice. A correctly built IFFT vector ensures the OFDM symbol matches the expected structure, essential for channel robustness.

   **`Technical note:`**
   Indices like N-26, N-25 represent negative subcarriers centered at zero, following FFT conventions.
   
---

## 6.5 Plot Spectrum

   - **Function:** `plotar_espectro`

   **`What it does:`**
   Applies FFT shift (fftshift) and plots the absolute magnitude |X\[k]| of the subcarriers, visualizing energy distribution in frequency.

   **`Why it matters:`**
   Enables checking spectral occupancy, spotting unexpected holes, and understanding the signal envelope before time conversion.

   **`Engineering reflection:`**
   The spectrum is the system’s fingerprint. Any allocation failure shows up here.
   
---

## 6.6 Modulate OFDM with IFFT and Cyclic Prefix

   - **Function:** `modular_ofdm`

   **`What it does:`**
   Applies IFFT to shift the signal to the time domain. Then adds a cyclic prefix (default 25% of the symbol), repeating the symbol’s end at its beginning.

   **`Why it matters:`**
   The cyclic prefix protects against multipath, transforming linear into circular convolution, enabling simple equalizers and reducing ISI.

   **`Deeper reflection:`**
   The cyclic prefix is an ingenious solution: it sacrifices some spectral efficiency to massively increase robustness — a classic engineering trade-off between practicality and efficiency.

