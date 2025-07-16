# **Introduction and Motivation**

This activity explores how digital transmitters work using two key setups provided in class.

The first uses 16QAM with 4 OFDM subcarriers, showing step by step how a binary sequence (64 bits) is mapped into modulation symbols, combined across subcarriers, processed via IFFT, and turned into a time-domain signal. It helps students understand basic digital transmission blocks and visualize the constellation, frequency spectrum, and output waveform.

The second follows the 802.11ax standard with 64QAM over 64 subcarriers (48 data, 4 pilots), demonstrating a more advanced, real-world system like Wi-Fi 6. It covers Gray-coded symbol mapping, full OFDM frame assembly, power normalization, and cyclic prefix addition, helping students connect theoretical concepts to the structure of modern wireless communications.

1 - [***Glossary of Key Terms***](#glossary-of-key-terms)  \
2 - [***Variable Meanings***](#variable-meanings)  \
3 - [***Table of Contents (Modulador 16QAM 4OFDM)***](#toc-modulador-16qam-4ofdm) \
4 - [***Table of Contents (Modulador 802.11ax 64QAM)***](#toc-modulador-80211ax-64qam) \
5 - [***Conclusion***](#conclusion) \
6 - [***Reflection***](#Reflection) 
---
# **Glossary of Key Terms**

### **1. QAM (Quadrature Amplitude Modulation)**

A **modulation technique** that combines amplitude and phase variations along two orthogonal axes — **I (in-phase)** and **Q (quadrature)** — to represent digital data in analog signals.
For example:

* **16QAM** → 16 distinct constellation points → encodes **4 bits/symbol**.
* **64QAM** → 64 points → encodes **6 bits/symbol**.

This approach increases spectral efficiency but also raises sensitivity to noise.
QAM is widely used in cable modems, 4G/5G networks, and digital TV.

> **Reflection:** Think of QAM like placing markers on a 2D map — the more markers, the more info per spot, but also the more precision needed to locate them reliably.
[**>**](#glossary-of-key-terms)  
### **2. OFDM (Orthogonal Frequency Division Multiplexing)**

A **transmission scheme** that splits data across many narrow, closely spaced, **orthogonal subcarriers**. Each subcarrier carries a low-rate stream, but combined, they form a high-rate, robust signal.

Benefits:

* High **spectral efficiency**.
* Resistance to **multipath fading** and interference.
* Simplifies equalization in dispersive channels.

Used in Wi-Fi (802.11a/g/n/ac/ax), LTE, DVB-T, and ADSL.

> **Historical note:** OFDM emerged from research in the 1960s but became practical only with modern DSPs capable of fast IFFT computations.
[**>**](#glossary-of-key-terms)  
### **3. 64-QAM**

A specific **QAM variant** with 64 constellation points arranged in an 8x8 grid. Each symbol carries **6 bits**.

It offers:

* High data rates.
* Greater susceptibility to noise and distortion compared to lower-order QAM like 16QAM.

> **Example:** LTE and Wi-Fi 802.11ax use adaptive modulation: under good signal conditions, they switch to 64-QAM or 256-QAM; under poor conditions, they fall back to 16QAM or QPSK.
[**>**](#glossary-of-key-terms)  
### **4. Symbol**

A **complex-valued unit** (real + imaginary part) representing one or more bits after modulation. In QAM, each symbol is visualized as a point in a **constellation diagram**.

> **Analogy:** A symbol is like a word in a sentence — it's a unit of meaning that carries a bundled package of bits.

### **5. IFFT (Inverse Fast Fourier Transform)**

An **algorithm** that converts frequency-domain data (amplitudes/phases per subcarrier) into a composite time-domain signal, synthesizing the OFDM waveform.

* Efficient implementation thanks to **FFT algorithms**.
* Key for assembling all subcarrier contributions into a single transmit signal.

> **Example:** Without IFFT, generating OFDM would require summing thousands of sines manually — computationally unfeasible.
[**>**](#glossary-of-key-terms)  
### **6. Cyclic Prefix (CP)**

A **guard interval** created by copying the end portion of an OFDM symbol and appending it to the beginning.

Purpose:

* Absorb **delayed echoes** (ISI — Inter-Symbol Interference).
* Preserve orthogonality between subcarriers.

> **Reflection:** Think of CP as adding a shock absorber to a car — it doesn't carry new data but makes the journey smoother and protects against “bumps” in the channel.
[**>**](#glossary-of-key-terms)  
### **7. Pilot Subcarriers (Pilots)**

Known **reference signals** inserted at fixed subcarrier positions among the data carriers.

Functions at the receiver:

* Synchronization (time/frequency).
* Channel estimation (tracking amplitude/phase distortions).
* Error correction adjustments.

> **Analogy:** Pilots are like road signs — they don’t carry your cargo, but they help you navigate the highway safely.
[**>**](#glossary-of-key-terms)  
### **8. 802.11ax (Wi-Fi 6)**

The **sixth generation Wi-Fi standard**, focusing on:

* **OFDMA (Orthogonal Frequency Division Multiple Access)** for multi-user efficiency.
* Higher **throughput and spectral efficiency**.
* Target Wake Time (TWT) to extend battery life of devices.
* Better performance in crowded environments.

> **Context:** Wi-Fi 6 is crucial for the IoT era, where dozens of devices (phones, TVs, sensors) compete for airtime.
[**>**](#glossary-of-key-terms)  
### **9. Subcarriers**

Narrow-bandwidth carriers that divide the total transmission bandwidth in OFDM systems.

* Each subcarrier is modulated independently (e.g., with QAM symbols).
* Their orthogonality ensures no interference despite tight packing.

> **Analogy:** Imagine musicians in an orchestra playing different notes — orthogonality ensures they harmonize instead of clashing.
[**>**](#glossary-of-key-terms)  
### **10. Gray Mapping**

A **bit-to-symbol assignment strategy** where adjacent constellation points differ by only **one bit**.

Benefits:

* Minimizes **bit error rate** under noisy conditions.
* A single symbol error likely flips just **one bit**.

> **Reflection:** Gray mapping is like designing a keyboard where neighboring keys cause minimal typos — small slips lead to minor, not catastrophic, errors.
[**>**](#glossary-of-key-terms)


---
[***^***](#introduction-and-motivation)

---
---

# **Variable Meanings:**

* **I:** In-phase component (real part of the symbol).
* **Q:** Quadrature component (imaginary part of the symbol).
* **A\_j:** Amplitude (magnitude) of symbol j.
* **theta\_j (or θ\_j):** Phase angle (in radians or degrees) of symbol j.
* **s:** Complex symbol calculated as A\_j \* e^(j \* theta\_j).
* **X\[k]:** Frequency-domain vector before IFFT; holds the mapped data and pilots per subcarrier k.
* **x\[n]:** Time-domain signal (OFDM symbol) after IFFT.
  
[***^***](#introduction-and-motivation)

---
---

# TOC (Modulador 16QAM 4OFDM)
1. [In a Nutshell (Modulador 16QAM 4OFDM)](#in-a-nutshell-modulador-16qam-4ofdm)  
2. - [***Glossary of Key Terms (Background Knowledge)***](#glossary-of-key-terms)   
3. - [***Variable Meanings***](#variable-meanings)  
4. [General Summary of What Was Done](#general-summary-of-what-was-done-16qam-with-4-ofdm-subcarriers)  
5. [Step-by-Step Summary (Bullet Points of Internal Activities)](#step-by-step-summary-bullet-points-of-internal-activities)  
   - [5.1 Decimal-to-binary conversion (64 bits)](#decimal-to-binary-conversion-64-bits)  
   - [5.2 16QAM Mapping (Modulation)](#16qam-mapping-modulation)  
   - [5.3 Detailed Symbol Output](#detailed-symbol-output)  
   - [5.4 16QAM Constellation Plot](#16qam-constellation-plot)  
   - [5.5 IFFT Vector Construction (OFDM)](#ifft-vector-construction-ofdm)  
   - [5.6 IFFT Execution (Time-Domain Signal Generation)](#ifft-execution-time-domain-signal-generation)  
   - [5.7 Spectrum Plot](#spectrum-plot)  
   - [5.8 Time-Domain Signal Plot](#time-domain-signal-plot)  
  
[***^***](#introduction-and-motivation)

# In a Nutshell (Modulador 16QAM 4OFDM)

This document provides a brief introduction and summary of a classroom activity designed to demonstrate how digital communication systems work in practice. The focus is on a simple transmitter using [***16QAM***](#glossary-of-key-terms)   modulation combined with [***OFDM***](#glossary-of-key-terms)   over [***4 subcarriers***](#glossary-of-key-terms-background-knowledge). The goal is to help readers, especially students, understand how binary data is processed and transformed step by step into a physical signal ready for transmission. The explanation includes key background concepts, definitions of variables, and a clear breakdown of the operations performed in the provided Python code.

[***^***](#introduction-and-motivation)

# **General Summary of What Was Done (16QAM with 4 OFDM Subcarriers)**

We developed and analyzed a modulation system combining [***16QAM***](#glossary-of-key-terms)  with [***OFDM***](#glossary-of-key-terms)  using [***4 subcarriers***](#glossary-of-key-terms-background-knowledge). The idea was to take a 64-bit binary sequence, modulate it into [***16QAM symbols***](#glossary-of-key-terms-background-knowledge), organize these symbols into [***OFDM***](#glossary-of-key-terms)   subcarriers, generate the time-domain signal via IFFT, and visualize all intermediate steps both numerically and graphically.

The goal was to understand how binary data becomes a transmitted signal, following each classic stage of a digital transmitter.

[**>***](#toc-modulador-16qam-4ofdm) 

# **Step-by-Step Summary (Bullet Points of Internal Activities)**

## 5.1. Decimal-to-binary conversion (64 bits)

   * Converts user input decimal number to a 64-bit binary string.
   * Each 4-bit block corresponds to a 16QAM symbol.
---

[**>***](#toc-modulador-16qam-4ofdm) 

## 5.2. 16QAM Mapping (Modulation)

   * For each 4-bit group, retrieves:

     * I/Q values for plotting.
     * Amplitude A\_j and phase theta\_j for symbol calculation.
   * Computes s = A\_j \* e^(j^theta\_j).
[**>***](#toc-modulador-16qam-4ofdm) 
---
## 5.3. Detailed Symbol Output

   * Prints per-symbol details:

     * Bits, I/Q values, A\_j, theta\_j, complex result.
[**>***](#toc-modulador-16qam-4ofdm) 
---
## 5.4. [***16QAM***](#glossary-of-key-terms) Constellation Plot

   * Graph of all 16 constellation points.
   * Marks active (used) symbols.
   * Labels each with its 4-bit input.
[**>***](#toc-modulador-16qam-4ofdm) 
---
## 5.5. IFFT Vector Construction (OFDM)

   * Groups 16QAM symbols into sets of 4 (subcarriers).
   * Prepares X\[k] vector.
[**>***](#toc-modulador-16qam-4ofdm) 
---
## 5.6. IFFT Execution (Time-Domain Signal Generation)

   * Computes x\[n] = IFFT(X\[k]).
[**>***](#toc-modulador-16qam-4ofdm) 
---
## 5.7. Spectrum Plot

   * Stem plot showing |X\[k]| per subcarrier.
[**>***](#toc-modulador-16qam-4ofdm) 
---
## 5.8. Time-Domain Signal Plot

   * Graphs real part over time.
   * Indicates OFDM block divisions.
[**>***](#toc-modulador-16qam-4ofdm) 
---

[***^***](#introduction-and-motivation)

---
# **TOC (Modulador 802.11ax 64QAM)**

1. [In a nutshell (Modulador 802.11ax 64QAM)](#in-a-nutshell-modulador-80211ax-64qam)
2. - [***Glossary of Key Terms (Background Knowledge)***](#glossary-of-key-terms)   
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
  
[***^***](#introduction-and-motivation)

# In a nutshell (Modulador 802.11ax 64QAM)

This document describes a Python script implementing an [***OFDM (Orthogonal Frequency Division Multiplexing)***](#glossary-of-key-terms)    modulator following the  [***802.11ax (Wi-Fi 6)***](#glossary-of-key-terms)   standard with 64-QAM modulation. It explains the general structure, technical layers, limitations, glossary of key terms, and details of six core activities included in the script. It generates:

* Symbol mapping
* [***IFFT***](#glossary-of-key-terms)  vector assembly (OFDM base)
* Frequency spectrum
* Final OFDM symbol with cyclic prefix

This process allows end-to-end simulation of the digital modulation process, connecting data layers to the physical signal.

[**>**](#introduction-and-motivation)

# General Structure and Layers

This script simulates the end-to-end operation of the digital transmitter side of a Wi-Fi 802.11ax system, organized into three functional layers:

1. Data Layer → Modulated Symbols
   Converts binary bits into complex symbols using 64-QAM with Gray mapping.

2. Frequency Layer → OFDM Vector
   Inserts modulated symbols into the subcarrier vector (64 total, 48 data, 4 pilots) to prepare the OFDM spectrum.

3. Time Layer → Transmission Signal
   Converts to time domain via IFFT and adds a cyclic prefix to combat inter-symbol interference (ISI).

[***^***](#introduction-and-motivation)

Summary pipeline:
raw bits → symbols → spectrum → time-domain signal ready for antenna

# Disclaimer: Didactic Limitations

This script is a didactic model and does not represent a complete real-world system.

It:

* Does not include real channels (fading, noise, attenuation)
* Does not apply channel coding (FEC, interleaving)
* Does not simulate a receiver (FFT, equalization, demodulation)

Its purpose is to help understand digital transformations at the transmitter, exploring concepts like symbol mapping, OFDM assembly, and spectral analysis.


[***^***](#introduction-and-motivation)

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
   
[***^***](#introduction-and-motivation)

---

## 6.2 Validate and Modulate Decimal Input

- **Function:** `validar_e_modular_64qam`

   **`What it does:`**
   Takes a decimal number representing 288 bits (48 symbols × 6 bits), converts it to binary, splits it into 6-bit blocks, and translates each block into a 64-QAM complex symbol.

   **`Why it matters:`**
   Simulates the physical layer without an external encoder. Enables generating realistic data frames for end-to-end testing, ensuring correct digital-to-analog translation.

   **`Didactic analogy:`**
   It is like translating words into map coordinates — without this step, you cannot turn digital information into physical signals.

[***^***](#introduction-and-motivation)

---

## 6.3 Plot Constellation

   - **Function:** `plotar_constelacao_qam`
  
   **`What it does:`**
   Draws the constellation diagram, showing all possible points in gray and highlighting the current transmission’s points in red (or marked with x), also annotating their bits.

   **`Why it matters:`**
   Visualizing the constellation clarifies symbol spacing, patterns, and energy distribution. It can reveal DC offsets, nonlinear distortions, or mapping errors.

   **`Technical reflection:`**
   In research and teaching, a good plot is worth a thousand words. It reveals distortions, symmetries, or bugs.
   
[**>***](#toc-modulador-80211ax-64qam) 

---
## 6.4 Build IFFT Vector
   
   - **Function:** `construir_vetor_ifft`

   **`What it does:`**
   Places the 48 modulated symbols into the correct 64-subcarrier indices, adding 4 known pilots for channel estimation.

   **`Why it matters:`**
   Bridges theory (802.11ax subcarrier allocation) and practice. A correctly built IFFT vector ensures the OFDM symbol matches the expected structure, essential for channel robustness.

   **`Technical note:`**
   Indices like N-26, N-25 represent negative subcarriers centered at zero, following FFT conventions.
   
[**>***](#toc-modulador-80211ax-64qam) 

---
## 6.5 Plot Spectrum

   - **Function:** `plotar_espectro`

   **`What it does:`**
   Applies FFT shift (fftshift) and plots the absolute magnitude |X\[k]| of the subcarriers, visualizing energy distribution in frequency.

   **`Why it matters:`**
   Enables checking spectral occupancy, spotting unexpected holes, and understanding the signal envelope before time conversion.

   **`Engineering reflection:`**
   The spectrum is the system’s fingerprint. Any allocation failure shows up here. 
   
[**>***](#toc-modulador-80211ax-64qam) 

---
## 6.6 Modulate OFDM with IFFT and Cyclic Prefix

   - **Function:** `modular_ofdm`

   **`What it does:`**
   Applies IFFT to shift the signal to the time domain. Then adds a cyclic prefix (default 25% of the symbol), repeating the symbol’s end at its beginning.

   **`Why it matters:`**
   The cyclic prefix protects against multipath, transforming linear into circular convolution, enabling simple equalizers and reducing ISI.

   **`Deeper reflection:`**
   The cyclic prefix is an ingenious solution: it sacrifices some spectral efficiency to massively increase robustness — a classic engineering trade-off between practicality and efficiency.
   
[**>***](#toc-modulador-80211ax-64qam) 

---
[***^***](#introduction-and-motivation)

---
---
---

# Conclusion

This project provided a practical implementation of fundamental concepts in digital modulation and Orthogonal Frequency Division Multiplexing (OFDM), using didactic Python scripts for two cases: **16QAM with 4 subcarriers** and **64QAM following the 802.11ax (Wi-Fi 6) standard**.

               Through the development and analysis of these modulators, we were able to explore:

1. How binary streams are mapped into complex-valued symbols using Quadrature Amplitude Modulation (QAM), applying **Gray Mapping** to minimize bit errors;  
2. How OFDM organizes these symbols over orthogonal subcarriers, using the **Inverse Fast Fourier Transform (IFFT)** to convert from frequency to time domain;  
3. The role of the **Cyclic Prefix (CP)** in mitigating inter-symbol interference (ISI), improving robustness over multipath channels;  
4. How **pilot subcarriers** help with receiver-side synchronization, channel estimation, and equalization, ensuring reliable communication.

The Python codes not only allowed generation and visualization of constellation diagrams but also provided detailed inspection of the input/output vectors, offering a step-by-step demonstration of how raw data is transformed during the modulation process.

This experience reinforces the essential role of computational simulation in learning modern communication systems, bridging theoretical understanding with hands-on practice. It also highlights the technological progress up to the 802.11ax standard, which incorporates **64QAM**, **Orthogonal Frequency Division Multiple Access (OFDMA)**, and advanced spectral efficiency techniques to support multiple users and high data rates.

[***^***](#introduction-and-motivation)

---

# Reflection

Mastering these fundamental building blocks opens the door to more advanced challenges, such as:

- Implementing **Additive White Gaussian Noise (AWGN)** in simulations to study system resilience under noisy conditions;
- Adding **selective fading channel models** to simulate real-world multipath propagation effects;
- Analyzing **Bit Error Rate (BER)** performance curves for different modulation schemes (e.g., comparing 16QAM vs. 64QAM) under varying signal-to-noise ratios (SNR);
- Exploring **Software-Defined Radio (SDR)** platforms to implement these algorithms in real-time on hardware, enabling over-the-air transmission and reception.

[***^***](#introduction-and-motivation)




