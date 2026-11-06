# Rapid Possession — `alexscaves:rapid_possession` (Alex's Caves Continued 1.0.10)

**Estado individual:** ✅ somente **contrato técnico estático** `STATIC_TECHNICAL_CATALOG_ONLY` / `SHA_EXACT_BINARY_BEHAVIOR` (sujeito à CI final). **Hook mutador:** `NOT_VERIFIED`; **QA física:** `NOT_TESTED`; **mutação:** `NO_MUTATION`; **provider integral:** não encerrado. Nenhuma perk executável, mudança de Stage ou integração no runtime Black Arcana está homologada.

## 1. Identidade, versão e texto publisher

- **Provider:** Alex's Caves Continued, `mod_id=alexscaves`, JAR publisher **1.0.10**, Minecraft 1.21.1 / NeoForge / Java 21. Artefato selecionado pela modlist do sibling RPG Skill Tree.
- **Artefato:** CurseForge projeto `1645389`, arquivo `8856293`, `alexscaves-1.0.10-neoforge+1.21.1.jar` (**75.279.314 bytes**). SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`; SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`.
- **Chave:** `alexscaves:rapid_possession`; recurso `data/alexscaves/enchantment/rapid_possession.json`, **376 bytes**, SHA-256 `449eda001a6bb6507ef4e43cc18e601659d970e8bd7d43967aff32dfed07288a`.
- **Descrição literal en-US no JAR:** “Mobs possessed by the Totem of Possession will move faster”. Tradução explicativa: mobs controlados pelo Totem of Possession se deslocam mais rapidamente. A descrição não promete aumento de alcance, duração, ataques ou acerto.
- **Tag de equipamento:** `#alexscaves:enchantable/totem_of_possession`; `data/alexscaves/tags/item/enchantable/totem_of_possession.json` contém `alexscaves:totem_of_possession`, SHA-256 `185a085206993877d91ca6d8c697273c14f945b1d55cb6179e3236c138c357cf`.

Fonte primária: [sonda do JAR físico](../../../../../docs/qa/alexscaves_1010_rapid_possession_probe.py), [selo individual](../EXACT-RAPID-POSSESSION-CONTRACT-1.0.10.json), [contrato binário preexistente das oito ações](../EXACT-TECHNICAL-CONTRACTS-1.0.10.json) e [ação original de controle remoto](../actions/totem-possession-remote-control.md). O source público `Codx-org/AlexsCavesContinued@523308608422ab8e31974befa7111ecdf495dd37` declara versão **1.1.1**, não é autoridade para fixar os valores do JAR 1.0.10.

## 2. JSON, níveis, peso e custos

| Campo | Configuração declarada pelo JAR | Consequência |
|---|---|---|
| `description.translate` | `enchantment.alexscaves.rapid_possession` | Chave de idioma |
| `supported_items` | `#alexscaves:enchantable/totem_of_possession` | Restrito ao tag publisher; overrides do pack não verificados |
| `weight` | **10** | Peso declarativo, não chance de sucesso da possessão |
| `max_level` | **3** (I–III) | Máximo de dados; código usa nível lido, não impõe clamp próprio |
| `min_cost` | base **1**, incremento **5** | I=**1**, II=**6**, III=**11** |
| `max_cost` | base **41**, incremento **10** | I=**41**, II=**51**, III=**61** |
| `anvil_cost` | **1** | Custo de anvil declarativo, distinto de desgaste por tick |
| `slots` | `["mainhand"]` | Compatibilidade e transferência reais ficam sob a engine |
| `exclusive_set`/`effects` | Ausentes do recurso | Não prova incompatibilidade ou ausência de outras condições externas |

Não gera uma segunda habilidade. `Rapid Possession` é um modificador numérico consultado durante o uso do **Totem of Possession**, cuja raiz semântica de controle já é catalogada.

## 3. Fórmula nativa e relação com movimento

