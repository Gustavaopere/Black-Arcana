# Blood Brand

**Estado do contrato:** ✅ `COMPLETE_PERK_READY` — `STATIC_TECHNICAL_CATALOG_ONLY` · `SHA_EXACT_BINARY_BEHAVIOR` · `mutating_hook=NOT_VERIFIED` · `physical_qa=NOT_TESTED`.

> O ✅ cobre exclusivamente a documentação estática SHA-exata deste objeto. Não homologa hook mutador, execução no pack, configuração efetiva nem universo integral do provider.

## 1. Identidade e proveniência

| Campo | Valor verificado |
|---|---|
| Provider | Apprentice's Codex |
| Mod ID | `apprenticecodex` |
| Nome de exibição | Blood Brand (nome funcional, não traduzido) |
| Registry ID | `apprenticecodex:blood_brand` |
| Host | Iron's Spells 'n Spellbooks (`AbstractSpell`) |
| Escola | `SchoolRegistry.BLOOD_RESOURCE` (Blood) |
| Raridade mínima | `SpellRarity.RARE` |
| Níveis | 1–5 (`DefaultConfig.setMaxLevel(5)`) |
| Tipo de cast | `CastType.INSTANT` |
| Cooldown declarado | `4.0` s |
| Recurso | Mana do Iron's (`baseManaCost=35`, `manaCostPerLevel=10`) |
| JAR exato | `apprentice_codex-1.0.1-mc1.21.1.jar` |
| SHA-256 do JAR | `47018AD8C6C6187B17C6BFC4D4F2FFF44EA2ED560719EBB6566A750715757947` |
| SHA-1 do JAR | `3077999F51299A53A0AF1B8A1AEC22F4099E36A3` |
| Ambiente | Minecraft 1.21.1 · NeoForge 21.1.250 · Java 21 (JDK 21.0.12 na inspeção) |
| Classe de implementação | `jp.aquafactory.apprenticecodex.spell.bloodbrand.BloodBrand` |
| Evidência compartilhada | [`EXACT-TECHNICAL-CONTRACTS-1.0.1.md`](../EXACT-TECHNICAL-CONTRACTS-1.0.1.md) |

A versão 0.9.7.1 anterior ficou registrada apenas como histórico; nenhum de seus valores foi reaproveitado sem confirmação no artefato 1.0.1.

## 2. Localizadores para o Codex

| Elemento | Localizador |
|---|---|
| Registro | `SpellRegistry.reg("blood_brand", BloodBrand::new)` |
| Config | `BloodBrand.config` (`new DefaultConfig().setMinRarity(RARE).setSchoolResource(BLOOD_RESOURCE).setMaxLevel(5).setCooldownSeconds(4.0).build()`) |
| Coeficientes | `BloodBrand.<init>()`: `baseSpellPower=100`, `spellPowerPerLevel=75`, `baseManaCost=35`, `manaCostPerLevel=10`, `castTime=0` |
| Dano de contato | `BloodBrand.getDamage(int,LivingEntity)` |
| Dano de burst | `BloodBrand.getExplodeDamage(int,LivingEntity)` |
| Raio | `BloodBrand.getExplodeRange()` → `5` |
| Spawn | `BloodBrand.onCast(Level,int,LivingEntity,CastSource,MagicData)` |
| Origem do projétil | `BloodBrand.resolveLaunchGeometry(LivingEntity)` |
| Entidade | `jp.aquafactory.apprenticecodex.spell.bloodbrand.BloodBrandKunai` |
| Burst | `jp.aquafactory.apprenticecodex.spell.bloodbrand.BloodBrandBurst` |
| Estado persistente | `jp.aquafactory.apprenticecodex.spell.bloodbrand.BloodBrandState` (`record BloodBrandState(UUID casterUuid, float burstDamage, double range)`) |
| Eventos | `jp.aquafactory.apprenticecodex.spell.bloodbrand.BloodBrandEvents` (`EntityTickEvent.Post`, `LivingDeathEvent`) |
| Multiplicador | `ApprenticeCodexServerConfig.damageMultiplier(DamageMultiplierKey.BLOOD_BRAND)` |

Os descriptors completos e os offsets JVM estão em `scratch/javap_check.txt` (347.597 bytes, `javap -p -s -c`, `EXIT=0`), não publicados integralmente.

## 3. Casting / execução

