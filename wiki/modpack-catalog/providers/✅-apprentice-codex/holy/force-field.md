# Force Field

- **Provider:** Apprentice's Codex
- **Mod ID:** `apprenticecodex`
- **Installed JAR:** `apprentice_codex-0.9.7.1+mc1.21.1.jar`
- **Registry ID:** `apprenticecodex:force_field`
- **Iron's school:** Holy
- **Levels:** 1–3
- **Minimum rarity:** Epic
- **Cast type:** Continuous
- **Cooldown:** 15 s
- **Resource:** Iron's mana
- **Source pin:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`

## Exact source coefficients

- `baseSpellPower = 100`
- `spellPowerPerLevel = 20`
- `baseManaCost = 15`
- `manaCostPerLevel = 0`
- `castTime = 100 ticks / 5 s`

Mana drain per intercepted hit:

`forceFieldDrainManaBasePerHit / max(1, spellPower / 100)`

If **Protection Spell Supporter** is equipped, that result is halved.

The same provider accessory doubles the effective cast duration after normal Iron's cast-time resolution.

## Defense lifecycle

Every server cast tick calls the provider's `ForceFieldDefenseEvent.interceptNearbyProjectiles(...)`. The defense event, not the spell class itself, owns projectile/attack interception, mana consumption, rejection/repulsion and any supported spell-projectile semantics.

Provider guide semantics: deploy an invisible all-direction field that repels enemy attacks, consumes a large amount of mana when it knocks something away, and can repel certain spells.

## Causality/resource authority

Intercepting an attack is one provider-owned defensive settlement. A Black Arcana observer must not:

- subtract mana again;
- destroy/reflect the same projectile a second time;
- award a separate cast per intercepted projectile;
- convert the intercepted attack into an offensive proc chain unless a future integration contract explicitly supports it.

## Deduplication

Direct overlap with Black Arcana Order/barrier concepts. An Order spell must provide materially different law/seal/enforcement semantics, not merely another omnidirectional projectile wall.

## Confidence

`SOURCE-PINNED SPELL + DEFENSE EVENT ENTRYPOINT / EXACT INTERCEPTABLE TARGET SET + PACK DRAIN CONFIG QA PENDING`

## Localizadores para Codex — source exato

- **Registry + identidade:** `apprenticecodex:force_field` → `SpellRegistry.reg("force_field", ForceField::new)` no source 0.9.7.1.
- **Classe Java verificável:** [`jp.aquafactory.apprenticecodex.spell.forcefield.ForceField`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/forcefield/ForceField.java) (`hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`).
- **Leitura para perks:** consultar os coeficientes, fórmulas, condições de alvo e relações causa→efeito já registrados nesta ficha; rastrear métodos da classe e classes auxiliares antes de afirmar que qualquer área, alvo, número de entidades ou duração é modificável externamente.
- **Contrato:** host Iron's controla casting e mana; Apprentice's Codex controla o efeito; RPG Skill Tree controla perks/Mastery/gates; Black Arcana só integra via boundary real, sem segunda liquidação de custo/efeito. Sem hook comprovado para a mutação: **⚠️ condicionado/fail-closed**.
- **Pendências:** classificar hooks com signature e validar entidades/efeitos secundários, QA no JAR físico e Survival. O link é prova de localização estática, não de interoperabilidade implementada.

---

## Engenharia causal aprofundada — 0.9.7.1 (audit de source, 2026-10-13)

**Prova rastreável:** [`forcefield/ForceField.java`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/forcefield/ForceField.java) · [`forcefield/ForceFieldDefenseEvent.java`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/forcefield/ForceFieldDefenseEvent.java). Source `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e` (declara 0.9.7.1); o JAR físico da modlist tem identidade/versionamento corroborados, **sem equivalência dos corpos compilados demonstrada**.

### Interceptação e cobrança sob concorrência de eventos

- **Scan ativo:** `ForceFieldDefenseEvent.interceptNearbyProjectiles`, chamado durante o cast, opera no servidor com `MagicData` válido e spell level positivo. Examina `Projectile` em `caster.getBoundingBox().inflate(INTERCEPT_RADIUS)`, com `INTERCEPT_RADIUS=3.0`, e predicado `shouldInterceptProjectile`.
- **Dano direto:** `onLivingAttack(LivingIncomingDamageEvent)` é inscrito com `EventPriority.HIGHEST`, resolve `ActiveForceField` e verifica `isBlockableByForceField`. No ramo elegível chama `event.setCanceled(true)`, depois trata melee com knockback, projétil direto com neutralização, ou tentativa de equivalência de counterspell conforme o tipo de fonte. Um cancelamento nesse handler não prova resultado final sob listeners de terceiros.
- **Neutralização de projectile:** `neutralizeProjectile` tenta `tryCounterspellEquivalent`; se não resolver, tenta desvio **somente se `DEFLECT_COUNT_TAG<=0`**, marcando contagem, depois `tryCatchProjectile`, e por fim `projectile.discard()`. `onProjectileDefenseFailed` é caminho separado de apresentação de falha; não equiparar falha visual à aplicação de dano.
- **Mana e cadeia:** `onForceFieldIntercept` chama `drainManaOnIntercept`, que usa `ForceField.getDrainManaPerHit(spellLevel,caster)` para deduzir o mana Iron's, com piso zero. Se o saldo chega a zero, chama `MagicTools.cancelCasting(caster,true)`. Tags `LAST_INTERCEPT_SOURCE_TAG`, `LAST_INTERCEPT_TICK_TAG` e `SAME_SOURCE_INTERCEPT_COOLDOWN_TICKS=10` participam do amortecimento de feedback de origem; não extrapolar uma política universal de antirreplay.
- **Perks:** um projétil pode atravessar scan por tick e evento de dano; sem token canônico de interceptação entre providers, não conceder dois procs, não refletir/capturar novamente e não cobrar segunda parcela. Requer QA de Arrow piercing, melee, spell projectiles, outros escudos, listener priority, mana exaurida e PvP.

### Perfil para integração de perks e QA

- **A / atributo e rank:** stats e estado de Iron's/Codex são lidos do provider, sem sobrescrita automática. Valores efetivos dependem de configuração e outros mods.
- **B / causalidade:** raiz `apprenticecodex:force_field`, mantendo eventos, tarefas e recursos da cadeia sob authority externa; não atribuir Mastery por cada callback de efeito secundário.
- **C/D / política:** nenhuma API/hook de RPG Skill Tree homologada pela simples presença desses métodos. **⛔** fail-closed para adapter e **⚠️** QA da versão instalada (JAR, host, Survival, servidor, multiplayer, dependências opcionais e claims).
- **Clean-room:** somente especificação factual própria; não transplantar implementação upstream.

[Matriz causal desta etapa](../PERK-ENGINEERING-MATRIX-HIGH-RISK-0.9.7.1.md).