`TotemOfPossessionItem.onUseTick(Level,LivingEntity,ItemStack,int)` lê o nível da **stack ativa** por `ACCompat.enchantLevel(stack, ACEnchantmentRegistry.RAPID_POSSESSION)` e calcula:

```text
elapsed = 72000 - remainingUseTicks
ramp = (elapsed < 15) ? elapsed / 15F : 1F

viewRayDistance = 32F * ramp
movementFactor = 1.25F + 0.35F * rapidPossessionLevel

Mob navigation: moveTo(destination, ramp * movementFactor)
Non-Mob velocity: oldVelocity * 0.8F + direction * (0.15F * movementFactor)
```

Esse texto é **pseudocódigo explicativo** para leitura técnica; não é código copiado, integrado ou usado como novo executor. O JAR exato confirma a sequência de instruções JVM `onUseTick @318–334`: `ldc 1.25f`, `ldc 0.35f`, `getstatic RAPID_POSSESSION`, `ACCompat.enchantLevel`, `i2f`, `fmul`, `fadd`, `fstore 10`. O raycast `32F×ramp` tem outro valor em `@310–316`; nenhum dos dois se confunde com a distância usuário↔alvo vinculado ou a geometria da checagem de olhar.

| Nível lido | Fator `1,25+0,35L` | Mob: speed solicitada em `ramp=1` | Parcela não-Mob `0,15×fator` |
|---:|---:|---:|---:|
| 0 — ausente | 1,25 | 1,25 | 0,1875 |
| I | 1,60 | 1,60 | 0,2400 |
| II | 1,95 | 1,95 | 0,2925 |
| III | 2,30 | 2,30 | 0,3450 |

**Unidades e limites:** `navigation.moveTo` recebe um parâmetro de velocidade do pathfinding; **não** é deslocamento físico garantido de 1,6–2,3 blocos/tick. Para não-Mobs, `oldVelocity×0,8` mantém inércia e a direção só é normalizada quando o comprimento supera 1; há regras próprias de achatamento Y e degrau vertical `+0,6` para obstáculos no chão. A parcela `0,15×fator` não é velocidade terminal nem distância por tick. O `ramp` multiplica explicitamente a velocidade solicitada aos Mobs e o **alcance do raio de comando**, não a adição na velocidade não-Mob.

A duração da rampa é definida pelo tempo de uso corrente, normalmente até **15 ticks** no caminho descrito. `getUseDuration=72000` é o tempo máximo declarado de uso, não uma garantia de possessão contínua. Níveis acima de III inseridos externamente não recebem limites seguros dessa fórmula por si só.

## 4. Gates, alvo e dano nativo permanecem separados

O ataque corpo a corpo do Totem define uma **vinculação** ao entity UUID quando alvo elegível; a tag de resistência `#alexscaves:resists_totem_of_possession` e o config `totem_of_possession_works_on_players` são filtros próprios. O uso resolve o alvo no `ServerLevel` atual e passa pelo teste angular do olhar e LOS; **Sightless** pode bypassar esse gate, mas Rapid Possession não. Falha do olhar, alvo ausente, vida, deterioração da stack ou config podem impedir ou encerrar o controle. `ControllingEntityID`, `BoundEntityUUID` e `BoundEntityTag` são estados diferentes.

O destino é determinado a partir do **raio de visão do jogador** com `ProjectileUtil.getHitResultOnViewVector`, excluindo a entidade controlada e considerando candidatos projectile-hittable. A regra de comando não fixa, por si só, um alcance máximo entre usuário e entidade já vinculada. `Rapid Possession` não altera o predicado de mira nem o tag de resistência, e não adiciona alvos.

Durante o uso, o servidor procura LivingEntities na AABB da entidade controlada inflada por **3 blocos** e filtra usuário, controlado, aliados e passageiros incompatíveis. Para um Mob controlado ajusta `target`/`lastHurtByMob`; para Player controlado invoca `attack` e reinicia o contador de ataque. Não há **dano extra por nível de Rapid Possession**, ampliação dessa AABB ou garantia de hit. A seleção e os ataques podem abranger mais de um candidato dentro do loop nativo; não criar segundo processamento.

