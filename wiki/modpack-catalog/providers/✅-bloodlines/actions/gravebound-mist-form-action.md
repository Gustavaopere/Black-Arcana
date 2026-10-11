# Mist Form — Bloodlines 3.0.9

Estado: **✅ CATALOGADO / COUNTED_SOURCE_PINNED — identidade da Action e contrato auditados**

## Identidade e origem

- **Tipo:** `IAction` registrada pelo Bloodlines no registro de Actions do Vampirism; **não** é uma spell do Iron's/Ars.
- **Registry ID:** `bloodlines:gravebound_mist_form_action`.
- **Bloodline:** `Gravebound`.
- **Versão instalada:** `bloodlines-1.21-3.0.9.jar`, com Vampirism `1.10.13`; prova detalhada via source pin `TheDrOfDoctoring/bloodlines@c8fd517d204d09dfcb9a544c17d7df87755eaa5c`.
- **Tratamento semântico:** **COUNTED_SOURCE_PINNED (já contado):** identidade provider-owned no conjunto de 28 Actions normalmente alcançáveis, sob os gates e recursos definidos pelo provider. Este arquivo não adiciona um objeto semântico ao ledger.
- **Execução/settlement:** Vampirism `IActionHandler` e Bloodlines mantêm autoridade de ativação, cooldown, duração, skills, sangue, Souls, Phylactery, efeitos e limpeza; Black Arcana não adiciona custo, cast ou lifecycle duplicado.

## Contrato individual preservado da auditoria do projeto

Mist Form is not a normal manual survival action. From configured immortality rank **3**, Bloodlines force-enables its skill, and the lethal-damage hook sets the state and toggles the action when resurrection conditions pass.

Defaults:

- duration **20 s**;
- cooldown **90 s**, or **30 s** with Faster Resurrection;
- required Souls by rank: **15 / 12 / 8 / 5**;
- reduced-cost array with Cheaper Resurrection: **10 / 8 / 6 / 3**;
- flight speed **0.015**.

While active:

- Armor `-1 ADD_MULTIPLIED_TOTAL`;
- Armor Toughness `-1 ADD_MULTIPLIED_TOTAL`;
- Max Health `-0.15 ADD_MULTIPLIED_TOTAL`;
- NeoForge Creative Flight +1;
- forced crouching-sized mist dimensions.

On deactivation the state pays the resurrection Soul cost only when `state.getSouls() > requiredSouls`. Having **exactly** the configured cost is insufficient and falls into the death path. This strict reserve-one behavior must be preserved unless the provider itself is patched intentionally.

## Limites e testes

Os números acima são observações/defaults de source-pinned 3.0.9, não valores medidos em `config/` implantado nem resultado de conjuração física. Aplicam-se os gates reais de Bloodline, skill tree, rank, estado e recursos. Verificar no modpack cliente/servidor a interoperabilidade com Vampirism 1.10.13 e demais addons antes de integrar ou certificar efetividade.

**Referências canônicas:** [ACTION-CATALOG.md](../ACTION-CATALOG.md) · [MAGIAS.md](../MAGIAS.md) · [TECHNICAL-AUDIT.md](../TECHNICAL-AUDIT.md) · [INTEGRATION-RULES.md](../INTEGRATION-RULES.md). Documento clean-room: transcrição da auditoria factual do próprio repositório, sem código ou assets upstream.