1. `AbstractSpell` resolve intenção, mana, cooldown e nível; `castTime=0` e `CastType.INSTANT`.
2. `BloodBrand.onCast` verifica `level instanceof ServerLevel`. Fora do servidor, nenhuma entidade é criada.
3. `resolveLaunchGeometry(caster)`:
   - se `caster instanceof ServerPlayer` e `RemoteOwnerCastContext.get(serverPlayer) != null`, usa `forward()` e `eyePosition()` do contexto remoto, com owner explícito;
   - caso contrário usa `caster.getLookAngle()` e `caster.getEyePosition()`.
4. Cria `BloodBrandKunai` com `EntityRegistry.BLOOD_BRAND_KUNAI`, define posição, `setDamage`, `setBurstDamage`, `setBurstRange(5)`, `setProjectileVelocity(forward)` e chama `serverLevel.addFreshEntity(projectile)`.
5. `super.onCast(...)` completa o fluxo do Iron's.

Guardas e custos são owned pelo Iron's. No JAR físico do host, `AbstractSpell.getManaCost(int)` (`(I)I`, offsets 0–29) calcula `(baseManaCost + manaCostPerLevel*(level-1)) * SpellConfigParameter.MANA_MULTIPLIER` e trunca com `d2i`; `getSpellCooldown()` (`()I`, offsets 0–18) calcula `COOLDOWN_IN_SECONDS * 20.0d` e trunca com `d2i`; `getCastTime(int)` (`(I)I`, offsets 0–16) retorna `0` para `CastType.INSTANT`. Assim, `35`, `10`, `4.0` e `castTime=0` são coeficientes declarados pelo Apprentice Codex; mana/cooldown efetivos dependem da config instalada do Iron's, **NÃO VERIFICADA**. `getSpellPower(int,Entity)` (`(ILnet/minecraft/world/entity/Entity;)F`, offsets 0–79) aplica ainda `AttributeRegistry.SPELL_POWER`, `SchoolType.getPowerFor(LivingEntity)` e `POWER_MULTIPLIER`. Ver âncoras em [`EXACT-TECHNICAL-CONTRACTS-1.0.1.md`](../EXACT-TECHNICAL-CONTRACTS-1.0.1.md).

## 4. Targeting / geometria

| Propriedade | Valor e consumidor |
|---|---|
| Aquisição de alvo | Nenhuma seleção prévia: projétil dirigido pela direção de olhar/contexto remoto. |
| Impacto | Colisão de entidade do `BloodBrandKunai`; `CombatTools.isValidCombatTarget` filtra alvo e owner. |
| Raio do burst | `5` blocos, repassado por `setBurstRange` e persistido em `BloodBrandState.range`. |
| Geometria do burst | `BloodBrandBurst` usa `HashSet<UUID>` de entidades já atingidas, AABB inflada pelo raio, distância até a AABB do alvo e `Utils.hasLineOfSight(level, center, targetBox.getCenter(), false)`. Sem linha de visão, o alvo não é atingido. |
| Projétil | `SPEED=1.68`; `LIFE_TICKS=100`; `AIR_DRAG=0.99` (`Vec3.scale(0.99)` em `tick()`); aceleração `-0.03` bloco/tick² aplicada quando `!isNoGravity()`; `setViewScale(8.0)` no construtor. |
| Gravidade | `GRAVITY = 0.03` é magnitude positiva declarada; em `tick()` o delta recebe `Vec3.add(0.0, -0.03d, 0.0)` quando `!isNoGravity()`. Aceleração vertical efetiva: **-0.03 bloco/tick²**. Constante e aceleração são grandezas distintas; nenhum consumo de `GRAVITY` foi demonstrado nas classes inspecionadas. |

## 5. Resultado

- **Contato:** dano `DamageTypes.BLOOD_BRAND` aplicado por `CombatTools.applyDamage`, com `KnockbackTypes.NO_KNOCKBACK`, escola Blood e owner resolvido por `CombatTools.getDamageSource(level, this, owner, ...)`.
- **Marcação:** `BloodBrandState` associa `casterUuid`, `burstDamage` e `range` à vítima; `BloodBrandEvents` observa tick e morte.
- **Burst na morte:** `BloodBrandBurst` aplica `burstDamage` a entidades próximas com `DamageTypes.BLOOD_BRAND_BURST`; na variante reforçada por Higanbana usa `DamageTypes.BLOOD_BRAND_HIGANBANA_BURST`. Deduplicação por `HashSet<UUID>` e filtro `CombatTools.isValidCombatTarget(..., caster)`; `Player` não é candidato.
- **Cura:** `healRate = 0.5` no burst normal e `1.0` no reforçado, aplicada sobre `max(0, healthBefore - healthAfter)` de cada alvo dano, somada e curada uma vez no caster via `CombatTools.applySpellHealing`. Provider-owned e não observada em execução.
- **Interação:** matar uma vítima marcada com Higanbana produz burst reforçado raio/dano `× 1.5`; a causa continua sendo o mesmo `Blood Brand cast`.
- **Efeitos secundários:** partículas `DustParticleOptions` e som `SoundRegistry.ICE_DAGGER_THROW` no cast.

