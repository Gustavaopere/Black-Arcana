# Echo Cast

**Estado do contrato:** ✅ `COMPLETE_PERK_READY` — `STATIC_TECHNICAL_CATALOG_ONLY` · `SHA_EXACT_BINARY_BEHAVIOR` · `mutating_hook=NOT_VERIFIED` · `physical_qa=NOT_TESTED`.

> O ✅ cobre exclusivamente a documentação estática SHA-exata deste objeto. Não homologa hook mutador, execução no pack, configuração efetiva nem universo integral do provider.

## 1. Identidade e proveniência

| Campo | Valor verificado |
|---|---|
| Provider | Apprentice's Codex |
| Mod ID | `apprenticecodex` |
| Nome de exibição | Echo Cast (nome funcional, não traduzido) |
| Registry ID | `apprenticecodex:echo_cast` |
| Host | Iron's Spells 'n Spellbooks (`AbstractSpell`) |
| Escola | `SchoolRegistry.ELDRITCH_RESOURCE` (Eldritch) |
| Raridade mínima | `SpellRarity.LEGENDARY` |
| Níveis | 1 (`DefaultConfig.setMaxLevel(1)`) |
| Tipo de cast | `CastType.LONG` |
| Cast time | `20` ticks |
| Cooldown declarado | `0.0` s na magia; o cooldown efetivo é recalculado pelo sistema de repeat |
| Recurso | Mana do Iron's (`baseManaCost=50`, `manaCostPerLevel=0`) |
| Spell power | `baseSpellPower=0`, `spellPowerPerLevel=0` |
| Aquisição | `setAllowCrafting(false)`, `requiresLearning()=false`, `allowLooting()=false`, `HiddenFromEldritchResearch` |
| JAR exato | `apprentice_codex-1.0.1-mc1.21.1.jar` |
| SHA-256 do JAR | `47018AD8C6C6187B17C6BFC4D4F2FFF44EA2ED560719EBB6566A750715757947` |
| SHA-1 do JAR | `3077999F51299A53A0AF1B8A1AEC22F4099E36A3` |
| Ambiente | Minecraft 1.21.1 · NeoForge 21.1.250 · Java 21 (JDK 21.0.12 na inspeção) |
| Classe de implementação | `jp.aquafactory.apprenticecodex.spell.echocast.EchoCast` |
| Evidência compartilhada | [`EXACT-TECHNICAL-CONTRACTS-1.0.1.md`](../EXACT-TECHNICAL-CONTRACTS-1.0.1.md) |

## 2. Localizadores para o Codex

| Elemento | Localizador |
|---|---|
| Registro | `SpellRegistry.reg("echo_cast", EchoCast::new)` |
| Config | `EchoCast.config`: `LEGENDARY`, `ELDRITCH_RESOURCE`, `maxLevel=1`, `cooldownSeconds=0.0`, `allowCrafting=false` |
| Coeficientes | `EchoCast.<init>()`: `baseSpellPower=0`, `spellPowerPerLevel=0`, `baseManaCost=50`, `manaCostPerLevel=0`, `castTime=20` |
| Pré-condição | `EchoCast.checkPreCastConditions(...)` |
| Aplicação do efeito | `EchoCast.onCast(...)` |
| Efeito | `jp.aquafactory.apprenticecodex.effect.EchoSpell` (`DURATION_TICKS=300`) |
| Staff | `jp.aquafactory.apprenticecodex.item.multicastechostaff.MulticastEchoStaff.isMulticastEchoStaff(ItemStack)` |
| Motor de repeat | `jp.aquafactory.apprenticecodex.item.multicastechostaff.MulticastEchoStaffCastHelper` |
| Dano de repeat | `MulticastEchoStaffAttackHandler` / `MulticastEchoStaffAttackProfileManager` |
| Efeitos de repeat | `MulticastEchoStaffMobEffectHandler` / `MulticastEchoStaffMobEffectProfileManager` |
| Config | `jp.aquafactory.apprenticecodex.config.item.MulticastEchoStaffServerConfig` |

Descriptors e offsets JVM estão em `scratch/javap_check.txt` (`javap -p -s -c`, `EXIT=0`, 347.597 bytes), não publicados integralmente.

## 3. Casting / execução

