import numpy as np

def analisis_sre(h):

    # --------------------------------------------------
    # 1. Normalización del filtro
    # --------------------------------------------------
    energia = np.sum(h**2)
    h_norm = h / np.sqrt(energia)

    print(f"Potencia del filtro RC antes de normalizar = {energia}")
    print(f"Potencia del filtro RC después de normalizar = {np.sum(h_norm**2)}")

    # --------------------------------------------------
    # 2. Probar diferentes cantidades de bits
    #    fraccionarios
    # --------------------------------------------------
    NBF_values = range(1, 13)
    sre_db = []

    for NBF in NBF_values:
        # Resolución del punto fijo
        escala = 2**NBF

        # Cuantización
        h_fixed = np.round(h_norm * escala) / escala    #estoy redondeando

        # --------------------------------------------------
        # 3. Error de cuantización
        # --------------------------------------------------

        error = h_norm - h_fixed

        # Potencia de la señal
        P_signal = np.sum(h_norm**2)

        # Potencia del error
        P_error = np.sum(error**2)

        # --------------------------------------------------
        # 4. SRE
        # --------------------------------------------------
        if P_error == 0:
            sre = np.inf
        else:
            sre = 10 * np.log10(P_signal / P_error)
        sre_db.append(sre)
        print( f"NBF = {NBF:2d} | "f"SRE = {sre:8.3f} dB")

    return list(NBF_values), sre_db, h_norm