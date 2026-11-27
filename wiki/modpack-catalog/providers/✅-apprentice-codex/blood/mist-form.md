# Mist Form

**Estado do contrato:** ✅ `COMPLETE_PERK_READY` — `STATIC_TECHNICAL_CATALOG_ONLY` · `SHA_EXACT_BINARY_BEHAVIOR` · `mutating_hook=NOT_VERIFIED` · `physical_qa=NOT_TESTED`.

> O ✅ cobre exclusivamente a documentação estática SHA-exata deste objeto. Não homologa hook mutador, execução no pack, configuração efetiva nem universo integral do provider.

## 1. Identidade e proveniência

| Campo | Valor verificado |
|---|---|
| Provider | Apprentice's Codex |
| Mod ID | `apprenticecodex` |
| Nome de exibição | Mist Form (nome funcional, não traduzido) |
| Registry ID | `apprenticecodex:mist_form` |
| Host | Iron's Spells 'n Spellbooks (`AbstractSpell`) |
| Escola | `SchoolRegistry.BLOOD_RESOURCE` (Blood) |
| Raridade mínima | `SpellRarity.EPIC` |
| Níveis | 1–3 (`DefaultConfig.setMaxLevel(3)`) |
| Tipo de cast | `CastType.LONG` |
| Cast time | `30` ticks |
| Cooldown declarado | `30.0` s |
| Recurso | Mana do Iron's (`baseManaCost=150`, `manaCostPerLevel=30`) |
| JAR exato | `apprentice_codex-1.0.1-mc1.21.1.jar` |
| SHA-256 do JAR | `47018AD8C6C6187B17C6BFC4D4F2FFF44EA2ED560719EBB6566A750715757947` |
| SHA-1 do JAR | `3077999F51299A53A0AF1B8A1AEC22F4099E36A3` |
| Ambiente | Minecraft 1.21.1 · NeoForge 21.1.250 · Java 21 (JDK 21.0.12 na inspeção) |
| Classe de implementação | `jp.aquafactory.apprenticecodex.spell.mistform.MistForm` |
| Evidência compartilhada | [`EXACT-TECHNICAL-CONTRACTS-1.0.1.md`](../EXACT-TECHNICAL-CONTRACTS-1.0.1.md) |

## 2. Localizadores para o Codex

| Elemento | Localizador |
|---|---|
| Registro | `SpellRegistry.reg("mist_form", MistForm::new)` |
| Config | `MistForm.config`: `EPIC`, `BLOOD_RESOURCE`, `maxLevel=3`, `cooldownSeconds=30.0` |
| Coeficientes | `MistForm.<init>()`: `baseSpellPower=50`, `spellPowerPerLevel=15`, `baseManaCost=150`, `manaCostPerLevel=30`, `castTime=30` |
| Duração | `MistForm.getDuration(int,LivingEntity)` |
| Aplicação | `MistForm.onCast(...)` |
| Efeito | `jp.aquafactory.apprenticecodex.effect.MistFormEffect` |
| Tick do jogador | `jp.aquafactory.apprenticecodex.spell.mistform.MistFormEvents.onPlayerTick(Pre)` |
| Quebra por ataque | `MistFormEvents.onLivingDamage(Post)` |
| Pass-through | `MistFormCollisionHelper.canPassThrough(BlockState,CollisionContext)` |
| Restrição de movimento | `MistFormMovementRestrictionHelper.ignoresMovementRestriction(Entity,BlockState)` |
| Render | `MistFormClientRenderEvent.onRenderPlayerPre(Pre)` |
| Supressão de awareness | `SummonedFirearmTools.suppressNearbyAwareness(level, entity, entity, 32.0)` |

Descriptors e offsets JVM estão em `scratch/javap_check.txt` (`javap -p -s -c`, `EXIT=0`, 347.597 bytes), não publicados integralmente.

## 3. Casting / execução

