# date_monitor.py - Módulo de Detecção de Mêsversário e Aniversário

import os
import datetime

def detectar_datas_relevantes(pasta, dias_inatividade=180):
    hoje = datetime.datetime.now()
    avisos = []

    for root, _, files in os.walk(pasta):
        for nome in files:
            caminho = os.path.join(root, nome)
            try:
                criado = datetime.datetime.fromtimestamp(os.path.getctime(caminho))
                modificado = datetime.datetime.fromtimestamp(os.path.getmtime(caminho))
                idade_dias = (hoje - criado).days
                modificado_dias = (hoje - modificado).days

                if idade_dias % 30 == 0 and idade_dias < 365:
                    avisos.append({
                        "nome": nome,
                        "caminho": caminho,
                        "tipo": "🗓️ Mêsversário",
                        "criado": criado.date(),
                        "modificado": modificado.date()
                    })
                elif idade_dias >= 365 and idade_dias % 365 == 0:
                    avisos.append({
                        "nome": nome,
                        "caminho": caminho,
                        "tipo": "🎉 Aniversário",
                        "criado": criado.date(),
                        "modificado": modificado.date()
                    })
                elif modificado_dias > dias_inatividade:
                    avisos.append({
                        "nome": nome,
                        "caminho": caminho,
                        "tipo": "❌ Inativo",
                        "criado": criado.date(),
                        "modificado": modificado.date()
                    })
            except Exception as e:
                continue

    return avisos


def exibir_resumo_terminal(avisos):
    print("\n--- Avisos de Arquivos ---")
    for aviso in avisos:
        print(f"{aviso['tipo']} - {aviso['nome']}")
        print(f"  Criado em: {aviso['criado']} | Modificado em: {aviso['modificado']}")
        print(f"  Caminho: {aviso['caminho']}\n")


if __name__ == "__main__":
    pasta_alvo = input("Informe o caminho da pasta a analisar: ")
    avisos = detectar_datas_relevantes(pasta_alvo)
    exibir_resumo_terminal(avisos)
