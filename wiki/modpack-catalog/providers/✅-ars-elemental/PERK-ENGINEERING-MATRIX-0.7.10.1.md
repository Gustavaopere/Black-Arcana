# Ars Elemental 0.7.10.1 — matriz de engenharia de perks por objeto

Status: ✅ **47/47 fichas de objeto** com classe source-located e IDs binários anteriormente confirmados; ⚠️ equivalência binária de implementação / config deploy / QA runtime não confirmadas; ⛔ nenhum adapter RPG validado.

**Fonte de identificação:** `ars_elemental-1.21.1-0.7.10.1.jar`, SHA-1 `a1e4021177aae0e16c1f7c6487a82f0b68bbade3`. Fonte Java factual `Alexthw46/Ars-Elemental@fe9d37e947c5fffd4f89a6ae4dd87ae52489b30d`; host Ars Nouveau 5.13.1 `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`. O source pin não é prova de equivalência de todos os bytes/implementações do JAR.

## 39 Glyph Parts

### 23 efeitos

| Ficha | Parâmetro ou cadeia causal localizada | Integração |
|---|---|---|
| [bubble-shield](glyphs/bubble-shield.md) | Mana Bubble: mana capability, 350 absorption cost config; buff downstream | ⚠️ executor/config; ⛔ adapter RPG |
| [cauterize](glyphs/cauterize.md) | dano aceito 3 → remove harmful milk-curable/allowlist | ⚠️ executor/config; ⛔ adapter RPG |
| [cavitate](glyphs/cavitate.md) | BubbleEntity → dano 8+3A → AABB 2+AOE + Soaked | ⚠️ executor/config; ⛔ adapter RPG |
| [charm](glyphs/charm.md) | mob max HP default 150; chance 10+5A e resistência por %vida | ⚠️ executor/config; ⛔ adapter RPG |
| [conflagrate](glyphs/conflagrate.md) | onFire e hit aceito → AABB 3+AOE, +60 fire ticks, dano secundário 75% | ⚠️ executor/config; ⛔ adapter RPG |
| [conjure-terrain](glyphs/conjure-terrain.md) | count(Amplify) decide material; preview da próxima parte; world helper | ⚠️ executor/config; ⛔ adapter RPG |
| [create-geyser](glyphs/create-geyser.md) | altura max(0,4+2A), duração 20*(5+T), entity water/lava | ⚠️ executor/config; ⛔ adapter RPG |
| [discharge](glyphs/discharge.md) | Shocked/Lure, +30% via Lure; energy 25% e dano x1.1 por armadura | ⚠️ executor/config; ⛔ adapter RPG |
| [envenom](glyphs/envenom.md) | POISON prévio soma amplifier/2 ao SpellStats antes de VENOM | ⚠️ executor/config; ⛔ adapter RPG |
| [life-link](glyphs/life-link.md) | duas EntityCarryMEI, owner/inverse Sensitive, duração por helper | ⚠️ executor/config; ⛔ adapter RPG |
| [mist-cloud](glyphs/mist-cloud.md) | duration=(int)(100+20T); radius=3+AOE; entity persistente | ⚠️ executor/config; ⛔ adapter RPG |
| [nullify-defense](glyphs/nullify-defense.md) | invulnerableTime=0; recipe default-disabled; sem dano | ⚠️ executor/config; ⛔ adapter RPG |
| [oxidize](glyphs/oxidize.md) | RUST entidade; bloco AOE com setBlock(pos original) sob chance 0.1 | ⚠️ executor/config; ⛔ adapter RPG |
| [phantom-grasp](glyphs/phantom-grasp.md) | 3+3A; inverte cura/dano, player exhaustion 2.5*(1.5+A) | ⚠️ executor/config; ⛔ adapter RPG |
| [poison-spores](glyphs/poison-spores.md) | POISON/HUNGER/VENOM gate; 6+2.5A, AOE3+; blossom chance 5% | ⚠️ executor/config; ⛔ adapter RPG |
| [rage](glyphs/rage.md) | Mob only; potion duration getter base 60, extend 120 | ⚠️ executor/config; ⛔ adapter RPG |
| [sliding](glyphs/sliding.md) | registro glyph_slip_feet; status ICE_SLIDE | ⚠️ executor/config; ⛔ adapter RPG |
| [spark](glyphs/spark.md) | 3+1.5A+2 wet; Shocked/Lure mesmo se attemptDamage não aceito | ⚠️ executor/config; ⛔ adapter RPG |
| [spike](glyphs/spike.md) | spike chão / falling spike, 8+2.5A; maxFallDamage config40 | ⚠️ executor/config; ⛔ adapter RPG |
| [summon-bee](glyphs/summon-bee.md) | 3+Split bees; duration20*(60+60T); Summon Rework gate | ⚠️ executor/config; ⛔ adapter RPG |
| [summon-slime](glyphs/summon-slime.md) | 3+Split slimes; size (int)(2+A), focus variant | ⚠️ executor/config; ⛔ adapter RPG |
| [water-jet](glyphs/water-jet.md) | 1+Split jets; seleção próximo/randomizado AABB10; 1 marker entity | ⚠️ executor/config; ⛔ adapter RPG |
| [watery-grave](glyphs/watery-grave.md) | Extend→status; else deltaY <= -1; air−50*(3+A), zombie conversion | ⚠️ executor/config; ⛔ adapter RPG |

### 2 cast methods + 2 propagators