1. `CastType.LONG`, `castTime=20` ticks; mana `50`; sem spell power própria.
2. `checkPreCastConditions` exige `MulticastEchoStaff` em mainhand **ou** offhand e amplifier abaixo do limite; falha envia mensagem ao `ServerPlayer` e retorna `false`.
3. `maxEchoAmplifier() = ApprenticeCodexServerConfig.multicastEchoStaffMaxMulticastCount() - 1`; default `10 - 1 = 9` repetições extras.
4. `onCast` lê `EffectRegistry.ECHO_SPELL`: `amplifier = existing == null ? 0 : min(existing.amplifier + 1, maxEchoAmplifier())`; aplica `MobEffectInstance(ECHO_SPELL, 300, amplifier)`.
5. `EchoSpell` é `BENEFICIAL`, `DURATION_TICKS=300` e `shouldApplyEffectTickThisTick(...) = false` — não executa tick de efeito.
6. Som de início/fim: `SoundRegistry.MULTICAST`; animação: `SpellAnimations.BOW_CHARGE_ANIMATION`.

O repeat não é feito por `EchoCast` em si. `MulticastEchoStaffCastHelper.isEchoTarget` exclui explicitamente o próprio `Echo Cast` e exige que o item de cast seja `MulticastEchoStaff`.

Guardas e custos são owned pelo Iron's. No JAR físico do host, `AbstractSpell.getManaCost(int)` (`(I)I`, offsets 0–29) calcula `(baseManaCost + manaCostPerLevel*(level-1)) * MANA_MULTIPLIER` e trunca com `d2i`; `getSpellCooldown()` (`()I`, offsets 0–18) calcula `COOLDOWN_IN_SECONDS * 20.0d` e trunca com `d2i`; `getCastTime(int)` (`(I)I`, offsets 0–16) retorna `0` para `CastType.INSTANT` e o campo `castTime` nos demais tipos — aqui `CastType.LONG` com `20` ticks. `getLevelFor(int,LivingEntity)` (`(ILnet/minecraft/world/entity/LivingEntity;)I`, offsets 0–64) aplica Curios e `ModifySpellLevelEvent`. Assim, `50`, `0`, `0`, `0`, `0.0` e `castTime=20` são coeficientes declarados pelo Apprentice Codex; mana e cooldown efetivos dependem da config instalada do Iron's, atributos e eventos, **NÃO VERIFICADOS**. O cooldown final do repeat é calculado pelo provider, conforme a seção 5. Ver âncoras em [`EXACT-TECHNICAL-CONTRACTS-1.0.1.md`](../EXACT-TECHNICAL-CONTRACTS-1.0.1.md).

## 4. Targeting / geometria

| Propriedade | Valor e consumidor |
|---|---|
| Alvo da magia | O próprio caster; nenhum alvo ofensivo selecionado. |
| Pré-condição | Staff em uma das mãos; verificado em `checkPreCastConditions` e novamente durante cada repeat. |
| Alvo do repeat | A magia repetida conserva `spellId`, `spellLevel`, `castSource` e item de cast do `ActiveNormalCastContext`. |
| Tipos repetíveis | `isUnsupportedMulticastTarget` rejeita cast type fora de `INSTANT`/`LONG`, `getRecastCount >= 1` e `IMulticastUnsupportedSpell`. `Echo Cast` está fora do conjunto por exclusão explícita. |
| AOE própria | `N/A`: `Echo Cast` não possui caixa, raio ou projétil. Geometria é da magia repetida. |

## 5. Resultado

- `onServerPreCast` armazena `PreCastEchoContext(item, spellId, amplifier)` quando há `ECHO_SPELL` ativa.
- `onCastSpellStart` confirma sequência ativa (`MagicData.isCasting`, nível, spellId, castSource e item iguais) e revalida `checkPreCastConditions` com `AdditionalCastData` temporariamente limpo; então grava `ActiveNormalCastContext`.
- `onServerCastComplete` (sem cancelamento) remove `ECHO_SPELL`, calcula `remainingCasts = min(amplifier + 1, maxMulticastCount)` e agenda `MulticastJob` com `nextCastGameTime = gameTime + multicastDelayTicks` (default `2`, faixa `1–20`).
- Cada tick do job verifica staff nas mãos, mana quando `castSource.consumesMana()` e o gate de criatividade; executa `spell.onServerPreCast` + `castSpell(..., false)` ou caminho de `AbstractSummonWeaponSpell`, com `AdditionalCastData` preservado/restaurado.
- Cooldowns normais durante o repeat são cancelados em `SpellCooldownAddedEvent.Pre`. Ao finalizar, `SpellCooldownHelper.addCooldownRespectingCreativeConfig` chama `resolveFinalCooldown`.
- `resolveFinalCooldown`: se `baseCooldown > cooldownCapTicks`, preserva `baseCooldown`; senão `min(cap, ceil((amplifier+2)*cooldownMultiplier*baseCooldown + (amplifier+1)*castTimeCooldownMultiplier*effectiveCastTime))`. Defaults: `cooldownMultiplier=1.2`, `castTimeCooldownMultiplier=1.0`, `cooldownCapTicks=12000`.
- `MulticastEchoStaffAttackHandler` ajusta dano de ataques repetidos por perfil (`repeatDamageMultiplier` default `1.0`, multiplicador de origem STAFF) e pode ignorar iframe/redefinir iframe pós-hit conforme perfil. `attackProfilesEnabled` default `true`.
- `MulticastEchoStaffMobEffectHandler` captura efeitos não-instantâneos aplicados durante o repeat e aplica extensões de duração/amplifier por perfil, com categorias habilitadas por config e caps opcionais desligados por default.
- Estados voláteis (`PRE_CAST_CONTEXTS`, `ACTIVE_NORMAL_CASTS`, `MULTICAST_JOBS`, `FINAL_COOLDOWN_CONTEXTS`) são `ConcurrentMap` por UUID e limpos em logout, mudança de dimensão e morte.

