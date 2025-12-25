import os
import json
import matplotlib.pyplot as plt
import pandas as pd
from DyMat import DymolaMat

# -------------------------------
# Fonctions utilitaires
# -------------------------------

def load_mat(file_path):
    """Charge le fichier .mat Dymola."""
    return DymolaMat(file_path)

def extract_data(dm):
    """
    Extrait :
      - les séries temporelles (len(series) == len(time))
      - les variables statiques / géométriques
    Retourne (df_timeseries, dict_static)
    """
    datasets = [k for k in dm.mat.keys() if k.startswith("data")]
    if not datasets:
        raise ValueError("Aucun dataset data_* trouvé dans le fichier .mat")

    main = max(datasets, key=lambda k: dm.mat[k].shape[1])
    time = dm.mat[main][0]

    timeseries = {"time": time}
    static = {}

    for name in dm.names():
        try:
            val = dm.data(name)
            if hasattr(val, "__len__") and len(val) == len(time):
                timeseries[name] = val
            else:
                static[name] = val.tolist() if hasattr(val, "__iter__") else val
        except:
            pass

    return pd.DataFrame(timeseries), static

def plot_signals(df, signals, output_dir):
    """Trace les courbes pour les signaux spécifiés."""
    os.makedirs(output_dir, exist_ok=True)
    for signal in signals:
        if signal in df.columns:
            plt.figure()
            plt.plot(df["time"], df[signal])
            plt.xlabel("Time")
            plt.ylabel(signal)
            plt.title(signal)
            plt.grid(True)
            plt.tight_layout()
            plt.savefig(os.path.join(output_dir, f"{signal}.png"))
            plt.close()
        else:
            print(f"Signal {signal} non trouvé dans le fichier.")

def export_outputs(df, static, file_name):
    """Export CSV pour les timeseries et JSON pour les statiques."""
    os.makedirs("outputs/csv", exist_ok=True)
    os.makedirs("outputs/json", exist_ok=True)

    csv_path = f"outputs/csv/{file_name}.csv"
    json_path = f"outputs/json/{file_name}_static.json"

    df.to_csv(csv_path, index=False)
    with open(json_path, "w") as f:
        json.dump(static, f, indent=2)

# -------------------------------
# Pipeline principale
# -------------------------------

def run(file_path):
    print(f"Chargement du fichier : {file_path}")
    dm = load_mat(file_path)
    df, static = extract_data(dm)

    # Exclusion des colonnes constantes et on garde celles qui changent dans le temps
    key_signals = [col for col in df.columns if col != "time" and df[col].nunique() > 1]

    print(f"Signaux clés identifiés : {key_signals}")
    plot_signals(df, key_signals, output_dir="outputs/plots")
    export_outputs(df, static, os.path.basename(file_path).replace(".mat",""))

    print("Pipeline terminée")

# -------------------------------
# Exécution CLI
# -------------------------------

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage : python dyma_reader.py <chemin_fichier.mat>")
        sys.exit(1)
    run(sys.argv[1])
