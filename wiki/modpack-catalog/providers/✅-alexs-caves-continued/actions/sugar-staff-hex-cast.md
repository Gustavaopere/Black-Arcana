# Sugar Staff — Hex Cast

- Provider: **Alex's Caves Continued** (`alexscaves`)
- Version: `1.0.10`
- Exact physical/publisher SHA-1: `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`
- Owner: `alexscaves:sugar_staff`
- Trigger: sneaking direct item use
- State: `COUNTED_EXACT`

## Semantic identity

Sneaking use selects the provider Sugar Staff Hex branch and creates one Hex action at the provider-resolved ground position. This is a separate selectable root from Peppermint Cast.

## Exact acquisition

Exact provider data closes Sugar Staff through Licowitch loot.

## Boundary

Numerical tuning, cooldowns, targeting, entities, effects, particles and sounds remain provider authority. Black Arcana catalogs the identity and must not replay provider settlement.

Sources: `../EXACT-1.0.10-ARTIFACT-AUDIT.md`, `../ITEM-ACTION-DISPOSITION-1.0.10.md`.

## Engenharia causal — fonte público fixado, NÃO paridade binária

**Proveniência dos números abaixo:** inspeção somente-leitura do fonte público `Codx-org/AlexsCavesContinued@523308608422ab8e31974befa7111ecdf495dd37` (LGPL-3.0), corroborando qualitativamente a identidade do JAR físico 1.0.10. O catálogo anterior comprova os **8 registros de ações pela inspeção do JAR**, mas **não** que este snapshot público foi compilado em bytes idênticos ao artefato `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`. Assim, os valores a seguir são **SOURCE_SNAPSHOT_ONLY**, não parâmetros certificados da versão física. Configuração efetiva, hooks mutadores e QA física: `NOT_VERIFIED`.

| Propriedade | Comportamento observado no snapshot público |
|---|---|
| Entrada | `SugarStaffItem.use` com `player.isShiftKeyDown()`, em ramo separado do Peppermint e criação server-side de `SugarStaffHexEntity` |
| Posição / target | `ACMath.getGroundBelowPosition(level, player.getEyePosition())`; não usa entidade-alvo do ramo Peppermint: é área centrada no chão encontrado pela função provider-owned |
| Escala | `setHexScale(1.0F + 0.25F * level(HUMUNGOUS_HEX))`; dimensões da entidade `width=4*hexScale`, `height=0.25F` |
| Duração | `setLifespan(100 + 60 * level(SPELL_LASTING))` ticks; default sincronizado da entidade `100` |
| Recarga/custo | `ACCompat.addCooldown(..., 100)` ticks no uso de Hex e uma unidade de durabilidade; não foi observada cobrança direta de mana neste método |
| Alvo e filtro | `SugarStaffHexEntity.hurtEntities` avalia entidades vivas na AABB da Hex e adicionalmente `distanceTo(this) <= 4.0F`, excluindo owner/aliados de acordo com lógica de friendly-fire |
| Tipo / dano | `damageSources().indirectMagic(this, owner)`; `1.0F` nos ticks ordinários e `6.0F` quando `despawnsIn < 5`; nessa janela aplica knockback `0.9F` |
| Tick / finalização | `tick()` decrementa `despawnsIn`, executa `hurtEntities(despawnsIn < 5)` e descarta ao expirar; a janela final ocorre em ticks sucessivos, **não** é prova de uma única explosão de dano |

### Interação perigosa para perks

`width=4*scale` descreve dimensão da hitbox, enquanto o teste radial de `4.0F` é uma segunda condição. Aumentar só a escala **não** prova ampliação proporcional de alcance em todos os eixos. A duração é escrita pelo staff; o `HEX_SCALE` da entidade é sincronizado, mas a fonte não demonstra uma API externa para alterar após o cast. Uma perk de área/duração deve aguardar contrato real de hook com momento de execução, anti-duplicação e autoridade do provider; do contrário **⛔ fail-closed**. Não repetir a aplicação periódica do `indirectMagic` no pipeline Black Arcana.

**Referência method-pinned:** [`SugarStaffItem.java`](https://github.com/Codx-org/AlexsCavesContinued/blob/523308608422ab8e31974befa7111ecdf495dd37/src/main/java/com/github/alexmodguy/alexscaves/server/item/SugarStaffItem.java), [`SugarStaffHexEntity.java`](https://github.com/Codx-org/AlexsCavesContinued/blob/523308608422ab8e31974befa7111ecdf495dd37/src/main/java/com/github/alexmodguy/alexscaves/server/entity/item/SugarStaffHexEntity.java); [auditoria exata](../EXACT-1.0.10-ARTIFACT-AUDIT.md).
