# Mantis Leap

**Estado do contrato:** ✅ `COMPLETE_PERK_READY` — `STATIC_TECHNICAL_CATALOG_ONLY` · `SHA_EXACT_BINARY_BEHAVIOR` · `mutating_hook=NOT_VERIFIED` · `physical_qa=NOT_TESTED`.

> O ✅ cobre exclusivamente a documentação estática SHA-exata deste objeto. Não homologa hook mutador, execução no pack, configuração efetiva, universo integral do provider nem QA físico.

## 1. Identidade e proveniência

| Campo | Valor verificado |
|---|---|
| Provider | Apprentice's Codex |
| Mod ID | `apprenticecodex` |
| Registry ID | `apprenticecodex:mantis_leap` |
| Host | Iron's Spells 'n Spellbooks (`AbstractSummonWeaponSpell<MantisLeapBladeEntity>`) |
| Interfaces | `ICastHighlightSpell`, `IMulticastUnsupportedSpell` |
| Escola | `SchoolRegistry.ENDER_RESOURCE` (Ender) |
| Raridade mínima | `SpellRarity.RARE` |
| Níveis | 1–3 (`DefaultConfig.setMaxLevel(3)`) |
| Tipo de cast | `CastType.LONG` |
| Interrompível | `canBeInterrupted(...)=false` |
| Cooldown declarado | `8.0` s |
| Recurso | Mana do Iron's (`baseManaCost=70`, `manaCostPerLevel=15`) |
| JAR exato | `apprentice_codex-1.0.1.1-mc1.21.1.jar` |
| SHA-256 do JAR | `9C5244E75DBCA95BDAF48A85F0C189F8456149D1220BAD5FF339A86BCE04AC86` |
| SHA-1 do JAR | `A3F9C73EBD77D15B7E77AE14F4D0F695FEC3B7CF` |
| Ambiente | Minecraft 1.21.1 · NeoForge · Java 21 (JDK 21.0.12 na inspeção) |
| Classe de implementação | `jp.aquafactory.apprenticecodex.spell.mantisleap.MantisLeap` |
| Evidência compartilhada | [`EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md`](../EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md) |

As versões 0.9.7.1 e 1.0.1 permanecem como histórico; nenhum valor foi reaproveitado sem confirmação no artefato físico 1.0.1.1.

## 2. Localizadores para o Codex

| Elemento | Localizador |
|---|---|
| Registro | `SpellRegistry.reg("mantis_leap", MantisLeap::new)` |
| Config | `MantisLeap.config` (`RARE`, nível 3, cooldown `8.0`) |
| Coeficientes | `MantisLeap.<init>()`: `baseSpellPower=1200`, `spellPowerPerLevel=400`, `baseManaCost=70`, `manaCostPerLevel=15`, `castTime=25` |
| Constantes | `RAYCAST_WIDTH=1.0`, `TARGET_STOP_DISTANCE=1.0`, `MIN_LEAP_DISTANCE=0.25`, `MIN_LEAP_DURATION_TICKS=10` |
| Dano | `MantisLeap.getDamage(int,LivingEntity)` → `power/100 * damageMultiplier(MANTIS_LEAP)` |
| Alcance | `getRange(int,LivingEntity)` → `min(32, power/100)` |
| Tempo por bloco | `getLeapTicksPerBlock(...)` → `max(0.25, 2.5 - power/800)` |
| Arco | `getLeapArcHeight()` → `1.5` |
| Highlight | `getHighlightEntity(Player,int)` via `RaycastTools.raycastFromEye(..., getRange(...), 1.0, isValidCombatTarget)`, cor `4491519` |
| Destino | `resolveLeapDestination`, `resolveEntityDestination`, `clampDistance` |
| Início do salto | `startLeap(...)`: grava `MANTIS_LEAP_STATE` com `totalTicks`, `elapsedTicks`, start/target, `arcHeight`, `bladeEntityId`, `stagnantTicks`, `noGravityApplied` |
| Interpolação | `calculateEasedPosition` (`easeOutCubic`, arco `4*h*p*(1-p)`) |
| Tick de movimento | `MantisLeapMovementEvent.onPlayerTick(Pre)`, `applyNoGravity`, `calculateStagnantTicks`, `finalizeLeap`, `startPostLeapInvulnerability` |
| Invulnerabilidade | `POST_LEAP_INVULNERABLE_TICKS=20`, `STAGNANT_TICK_LIMIT=4`, `STAGNANT_PROGRESS_EPSILON_SQ=0.01`, `WATCHDOG_MIN_DISTANCE_SQ=1.0` |
| Blade | `MantisLeapBladeEntity`, `MantisLeapBladeRenderer` |

Bytecode: `scratch/javap1011_ender10.txt` (`javap -classpath <JAR> -p -s -c`, `EXIT=0`, SHA-256 `0095E23B21918E38B4BD7D6C47DA8C3503753F0F988C00AB04A786060E2C50E5`); decompilação: `scratch/ender10_sources.txt` (SHA-256 `F3953EB8FCFB793EC501694E054E3C3CBE187E557B09B6CF158828692A97A645`).

## 3. Casting / execução

1. `AbstractSummonWeaponSpell` cria/reusa `MantisLeapBladeEntity`; `onCastNoWeapon` e `onInitialCastWithWeapon`/`onCastTickWithWeapon` aplicam `setDamage(getDamage(...))` a cada tick de cast.
2. `onCastCompleteWithWeapon`: se cancelado, `RELEASE_WEAPON`; senão `resolveLeapDestination` + `startLeap(..., getLeapTicksPerBlock(...), getLeapArcHeight(), weapon.getId())`.
3. Se `startLeap` retorna `false`, a blade executa `slash(level)` imediatamente (distância² < `0.0625` recusa). Se aceito, `KEEP_WEAPON` e som `VANILLA_HIGH_JUMP`.
4. `onClientCast` repete a resolução no cliente com `bladeEntityId=-1` para predição; a lógica de dano da blade permanece servidor-owner.
5. `MantisLeapMovementEvent.onPlayerTick(Pre)` aplica gravidade zero, interpola posição com `easeOutCubic`, zera `fallDistance`, marca `hasImpulse`/`hurtMarked`, e monitora estagnação (`STAGNANT_TICK_LIMIT=4`).

