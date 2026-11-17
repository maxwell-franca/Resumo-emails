#!/usr/bin/env python3
"""
Limpa um export de workflow do n8n antes de publicar no GitHub.

Uso:
    python scripts/limpar_workflow.py meu-export.private.json workflow/resumo-diario-emails-agenda.json

O que faz:
  - troca qualquer endereço de e-mail por COLOQUE_SEU_EMAIL_AQUI
  - remove as referências a credenciais (id e nome) de cada nó
  - remove ids do workflow e da instância (id, versionId, meta, webhookId)
  - esvazia pinData (dados fixados de execuções podem conter e-mails reais)
  - aponta o nó do Google Calendar para a agenda principal ("primary")

No final confere o resultado e termina com erro (código 1) se sobrar algo suspeito.
Nenhum e-mail é impresso na tela.
"""
import json
import re
import sys

EMAIL = re.compile(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+")
PLACEHOLDER = "COLOQUE_SEU_EMAIL_AQUI"


def scrub(value):
    """Troca e-mails por placeholder em qualquer string do JSON."""
    if isinstance(value, str):
        return EMAIL.sub(PLACEHOLDER, value)
    if isinstance(value, list):
        return [scrub(v) for v in value]
    if isinstance(value, dict):
        return {k: scrub(v) for k, v in value.items()}
    return value


def limpar(wf):
    for chave in ("id", "versionId", "triggerCount", "meta"):
        wf.pop(chave, None)
    wf["pinData"] = {}
    for no in wf.get("nodes", []):
        no.pop("credentials", None)
        no.pop("webhookId", None)
        if no.get("type", "").endswith("googleCalendar") and "calendar" in no.get("parameters", {}):
            no["parameters"]["calendar"] = {"__rl": True, "value": "primary", "mode": "id"}
    return scrub(wf)


def problemas(wf):
    """Lista o que ainda parece dado pessoal ou da instância (sem imprimir os valores)."""
    achados = []
    texto = json.dumps(wf, ensure_ascii=False)
    sobra = [e for e in EMAIL.findall(texto) if e != PLACEHOLDER]
    if sobra:
        achados.append(f"{len(sobra)} e-mail(s) ainda no arquivo")
    for chave in ("credentials", "instanceId", "webhookId", "versionId"):
        if f'"{chave}"' in texto:
            achados.append(f'chave "{chave}" ainda presente')
    if wf.get("pinData"):
        achados.append("pinData não está vazio")
    return achados


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    origem, destino = sys.argv[1], sys.argv[2]
    with open(origem, encoding="utf-8") as f:
        wf = json.load(f)
    limpo = limpar(wf)
    achados = problemas(limpo)
    if achados:
        sys.exit("NÃO publicado, revise: " + "; ".join(achados))
    with open(destino, "w", encoding="utf-8") as f:
        json.dump(limpo, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"OK: {destino} gravado ({len(limpo['nodes'])} nós, sem e-mails, credenciais ou IDs da instância).")


if __name__ == "__main__":
    main()
