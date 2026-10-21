# Possessed Soul Blade

**Prova binária física (2026-10-13):** ✅ `COUNTED_EXACT` — `legendary_spellbooks:possessed_soul_blade`, classe `dev.higurashi.legendary_spellbooks.common.spells.blood.PossessedSoulBladeSpell`; [Java21 #38453654179](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38453654179) / [dossiê](../EXACT-BINARY-SPELLS-0.3.2.md). Parâmetros efetivos e Survival ⚠️, +0 raízes.

- ID: `legendary_spellbooks:possessed_soul_blade`
- School runtime: Evocation nos níveis 1–2; Blood nos níveis 3–4
- Levels: 1–4
- Min rarity: Epic
- Cooldown: 20 s
- Cast-time field: 35 ticks
- Mana neutral: 125 / 150 / 175 / 200
- Spell power neutral: 6 / 10 / 14 / 18
- Blade rings: 3 / 4 / 5 / 6
- Approx. blade count from provider formula `floor(1.5 × rings)`: 4 / 6 / 7 / 9
- Estado Black Arcana: `JÁ EXISTE / SEM ALTERAÇÃO PLANEJADA`

## Contract

É uma spell de escola dupla real, implementada sobre `BaseDoubleSchoolSpell`. O provider muda a escola efetiva para Blood a partir do nível 3; Black Arcana não deve congelar a classificação em uma única escola nem aplicar power/resistance pelo ramo errado.

O cast cria os anéis/lâminas provider-native e conserva a resolução de dano no próprio addon/Iron's.

## Acquisition

Pool do Possessed Paladin: níveis 1–3, weight 10. O config da spell não desabilita crafting.

## Regra para o Black Arcana

Consultar a escola efetiva do spell level quando necessário. Não duplicar blades, dano ou school-power application.

## Source

`PossessedSoulBladeSpell.java`, `BaseDoubleSchoolSpell.java` @ `Higurashi34m/Legendary-Spellbooks@62ced2f2b2693aa841251473cbbd726fdd928ed3`.

## Engenharia causal para perks — 17/10/2026

**Proveniência:** identificação física `legendary_spellbooks-1.21.1+neo-0.3.2.jar`, SHA-1 `bda5b1fbe50ad834a6a76ad36789743c1057ebf5` (30/30 registros). Corpo de método proveniente de `Higurashi34m/Legendary-Spellbooks@62ced2f2b2693aa841251473cbbd726fdd928ed3` com nível de evidência **SOURCE_CAUSALITY**. Não equivale a QA do pack Iron's 3.16.3/Legendary Monsters 2.2.2 nem a assinatura de adapter RPG homologada.

| Eixo | Algoritmo/fórmula em fonte | Política |
|---|---|---|
| Escola dinâmica | `PossessedSoulBladeSpell extends BaseDoubleSchoolSpell`; config inicialmente EVOCATION, `getChangeSchoolLevel()=maxLevel/2+1=3`. `isAnother(level)` true em níveis **3 e 4** muda `getSchoolType()` para BLOOD. No `getSpellPower`, seleciona school multiplier da escola efetiva além de SPELL_POWER global e config POWER_MULTIPLIER. | Perks por school devem consultar nível/escola efetiva; ⛔ não aplicar dois school multipliers simultaneamente. |
| Cast/custo | Nível 1–4, cooldown 20s, CastType.LONG, castTime=35 ticks, mana `125+25×(level−1)`, power neutro `6+4×(level−1)`. | Config e cast sob Iron's; nenhuma segunda cobrança. |
| Geometria / quantidade | `ringCount=min(level+2,10)` = **3/4/5/6**; `bladeCount=floor(1.5×ringCount)` = **4/6/7/9 por anel**, não total de projéteis. O loop externo executa ringCount vezes, logo até **12/24/35/54 SoulBladeEntity** por cast, condicionado ao ground raycast. A página anteriormente chamava 4/6/7/9 de blade count sem total, agora distinguido explicitamente. | Fan-out de até 54 entidades exige orçamento/caps. **SEM_HOOK_SEGURO** para tamanho do anel ou count individual. |
| Raio/posição | Ring i (começando em zero) tem raio `(i+1)×2` blocos; raio último **6/8/10/12 blocos**. `RaycastUtils.findGround(level,point,5,3)`; se null, **continue** só daquele ponto. | Não confundir estes raios de spawn com alcance de hitbox/dano de `SoulBladeEntity`. |
| Warmup/escala | Cada entidade recebe `warmup=i×2 ticks`, yaw face-out e `damage=(int)getSpellPower(level,caster)`, que **trunca** power efetivo. Recebe `isAnother(level)` boolean para variante Blood. | Projectile owner, hit timing, AOE, dano e DamageType de `SoulBladeEntity` estão no Legendary Monsters externo: **NÃO VERIFICADO** no JAR 2.2.2. |
| Lifecycle/dedup | Uma cast raiz gera múltiplas lâminas; client VFX usa cores diferentes conforme a escola. | ⛔ não creditar escola/magia extra às lâminas; Mastery por hits reais e cast único. |

**Âncoras:** [PossessedSoulBladeSpell](https://github.com/Higurashi34m/Legendary-Spellbooks/blob/62ced2f2b2693aa841251473cbbd726fdd928ed3/src/main/java/dev/higurashi/legendary_spellbooks/common/spells/blood/PossessedSoulBladeSpell.java#L32-L110); [BaseDoubleSchoolSpell — escola e power](https://github.com/Higurashi34m/Legendary-Spellbooks/blob/62ced2f2b2693aa841251473cbbd726fdd928ed3/src/main/java/dev/higurashi/legendary_spellbooks/api/spells/BaseDoubleSchoolSpell.java#L19-L55).

**QA:** presença de spell level 3 ou 4 e troca de school, atributos e resistências Blood vs Evocation, total 12/24/35/54, terreno/altura, PvP/claims, damage truncation, efeitos de Blood external, performance no servidor dedicado. **+0 IDs.**
