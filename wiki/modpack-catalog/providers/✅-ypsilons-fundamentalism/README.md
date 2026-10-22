# Ypsilon's Fundamentalism / Fundamental Principles

**✅ Prova binária 2026-10-13:** [15/15 spell IDs físicos](EXACT-BINARY-SPELLS-1.1.7.1.md), [Java21 #38436717443](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38436717443) SUCCESS, CurseForge file 8558503 **858749 bytes**, SHA-1 `a2855c253202a8fcc2925fcf5b1bf86d64fbe4da` igual ao registro da modlist física #575. `COUNTED_EXACT` para registry de spells, **+0** raízes, campanha **18/39 exatos / 21/39 pendentes**, mínimos **1857 global / 1855 escopo** inalterados. **13 Principles não são mais 13 feitiços**; XP, mana/casts, side/thread, configuração, multiplayer/Survival ⚠️. Conteúdo source-pinned abaixo continua histórico, não valida runtime.


## Estado canônico

- JAR instalado: `ypfundamentals-1.1.7.1.jar`
- mod id: `ypfundamentals`
- Minecraft: `1.21.1`
- versão: `1.1.7.1`
- source pin exato: `ypsilonM/FundamentalPrinciples-1.21.1@a9b8f8222fb2a800edece8c1568984bd2a764fc2` (`final 1.1.7.1`)
- source dependency: Iron's `3.16.2`; pack: Iron's `3.16.3` → runtime QA obrigatório para delta de API/comportamento.
- catálogo de spells: **15/15 ATIVOS — COMPLETO**.

## Spells ativos por escola

| Escola | Quantidade | Spells |
|---|---:|---|
| Ice | 1 | Frozen Chains |
| Fire | 4 | Burning Spirit, Pyrokinesis, Tonatiuh, Ignite |
| Blood | 3 | Bloodstream, Thorn, Laceration |
| Holy | 2 | Holy Lightning, Sacred Disk |
| Ender | 2 | Pull, Lapsus |
| Evocation | 1 | Taunt |
| Fundamentalism | 2 | Law Of Regression, Saeptum |
| **Total** | **15** | |

O registry exato está em `src/main/java/com/ypsi/fundamentalism/spells/ModSpells.java`. Registrations comentados como Yggdrasil, Copycat, Steal Summon, Mirror e Proiectum **não são conteúdo ativo** desta versão.

## Sistema transversal: 13 Principles

Este provider não é somente um pacote de spells. Ele analisa o `SpellRegistry` global por ASM, classifica spells de outros providers em 13 Principles, mantém nível/XP persistente por jogador, aplica passivas e gates, além de possuir fatigue e progressão de spellbooks. Ver `PRINCIPLES.md`.

**Authority:** Ypsilon é authority para classificação, XP, nível, fatigue, passivas e unlocks de Principles. Black Arcana não deve criar um segundo ledger paralelo.

## Estrutura

- `TECHNICAL-AUDIT.md` — authority, hooks, QA e deduplicação.
- `PRINCIPLES.md` — 13 Principles e seus contratos.
- `<school>/<spell>.md` — ficha individual dos 15 spells.

## Definição de COMPLETO

`15/15` significa que todos os registrations ativos da release exata possuem ficha e que todo campo obrigatório está sustentado por source ou explicitamente marcado `NÃO VERIFICADO`. Não significa que todos os bugs upstream, compatibilidades 3.16.2→3.16.3 ou testes multiplayer estejam validados.

## Principles — fichas técnicas individuais (22/10/2026)

Os [13 sistemas/passivas agora têm ficha individual](principles/README.md), além das 15 magias já catalogadas. O recorte mede **13/13 fichas de categorias enum**, sem somar 13 spells, sem fechar todos os parâmetros técnicos do provider e sem PASS físico. A [visão agregada](PRINCIPLES.md) foi corrigida para os consumidores reais de range, recast, cooldown, efeitos, custos e XP. Nenhuma nova perk, adapter ou alteração runtime.