1. `CastType.LONG` e `castTime=30` ticks; o Iron's owned a janela de canalização,mana e cooldown.
2. `onCast` executa apenas fora do cliente: adiciona `EffectRegistry.MIST_FORM` com duração calculada, amplifier `0`, `ambient=false`, `visible=false`, `showIcon=true`.
3. Imediatamente chama `SummonedFirearmTools.suppressNearbyAwareness` com raio `32.0` blocos. O efeito dessa supressão é provider-owned e não foi observado em execução.
4. `super.onCast(...)` completa o fluxo do host.
5. Som de início: `SoundRegistry.MIST_FORM_START`; fim: `SoundRegistry.MIST_FORM_FINISHED`; animação inicial: `SpellAnimations.CAST_KNEELING_PRAYER`.

## 4. Targeting / geometria

| Propriedade | Valor e consumidor |
|---|---|
| Alvo | O próprio caster; não há seleção de entidade. |
| Área de supressão | Raio `32.0` blocos em `suppressNearbyAwareness`. |
| Nenhuma AOE ofensiva | `N/A`: a magia não calcula dano nem caixa de ataque. |
| Colisão | `MistFormCollisionHelper` exige `Player` com efeito, bloco em `TagRegistry.Blocks.MIST_FORM_PASSABLE` e ausência do bloco na denylist de servidor. |
| Movimento | `MistFormMovementRestrictionHelper` exige `Player` com efeito e bloco em `TagRegistry.Blocks.MIST_FORM_IGNORES_MOVEMENT_RESTRICTION`. |
| Alcance de colisão/movimento | NÃO VERIFICADO: os dois helpers existem, mas nenhum callsite foi demonstrado no escopo decompilado examinado. Não promover como hook. |

## 5. Resultado

- `MistFormEffect` é `MobEffectCategory.BENEFICIAL`, cor `16055551`, e registra quatro modificadores:
  - `Attributes.MOVEMENT_SPEED`, ID `apprenticecodex:mist_form_movement_speed`, `Operation.ADD_MULTIPLIED_TOTAL`, `+0.2`;
  - `Attributes.STEP_HEIGHT`, ID `apprenticecodex:mist_form_step_height`, `Operation.ADD_VALUE`, `+0.5`;
  - `AttributeRegistry.FIRE_MAGIC_RESIST`, ID `apprenticecodex:mist_form_fire_resist`, `Operation.ADD_VALUE`, `-1.0`;
  - `AttributeRegistry.HOLY_MAGIC_RESIST`, ID `apprenticecodex:mist_form_holy_resist`, `Operation.ADD_VALUE`, `-1.0`.
- `JUMP_POWER_ADDITION = 0.3F` é declarado, mas nenhum `addAttributeModifier` correspondente foi encontrado no construtor: **NÃO VERIFICADO** como consumer.
- Slow fall: `PlayerTickEvent.Pre`, quando não `onGround`, não voando, não elytra e não passenger; se `movement.y < -0.08`, vira `-0.08`; `fallDistance=0`.
- Fluid standing: `canStandOnFluid` retorna falso com shift, spectator, passenger, sem efeito ou ao tocar fluido; nesse último caso desativa por `20` ticks. Com suporte encontrado, alinha `player.y` a `surfaceY + 0.02` dentro dos limites `-0.35`/`+0.65`, zera movimento vertical descendente, marca `onGround=true` e zera `fallDistance`. A varredura usa `FLUID_SCAN_BELOW=0.18`, `FLUID_SCAN_ABOVE=0.08`, `FLUID_SURFACE_EPSILON=0.02`.
- Partículas: `DustParticleOptions(0.88, 0.98, 1.0, 0.85)`, duas por tick par (`tickCount % 2 == 0`) no `ServerLevel`.
- Render: `MistFormClientRenderEvent` cancela `RenderPlayerEvent.Pre` para jogadores com o efeito.
- Quebra: `LivingDamageEvent.Post` com `EventPriority.LOWEST`; se `newDamage > 0`, fonte for `LivingEntity` diferente da vítima e atacante tiver o efeito, `attacker.removeEffect(MIST_FORM)`.

