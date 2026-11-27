# Higanbana

**Estado do contrato:** ✅ `COMPLETE_PERK_READY` — `STATIC_TECHNICAL_CATALOG_ONLY` · `SHA_EXACT_BINARY_BEHAVIOR` · `mutating_hook=NOT_VERIFIED` · `physical_qa=NOT_TESTED`.

> O ✅ cobre exclusivamente a documentação estática SHA-exata deste objeto. Não homologa hook mutador, execução no pack, configuração efetiva nem universo integral do provider.

## 1. Identidade e proveniência

| Campo | Valor verificado |
|---|---|
| Provider | Apprentice's Codex |
| Mod ID | `apprenticecodex` |
| Nome de exibição | Higanbana (nome funcional, não traduzido) |
| Registry ID | `apprenticecodex:higanbana` |
| Host | Iron's Spells 'n Spellbooks (`AbstractSummonWeaponSpell<HiganbanaKatanaEntity>`) |
| Escola | `SchoolRegistry.BLOOD_RESOURCE` (Blood) |
| Raridade mínima | `SpellRarity.COMMON` |
| Níveis | 1–5 (`DefaultConfig.setMaxLevel(5)`) |
| Tipo de cast | `CastType.INSTANT` |
| Cooldown declarado | `4.0` s |
| Recurso | Mana do Iron's (`baseManaCost=40`, `manaCostPerLevel=20`) |
| JAR exato | `apprentice_codex-1.0.1.1-mc1.21.1.jar` |
| SHA-256 do JAR | `9C5244E75DBCA95BDAF48A85F0C189F8456149D1220BAD5FF339A86BCE04AC86` |
| SHA-1 do JAR | `A3F9C73EBD77D15B7E77AE14F4D0F695FEC3B7CF` |
| Ambiente | Minecraft 1.21.1 · NeoForge 21.1.250 · Java 21 (JDK 21.0.12 na inspeção) |
| Classe de implementação | `jp.aquafactory.apprenticecodex.spell.higanbana.Higanbana` |
| Evidência compartilhada | [`EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md`](../EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md) |

## 2. Localizadores para o Codex

| Elemento | Localizador |
|---|---|
| Registro | `SpellRegistry.reg("higanbana", Higanbana::new)` |
| Config | `Higanbana.config`: `COMMON`, `BLOOD_RESOURCE`, `maxLevel=5`, `cooldownSeconds=4.0` |
| Coeficientes | `Higanbana.<init>()`: `baseSpellPower=100`, `spellPowerPerLevel=100`, `baseManaCost=40`, `manaCostPerLevel=20`, `castTime=0` |
| Dano | `Higanbana.getDamage(int,LivingEntity)` |
| Alcance informativo | `Higanbana.getRange()` → `HiganbanaKatanaEntity.getAttackDepth()` |
| Número de cortes | `Higanbana.getSlashCount()` → `4` |
| Spawn/inicialização | `Higanbana.onCastNoWeapon(...)`, `Higanbana.onInitialCastWithWeapon(...)` |
| Entidade | `jp.aquafactory.apprenticecodex.spell.higanbana.HiganbanaKatanaEntity` |
| Corte | `HiganbanaKatanaEntity.tickOnServer`, `canSlash`, `slash`, `performSlash` |
| Caixa de ataque | `RaycastTools.HorizontalOrientedBox` em `performSlash` |
| Lifesteal | `jp.aquafactory.apprenticecodex.spell.higanbana.HiganbanaLifestealEvent.onLivingDamage(Post)` |
| Multiplicador | `ApprenticeCodexServerConfig.damageMultiplier(DamageMultiplierKey.HIGANBANA)` |

Descritores e offsets JVM foram reconsultados no JAR 1.0.1.1: saída `scratch/javap1011_legacy.txt` (`javap -classpath <JAR> -p -s -c`, `EXIT=0`, 233.376 bytes, SHA-256 `F59E0944BA6C04BF5A2B3A28145C9403B225EDF7EEC8425D4A0B6E189F63CCF3`) e anotações/constantes em `scratch/javap1011_v.txt` (`EXIT=0`), não publicadas integralmente.

## 3. Casting / execução

