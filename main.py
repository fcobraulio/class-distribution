import argparse
import os
import random
from collections import defaultdict

import pandas as pd

DATA_DIR = "data"
TURMAS_FILE = os.path.join(DATA_DIR, "turmas.csv")
PREF_FILE = os.path.join(DATA_DIR, "preferencias.csv")
RESULT_FILE = os.path.join(DATA_DIR, "results.csv")


def gerar_preferencias_aleatorias():
    df = pd.read_csv(TURMAS_FILE)
    disciplinas = df["disciplina"].unique().tolist()

    professores = ["PROFESSOR1", "PROFESSOR2", "PROFESSOR3", "PROFESSOR4"]

    # Criar conflitos nas primeiras preferências
    random.shuffle(disciplinas)
    conflito = disciplinas[:2]

    registros = []

    for prof in professores:
        prefs = disciplinas.copy()
        random.shuffle(prefs)

        # Forçar conflito nas primeiras posições
        prefs[0] = conflito[0]
        prefs[1] = conflito[1]

        for ordem, disciplina in enumerate(prefs):
            registros.append({
                "nome_professor": prof,
                "preferencia": ordem + 1,
                "disciplina": disciplina
            })

    pref_df = pd.DataFrame(registros)
    pref_df.to_csv(PREF_FILE, index=False)
    print("Arquivo preferencias.csv gerado com conflitos simulados.")


def carregar_preferencias():
    pref_df = pd.read_csv(PREF_FILE)
    preferencias = defaultdict(dict)

    for _, row in pref_df.iterrows():
        preferencias[row["nome_professor"]][row["disciplina"]] = row["preferencia"]

    return preferencias


def distribuir_turmas(semestre):
    df = pd.read_csv(TURMAS_FILE)

    df["semestre"] = pd.to_numeric(df["semestre"], errors="coerce")
    df = df[df["semestre"] == semestre].copy()

    if df.empty:
        print("⚠ Nenhuma turma encontrada.")
        return

    preferencias = carregar_preferencias()
    professores = list(preferencias.keys())

    carga_professor = {prof: 0 for prof in professores}
    resultado = []

    # Ordenar turmas maiores primeiro ajuda equilíbrio global
    df = df.sort_values(by="quantidade", ascending=False)

    for _, row in df.iterrows():
        disciplina = row["disciplina"]
        horas = int(row["quantidade"])

        melhor_prof = None
        melhor_score = float("inf")

        for prof in professores:
            if disciplina not in preferencias[prof]:
                continue

            # Simular nova carga
            nova_carga = carga_professor[prof] + horas

            # Simular cargas totais
            cargas_simuladas = carga_professor.copy()
            cargas_simuladas[prof] = nova_carga

            diff = max(cargas_simuladas.values()) - min(cargas_simuladas.values())

            # Score = preferência + penalidade por desbalanceamento
            score = (
                preferencias[prof][disciplina] * 10
                + diff * 5
                + nova_carga
            )

            if score < melhor_score:
                melhor_score = score
                melhor_prof = prof

        # fallback
        if melhor_prof is None:
            melhor_prof = min(professores, key=lambda p: carga_professor[p])

        carga_professor[melhor_prof] += horas

        nova_linha = row.to_dict()
        nova_linha["professor"] = melhor_prof
        resultado.append(nova_linha)

    resultado_df = pd.DataFrame(resultado)
    resultado_df.to_csv(RESULT_FILE, index=False)

    print("\nDistribuição final:")
    print(resultado_df)
    print("\nCarga horária final:")
    print(carga_professor)
    print("Diferença máxima:",
          max(carga_professor.values()) - min(carga_professor.values()))

    resultado_df = pd.DataFrame(resultado)
    resultado_df.to_csv(RESULT_FILE, index=False)

    print("\nDistribuição final:")
    print(resultado_df)
    print("\nCarga horária final:")
    print(carga_professor)


def main():
    parser = argparse.ArgumentParser(
        description="Distribuição de turmas entre professores"
    )

    parser.add_argument(
        "semestre",
        type=int,
        choices=[1, 2],
        help="Semestre letivo (1 ou 2)"
    )

    parser.add_argument(
        "--gerar-preferencias",
        action="store_true",
        help="Gera um novo arquivo preferencias.csv aleatório"
    )

    args = parser.parse_args()

    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    # Se o usuário pediu para gerar novas preferências
    if args.gerar_preferencias:
        gerar_preferencias_aleatorias()

    # Se não existe arquivo e não pediu para gerar → erro claro
    if not os.path.exists(PREF_FILE):
        raise FileNotFoundError(
            "Arquivo preferencias.csv não encontrado. "
            "Use --gerar-preferencias para criar um automaticamente."
        )

    distribuir_turmas(args.semestre)


if __name__ == "__main__":
    main()