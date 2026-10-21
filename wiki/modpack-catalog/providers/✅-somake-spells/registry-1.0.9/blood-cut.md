# `somakespells:blood_cut`

- Provider: **Somake Spells** (`somakespells`)
- Artifact: `somakespells-1.0.9-1.21.1.jar`
- Physical / publisher SHA-1: `171841ac9f802be9309ecc166c1d972ac6d404c0`
- Substrate: **Iron's Spells 'n Spellbooks**
- Registry identity: `somakespells:blood_cut`
- Registration gate: **Unconditional**
- Current composition registration: **ADMITTED**
- State: `EXACT_PHYSICAL_REGISTRY / CURRENT_REGISTRATION_ADMITTED / STRICT_COUNT_CONDITIONAL`

## Registration evidence

The exact physical 1.0.9 `ModSpells` topology registers this identity without an optional-provider registration predicate.

The exact current artifact has 83 unique Somake spell registry IDs, and the present mod composition satisfies all optional registration predicates. This card records one of those **83/83 currently admitted registrations**.

## Host / progression boundary

Exact 1.0.9 structural evidence found no provider `isEnabled()` override among the 83 spell classes. That does **not** substitute for the effective deployed Iron's spell configuration.

This identity is not among the seven provider `allowCrafting()` override identities isolated by the exact 1.0.9 structural audit. Effective Iron's host `allow_crafting`/datapack state and actual survival acquisition are still not treated as deployed facts.

Still unresolved for strict semantic promotion:

- effective Iron's per-spell/global/datapack `enabled`;
- effective Iron's `allow_crafting` where applicable;
- deployed Somake `enableSpellLockSystem` COMMON value;
- object-level or bounded-set survival acquisition/reachability;
- assembled-pack progression/runtime settlement.

## Counting boundary

This is an exact current registry identity, not yet an independently strict-counted semantic action. Registration presence alone does not add this card to the strict numerator while the host/provider config and reachability gates above remain open.

Do not infer display name, school, level, rarity, mana cost, cooldown, damage, duration, targeting, recipe, loot source or formulas from the registry path.

## Authority

Iron's owns host casting/resource/cooldown settlement. Somake owns this spell identity and its provider progression. Black Arcana catalogs and may observe supported provider state; it does not recreate either runtime.

Sources: `../EXACT-1.0.9-REGISTRY-AUDIT.md`, `../EXACT-1.0.9-REGISTRATION-GATE-MAP.md`, `../SPELL-CATALOG-1.0.9.md`.

## Dossiê compilado de casting, efeito e caminho de dano (21/10/2026)