1. `CastType.INSTANT`, `castTime=0`. Iron's resolve intenção, mana, cooldown e nível.
2. `onCastNoWeapon` cria `HiganbanaKatanaEntity` com `EntityRegistry.HIGANBANA_KATANA` e `level.addFreshEntity`. O método não contém guarda `ServerLevel` explícita; a chamada é provider/host-owned.
3. `onInitialCastWithWeapon` aplica `setDamage(getDamage(...))`, `setRemainingSlashCount(4)` e `setFirstSlashStandby(5)`. O literal `5` é usado diretamente, embora exista `FIRST_SLASH_DELAY_TICK = 5`.
4. `tickOnServer` descarta a entidade sem owner; com owner, decrementa `releaseDelayTick`, `slashEffectTick` e `slashStandbyTick`, e chama `slash()` quando `canSlash()`.
5. `canSlash()` exige `remainingSlashCount > 0`, `slashStandbyTick <= 0` e `releaseDelayTick < 0`.
6. Cada `slash()` decrementa o contador, reinicia standby em `5` ticks e, no último corte, agenda `scheduleRelease(10)`; ao zerar o delay, a katana é descartada.
7. `onCastCompleteWithWeapon` mantém a arma (`KEEP_WEAPON`) salvo cancelamento (`RELEASE_WEAPON`).

Guardas e custos são owned pelo Iron's. No JAR físico do host, `AbstractSpell.getManaCost(int)` (`(I)I`, offsets 0–29) calcula `(baseManaCost + manaCostPerLevel*(level-1)) * MANA_MULTIPLIER` e trunca com `d2i`; `getSpellCooldown()` (`()I`, offsets 0–18) calcula `COOLDOWN_IN_SECONDS * 20.0d` e trunca com `d2i`; `getCastTime(int)` (`(I)I`, offsets 0–16) retorna `0` para `CastType.INSTANT`. `getSpellPower(int,Entity)` (`(ILnet/minecraft/world/entity/Entity;)F`, offsets 0–79) multiplica ainda por `AttributeRegistry.SPELL_POWER`, `SchoolType.getPowerFor(LivingEntity)` e `POWER_MULTIPLIER`; `getLevelFor(int,LivingEntity)` (`(ILnet/minecraft/world/entity/LivingEntity;)I`, offsets 0–64) aplica Curios e `ModifySpellLevelEvent`. Assim, `40`, `20`, `100`, `100`, `4.0` e `castTime=0` são coeficientes declarados pelo Apprentice Codex; mana, cooldown, power e nível efetivos dependem da config instalada do Iron's, atributos e eventos, **NÃO VERIFICADOS**. Ver âncoras em [`EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md`](../EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md).

## 4. Targeting / geometria

| Propriedade | Valor e consumidor |
|---|---|
| Aquisição de alvo | Nenhum lock-on prévio; a caixa é orientada por `this.position()` e `this.getLookAngle()`. |
| Filtro | `e != owner && CombatTools.isValidCombatTarget(e, owner)`; `hit.blockOccluded()` bloqueia o corte. |
| Caixa | `new HorizontalOrientedBox(position, lookAngle, 2.5, 0.75, 2.5)` — meia-largura `2.5`, meia-altura `0.75`, profundidade `2.5`, em blocos. |
| Constantes | `ATTACK_HALF_WIDTH=2.5`, `ATTACK_HALF_HEIGHT=0.75`, `ATTACK_DEPTH=2.5`. |
| Divergência verificada | `getAttackDepth()` retorna `3.4` e é o valor consumido por `Higanbana.getRange()`/tooltip; a caixa real de dano usa `ATTACK_DEPTH=2.5`. Ambos são registrados com consumidores distintos. |
| Standby | `FOLLOW_FORWARD_OFFSET=0.9`; posição calculada por `RotationTools.calculateBehindPosition(owner, -0.9, 0.0, -0.75)` com limitação por colisão. |
| Trail | `SHOW_TRAIL` sincronizado; `slashEffectTick=10` controla a duração visual; cor ARGB `-65536`. |

## 5. Resultado

