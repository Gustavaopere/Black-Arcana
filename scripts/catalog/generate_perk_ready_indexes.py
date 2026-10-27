#!/usr/bin/env python3
"""Regenerate strict perk-ready indexes; never infer 100% from legacy ✅ folders.

The denominator is individual Markdown cards found under providers, not every
possible object in compiled registries or aggregate JSON/catalog documents.
Run without flags to update all INDEX.md, then --check to verify consistency.
"""
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_perk_ready_indexes as qa

ROOT = qa.PROVIDERS
TICK = chr(96)

def friendly(value: str) -> str:
    return value.removeprefix("✅-").replace("_", " ").replace("-", " ").title()

def bar(done: int, total: int) -> str:
    count = (20 * done // total) if total else 0
    return ("█" * count + "░" * (20 - count) +
            (f" {100 * done / total:.1f}%" if total else " — não determinado"))

def alphabetical_scope(mods: list[Path], cards: list[Path]) -> dict:
    """Verified alphabetical triage; never imply perk-ready from semantic closure."""
    path = ROOT.parent / "meta/ALPHABETICAL-CATALOG-STATUS.json"
    if not path.is_file():
        return {"completed_prefix": [], "next_provider": None}
    doc = json.loads(path.read_text(encoding="utf8"))
    if doc.get("schema_version") != 1 or doc.get("order") != "provider_directory_name_ascending":
        raise ValueError("invalid alphabetical catalog ledger schema")
    entries = doc.get("completed_prefix")
    names = [p.name for p in mods]
    if not isinstance(entries, list) or len(entries) > len(names):
        raise ValueError("invalid completed alphabetical prefix")
    if [x.get("provider") for x in entries] != names[:len(entries)]:
        raise ValueError("alphabetical catalog entries must be a contiguous provider prefix")
    if doc.get("next_provider") != (names[len(entries)] if len(entries) < len(names) else None):
        raise ValueError("next provider is not the next alphabetical entry")
    for item in entries:
        mod = ROOT / item["provider"]
        evidence = item.get("evidence")
        if (item.get("state") != "NONMAGICAL_SCOPE_CLOSED"
                or item.get("owned_magic_actions") != 0
                or evidence != item["provider"] + "/README.md"
                or any(mod in card.parents for card in cards)):
            raise ValueError("nonmagical catalog closure has unsupported claims")
        source = ROOT / evidence
        if not source.is_file():
            raise ValueError("nonmagical scope lacks a local evidence document")
        facts = source.read_text(encoding="utf8")
        if not all(token in facts for token in (
                "Provider-owned spells: **0**",
                "Provider-owned rituals/rites: **0**",
                "Provider-owned equivalent discrete magical actions: **0**")):
            raise ValueError("nonmagical source fails closed on missing zero-action proof")
    return doc


def directory_index(folder: Path, dirs: list[Path], cards: list[Path],
                    ledger: dict) -> str:
    parts = folder.relative_to(ROOT).parts
    mod = ROOT / parts[0]
    group = sorted(p for p in cards if folder in p.parents)
    complete = sum(qa.certified(p, ledger) for p in group)
    manifest_link = "../" * (len(parts) + 1) + "meta/PERK-READY-CERTIFICATIONS.json"
    rows = [
        "# Índice técnico para perks — " + " / ".join(friendly(x) for x in parts), "",
        "> Índice das fichas individuais identificadas por nome de arquivo. Uma ficha "
        "existente ou pasta antiga ✅ não certifica parâmetros, fluxo causal, "
        "integração ou testes.", "",
        f"**Homologadas para perks (somente fichas detectadas): {complete}/{len(group)}.**",
        f"**Barra do recorte documental:** {TICK}{bar(complete, len(group))}{TICK}",
        "**Denominador de todo o conteúdo integrável:** não verificado; o recorte "
        "não equivale ao progresso total do mod.", "",
    ]
    if folder == mod:
        alpha = alphabetical_scope(sorted(p for p in ROOT.iterdir() if p.is_dir()), cards)
        closed = {item["provider"]: item for item in alpha["completed_prefix"]}
        if mod.name in closed:
            rows += [
                "**Catalogação semântica (independente da homologação de perks):** "
                "✅ escopo encerrado: 0 feitiços, 0 rituais e 0 habilidades mágicas "
                "próprias. Apenas apresentação visual; [evidência](README.md).", ""
            ]
        elif mod.name == alpha["next_provider"]:
            rows += [
                "**Fila alfabética:** 🟡 próximo provider a concluir. "
                "Não presumir 100% a partir de inventário agregado.", ""
            ]
        known = ledger.get("known_rosters", {}).get(mod.name)
        if known:
            rows += [
                f'**Registro específico confirmado:** {known["scope"]}: {known["total"]} '
                f'([fonte]({known["source"]})). Outros sistemas/objetos podem existir.', ""
            ]
        rows += [
            ("**Estado técnico global:** ✅ 100% certificado com escopo fechado."
             if qa.mod_certified(mod, cards, ledger) else
             "**Estado técnico global:** ⚠️ NÃO HOMOLOGADO como 100%; "
             "universo integral ainda depende de validação."), ""
        ]
    elif group and complete == len(group):
        rows += [
            "**Estado desta subpasta:** ✅ contratos técnicos estáticos de todas as "
            "fichas detectadas certificados; recorte documental, sem homologação "
            "de hooks mutadores, QA físico ou universo integral do provider.", ""
        ]
    else:
        rows += [
            "**Estado desta subpasta:** ⚠️ validação técnica individual pendente; "
            "status histórico de catálogo não é certificação.", ""
        ]
    if group:
        rows += ["| Estado | Objeto / habilidade identificada | Ficha |", "|---|---|---|"]
        for card in group:
            rel = card.relative_to(folder).as_posix()
            category = "/".join(card.relative_to(folder).parts[:-1]) or "ficha"
            symbol = "✅" if qa.certified(card, ledger) else "⚠️"
            rows.append(f"| {symbol} | {friendly(card.stem)} | "
                        f"[{category}/{card.name}]({rel}) |")
    else:
        rows += [
            "*Nenhuma ficha individual detectada nesta árvore pelas regras conservadoras.* "
            "Isso **não significa zero** magias/habilidades: podem existir inventários "
            "agregados, JSONs, classes ou registros ainda não desmembrados.", ""
        ]
    children = sorted(d for d in dirs if d.parent == folder)
    if children:
        rows += ["", "## Subpastas", "",
                 "| Subpasta | Fichas individuais detectadas | Índice |", "|---|---:|---|"]
        for child in children:
            count = sum(child in card.parents for card in cards)
            rows.append(f"| {friendly(child.name)} | {count} | "
                        f"[Abrir índice]({child.name}/INDEX.md) |")
    rows += [
        "", "## Critério do ✅", "",
        "Somente fichas individualmente auditadas no manifesto "
        f"[PERK-READY-CERTIFICATIONS.json]({manifest_link}) podem receber ✅, "
        "exigindo identidade, comportamento, parâmetros, targeting, custos, "
        "boundary de integração e validação documentados. Hook inseguro ou "
        "desconhecido nunca é presumido.", "",
        "Arquivos técnicos de apoio e inventários agregados continuam relevantes, "
        "mas não são contabilizados como objetos concluídos. O algoritmo deve "
        "ser revisado por provider antes de declarar universo fechado.", ""
    ]
    return "\n".join(rows)

def global_index(mods: list[Path], cards: list[Path], ledger: dict) -> str:
    alpha = alphabetical_scope(mods, cards)
    closed = {item["provider"] for item in alpha["completed_prefix"]}
    next_mod = alpha["next_provider"]
    done = sum(qa.mod_certified(mod, cards, ledger) for mod in mods)
    object_done = sum(qa.certified(card, ledger) for card in cards)
    rows = [
        "# Índice geral — certificação 100% para perks", "",
        "> Os prefixos ✅ antigos significam inventário histórico, não 100% técnico "
        "para perks.", "",
        f"**Mods com escopo integral certificado: {done}/{len(mods)}.**",
        f"**Fichas com contrato técnico estático certificado: {object_done}/{len(cards)}.**",
        f"**Barra das fichas estáticas observadas:** {TICK}{bar(object_done, len(cards))}{TICK}",
        f"**Progresso global confirmado:** {TICK}{bar(done, len(mods))}{TICK}",
        "**Escopo:** pastas atuais de providers; a modlist pode conter outros "
        "mods/sistemas ainda não representados. Objetos ausentes do catálogo "
        "não são presumidos inexistentes.", "",
        f"**Revisão alfabética do catálogo semântico:** {len(closed)}/{len(mods)} "
        "providers com escopo explicitamente encerrado; nesta fase, "
        f"{len(closed)} classificado(s) sem ações mágicas próprias. "
        "Esse contador NÃO equivale a providers perk-ready.",
        f"**Próximo na fila alfabética:** {friendly(next_mod) if next_mod else 'Nenhum'}.", "",
        "| Estado 100% | Mod/provider | Fichas individuais candidatas | "
        "Fichas 100% certificadas | Índice |", "|---|---|---:|---:|---|",
    ]
    for mod in mods:
        selected = [p for p in cards if mod in p.parents]
        certified = sum(qa.certified(p, ledger) for p in selected)
        state = "✅" if qa.mod_certified(mod, cards, ledger) else "⚠️"
        display = friendly(mod.name)
        if mod.name in closed:
            display += " — ✅ escopo semântico encerrado (0 ações mágicas)"
        elif mod.name == next_mod:
            display += " — 🟡 próximo na fila"
        rows.append(f"| {state} | {display} | "
                    f"{len(selected) if selected else '—'} | {certified} | "
                    f"[Ver fichas]({mod.name}/INDEX.md) |")
    rows += [
        "", "**Legenda:** ✅ 100% certificado; ⚠️ parcial/condicionado ou ainda não "
        "homologado; ❌ não catalogado após auditoria específica; 🟡 em implementação; "
        "⛔ bloqueado por contrato. Ausência de ficha detectada não prova que "
        "não exista conteúdo.", "",
        "**Atenção:** as fichas candidatas são um recorte documental, NÃO o "
        "universo total de feitiços e sistemas. A barra de fichas estáticas observadas "
        "usa certificados/fichas detectadas. A barra Progresso global confirmado "
        "usa providers com escopo integral certificado.", ""
    ]
    return "\n".join(rows)

def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--check", action="store_true",
                   help="verify current committed indexes without modifications")
    args = p.parse_args()
    if args.check:
        result = qa.check()
        ledger = qa.read_ledger(qa.LEDGER)
        dirs, mods, cards = qa.inventory()
        # Verify the generated alphabetical ledger text as well as the numeric
        # index contract, so catalog status cannot be silently hand-edited.
        expected = global_index(mods, cards, ledger)
        if (ROOT / "INDEX.md").read_text(encoding="utf8") != expected:
            result["problems"].append("global alphabetical catalog status drift")
        alpha = alphabetical_scope(mods, cards)
        watched = {item["provider"] for item in alpha["completed_prefix"]}
        if alpha["next_provider"]:
            watched.add(alpha["next_provider"])
        for name in watched:
            folder = ROOT / name
            expected_mod = directory_index(folder, dirs, cards, ledger)
            if (folder / "INDEX.md").read_text(encoding="utf8") != expected_mod:
                result["problems"].append("provider alphabetical catalog status drift: " + name)
        print(f"INDEX CHECK: {result['expected_indexes']} indexes, "
              f"{result['candidate_cards']} candidate cards, "
              f"{len(result['problems'])} errors")
        return int(bool(result["problems"]))
    ledger = qa.read_ledger(qa.LEDGER)
    dirs, mods, cards = qa.inventory()
    changed = 0
    for folder in dirs:
        dest = folder / "INDEX.md"
        data = directory_index(folder, dirs, cards, ledger)
        if not dest.is_file() or dest.read_text(encoding="utf8") != data:
            dest.write_text(data, encoding="utf8")
            changed += 1
    dest = ROOT / "INDEX.md"
    data = global_index(mods, cards, ledger)
    if not dest.is_file() or dest.read_text(encoding="utf8") != data:
        dest.write_text(data, encoding="utf8")
        changed += 1
    print(f"Generated {len(dirs) + 1} indexes; changed={changed}; "
          f"providers={len(mods)} cards={len(cards)}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
