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
| JAR exato | `apprentice_codex-1.0.1.1-mc1.21.1.jar` |
| SHA-256 do JAR | `9C5244E75DBCA95BDAF48A85F0C189F8456149D1220BAD5FF339A86BCE04AC86` |
| SHA-1 do JAR | `A3F9C73EBD77D15B7E77AE14F4D0F695FEC3B7CF` |
| Ambiente | Minecraft 1.21.1 · NeoForge 21.1.250 · Java 21 (JDK 21.0.12 na inspeção) |
| Classe de implementação | `jp.aquafactory.apprenticecodex.spell.mistform.MistForm` |
| Evidência compartilhada | [`EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md`](../EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md) |

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
| Colisão — mixin | `jp.aquafactory.apprenticecodex.mixin.BlockStateBaseMistFormCollisionMixin` → `BlockBehaviour$BlockStateBase.getCollisionShape(...)`, `@Inject(RETURN, cancellable=true)` |
| Movimento — mixin | `jp.aquafactory.apprenticecodex.mixin.EntityMistFormMovementRestrictionMixin` → `Entity.makeStuckInBlock`, `@Inject(HEAD, cancellable=true)` |
| Pulo/fluido — mixin | `jp.aquafactory.apprenticecodex.mixin.LivingEntityMistFormMixin` → `LivingEntity.getJumpBoostPower` (`RETURN`) e `LivingEntity.canStandOnFluid` (`HEAD`), ambos `cancellable=true` |
| Config | `jp.aquafactory.apprenticecodex.config.spell.MistFormServerConfig` (`passableBlockDenylist`, `isPassableBlockDenied`, `setPassableBlockDenylistForGameTest`) |
| Registro de mixins | `mixins.apprenticecodex.json` (linhas 41, 44, 67; `injectors.defaultRequire=1`) |
| Render | `MistFormClientRenderEvent.onRenderPlayerPre(Pre)` |
| Supressão de awareness | `SummonedFirearmTools.suppressNearbyAwareness(level, entity, entity, 32.0)` |

Descritores e offsets JVM foram reconsultados no JAR 1.0.1.1: saída `scratch/javap1011_legacy.txt` (`javap -classpath <JAR> -p -s -c`, `EXIT=0`, 233.376 bytes, SHA-256 `F59E0944BA6C04BF5A2B3A28145C9403B225EDF7EEC8425D4A0B6E189F63CCF3`) e anotações/constantes em `scratch/javap1011_v.txt` (`EXIT=0`), não publicadas integralmente.

## 3. Casting / execução

1. `CastType.LONG` e `castTime=30` ticks; o Iron's owned a janela de canalização,mana e cooldown.
2. `onCast` executa apenas fora do cliente: adiciona `EffectRegistry.MIST_FORM` com duração calculada, amplifier `0`, `ambient=false`, `visible=false`, `showIcon=true`.
3. Imediatamente chama `SummonedFirearmTools.suppressNearbyAwareness` com raio `32.0` blocos. O efeito dessa supressão é provider-owned e não foi observado em execução.
4. `super.onCast(...)` completa o fluxo do host.
5. Som de início: `SoundRegistry.MIST_FORM_START`; fim: `SoundRegistry.MIST_FORM_FINISHED`; animação inicial: `SpellAnimations.CAST_KNEELING_PRAYER`.

Guardas e custos são owned pelo Iron's. No JAR físico do host, `AbstractSpell.getManaCost(int)` (`(I)I`, offsets 0–29) calcula `(baseManaCost + manaCostPerLevel*(level-1)) * MANA_MULTIPLIER` e trunca com `d2i`; `getSpellCooldown()` (`()I`, offsets 0–18) calcula `COOLDOWN_IN_SECONDS * 20.0d` e trunca com `d2i`; `getCastTime(int)` (`(I)I`, offsets 0–16) retorna o campo `castTime` porque o tipo é `CastType.LONG` — `30` ticks. `getSpellPower(int,Entity)` (`(ILnet/minecraft/world/entity/Entity;)F`, offsets 0–79) multiplica ainda por `AttributeRegistry.SPELL_POWER`, `SchoolType.getPowerFor(LivingEntity)` e `POWER_MULTIPLIER`; `getLevelFor(int,LivingEntity)` (`(ILnet/minecraft/world/entity/LivingEntity;)I`, offsets 0–64) aplica Curios e `ModifySpellLevelEvent`. Assim, `150`, `30`, `50`, `15`, `30.0` e `castTime=30` são coeficientes declarados pelo Apprentice Codex; mana, cooldown, power, duração e nível efetivos dependem da config instalada do Iron's, atributos e eventos, **NÃO VERIFICADOS**. Ver âncoras em [`EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md`](../EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md).

## 4. Targeting / geometria

