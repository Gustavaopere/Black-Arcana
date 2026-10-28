# Sugar Staff — Peppermint Cast

- Provider: **Alex's Caves Continued** (`alexscaves`)
- Version: `1.0.10`
- Exact physical/publisher SHA-1: `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`
- Owner: `alexscaves:sugar_staff`
- Trigger: normal direct item use
- State: `COUNTED_EXACT`

## Semantic identity

Normal use selects the provider Peppermint Cast branch and creates its peppermint action pattern around/from the player. This is distinct from the sneaking Hex branch because the player deliberately selects a separate causal action.

## Exact acquisition

Exact provider data closes Sugar Staff through Licowitch loot.

## Boundary

Numerical tuning, cooldowns, targeting, entities, effects, particles and sounds remain provider authority. Black Arcana catalogs the identity and must not replay provider settlement.

Sources: `../EXACT-1.0.10-ARTIFACT-AUDIT.md`, `../ITEM-ACTION-DISPOSITION-1.0.10.md`.

## Engenharia causal — fonte público fixado, NÃO paridade binária

**Proveniência dos números abaixo:** inspeção somente-leitura do fonte público `Codx-org/AlexsCavesContinued@523308608422ab8e31974befa7111ecdf495dd37` (LGPL-3.0), corroborando qualitativamente a identidade do JAR físico 1.0.10. O catálogo anterior comprova os **8 registros de ações pela inspeção do JAR**, mas **não** que este snapshot público foi compilado em bytes idênticos ao artefato `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`. Assim, os valores a seguir são **SOURCE_SNAPSHOT_ONLY**, não parâmetros certificados da versão física. Configuração efetiva, hooks mutadores e QA física: `NOT_VERIFIED`.

| Propriedade | Comportamento observado no snapshot público |
|---|---|
| Entrada | `SugarStaffItem.use` com `!player.isShiftKeyDown()`; lançamento de entidades no servidor, independente da ação Hex |
| Quantidade | `3 + level(MULTIPLE_MINT)` instâncias `SpinningPeppermintEntity` por ativação |
| Duração da entidade | `setLifespan(80)` ticks em cada peppermint; `LIFESPAN` sincronizado tem default `200` no construtor da entidade, mas o staff **sobrescreve com 80**; não confundir default de classe com cast do item |
| Cooldown por uso | `80` ticks baseline; `20` ticks em `PEPPERMINT_PUNTING`; `50` ticks quando `SEEKCANDY` tem alvo elegível (essa atribuição ocorre depois de PUNTING) |
| Target assistido | Seleção via `SeaStaffItem.getClosestLookingAtEntityFor(..., 32)`; `SEEKCANDY` registra **entity ID** (`setSeekingEntityId`), não UUID, e a entidade resolve o alvo durante seus ticks |
| Padrão reto | `PEPPERMINT_PUNTING` define `STRAIGHT=true` e rotação `180 + yaw + (i - 1)*15`; sem ele, órbita inicial `180+(i-1)*30` com `STRAIGHT=false` |
| Custo | Um ponto de durabilidade do item no método de uso; nenhuma cobrança de mana observada nesse método |
| DamageSource | `SpinningPeppermintEntity.hurtEntities()` usa `mobProjectile`, dano `3.0F` por colisão de AABB e `knockback=0.3F`; alvo proprietário/aliados excluídos pelas condições da entidade |
| Ciclo e descarte | `tick()` calcula órbita ou trajetória reta, aplica colisão e descarta quando expira; acerto com seeking selecionado pode antecipar descarte |

### Risco de parâmetros sobrescritos no runtime

A criação do objeto configura `spinSpeed` para `8F`, `12F` ou `50F` e `spinRadius` para `3.5F`; porém `SpinningPeppermintEntity.tick()` executa `setSpinRadius(3F)` e `setSpinSpeed(7F)` em cada tick, **antes** do deslocamento. Não registrar esses valores iniciais como velocidade/raio sustentados nem propor perk por escrever nos setters sem comprovar quando o setter é lido. O comportamento físico e o efeito de mixins/datapacks exigem teste no JAR instalado.

**Integração:** `SugarStaffItem.use`, `SpinningPeppermintEntity.tick` e `hurtEntities` são superfícies internas observadas, não contratos de mutação suportados. A perk não deve gerar um segundo peppermint, somar dano de cada tick como spell independente nem modificar o cooldown na autoridade do Black Arcana. **⛔ Fail-closed** até hook e lifecycle verificados.

**Referência method-pinned:** [`SugarStaffItem.java`](https://github.com/Codx-org/AlexsCavesContinued/blob/523308608422ab8e31974befa7111ecdf495dd37/src/main/java/com/github/alexmodguy/alexscaves/server/item/SugarStaffItem.java), [`SpinningPeppermintEntity.java`](https://github.com/Codx-org/AlexsCavesContinued/blob/523308608422ab8e31974befa7111ecdf495dd37/src/main/java/com/github/alexmodguy/alexscaves/server/entity/item/SpinningPeppermintEntity.java), [`SeaStaffItem.java`](https://github.com/Codx-org/AlexsCavesContinued/blob/523308608422ab8e31974befa7111ecdf495dd37/src/main/java/com/github/alexmodguy/alexscaves/server/item/SeaStaffItem.java); [auditoria exata](../EXACT-1.0.10-ARTIFACT-AUDIT.md).
