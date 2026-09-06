# Magma Bomb

- **Status no modpack:** PRESENTE — provider instalado
- **Provider:** Iron's Spells 'n Spellbooks
- **Mod ID:** `irons_spellbooks`
- **JAR/versão:** `irons_spellbooks-1.21.1-3.16.3.jar` / `1.21.1-3.16.3`
- **Escola:** Fire
- **Níveis:** 1–8
- **Raridade:** Uncommon → Legendary
- **Cast:** Long
- **Mana:** 30–65
- **Cooldown:** 12 s
- **Dano de impacto atual:** 8
- **Dano AOE:** 1,7–3,9
- **Raio:** 4 blocos

## O que faz

Lança uma bomba de magma que explode ao impactar e deixa um campo de fogo no local.

## Escalonamento

A build atual lista impacto fixo 8, AOE 1,7–3,9 e raio 4 blocos. O changelog registra que o dano de impacto deixou de escalar com nível e que a parametrização de AOE/raio foi revisada; valores antigos não substituem os atuais.

## Obtenção e aprendizado

Segue o pipeline geral de scrolls/spellbooks do Iron's. Rotas específicas permanecem `NÃO VERIFICADO`.

## Deduplicação / world safety

Já cobre projétil de magma + explosão + campo persistente de fogo. A existência desse campo não autoriza Black Arcana a inferir vanilla fire spread, persistence ou mutação fora do provider; bridges devem observar, não duplicar, o field.

## Fonte / evidência

- Catálogo oficial atual: `https://iron.wiki/spells/`
- Changelog oficial: `https://iron.wiki/changelog/`
- Consulta: 2026-09-06.