## 4. Targeting / geometria

| Propriedade | Valor e consumidor |
|---|---|
| Alcance | `min(32, power/100)` blocos; nominal **12 / 16 / 20** nos níveis 1–3 sem modificadores |
| Raycast | largura `1.0`, entidades válidas via `CombatTools.isValidCombatTarget` |
| Destino em entidade | `hitPosition - look*max(1.0, target.getBbWidth()*0.5)`, com `Y = target.getY()` |
| Destino em bloco | `hitPosition` do raycast |
| Fallback sem hit | `start + look.normalize()*range` |
| Clamp | distância final limitada a `range` |
| Arco | `1.5` blocos, aplicado como `4*h*p*(1-p)` |
| Duração do salto | `max(10, ceil(distance * ticksPerBlock))` ticks |
| Ticks por bloco | `max(0.25, 2.5 - power/800)`; nominal **1.0 / 0.5 / 0.25** nos níveis 1–3, após o piso no nível 3 |
| Watchdog de estagnação | `stagnantTicks >= 4`, limiar `0.01` de progresso² e `WATCHDOG_MIN_DISTANCE_SQ=1.0` |
| Ajustes de pouso | `LANDING_Y_OFFSETS={0,0.5,1,-0.5,1.5,-1,2}` e nove offsets X/Z `{0,±0.35,±0.7}` combinados |
| Invulnerabilidade pós-salto | `20` ticks, somente contra dano de `Mob` (`LivingIncomingDamageEvent` com `event.getSource().getEntity() instanceof Mob`) |

O dano da blade é separado da movimentação: o salto não é um projétil e não é um ataque automático adicional.

## 5. Resultado

- `finalizeLeap` ajusta pouso; `startPostLeapInvulnerability` concede 20 ticks de imunidade a mobs.
- `deactivate` limpa o estado; `clearExpiredPostLeapInvulnerability` remove a janela expirada.
- Se morto ou passageiro durante o salto, o provider inicia a janela pós-salto e desativa.
- `IMulticastUnsupportedSpell`: multicast não é suportado; não inferir múltiplas blades por cast.

## 6. Scaling e caps

| Parâmetro | Fórmula literal | Unidade / ownership |
|---|---|---|
| Spell power | `1200 + 400*(level-1)` | float; host aplica atributos |
| Dano | `power/100 * damageMultiplier(MANTIS_LEAP)` | config **NÃO VERIFICADA** |
| Mana | `70 + 15*(level-1)` | Iron's mana |
| Alcance | `min(32, power/100)` | blocos, cap rígido `32` |
| Ticks por bloco | `max(0.25, 2.5 - power/800)` | piso `0.25` |
| Duração | `max(10, ceil(distance*ticksPerBlock))` | ticks |
| Cast time | `25` ticks | campo; cast `LONG` e não interrompível |
| Cooldown | `8.0` s | `DefaultConfig` |

## 7. Possibilidades de perks

- **A — atributo nativo:** spell power/mana/cooldown via `AbstractSpell`; alcance e tempo por bloco respondem ao poder.
- **B — evento verificado:** `PlayerTickEvent.Pre` e `LivingIncomingDamageEvent` são execução do provider; não há API segura demonstrada para mudar o arco, o watchdog ou a invulnerabilidade.
- **C — adapter condicionado:** alterar esses parâmetros exigiria substituir `MantisLeap`, `MantisLeapMovementEvent` e o estado `MANTIS_LEAP_STATE` com contrato de client/server sync. **CONDICIONADO**.
- **D — sem hook demonstrado:** não há hook comprovado para transformar o salto em teleporte persistente, remover o cap de 32 ou estender a i-frame sem risco. **NO_MUTATION / fail-closed**.
- `mutating_hook = NOT_VERIFIED`.

## 8. Causalidade

`um cast → uma blade + um salto interpolado → pouso/i-frame → slash`.

O salto, o movimento e a blade são uma única raiz semântica. Black Arcana/RPG não devem pagar Mastery por tick de voo nem tratar o i-frame como defesa independente.

## 9. Concepção de nova magia

Assinatura ocupada: "salto ofensivo com arma conjurada, arco fixo e i-frame curta pós-pouso". Nenhuma implementação foi realizada.

## 10. Verificação e pendências

- ✅ Identidade/hash, coeficientes, targeting, fórmulas de alcance/tempo, arco, watchdog, offsets de pouso e i-frame confirmados no bytecode 1.0.1.1.
- ⚠️ Multiplicador instalado, sincronia cliente/servidor em lag e comportamento com blocos/entidades móveis não certificados.
- ⚠️ `physical_qa=NOT_TESTED`: sem servidor Survival, PvP, portais, montarias ou teleportes.
- ⚠️ Universo integral do provider não encerrado.

## Localizadores para Codex — resumo operacional

- `castTime=25` é campo; `canBeInterrupted=false` e `CastType.LONG` definem o canal real.
- `POST_LEAP_INVULNERABLE_TICKS=20` cobre somente dano de `Mob`, não todas as fontes.
- Nenhum ponto de mutação segura demonstrado; manter fail-closed.
- Consultar [`EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md`](../EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md).