## 6. Scaling e caps

| Parâmetro | Fórmula literal | Unidade / ownership |
|---|---|---|
| Spell power | `50 + 15*(level-1)` conforme `AbstractSpell` | provider host |
| Mana | `150 + 30*(level-1)` | Iron's mana; default declarado |
| Duração | `Math.round(200 * spellPower / 100)` | ticks; arredondamento `Math.round` |
| Movement speed | `+0.2` `ADD_MULTIPLIED_TOTAL` | multiplicador total aditivo |
| Step height | `+0.5` `ADD_VALUE` | blocos |
| Resistências | `-1.0` `ADD_VALUE` para Fogo e Holy | attribute do Iron's |
| Queda | clamp em `-0.08` | blocos/tick |
| Denylist de phasing | `mistFormPassableBlockDenylist`, default lista vazia | config de servidor; valor instalado **NÃO VERIFICADO** |
| Cooldown / cast time | `30.0` s / `30` ticks | `DefaultConfig` e campo |

## 7. Possibilidades de perks

- **A — atributo nativo:** spell power, mana, cast time e cooldown via `AbstractSpell`; não é hook de mutação demonstrado.
- **B — evento/callback verificado:** `PlayerTickEvent.Pre` e `LivingDamageEvent.Post` são observadores do provider. Não foi demonstrado que uma perk possa alterar duração, slow fall ou quebra sem substituir o listener. **NO_MUTATION / fail-closed**.
- **C — adapter condicionado:** mudar a lista de blocos passáveis ou os modificadores exigiria holder de efeito/config com contrato explícito. **CONDICIONADO**.
- **D — sem hook demonstrado:** transformar a imunidade em AOE ofensiva, estender duração por hit ou remover a quebra por ataque não tem API/mixin seguro comprovado neste escopo.
- `mutating_hook = NOT_VERIFIED`.

## 8. Causalidade

`um cast canalizado → efeito no caster + supressão de awareness → ticks aplicam mobilidade/slow fall/fluid standing → dano recebido pelo caster como atacante remove o efeito`.

A remoção por ataque é provider-owned e não configura nova intenção. Black Arcana não deve awardar mastery por tick de efeito nem tratar phasing como dano ou cast separado.

## 9. Concepção de nova magia

Assinatura ocupada: "canalização que transforma o caster em névoa, altera mobilidade/resistências e termina ao atacar". Uma magia original Black Arcana precisaria de semântica materialmente distinta (por exemplo, imunidade sensorial sem phasing, ou transformação que persiste após ataque) para não duplicar esta identidade. Nenhuma implementação foi realizada.

## 10. Verificação e pendências

- ✅ Identidade, versão e hash do JAR; registro e classe; coeficientes; duração; atributos; tick; quebra; limites de validação.
- ⚠️ Configuraçãoefetiva do pack (denylist, multiplicadores) não lida.
- ⚠️ `physical_qa=NOT_TESTED`: sem cliente, servidor, Survival, PvP ou modpack real.
- ⚠️ Callsites de `MistFormCollisionHelper` e `MistFormMovementRestrictionHelper` não demonstrados; consumidor de `JUMP_POWER_ADDITION` não localizado.
- ⚠️ Universo integral do provider não encerrado: recorte observado de 5 fichas.

## Localizadores para Codex — resumo operacional

- Não presumir que helper, atributo ou evento seja ponto mutável por perk; todos são provider-owned e fail-closed.
- Para qualquer bridge, preservar a regra "atacar remove o efeito" e não duplicar custo, cooldown ou proc por tick.
- Consultar [`EXACT-TECHNICAL-CONTRACTS-1.0.1.md`](../EXACT-TECHNICAL-CONTRACTS-1.0.1.md) para hashes, comandos e limites da prova.