## 6. Scaling e caps

| Parâmetro | Fórmula literal | Unidade / ownership |
|---|---|---|
| Spell power | `100 + 75*(level-1)` conforme `AbstractSpell` | provider host; valor efetivo depende de atributos |
| Mana | `35 + 10*(level-1)` | Iron's mana; default declarado |
| Dano bruto de contato | `1 + spellPower/100` | float; `getDamage()` |
| Dano bruto de burst | `8 * spellPower/100` | float; `getExplodeDamage()` |
| Multiplicador de servidor | `ApprenticeCodexServerConfig.damageMultiplier(BLOOD_BRAND)` | default de config `1.0`, faixa `0.1–10.0`; valor instalado **NÃO VERIFICADO** |
| Raio | `5` constante | blocos |
| Duração da marca | `200` ticks | observado no fluxo `BloodBrandEvents`, confirmado nas classes 1.0.1 |
| Cooldown | `4.0` s | `DefaultConfig` |

Nenhum hard cap adicional de número de vítimas foi comprovado no JAR para além do `HashSet` de deduplicação.

## 7. Possibilidades de perks

- **A — atributo nativo:** spell power/mana/cooldown via `AbstractSpell` e atributos do Iron's; comprovado como contrato do host, não como hook de mutação deste objeto.
- **B — evento/callback verificado:** `ApprenticeCodexServerConfig.damageMultiplier` é configurável pelo servidor, mas não foi demonstrado como evento seguro invocável por perk por cast. `LivingDeathEvent`/`EntityTickEvent.Post` são observadores do provider; sua existência **não** autoriza alterar o burst.
- **C — adapter condicionado:** mudar raio, dano de burst, cura ou velocidade exige substituir/encapsular `BloodBrandKunai`/`BloodBrandBurst`/`BloodBrandState` com contrato explícito de owner e dedup. **CONDICIONADO**.
- **D — sem hook demonstrado:** para transformar alvo único em área, multiplicar burst ou conceder cura extra, não há API/mixin seguro comprovado neste escopo. **NO_MUTATION / fail-closed** até evidência de boundary real.
- `mutating_hook = NOT_VERIFIED`.

## 8. Causalidade

`um cast → um kunai → contato opcional → marca persistente → morte qualificada → um burst + uma cura`.

O burst e a cura não são casts independentes. Black Arcana não deve awardar mastery, procs ofensivos ou XP duas vezes (kunai + burst), nem tratar a morte como nova intenção do jogador. `BloodBrandState.isEmpty()` usa `casterUuid == UUID(0,0) || range <= 0`, o que impede burst sem caster/raio válidos.

## 9. Concepção de nova magia

Assinatura ocupada: "projétil de sangue que marca e explode na morte com cura proporcional". Uma magia original Black Arcana precisaria de semântica materialmente distinta (por exemplo, dano compartilhado sem marca persistente, ou cura dependente de canalização) para não duplicar esta identidade. Nenhuma implementação foi realizada.

## 10. Verificação e pendências

- ✅ Identidade, versão e hash do JAR; registro e classe; coeficientes; fórmulas; targeting; custos; boundary de mutação; limites de validação.
- ⚠️ Configuração efetiva do pack (multiplicador de dano) não lida.
- ⚠️ `physical_qa=NOT_TESTED`: sem cliente, servidor, Survival, PvP ou modpack real.
- ✅ Duração da marca (`200` ticks), heal rate (`0.5`/`1.0`), raio/dano reforçados (`×1.5`) e linha de visão do burst confirmados nas classes 1.0.1.
- ⚠️ Universo integral do provider não encerrado: recorte observado de 5 fichas.

## Localizadores para Codex — resumo operacional

- Não presumir que `setBurstRange` ou `setDamage` são pontos mutáveis por perk: são setters internos da entidade, sem callsite externo comprovado.
- Para qualquer bridge, correlacionar `casterUuid` e burst exatamente uma vez; não duplicar custo, cooldown, mana ou proc.
- Consultar [`EXACT-TECHNICAL-CONTRACTS-1.0.1.md`](../EXACT-TECHNICAL-CONTRACTS-1.0.1.md) para hashes, comandos e limites da prova.