| Propriedade | Valor e consumidor |
|---|---|
| Alvo | O próprio caster; não há seleção de entidade. |
| Área de supressão | Raio `32.0` blocos em `suppressNearbyAwareness`. |
| Nenhuma AOE ofensiva | `N/A`: a magia não calcula dano nem caixa de ataque. |
| Colisão | `MistFormCollisionHelper` exige `Player` com efeito, bloco em `TagRegistry.Blocks.MIST_FORM_PASSABLE` e ausência do bloco na denylist de servidor. |
| Movimento | `MistFormMovementRestrictionHelper` exige `Player` com efeito e bloco em `TagRegistry.Blocks.MIST_FORM_IGNORES_MOVEMENT_RESTRICTION`. |
| Callsite de colisão | `BlockStateBaseMistFormCollisionMixin.apprenticecodex$removeMistFormPassableCollision(...)`, offsets 0–33: se a forma retornada não estiver vazia, chama `asState()` e `MistFormCollisionHelper.canPassThrough(...)`; quando verdadeiro, `setReturnValue(Shapes.empty())`. |
| Callsite de movimento | `EntityMistFormMovementRestrictionMixin.apprenticecodex$ignoreMistFormMovementRestriction(BlockState,Vec3,CallbackInfo)`, offsets 0–15: chama `MistFormMovementRestrictionHelper.ignoresMovementRestriction(...)` e, quando verdadeiro, `CallbackInfo.cancel()`. |
| Bônus de pulo | `LivingEntityMistFormMixin.apprenticecodex$addMistFormJumpPower(CallbackInfoReturnable<Float>)`, offsets 0–44: exige `LivingEntity` com `EffectRegistry.MIST_FORM`, lê o retorno, soma literal `0.3f` e chama `setReturnValue(...)`. |

## 5. Resultado

- `MistFormEffect` é `MobEffectCategory.BENEFICIAL`, cor `16055551`, e registra quatro modificadores:
  - `Attributes.MOVEMENT_SPEED`, ID `apprenticecodex:mist_form_movement_speed`, `Operation.ADD_MULTIPLIED_TOTAL`, `+0.2`;
  - `Attributes.STEP_HEIGHT`, ID `apprenticecodex:mist_form_step_height`, `Operation.ADD_VALUE`, `+0.5`;
  - `AttributeRegistry.FIRE_MAGIC_RESIST`, ID `apprenticecodex:mist_form_fire_resist`, `Operation.ADD_VALUE`, `-1.0`;
  - `AttributeRegistry.HOLY_MAGIC_RESIST`, ID `apprenticecodex:mist_form_holy_resist`, `Operation.ADD_VALUE`, `-1.0`.
- `JUMP_POWER_ADDITION = 0.3F` é declarado como campo `float` na fonte de apoio; o `javap` confirma a existência do campo. Nenhum `addAttributeModifier` foi encontrado no construtor. O bônus efetivo de `+0.3` decorre do literal `0.3f` somado no callback `apprenticecodex$addMistFormJumpPower`; não foi demonstrada leitura do campo nas classes inspecionadas. Registrado como declaração auxiliar, não como consumer verificado.
- Slow fall: `PlayerTickEvent.Pre`, quando não `onGround`, não voando, não elytra e não passenger; se `movement.y < -0.08`, vira `-0.08`; `fallDistance=0`.
- Fluid standing: o gancho é `LivingEntityMistFormMixin.apprenticecodex$standOnFluidInMistForm(FluidState,CallbackInfoReturnable<Boolean>)`, offsets 0–48, injetado em `canStandOnFluid` no `HEAD`. O callback ignora fluido vazio; para `Player`, aceita `MistFormEvents.canStandOnFluid` ou `LongStrideFluidMovement.canStandOnFluid` e força retorno `true`. O cálculo provider-owned retorna falso com shift, spectator, passenger, sem efeito ou ao tocar fluido; nesse último caso desativa por `20` ticks. Com suporte encontrado, alinha `player.y` a `surfaceY + 0.02` dentro dos limites `-0.35`/`+0.65`, zera movimento vertical descendente, marca `onGround=true` e zera `fallDistance`. A varredura usa `FLUID_SCAN_BELOW=0.18`, `FLUID_SCAN_ABOVE=0.08`, `FLUID_SURFACE_EPSILON=0.02`.
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
| Denylist de phasing | `mistFormPassableBlockDenylist`, default lista vazia; aceita IDs de bloco e entradas `#tag`; consultada por `ApprenticeCodexServerConfig.isMistFormPassableBlockDenied(BlockState)` | config de servidor; valor instalado **NÃO VERIFICADO** |
| Bônus de pulo | `+0.3` | `float`; literal no callback do mixin, não modificação de atributo |
| Cooldown / cast time | `30.0` s / `30` ticks | `DefaultConfig` e campo |

## 7. Possibilidades de perks

- **A — atributo nativo:** spell power, mana, cast time e cooldown via `AbstractSpell`; não é hook de mutação demonstrado.
- **B — evento/callback verificado:** `PlayerTickEvent.Pre` e `LivingDamageEvent.Post` são observadores do provider; os três mixins são interceptações provider-owned do vanilla para o jogador com o efeito. Não foi demonstrado que uma perk externa possa alterar duração, slow fall, colisão, movimento, fluid standing ou pulo sem substituir o listener/mixin com contrato de owner. **NO_MUTATION / fail-closed**.
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
- ✅ Callsites de `MistFormCollisionHelper` e `MistFormMovementRestrictionHelper` e bônus de pulo localizados nos três mixins registrados no JAR 1.0.1.1; `JUMP_POWER_ADDITION` permanece como declaração sem consumer demonstrado.
- ⚠️ Configuração efetiva do pack (denylist, multiplicadores) não lida; **NÃO VERIFICADO**.
- ⚠️ `physical_qa=NOT_TESTED`: sem cliente, servidor, Survival, PvP ou modpack real.
- ⚠️ Universo integral do provider não encerrado: recorte observado de 15 fichas.

## Localizadores para Codex — resumo operacional

- Não presumir que helper, atributo ou evento seja ponto mutável por perk; todos são provider-owned e fail-closed.
- Para qualquer bridge, preservar a regra "atacar remove o efeito" e não duplicar custo, cooldown ou proc por tick.
- Consultar [`EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md`](../EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md) para hashes, comandos e limites da prova.
