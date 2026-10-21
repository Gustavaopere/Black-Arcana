# Energy Beam

**Prova binária física (2026-10-13):** ✅ `COUNTED_EXACT` — `legendary_spellbooks:energy_beam`, classe `dev.higurashi.legendary_spellbooks.common.spells.lightning.EnergyBeamSpell` ([Java 21 #38453654179](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38453654179); [dossiê SHA-exato](../EXACT-BINARY-SPELLS-0.3.2.md)). Valores e mecânicas source-pinned; runtime/Survival ⚠️; +0 raízes.

- ID: `legendary_spellbooks:energy_beam`
- School: Lightning
- Levels: 1–3
- Min rarity: Legendary
- Cooldown: 45 s
- Cast-time field: 45 ticks
- Mana neutral: 400 / 450 / 500
- Spell power neutral: 25 / 30 / 35
- Beam duration: 50 / 60 / 70 ticks
- CastSource: somente Spellbook; scroll falha explicitamente
- Crafting: desabilitado
- Estado Black Arcana: `JÁ EXISTE / SEM ALTERAÇÃO PLANEJADA`

## Contract

Durante o casting o provider aplica movimento vertical ao caster e, na resolução, cria o Energy Beam com lifetime `min(40 + 10 × spellLevel,80)`. Damage/ticks/motion são provider-owned.

## Acquisition

Pool do Cloud Golem: níveis 1–3, weight 8.

## Regra para o Black Arcana

Não contornar o gate de CastSource, não criar um segundo beam tick e não reaplicar o impulso vertical.

## Source

`EnergyBeamSpell.java` @ source pin 0.3.2.

## Engenharia causal para perks — 17/10/2026

**Provenance:** `legendary_spellbooks:energy_beam` ID estático exato (JAR 0.3.2); código **SOURCE_CAUSALITY** `Higurashi34m/Legendary-Spellbooks@62ced2f2b2693aa841251473cbbd726fdd928ed3`. Esta spell instancia `net.miauczel.legendary_monsters.entity.AnimatedMonster.Projectile.EnergyBeamEntity`: **a geometria de impacto/damage tick pertence ao provider Legendary Monsters 2.2.2**, não demonstrada por esta classe.

| Eixo | Implementação source-pinned | Limites de integração |
|---|---|---|
| Admissão/custo | `canBeCastedBy` permite estritamente `CastSource.SPELLBOOK`, rejeitando Command/Scroll/other. Cooldown **45s**, `castTime=45 ticks`, mana `400+50×(level−1)`; power `25+5×(level−1)` antes dos modificadores do caster. | `⛔` não contornar CastSource, mana ou cooldown do Iron's. |
| Movimento durante cast | `onServerCastTick` fixa componente Y de `caster.setDeltaMovement` em **0.20** ao agachar e **0.25** sem agachar, preservando X/Z, define `hurtMarked=true`. É impulso **por tick de casting**, não habilidade separada de voo. | Sem seam safe de boost/fly speed; testar Epíc Fight, gravity e collisions. |
| Spawn/direção | `onCast` escolhe spawn por `GeometryUtils.getRelativePos(caster,1.0,-0.15,0)`, yaw/pitch via helpers; instancia `EnergyBeamEntity` com esses valores, `duration`, `getSpellPower` e flag final 0.0, chama `level.addFreshEntity`, e `caster.resetFallDistance()`. | Range físico, largura do beam, target cap, método damage e hitbox = **NÃO VERIFICADO** no source da spell. |
| Duração e status | `duration=min(40+level×10,80)` → **50/60/70 ticks** para level 1–3. Aplica `BEAM_EFFECT` ao caster com amplifier `min(spellLevel,5)` → 1/2/3; não é `ANNIHILATION` nem nova identidade. | `SEM_HOOK_SEGURO` para timer/multiprojétil sem contrato do entity. |
| Dano/tipo | Parâmetro `damage` do construtor externa é **getSpellPower**; `DamageSource` exata e event settlement do beam físico não foram observados aqui. | `⛔` não aplicar dano adicional baseado apenas no constructor argument. |
| Causalidade | Uma action pode mover caster por 45 ticks e manter beam por 50–70 ticks; side-effects não representam casts adicionais. | Dedup por spell cast e impacto aceito, não `onServerCastTick`. |

**Âncora:** [EnergyBeamSpell.java](https://github.com/Higurashi34m/Legendary-Spellbooks/blob/62ced2f2b2693aa841251473cbbd726fdd928ed3/src/main/java/dev/higurashi/legendary_spellbooks/common/spells/lightning/EnergyBeamSpell.java#L30-L96).

**QA:** evolução de altitude e colisões, CastSource (scroll/command), beam owner e orientação, loaded Legendary Monsters 2.2.2, dano/range/claims, cliente, unload e i-frames. Sem classificar tipo de dano ou alcance ofensivo sem inspecionar o JAR real. **+0 IDs/adapter.**
