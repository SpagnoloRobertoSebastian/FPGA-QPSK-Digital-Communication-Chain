import numpy as np
import matplotlib.pyplot as plt


def resp_freq(filt, Ts, Nfreqs):

    n = np.arange(len(filt))

    # Vector de frecuencias logarítmicamente espaciado
    fmin = 1e-3
    fmax = 1.0 / (2.0 * Ts)

    freqs = np.logspace(
        np.log10(fmin),
        np.log10(fmax),
        Nfreqs
    )

    # Respuesta en frecuencia
    H = np.sum(
        filt * np.exp(
            -2j * np.pi * np.outer(freqs, n) * Ts
        ),
        axis=1
    )

    # Magnitud
    H_mag = np.abs(H)

    # Magnitud en dB
    H_dB = 20 * np.log10(H_mag)

    return (H_dB, freqs)