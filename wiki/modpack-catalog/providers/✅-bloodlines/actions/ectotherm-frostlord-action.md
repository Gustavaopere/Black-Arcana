# Lord of Frost — Bloodlines 3.0.9

Estado: **✅ CATALOGADO / COUNTED_SOURCE_PINNED — identidade da Action e contrato auditados**

## Identidade e origem

- **Tipo:** `IAction` registrada pelo Bloodlines no registro de Actions do Vampirism; **não** é uma spell do Iron's/Ars.
- **Registry ID:** `bloodlines:ectotherm_frostlord_action`.
- **Bloodline:** `Ectotherm`.
- **Versão instalada:** `bloodlines-1.21-3.0.9.jar`, com Vampirism `1.10.13`; prova detalhada via source pin `TheDrOfDoctoring/bloodlines@c8fd517d204d09dfcb9a544c17d7df87755eaa5c`.
- **Tratamento semântico:** **COUNTED_SOURCE_PINNED (já contado):** identidade provider-owned no conjunto de 28 Actions normalmente alcançáveis, sob os gates e recursos definidos pelo provider. Este arquivo não adiciona um objeto semântico ao ledger.
- **Execução/settlement:** Vampirism `IActionHandler` e Bloodlines mantêm autoridade de ativação, cooldown, duração, skills, sangue, Souls, Phylactery, efeitos e limpeza; Black Arcana não adiciona custo, cast ou lifecycle duplicado.

## Contrato individual preservado da auditoria do projeto

Defaults:

- cooldown **15 s**;
- duration by rank: **15 / 30 / 60 / 120 s**;
- Lord-of-Frost-duration skill multiplier: **2×**;
- increased attack-damage gate: rank **3** by default;
- attack-damage multipliers by rank config: **1.25 / 1.35 / 1.50 / 1.75**; implementation applies `value - 1` with `ADD_MULTIPLIED_BASE` after the configured rank gate.

If Ice Lord is enabled, activation toggles `icePhasing`; deactivation clears it. Frozen Attack/Slowness Attack crit hooks are evaluated while this action is active.

## Limites e testes

Os números acima são observações/defaults de source-pinned 3.0.9, não valores medidos em `config/` implantado nem resultado de conjuração física. Aplicam-se os gates reais de Bloodline, skill tree, rank, estado e recursos. Verificar no modpack cliente/servidor a interoperabilidade com Vampirism 1.10.13 e demais addons antes de integrar ou certificar efetividade.

**Referências canônicas:** [ACTION-CATALOG.md](../ACTION-CATALOG.md) · [MAGIAS.md](../MAGIAS.md) · [TECHNICAL-AUDIT.md](../TECHNICAL-AUDIT.md) · [INTEGRATION-RULES.md](../INTEGRATION-RULES.md). Documento clean-room: transcrição da auditoria factual do próprio repositório, sem código ou assets upstream.