- Cada corte aplica `CombatTools.applySpellDamage(hit.entity(), damage, source, SpellRegistry.HIGANBANA.get(), KnockbackTypes.NO_KNOCKBACK)` com `DamageTypes.HIGANBANA` no JAR 1.0.1.1; o bytecode foi verificado em `HiganbanaKatanaEntity`.
- Se o dano foi aplicado, `playDrainFeedback` toca `SoundRegistry.SLASH_DRAIN` e emite 20 partículas vermelhas no `ServerPlayer`.
- Som por corte: `SoundRegistry.KATANA_SLASH` e `SoundEvents.PLAYER_ATTACK_SWEEP`.
- Lifesteal: `LivingDamageEvent.Post` somente no servidor; exige `event.getSource().is(DamageTypes.HIGANBANA)`, `getSource().getEntity()` como `LivingEntity`, `newDamage > 0`; cura `dealtDamage * 0.5F` via `CombatTools.applySpellHealing`, com a escola da magia. O listener não possui guarda explícita `attacker != victim`.
- A cura é efeito secundário do dano registrado, não um novo cast.

## 6. Scaling e caps

| Parâmetro | Fórmula literal | Unidade / ownership |
|---|---|---|
| Spell power | `100 + 100*(level-1)` conforme `AbstractSpell` | provider host; valor efetivo depende de atributos |
| Mana | `40 + 20*(level-1)` | Iron's mana; default declarado |
| Dano | `(1 + spellPower/100) * damageMultiplier(HIGANBANA)` | float; multiplicador default `1.0`, faixa `0.1–10.0`; valor instalado **NÃO VERIFICADO** |
| Cortes | `4` constante | por cast |
| Delays | primeiro corte `5`; intervalo entre cortes `5`; trail `10`; release `10` | ticks |
| Cooldown | `4.0` s | `DefaultConfig` |
| Hard cap de alvos | NÃO VERIFICADO | `hitsHorizontalOrientedBox` não expõe limite numérico nesta classe |

A entidade persiste NBT `Damage`, `SlashStandbyTick`, `RemainingSlashCount` e `SlashPhase`; `releaseDelayTick` não é salvo/restaurado nesses métodos.

## 7. Possibilidades de perks

- **A — atributo nativo:** spell power/mana/cooldown via `AbstractSpell`; comprovado como contrato do host, não como hook de mutação deste objeto.
- **B — evento/callback verificado:** `damageMultiplier(HIGANBANA)` é config de servidor; `LivingDamageEvent.Post` é observador do lifesteal. Nenhum dos dois foi demonstrado como ponto seguro para perk alterar cortes ou cura por cast. **NO_MUTATION / fail-closed**.
- **C — adapter condicionado:** alterar número de cortes, caixa, delays ou cura exigiria substituir/encapsular `HiganbanaKatanaEntity` e preservar owner, NBT e dedup de dano. **CONDICIONADO**.
- **D — sem hook demonstrado:** converter cortes em área maior, mudar `3.4`/`2.5` ou duplicar lifesteal não tem API/mixin seguro comprovado neste escopo.
- `mutating_hook = NOT_VERIFIED`.

## 8. Causalidade

`um cast → uma katana → até quatro cortes no tempo → dano por corte + lifesteal por dano → release/discard`.

Cada corte é uma aplicação de dano dentro da mesma magia; o lifesteal não é cast independente. Black Arcana não deve awardar mastery/procs uma vez por corte se a semântica desejada for por cast, nem contar a cura como nova intenção do jogador.

## 9. Concepção de nova magia

Assinatura ocupada: "arma conjurada que executa quatro cortes orientados com drenagem de vida". Uma magia original Black Arcana precisaria de semântica materialmente distinta (por exemplo, cortes radiais sem arma persistente, ou cura dependente de carga) para não duplicar esta identidade. Nenhuma implementação foi realizada.

## 10. Verificação e pendências

- ✅ Identidade, versão e hash do JAR; registro e classe; coeficientes; fórmula de dano; targeting e caixa; timing; lifesteal; limites de validação.
- ⚠️ Configuração efetiva do pack (multiplicador de dano) não lida.
- ⚠️ `physical_qa=NOT_TESTED`: sem cliente, servidor, Survival, PvP ou modpack real.
- ⚠️ Consumo efetivo de `getAttackDepth()` fora do tooltip e do próprio provider não rastreado além de `Higanbana.getRange()`.
- ⚠️ Universo integral do provider não encerrado: recorte observado de 15 fichas.

## Localizadores para Codex — resumo operacional

- Não tratar `setDamage`, `setRemainingSlashCount` ou `setFirstSlashStandby` como pontos mutáveis por perk: são setters internos da entidade, sem callsite externo comprovado.
- Correlacionar `DamageTypes.HIGANBANA` com o lifesteal exatamente uma vez por evento de dano.
- Consultar [`EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md`](../EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md) para hashes, comandos e limites da prova.