## 6. Scaling e caps

| Parâmetro | Fórmula / default | Unidade / ownership |
|---|---|---|
| Mana | `50 + 0*(level-1)` | Iron's mana; default declarado |
| Cast time | `20` ticks | campo da magia |
| Duração do efeito | `300` ticks | `EchoSpell.DURATION_TICKS` |
| Amplifier máximo | `maxMulticastCount() - 1` | default `9` |
| Repetições | `amplifier + 1` até `maxMulticastCount` | default até `10` |
| Delay entre repetições | `2` ticks (faixa `1–20`) | config de servidor |
| Cooldown final | ver fórmula na seção 5 | ticks; valores efetivos de config **NÃO VERIFICADOS** |
| Dano de repeat | multiplicador de perfil × `repeatDamageMultiplier` (default `1.0`) | config/provider-owned |
| Caps de efeito | `durationServerCapEnabled=false`, `amplifierServerCapEnabled=false` por default | config de servidor |

## 7. Possibilidades de perks

- **A — atributo nativo:** mana/cast time via `AbstractSpell`; `baseSpellPower=0` não fornece escalonamento próprio.
- **B — evento/callback verificado:** `SpellCooldownAddedEvent.Pre`, `SpellDamageEvent` e `MobEffectEvent.Added` são observadores/mutadores internos do provider, mas acionados somente dentro do fluxo de repeat com contexto por UUID e casts autorais. Não foi demonstrado ponto seguro para uma perk externa alterar amplifier, delay ou fórmula sem quebrar o contrato de owner/cancelamento. **NO_MUTATION / fail-closed**.
- **C — adapter condicionado:** criar um novo consumidor de `ECHO_SPELL` exigiria preservar limpeza de efeito, maps concorrentes, gate de mana e cooldown final. **CONDICIONADO**.
- **D — sem hook demonstrado:** repetir `Echo Cast` a si mesmo, duplicar casts ou conceder repeat ilimitado não tem API/mixin seguro comprovado neste escopo.
- `mutating_hook = NOT_VERIFIED`.

## 8. Causalidade

`cast canalizado com staff → ECHO_SPELL(300 ticks, amplifier) → próximo cast elegível é capturado → efeito removido → N casts repetidos com delay → cooldown final recalculado`.

Cada repetição não é uma nova intenção do jogador para fins de XP/Mastery, embora execute `castSpell` da magia alvo. Black Arcana deve tratar o conjunto como uma causalidade de cast quando integrar procs.

## 9. Concepção de nova magia

Assinatura ocupada: "buff de repetição condicionado a staff que reexecuta a próxima magia compatível e recombina cooldown/cast time". Uma magia original Black Arcana precisaria de semântica materialmente distinta (por exemplo, eco de projeto já lançado sem buff de estado, ou repetição paga com recurso próprio) para não duplicar esta identidade. Nenhuma implementação foi realizada.

## 10. Verificação e pendências

- ✅ Identidade, versão e hash do JAR; registro e classe; pré-condição; efeito; cálculo de amplifier; delay; fórmula de cooldown; perfis de dano/efeito; limites de validação.
- ⚠️ Configuração efetiva do pack (delay, multiplicadores, caps, perfis) não lida; apenas defaults de código afirmados.
- ⚠️ `physical_qa=NOT_TESTED`: sem cliente, servidor, Survival, PvP ou modpack real.
- ⚠️ Catálogo completo de perfis de ataque/efeito por spellId não enumerado neste lote; tratado como provider-owned.
- ⚠️ Universo integral do provider não encerrado: recorte observado de 5 fichas.

## Localizadores para Codex — resumo operacional

- Não confundir `cooldownSeconds=0.0` da magia com o cooldown final do fluxo de repeat.
- Não awardar procs/mastery por cada repetição sem decisão explícita de design; a repetição é causalmente dependente do cast original.
- Consultar [`EXACT-TECHNICAL-CONTRACTS-1.0.1.md`](../EXACT-TECHNICAL-CONTRACTS-1.0.1.md) para hashes, comandos e limites da prova.
