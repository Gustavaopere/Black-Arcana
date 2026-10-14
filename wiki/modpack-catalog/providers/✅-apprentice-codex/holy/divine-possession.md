# Divine Possession

- **Provider:** Apprentice's Codex
- **Mod ID:** `apprenticecodex`
- **Installed JAR:** `apprentice_codex-0.9.7.1+mc1.21.1.jar`
- **Registry ID:** `apprenticecodex:divine_possession`
- **Iron's school:** Holy
- **Levels:** 1
- **Minimum rarity:** Legendary
- **Cast type:** Instant
- **Cooldown:** 300 s
- **Resource:** Iron's mana
- **Source pin:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`

## Exact source config

- `baseSpellPower = 0`
- `spellPowerPerLevel = 50`
- `baseManaCost = 600`
- `manaCostPerLevel = 200`
- `castTime = 0`
- `setAllowCrafting(false)`
- `allowLooting() = false`

Duration formula:

`400 + round(200 * spellPower / 100)` ticks.

The catalog preserves the formula rather than calculating a level-1 duration independently of Iron's exact `getSpellPower` semantics.

## Equipment gate

The source refuses casting unless **all four armor slots** contain an `ElementMaidenRobeItem`:

- head;
- chest;
- legs;
- feet.

This is a provider-native hard equipment gate, not a Black Arcana or RPG Skill Tree gate.

## What it does

A successful cast applies the provider's `DIVINE_POSSESSION` effect for the calculated duration.

Provider guide semantics: the full Maiden of the Elements outfit permits an elemental being to descend into the caster, temporarily causing the caster's strongest school bonus to apply to every other school.

The exact school-bonus equalization is implemented by the provider effect/equipment system. Black Arcana must not reproduce the same school-power transfer or treat the possession as its Corruption/Strain state.

## Acquisition

The spell is explicitly non-craftable and non-lootable; its usable identity is armor-bound according to the source and provider guide.

## Deduplication

Occupies the **full-set-gated temporary all-school power equalization/possession** niche.

## Confidence

`SOURCE-PINNED SPELL + FULL ARMOR GATE / EFFECT SCHOOL-BONUS IMPLEMENTATION + RUNTIME EQUIPMENT QA PENDING`

## Localizadores para Codex — source exato

- **Registry + identidade:** `apprenticecodex:divine_possession` → `SpellRegistry.reg("divine_possession", DivinePossession::new)` no source 0.9.7.1.
- **Classe Java verificável:** [`jp.aquafactory.apprenticecodex.spell.divinepossession.DivinePossession`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/divinepossession/DivinePossession.java) (`hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`).
- **Leitura para perks:** consultar os coeficientes, fórmulas, condições de alvo e relações causa→efeito já registrados nesta ficha; rastrear métodos da classe e classes auxiliares antes de afirmar que qualquer área, alvo, número de entidades ou duração é modificável externamente.
- **Contrato:** host Iron's controla casting e mana; Apprentice's Codex controla o efeito; RPG Skill Tree controla perks/Mastery/gates; Black Arcana só integra via boundary real, sem segunda liquidação de custo/efeito. Sem hook comprovado para a mutação: **⚠️ condicionado/fail-closed**.
- **Pendências:** classificar hooks com signature e validar entidades/efeitos secundários, QA no JAR físico e Survival. O link é prova de localização estática, não de interoperabilidade implementada.

---

## Engenharia causal aprofundada — lote persistente 0.9.7.1

**Classes verificadas:** [`divinepossession/DivinePossession.java`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/divinepossession/DivinePossession.java) · [`divinepossession/DivinePossessionPowerHelper.java`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/divinepossession/DivinePossessionPowerHelper.java). Source `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e` declarado 0.9.7.1; **não** há prova de equivalência bytecode dos métodos com o JAR físico da modlist. A inspeção não é um QA provider-native.

### Execução e integridade

- **Gate de equipamento:** `DivinePossession.canBeCastedBy` requer `hasFullElementMaidenRobe(player)`, que percorre `REQUIRED_ARMOR_SLOTS` e verifica que cada slot contém `ElementMaidenRobeItem`; se não, retorna `CastResult.Type.FAILURE` com mensagem `REQUIRED_ALL_PIECES_KEY`. Somente quando satisfaz passa para `super.canBeCastedBy` (incluindo validações Iron's).
- **Cast efetivo:** `onCast` adiciona um `MobEffectInstance(EffectRegistry.DIVINE_POSSESSION, getDurationTicks(spellLevel,entity),0,false,false,true)` e em seguida chama `super.onCast`. O método analisado **não** cria entidade nem gasta mana manualmente; custos base são da pipeline Iron's.
- **Fórmula condicionada:** `DivinePossessionPowerHelper.resolveSchoolPower(SchoolType,LivingEntity)` é helper de power, mas a presença do método não autoriza alterar poder/escola na BA; duração e strength efetivas exigem inspeção de estado/config no host e QA com os quatro itens.
- **Riscos:** remoção de peça enquanto buff está ativo, slots alterados por mods de armadura, recast, stacking, cancelamento e reboot. O gating pela armadura não é hook de RPG Skill Tree nem prova de perk; não duplicar bônus da potion.

### Interoperabilidade e QA

**Raiz contável:** `apprenticecodex:divine_possession`, já presente nas 83 spells. Efeitos secundários/ticks/entidades continuam provider-owned (Iron's/Apprentice's). **⛔** RPG Skill Tree só pode oferecer progressão/atributos/gates via contrato real; nenhum adapter de perks/Mastery foi implementado. Black Arcana não reexecuta nem debita recursos/cooldowns do provider. **⚠️** Persistem QA físico, modpack Survival, server+client, config, multiplayer, claims, lifecycle NBT e método de JAR. Stage 06.05 sem promoção.

[Matriz técnica da etapa](../PERK-ENGINEERING-MATRIX-PERSISTENT-0.9.7.1.md).
