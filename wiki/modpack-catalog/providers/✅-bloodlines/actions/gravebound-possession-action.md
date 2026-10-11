# Possession — Bloodlines 3.0.9

Estado: **✅ CATALOGADO / COUNTED_SOURCE_PINNED — identidade da Action e contrato auditados**

## Identidade e origem

- **Tipo:** `IAction` registrada pelo Bloodlines no registro de Actions do Vampirism; **não** é uma spell do Iron's/Ars.
- **Registry ID:** `bloodlines:gravebound_possession_action`.
- **Bloodline:** `Gravebound`.
- **Versão instalada:** `bloodlines-1.21-3.0.9.jar`, com Vampirism `1.10.13`; prova detalhada via source pin `TheDrOfDoctoring/bloodlines@c8fd517d204d09dfcb9a544c17d7df87755eaa5c`.
- **Tratamento semântico:** **COUNTED_SOURCE_PINNED (já contado):** identidade provider-owned no conjunto de 28 Actions normalmente alcançáveis, sob os gates e recursos definidos pelo provider. Este arquivo não adiciona um objeto semântico ao ledger.
- **Execução/settlement:** Vampirism `IActionHandler` e Bloodlines mantêm autoridade de ativação, cooldown, duração, skills, sangue, Souls, Phylactery, efeitos e limpeza; Black Arcana não adiciona custo, cast ou lifecycle duplicado.

## Contrato individual preservado da auditoria do projeto

Defaults:

- cost **3 Souls**;
- cooldown **120 s**;
- duration **100 s**.

Target must be alive and belong to `bloodlines:possession_whitelist`.

Audited whitelist (14 vanilla types):

- Zombie;
- Husk;
- Drowned;
- Skeleton;
- Bogged;
- Silverfish;
- Wither Skeleton;
- Villager;
- Zombie Villager;
- Creeper;
- Wolf;
- Enderman;
- Phantom;
- Stray.

On server the player's camera is moved to the possessed target. Bloodlines then routes possession-specific movement and interaction packets, including melee/ranged attacks, Creeper ignition and block interaction. No modded entity is implicitly supported merely because it resembles a whitelisted mob.

Logout/entity-leave/death hooks clear possession state to avoid stale ownership.

## Limites e testes

Os números acima são observações/defaults de source-pinned 3.0.9, não valores medidos em `config/` implantado nem resultado de conjuração física. Aplicam-se os gates reais de Bloodline, skill tree, rank, estado e recursos. Verificar no modpack cliente/servidor a interoperabilidade com Vampirism 1.10.13 e demais addons antes de integrar ou certificar efetividade.

**Referências canônicas:** [ACTION-CATALOG.md](../ACTION-CATALOG.md) · [MAGIAS.md](../MAGIAS.md) · [TECHNICAL-AUDIT.md](../TECHNICAL-AUDIT.md) · [INTEGRATION-RULES.md](../INTEGRATION-RULES.md). Documento clean-room: transcrição da auditoria factual do próprio repositório, sem código ou assets upstream.