`Astral Transferring` (transferência de vínculo a cada quatro ticks elegíveis), `Sightless` (gate de olhar/glow) e `Detonating Death` (explosão em condições de término) são outros encantamentos do mesmo item, com propriedades separadas. Rapid Possession não substitui seus gatilhos nem transforma transferência ou detonação em nova raiz mágica.

## 5. Custos, persistência e autoridade

A stack declara **1000 de durabilidade**. O caminho auditado escreve `setDamageValue` a cada uso-tick par **no cliente**, salvo jogador criativo; não demonstra desgaste equivalente server-side, nem aplicação de Unbreaking. Quando `damage >= maxDamage`, o provider encerra/consome a stack no caminho de término. O custo efetivo no multiplayer deve ser observado com rastreamento do componente de dano no cliente e servidor; o sync examinado manipula `CUSTOM_DATA`, não o componente de dano. `anvil_cost=1` não é custo por ação, e nenhum custo separado de mana/stamina/cooldown é criado pelo enchantment.

`UpdateItemTagMessage.handle` resolve entidade/mão por ID e tipo do item e aplica custom data, sem prova de vínculo entre sender e entidade ou reconstrução segura de `UseTime`, dano e autorização. Não usar essa mensagem para alterar nível, raio, velocidade ou vínculo como uma perk. A marca persistente `TotemPossessed` pode sobreviver a release, rebind ou troca de controlador, e o armazenamento da stack não comprova ownership exclusivo; reload, troca de dimensão, PvP/claims e múltiplos controladores exigem QA. `PossessionKeyMessage` pertence a outros consumidores de câmera; não é o canal de controle/movimento do Totem.

Para futuras perks, os campos **observados, não homologados** incluem `movementFactor`, `ramp`, `mobNavigationSpeed`, `nonMobVelocityDelta`, `viewRayCommandDistance`, `bindingUuid`, `controllerId`, `lookAndLosGate`, `targetAabb`, `nativeAttackDispatch`, `wearPerTick`, `clientServerState`, `saveReload`, `explosionOnce` e `ownershipValidation`. Toda mutação exige um seam real do provider, segurança server-authoritative, caps, manutenção de um único pipeline de binding/ataque/custo e respeito a proteções PvP/claims. A velocidade da entidade não pode ser interpretada como valor de Mastery ou reach disponível sem API real.

## 6. Evidência e próximos testes

- [Selo de Rapid Possession](../EXACT-RAPID-POSSESSION-CONTRACT-1.0.10.json) e [instruções de reprodução](../EXACT-RAPID-POSSESSION-CONTRACT-1.0.10.md).
- [Contrato binário anterior do Totem](../EXACT-TECHNICAL-CONTRACTS-1.0.10.json), [ação original detalhada](../actions/totem-possession-remote-control.md), [sonda de recurso/bytecode](../../../../../docs/qa/alexscaves_1010_rapid_possession_probe.py), [regressões individuais](../../../../../docs/qa/alexscaves_1010_rapid_possession_cards_test.py).

Testes físicos ainda exigidos: Mobs com navegação ativa versus Player/entidades não-Mob; trajetórias, obstáculos e rampa com níveis 0/I/II/III; alcance de raio, visão/LOS/Sightless, alvo transferido, jogadores com config true/false, server/client de desgaste, desconexão/dimensão/reload, duplo controlador e autorização da rede, claims/PvP e custos sob outros mods. A ficha não afirma aprovação desses testes.

**Conclusão limitada:** `STATIC_TECHNICAL_CATALOG_ONLY` / `SHA_EXACT_BINARY_BEHAVIOR`. `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `mutation=NO_MUTATION`, `provider_universe_closed=false`. Nenhuma implementação/runtime Black Arcana ou Stage foi modificada.