**Prova nova:** [auditoria Java21 #39546058075](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39546058075) **SUCCESS**, JAR SHA-1 físico `171841ac9f802be9309ecc166c1d972ac6d404c0`, **16 testes sintéticos**, duas classes únicas, **7 métodos de spell e 2 de efeito** com referências simbólicas conferidas. [Matriz técnica completa](blood-cut-technical-gate.md).

| Eixo útil para perks | Prova exata / limite |
|---|---|
| Classe de spell | `com.somake.somakespells.spells.blood.BloodCutSpell` |
| Cast | `getCastType()` referencia `CastType.INSTANT`; `onCast(Level,int,LivingEntity,CastSource,MagicData)` invoca `getSpellPower`, cria `MobEffectInstance` do `ModMobEffects.BLOOD_CUT` e chama `LivingEntity.addEffect` e `AbstractSpell.onCast` |
| Efeito downstream | `com.somake.somakespells.effect.blood.BloodCutEffect` contém `onLivingDamage(LivingDamageEvent.Post)` com **cinco branches** |
| Causalidade / dano | `onLivingDamage` referencia `getNewDamage`, `getSource`, `getEntity`, `MobEffectInstance.getAmplifier`, `getDamageModifier`, `LivingEntity.invulnerableTime` e `DamageSources.applyDamage`; o registro do listener e os gates condicionais permanecem pendentes |
| Escalonamento | `BloodCutEffect.getDamageModifier(int,LivingEntity)` referencia `ModSpells.BLOOD_CUT` e `BloodCutSpell.getEntityPowerMultiplier` (**dois branches**); **fórmula e limites NÃO verificados** |
| Lifesteal | `getDamageSource` referencia `SpellDamageSource.setLifestealPercent(float)`; taxa, origem, condições e cura resultante NÃO verificadas |
| Targeting / geometria | Alvo real, distância, LOS, área, hitbox, projetil, raio, velocidade e limites NÃO verificados. `SELF_CAST_ANIMATION` é apenas um marcador de animação |
| Recursos / tempo | Mana, cooldown, duração do efeito, ticks, config host e gates Survival NÃO verificados |
| Mutabilidade por perk | ⛔ `FAIL_CLOSED`: nenhuma API/hook mutador por jogador foi certificada; não criar segundo pipeline de dano, cura ou custo |

A presença de `LivingDamageEvent.Post` e `DamageSources.applyDamage` na mesma classe torna necessária uma prova de **filtros e prevenção de proc-chain** antes de qualquer integração que amplifique dano. O resultado é uma topologia de callsites compilados, não observação de execução real nem permissão de alterar o provider.


## Prova exata de inscrição declarativa do evento — 21/10/2026 (PR #858)

[Java21 #39549751471](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39549751471) passou com JAR SHA-1 idêntico e **20 testes sintéticos**. Foram identificados **EventBusSubscriber** como anotação runtime da classe BloodCutEffect e **SubscribeEvent** como anotação runtime de onLivingDamage(LivingDamageEvent.Post). As duas anotações são símbolos efetivos do classfile, não observação de despacho em jogo ou exposição de API mutadora.

No método onLivingDamage há **103 instruções**, **5 desvios** (ifeq, ifeq, ifnull, ifne e goto), **uma** referência invocada a getNewDamage e **uma** a DamageSources.applyDamage. A ordem de callsites situa a fonte de dano Blood Cut antes de applyDamage, mas não determina quais branches são atravessados. getDamageModifier possui **19 instruções** e **dois desvios**, sem fórmula homologada.

**Engenharia de perks:** aumentar dano/área, alterar alvo ou ativar proc/Mastery no evento Post continua **⛔ FAIL_CLOSED** até inspeção de predicados, deduplicação, configuração de Iron's e QA real. [Dossiê de evento](../EXACT-BINARY-BLOOD-CUT-EVENT-1.0.9.md). Nenhuma magia/adapter adicionado.


## CFG compilado e retorno float exato — 21/10/2026 (PR #859)

A [auditoria Java21 #39553030589](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39553030589) confirmou o mesmo SHA-1 físico **171841ac9f802be9309ecc166c1d972ac6d404c0**, com **41 testes sintéticos**, e inspecionou o fluxo de métodos do JAR 1.0.9.

- **onLivingDamage(LivingDamageEvent.Post)**: grafo normal de **103 instruções / 5 desvios**, com **2 caminhos sintáticos** que alcançam o único callsite de `DamageSources.applyDamage` e **3 que não alcançam**. Não são 5 eventos nem probabilidades, e o grafo não resolve filtros/recursão.
- **BloodCutEffect.getDamageModifier(int a, LivingEntity e):float** — duas rotas até `freturn`, certificadas por pilha JVM:

```text
factor = (e != null) ? BloodCutSpell.getEntityPowerMultiplier(e) : 1.0f
return ((float)(a + 1) * factor) * 0.1f
```

Preservar exatamente as duas multiplicações `float` na ordem compilada; `a` e `e` são argumentos do getter, **a proveniência a partir do evento permanece por comprovar**. O retorno não equivale a dano final ou permissão para modificá-lo via RPG Skill Tree. A função `getEntityPowerMultiplier`, os filtros de `onLivingDamage`, as configurações efetivas, dano secundário e Survival continuam condicionados. **⛔ FAIL_CLOSED para mutações de perk.**

[Dossiê detalhado de CFG e retorno numérico](../EXACT-BINARY-BLOOD-CUT-CFG-MODIFIER-1.0.9.md). Nenhuma raiz adicional ou adapter foi implementado.


## Parâmetro `lifesteal` do damage source — prova física em 21/10/2026 (PR #860)

[Auditoria Java 21 #39594615862](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39594615862) **SUCCESS**, SHA-1 físico Somake 1.0.9 conferido, **51 testes sintéticos**. O método compilado `BloodCutSpell.getDamageSource(Entity,Entity):SpellDamageSource` contém sete instruções: chamada à fonte-base do Iron's (índice 3), `ldc` carregando **`0.15f`** (índice 4), `SpellDamageSource.setLifestealPercent(float)` (índice 5), seguido de `areturn` (índice 6). A adjacência certifica o **parâmetro literal passado ao setter**.

O parâmetro nominal é `0.15f`; **não** se pode afirmar que Blood Cut cure 15% do dano sem examinar o tratamento efetivo do setter e do dano secundário pelo host. Hooks por caster, dano aplicado, alvo da cura, caps e QA real continuam ⚠️/⛔. [Dossiê de lifesteal e limites](../EXACT-BINARY-BLOOD-CUT-LIFESTEAL-1.0.9.md).

## Causalidade do evento Post, entidade e amplificador (PR #861, 21/10/2026)

O [gate Java21 #39599959888](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39599959888), com **73 testes sintéticos** e SHA-1 Somake 1.0.9 confirmado, provou no classfile: `event.getSource().getEntity()` → guarda `LivingEntity` → `local_1`; `local_1.getEffect(BLOOD_CUT)` → `local_2`; `local_2.getAmplifier()` → `getDamageModifier(int,LivingEntity)` juntamente com `local_1`. `event.getNewDamage()` multiplica o resultado por `fmul` e armazena `fstore_3`.

Também há um gate de exclusão: **`event.getSource() instanceof SpellDamageSource` resulta em retorno imediato**, antes do dano secundário. Isso não comprova imunidade a todas as formas de recursão ou dano efetivo. O argumento `LivingEntity` representa a entidade de origem do dano, **não necessariamente o caster original**.

A fórmula numérica certificada para o valor intermediário é `getNewDamage() * (((float)(amplifier + 1) * getEntityPowerMultiplier(sourceEntity)) * 0.1f)`, preservando a ordem `float`. O alvo efetivo de `DamageSources.applyDamage`, a mitigação e a cura permanecem ⚠️; hooks per-player seguem ⛔. [Dossiê causal completo](../EXACT-BINARY-BLOOD-CUT-CAUSAL-EVENT-1.0.9.md). Nenhum spell ou adapter adicional.

## Novo gate exato: alvo e source de DamageSources.applyDamage (PR #862, 21/10/2026)

[Java 21 #39604864087](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39604864087) **SUCCESS**, SHA-1 publisher Somake 1.0.9, **86 testes sintéticos**. No final de `BloodCutEffect.onLivingDamage`, o `applyDamage(Entity,float,DamageSource):boolean` recebe **`event.getEntity()` como alvo**, **`local_3` como float de dano solicitado** e **`BloodCutSpell.getDamageSource(local_1)` como source**. `local_1` é a entidade associada à fonte do dano original, comprovada no PR #861. A chamada de dano tem índice 100; o booleano é descartado, portanto não certifica sucesso do dano.

**Distinção de sobrecarga essencial:** o handler usa `getDamageSource(Entity)` (1 arg), enquanto o setter nominal de lifesteal `0.15f` foi observado na sobrecarga `getDamageSource(Entity,Entity)` (2 args). Delegação entre elas e cura real **não estão provadas**; ⚠️ condicionado e perks ⛔ FAIL_CLOSED. [Dossiê de aplicação do dano](../EXACT-BINARY-BLOOD-CUT-APPLY-DAMAGE-1.0.9.md).
