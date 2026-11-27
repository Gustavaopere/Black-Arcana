# Long Stride

**Estado do contrato:** ✅ `COMPLETE_PERK_READY` — `STATIC_TECHNICAL_CATALOG_ONLY` · `SHA_EXACT_BINARY_BEHAVIOR` · `mutating_hook=NOT_VERIFIED` · `physical_qa=NOT_TESTED`.

> O ✅ cobre exclusivamente a documentação estática SHA-exata deste objeto. Não homologa hook mutador, execução no pack, configuração efetiva, universo integral do provider nem QA físico.

## 1. Identidade e proveniência

| Campo | Valor verificado |
|---|---|
| Provider | Apprentice's Codex |
| Mod ID | `apprenticecodex` |
| Registry ID | `apprenticecodex:long_stride` |
| Host | Iron's Spells 'n Spellbooks (`AbstractSpell`) |
| Escola | `SchoolRegistry.ENDER_RESOURCE` (Ender) |
| Raridade mínima | `SpellRarity.RARE` |
| Níveis | 1 (`DefaultConfig.setMaxLevel(1)`) |
| Tipo de cast | `CastType.CONTINUOUS` |
| Cooldown declarado | `12.0` s |
| Recurso | Mana do Iron's (`baseManaCost=12`, `manaCostPerLevel=-1`, irrelevante no range de um nível) |
| Crafting / looting | `setAllowCrafting(false)` / `allowLooting()=false` |
| JAR exato | `apprentice_codex-1.0.1.1-mc1.21.1.jar` |
| SHA-256 do JAR | `9C5244E75DBCA95BDAF48A85F0C189F8456149D1220BAD5FF339A86BCE04AC86` |
| SHA-1 do JAR | `A3F9C73EBD77D15B7E77AE14F4D0F695FEC3B7CF` |
| Ambiente | Minecraft 1.21.1 · NeoForge · Java 21 (JDK 21.0.12 na inspeção) |
| Classe de implementação | `jp.aquafactory.apprenticecodex.spell.longstride.LongStride` |
| Evidência compartilhada | [`EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md`](../EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md) |

As versões 0.9.7.1 e 1.0.1 permanecem como histórico; nenhum valor foi reaproveitado sem confirmação no artefato físico 1.0.1.1.

## 2. Localizadores para o Codex

| Elemento | Localizador |
|---|---|
| Registro | `SpellRegistry.reg("long_stride", LongStride::new)` |
| Config | `LongStride.config` (`RARE`, nível 1, cooldown `12.0`, `setAllowCrafting(false)`) |
| Coeficientes | `LongStride.<init>()`: `baseSpellPower=0`, `spellPowerPerLevel=0`, `baseManaCost=12`, `manaCostPerLevel=-1`, `castTime=1200` |
| Cast time efetivo | `LongStride.getEffectiveCastTime(int,LivingEntity)` → `getCastTime(spellLevel)`, ignora redução de cast time |
| Amplificador | `LongStride.getMobEffectAmplifier(int)` → `spellLevel - 1` |
| Bônus exibido | `LongStride.getMoveSpeedBonusPercent(int)` → `10 + round(5 * amplifier)` (nível 1 = `10%`) |
| Refresh do efeito | `LongStride.onServerCastTick(...)` reaplica `EffectRegistry.LONG_STRIDE_MOBILITY` com duração `EFFECT_REFRESH_TICKS=5` |
| Efeito | `jp.aquafactory.apprenticecodex.effect.LongStrideMobility` (`CASTING_MOVE_SPEED_BONUS=0.8`, `STEP_HEIGHT_ADDITION=1.1`) |
| Base do efeito | `jp.aquafactory.apprenticecodex.effect.DynamicCastingMobilityEffect` (`getTargetCastingMoveSpeedBonus=0.8`, cap compartilhado em `CastingMoveSpeedAdjustment.MAX_CASTING_MOVE_SPEED_BONUS=0.8`) |
| Movimento em fluido | `jp.aquafactory.apprenticecodex.spell.longstride.LongStrideFluidMovement` (`onPlayerTick`, `apply`, `canStandOnFluid`, `findFluidSupport`) |

Bytecode: `scratch/javap1011_ender10.txt` (`javap -classpath <JAR> -p -s -c`, `EXIT=0`, SHA-256 `0095E23B21918E38B4BD7D6C47DA8C3503753F0F988C00AB04A786060E2C50E5`); decompilação: `scratch/ender10_sources.txt` (SHA-256 `F3953EB8FCFB793EC501694E054E3C3CBE187E557B09B6CF158828692A97A645`).

## 3. Casting / execução

1. `AbstractSpell` resolve mana/cooldown/nível; `castTime=1200` ticks (60 s) e `CastType.CONTINUOUS`.
2. `getEffectiveCastTime` retorna `getCastTime(spellLevel)` — reduções de cast time do host não encurtam este canal.
3. A cada tick de canal no servidor, `onServerCastTick` reaplica `MobEffectInstance(EffectRegistry.LONG_STRIDE_MOBILITY, 5, spellLevel-1, false, true, true)`.
4. `LongStrideMobility` adiciona dois modificadores: `MOVEMENT_SPEED` com `Operation.ADD_MULTIPLIED_TOTAL` e valor `0.1 + 0.05*amplifier` (0.10 no nível 1), e `STEP_HEIGHT` com `Operation.ADD_VALUE` e valor constante `1.1`.
5. `DynamicCastingMobilityEffect` sincroniza contribuições ao atributo `AttributeRegistry.CASTING_MOVESPEED` com `Operation.ADD_VALUE`, alvo `0.8` por efeito, limitado por `CastingMoveSpeedAdjustment.computeSharedBonus` a um teto compartilhado de `0.8` descontado de bônus externo. O `0.8` é uma grandeza distinta do `10%` exibido pela spell.

