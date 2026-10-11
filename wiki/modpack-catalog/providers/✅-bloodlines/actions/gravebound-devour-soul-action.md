# Devour Soul — Bloodlines 3.0.9

Estado: **✅ CATALOGADO / COUNTED_SOURCE_PINNED — identidade da Action e contrato auditados**

## Identidade e origem

- **Tipo:** `IAction` registrada pelo Bloodlines no registro de Actions do Vampirism; **não** é uma spell do Iron's/Ars.
- **Registry ID:** `bloodlines:gravebound_devour_soul_action`.
- **Bloodline:** `Gravebound`.
- **Versão instalada:** `bloodlines-1.21-3.0.9.jar`, com Vampirism `1.10.13`; prova detalhada via source pin `TheDrOfDoctoring/bloodlines@c8fd517d204d09dfcb9a544c17d7df87755eaa5c`.
- **Tratamento semântico:** **COUNTED_SOURCE_PINNED (já contado):** identidade provider-owned no conjunto de 28 Actions normalmente alcançáveis, sob os gates e recursos definidos pelo provider. Este arquivo não adiciona um objeto semântico ao ledger.
- **Execução/settlement:** Vampirism `IActionHandler` e Bloodlines mantêm autoridade de ativação, cooldown, duração, skills, sangue, Souls, Phylactery, efeitos e limpeza; Black Arcana não adiciona custo, cast ou lifecycle duplicado.

## Contrato individual preservado da auditoria do projeto

Cooldown by rank: **75 / 60 / 40 / 20 s**.

No Soul cost. Target eligibility remains `BloodlineGravebound.canDevour(...)`, including EntitySoulData, health threshold, distance and player-alive-time gates.

Static settlement finding: for any targeted `LivingEntity` while the manager is Gravebound, the action returns `true` even when `canDevour(...)` is false. Therefore an invalid living target may still be reported as successful to the action handler and consume cooldown. Runtime-test before attaching any completion-sensitive Black Arcana trigger.

## Limites e testes

Os números acima são observações/defaults de source-pinned 3.0.9, não valores medidos em `config/` implantado nem resultado de conjuração física. Aplicam-se os gates reais de Bloodline, skill tree, rank, estado e recursos. Verificar no modpack cliente/servidor a interoperabilidade com Vampirism 1.10.13 e demais addons antes de integrar ou certificar efetividade.

**Referências canônicas:** [ACTION-CATALOG.md](../ACTION-CATALOG.md) · [MAGIAS.md](../MAGIAS.md) · [TECHNICAL-AUDIT.md](../TECHNICAL-AUDIT.md) · [INTEGRATION-RULES.md](../INTEGRATION-RULES.md). Documento clean-room: transcrição da auditoria factual do próprio repositório, sem código ou assets upstream.
