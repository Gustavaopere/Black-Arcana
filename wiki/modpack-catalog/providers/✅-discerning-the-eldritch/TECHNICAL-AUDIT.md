# Discerning The Eldritch 1.4.4 — technical audit

## Provenance

- Pack: `discerning_the_eldritch-1.4.4-1.21.jar`.
- Notion reconciliado para runtime 1.4.4-1.21.
- Upstream branch: `1.21`.
- Head auditado: `7bbd81f902c65a4452f47656ebd948cae8cd5833`.
- `gradle.properties`: `mod_version=1.4.4-1.21`.
- `SpellRegistries`: 22 registrations reais.

## Authority map

- spell registry/cast lifecycle: Iron's + DTE spell classes;
- Silence/Metaphysical anti-cast: `SpellPreCastEvent` in DTE `ServerEvents`;
- Insanity: DTE attachments/config + server cast event;
- summons: `SpellSummonEvent`, `SummonManager`, provider entities;
- Abracadabra: `LivingDamageEvent.Pre` + `MobEffectEvent.Applicable`;
- Ritual: `DTESchoolRegistry.RITUAL` + `AbstractRitualSpell`;
- Fire soul-stack spending: `DTEDataComponentRegistry.SOUL_FIRE_STACKS`;
- Frostbite combo: `FROSTBITE_LEVEL` attachment + Iron's `CHILLED`;
- Blood/Fire lifesteal: Iron's `SpellDamageSource` fields set by the spells.

## Config defaults relevantes

- Mend Flesh hit lifesteal: enabled.
- Mend Flesh XP heal: enabled.
- Insanity system: disabled.
- Max Insanity: 15.
- Abracadabra damage cap: enabled.
- Abracadabra base cap: 80.
- Abracadabra harmful-effect prevention: enabled.

Runtime pack config pode sobrescrever esses defaults e deve ser observado antes de balanceamento final.

## Static-source QA findings

### Ravenous Revenant / Predator

`PredatorPotionEffect` primeiro entra em `if (attacker has PREDATOR)` e cria uma jaw de damage 20. O `else if` seguinte exige novamente Predator + target Prey, logo é inalcançável quando Predator é verdadeiro; além disso o segundo branch cria a jaw 25 sem `addFreshEntity`. O bônus Predator+Prey pretendido não deve ser considerado funcional sem runtime test/fix.

### Zealous Harbinger

Dentro do loop, cada projectile recebe `setPos(... z+i)` e imediatamente `setPos(... z-i)`. A primeira posição é sobrescrita; a disposição bilateral aparente no source não acontece por essas duas linhas. Gameplay/VFX final requer QA.

### Otherworldly Presence

Spell class confirma teleport + `METAPHYSICAL` por 10 s; server event confirma anti-cast. A descrição pública também afirma impedir causar/receber dano, mas esse settlement específico não foi localizado no conjunto de handlers auditado nesta passagem e permanece `NÃO VERIFICADO` no detalhe.

## Acquisition policy

Não assumir que todo registration é scroll genérico:

- `Conjure Gaoler`: crafting=false, looting=false, requiresLearning=false.
- `Guardian's Gaze`: crafting-by-player=false e looting=false.
- `Soul Slice` / `Soul Set Ablaze`: crafting=false, looting=false.
- Ritual: base class proíbe crafting; complexidade controla loot e cast source.
- `Exorcism`: crafting/loot permitidos somente quando Insanity system está enabled.

Onde nenhuma rota específica foi encontrada, a ficha registra o gate confirmado e deixa a fonte concreta de obtenção `NÃO VERIFICADO`.

## Integration rule

Provider-native first. Uma integração Black Arcana pode observar events/effects/attachments quando existe hook causal, mas não deve:

- duplicar damage settlement;
- reconstruir summon lifecycle;
- inferir Silence/Metaphysical por animação;
- conceder stack/XP por tentativa cancelada;
- reaplicar Frostbite/Insanity/Soul Fire em ledger paralelo;
- contornar acquisition/cast-source gates de Ritual.