Os canais de mana/cooldown/cast time/spell power são herdados; valores instalados **NÃO VERIFICADOS**.

## 4. Targeting / geometria

| Propriedade | Valor e consumidor |
|---|---|
| Alvo | Nenhum: efeito self aplicado ao casador enquanto canaliza. |
| Duração do efeito | `5` ticks por refresh, renovada a cada `onServerCastTick`. |
| Bônus de velocidade | `0.1 + 0.05*amplifier` (`ADD_MULTIPLIED_TOTAL`), amplificador `spellLevel-1`. |
| Step height | `+1.1` (`ADD_VALUE`) constante. |
| Bônus de cast move speed | `0.8` alvo, teto compartilhado `0.8` entre efeitos `DynamicCastingMobilityEffect` ativos. |
| Scan de superfície | `FLUID_SCAN_BELOW=0.18`, `FLUID_SCAN_ABOVE=0.08`, `FLUID_SURFACE_EPSILON=0.02`, snap `0.35` abaixo / `0.65` acima da superfície alvo. |

## 5. Resultado (movimento em fluido)

`LongStrideFluidMovement.onPlayerTick` (`PlayerTickEvent.Pre`) chama `apply`. `canControlFluidMovement` exige efeito ativo, não espectador, não passageiro, sem `abilities.flying` e sem `fallFlying`.

- Em fluido sem colisão sólida, `applyBuoyancy` aplica `vertical = min(0.1, movement.y + 0.03)`, zera `onGround` e `fallDistance`.
- Fora do contato com fluido caminhável, `applyFluidStanding` usa `findFluidSupport` (maior `surfaceY` na faixa `minY-0.18` a `minY+0.08`, com inset X/Z `0.05`), define `targetY = surfaceY + 0.02` e, dentro dos limites de snap, repousiciona o jogador, zera velocidade vertical e marca `onGround=true`.
- `hasSolidCollision` trata estados `WATERLOGGED=true` como colisão sólida, além de shapes de colisão não vazias.
- `canStandOnFluid` exige fluido não vazio, controle habilitado e ausência de contato com fluido caminhável.

Esses movimentos são provider-owned; não são teleportes nem casts adicionais.

## 6. Scaling e caps

| Parâmetro | Fórmula literal | Unidade / ownership |
|---|---|---|
| Spell power | `0 + 0*(level-1)` | sem escalonamento de poder |
| Mana | `12 - 1*(level-1)` | nível único, efetivo `12` |
| Cast time | `1200` ticks | fixo, ignora redução |
| Refresh | `5` ticks | duração por reaplicação do efeito |
| Bônus de movimento | `0.1 + 0.05*amplifier` | multiplicador total |
| Step height | `1.1` | aditivo |
| Cap de cast move speed | `0.8` | teto compartilhado |

## 7. Possibilidades de perks

- **A — atributo nativo:** `MOVEMENT_SPEED`, `STEP_HEIGHT` e `CASTING_MOVESPEED` são atributos reais alterados pelo efeito; porém o efeito é provider-owned e re aplicado a cada tick.
- **B — evento verificado:** `PlayerTickEvent.Pre` e `onServerCastTick` são pontos de execução do provider, não hooks de mutação segura demonstrados. `getEffectiveCastTime` ignora reduções externas por decisão explícita do código.
- **C — adapter condicionado:** alterar o bônus exigiria substituir `LongStrideMobility` ou os modificadores com contrato de limpeza e sincronização de atributos. **CONDICIONADO**.
- **D — sem hook demonstrado:** não há API segura comprovada para mudar o refresh, o bônus de cast speed ou o snap de fluido sem reaplicação conflitante. **NO_MUTATION / fail-closed**.
- `mutating_hook = NOT_VERIFIED`.

## 8. Causalidade

`um cast contínuo → refresh do efeito a cada 5 ticks → modificadores de atributo + movimento em fluido`.

O refresh é manutenção de uma única sessão. Black Arcana/RPG não devem gerar Mastery por tick, nem duplicar mana, movimento ou controle de fluido.

## 9. Concepção de nova magia

Assinatura ocupada: "canalização de mobilidade de exploração ligada a item, com travessia de fluidos". Uma magia original precisaria de semântica distinta (por exemplo, controle de fluido sem bônus de cast speed compartilhado) para não duplicar a identidade. Nenhuma implementação foi realizada.

## 10. Verificação e pendências

- ✅ Identidade/hash, coeficientes, cast time efetivo, refresh, modificadores de atributo e constantes de movimento em fluido confirmados no bytecode 1.0.1.1.
- ⚠️ Configuração efetiva e multiplicadores instalados não lidos.
- ⚠️ `physical_qa=NOT_TESTED`: sem cliente/servidor Survival, água/lava rasa, waterlogged, chunks, relogin ou PvP.
- ⚠️ AquisiçãoItem-only (crafting/looting desligados) não implica disponibilidade de scroll.
- ⚠️ Universo integral do provider não encerrado.

## Localizadores para Codex — resumo operacional

- Os `10%` exibidos e o `0.8` de `CASTING_MOVE_SPEED_BONUS` são grandezas distintas; não confundir.
- `getEffectiveCastTime` ignora redução de cast time por decisão do código, não por config lida.
- Nenhum ponto de mutação segura demonstrado; manter fail-closed.
- Consultar [`EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md`](../EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md).