| Ficha | Parâmetro ou cadeia causal localizada | Integração |
|---|---|---|
| [arc-projectile](glyphs/arc-projectile.md) | Cast Method: 1+Split, gravity, velocity max(0.2,1+acc/2), TTL60s | ⚠️ executor/config; ⛔ adapter RPG |
| [homing-projectile](glyphs/homing-projectile.md) | Cast Method: 1+Split, filters, velocity max(0.2,0.5+acc/5), TTL30s | ⚠️ executor/config; ⛔ adapter RPG |
| [propagate-arc](glyphs/propagate-arc.md) | Propagator: 1+Split arc entities; copyResolver, Reset limit | ⚠️ executor/config; ⛔ adapter RPG |
| [propagate-homing](glyphs/propagate-homing.md) | Propagator: 1+Split homing entities; filters, copyResolver | ⚠️ executor/config; ⛔ adapter RPG |

### 12 filtros (6 predicados e 6 negativos)

Cada filtro usa `ElementalAbstractFilter`, typeIndex=15; `inverted != super.shouldAffect(...)`; `onResolve` cancela contexto quando o predicado calculado falha. Isso não é uma ação ofensiva ou cast independente.

[aerial](glyphs/aerial.md) · [not-aerial](glyphs/not-aerial.md) · [aquatic](glyphs/aquatic.md) · [not-aquatic](glyphs/not-aquatic.md) · [fiery](glyphs/fiery.md) · [not-fiery](glyphs/not-fiery.md) · [insect](glyphs/insect.md) · [not-insect](glyphs/not-insect.md) · [summon](glyphs/summon.md) · [not-summon](glyphs/not-summon.md) · [undead](glyphs/undead.md) · [not-undead](glyphs/not-undead.md)

## 8 rituais

| Ritual | Cadeia causal resumida | Status |
|---|---|---|
| [ritual_attraction](rituals/cards/ritual_attraction.md) | 10 ticks, AABB radius 8+Earth Essences, motion, Source 10 | ✅ source-located; ⚠️ QA/Source real; ⛔ adapter |
| [ritual_detection](rituals/cards/ritual_detection.md) | 20 ticks progress, 15 progress, Monster AABB128, Glowing12000, Source250 | ✅ source-located; ⚠️ QA/Source real; ⛔ adapter |
| [ritual_pollination](rituals/cards/ritual_pollination.md) | 60/160-tick backoff, pollinating Bee ticks+100, Source10 | ✅ source-located; ⚠️ QA/Source real; ⛔ adapter |
| [ritual_repulsion](rituals/cards/ritual_repulsion.md) | 20/80-tick backoff, mobs/undead+Bone, REPEL200 ticks, Source10 | ✅ source-located; ⚠️ QA/Source real; ⛔ adapter |
| [ritual_squirrels](rituals/cards/ritual_squirrels.md) | Starbuncle AABB15/30, interval config default 600, buffs2400, Source150 | ✅ source-located; ⚠️ QA/Source real; ⛔ adapter |
| [ritual_tesla_coil](rituals/cards/ritual_tesla_coil.md) | 100 ticks, Living AABB(5,3,5), LightningEntity, Source500 | ✅ source-located; ⚠️ QA/Source real; ⛔ adapter |
| [ritual_archwood_forest](rituals/cards/ritual_archwood_forest.md) | ConjureBiomeRitual radius7+gems, 1 place/tick, Source50/5 placements | ✅ source-located; ⚠️ QA/Source real; ⛔ adapter |
| [ritual_archwood_forestation](rituals/cards/ritual_archwood_forestation.md) | FeaturePlacementRitual radius7+gems, mixed archwood tree/pods, variant state | ✅ source-located; ⚠️ QA/Source real; ⛔ adapter |

## Riscos relevantes para perks originais

- `EffectEnvenom` modifica `SpellStats` via setter em runtime; alterações em `EffectResolveEvent.Pre` devem observar mutações subsequentes e não apenas stats no instante do evento.
- `EffectConjureTerrain` lê `getBuffCount(Amplify)` para escolher material; editar apenas `setAmpMultiplier` não dá equivalência.
- `EffectOxidize` percorre `pos1` mas usa `setBlockAndUpdate(pos, ...)` no source pin: possível divergência entre checagem/posição alterada, **não** bug físico confirmado.
- `EffectCharm` usa RNG/HP cap e é player-only; não promover controle de mob como domínio de permissão do RPG.
- `EffectDischarge` faz extração real de energia das armaduras de alvo; não duplicar charges/retornos quando efeitos derivados forem observados.
- `MethodHomingProjectile` filtra aliados, summons, pets, invisíveis e players sem Sensitive; alterar aquisição de alvo exigiria integração e testes PvP.
- `RitualArchwoodForestation` altera variável `biomeType` durante `canConsumeItem`; salvar/carregar variante e causalidade do ritual precisam de QA.
- Os efeitos mundo/bloco (Conjure Terrain, Oxidize, outros) são provider-owned; a Black Arcana usa `WorldEffectPolicy` exclusivamente para suas próprias magias. Fontes com `destroyRespectsClaim` local e sem ele não garantem status de claim do runtime completo.
- `MethodCarianPhalanx` é dev-only (`!isProduction`) e permanece **excluído** dos 39. Receita de Nullify Defense é source-default-disabled. A existência no JAR não é acesso garantido em Survival.

## Critérios pendentes

⚠️ Config física instalada, prova method/JAR exata (quando necessária), protected claims, cheats/fake players, multiplayer, lifecycle de entidades auxiliares, scheduler e ajustes de orçamento. ⛔ API/adapters do RPG para progressão, perks, Mastery e gates sem testes de causalidade/cost parity. Nenhum teste CI/Survival foi realizado por esta edição documental.

[README](README.md) · [identidades binárias](EXACT-BINARY-GLYPHS-RITUALS-0.7.10.1.md) · [padrão global](../../meta/PERK-READY-TECHNICAL-STANDARD.md).
