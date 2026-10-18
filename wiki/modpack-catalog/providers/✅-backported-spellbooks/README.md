# Backported Spellbooks — physical 0.1.2 release / embedded metadata 0.1.0

## Gate NeoForge/Mixin do host 1.1.7.10 (18/10/2026)

✅ [#39164766070](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39164766070) **SUCCESS** com hash SHA-256 publisher fixado, **12/12** testes de manifesto + **10/10** de movimento, zero desvios. [Dossiê de configuração compilada](EXACT-BINARY-VANILLABACKPORT-MIXIN-DECLARATION-1.1.7.10.md): `neoforge.mods.toml` vincula `vanillabackport.mixins.json` com `required=true`, `JAVA_21` e `defaultRequire=1`; lista comum (não client-only) declara `EntityMixin`, `LivingEntityMixin`, `RangedAttributeMixin` e três classes físicas no JAR. Dependências `neoforge[21.1,)`, `minecraft[1.21.1,)`, `platform[1.3.3,)`, todas `side=BOTH`; Platform 1.3.3 figura na modlist #445. **Mixin declarado ≠ runtime aplicado**; loader completo, SHAs locais, atributos resolvidos, gameplay e APIs externas permanecem ⚠️/⛔. +0 magias e +0 adapters.

## Host 1.1.7.10 — bounciness limitada a 1.0 (18/10/2026)

✅ [Java21 #39156441117](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39156441117) verificou publisher `VanillaBackport-neoforge-1.21.1-1.1.7.10.jar` SHA-256 `ecd807ac358e243ede17819455788c7b7a0ce5e0af4aecee82c1c62c586d818d` (54.902.084 bytes), 10/10 autotestes e zero desvios. O [dossiê cross-host](EXACT-BINARY-VANILLABACKPORT-MOBILITY-HOST-1.1.7.10.md) confirma os três `RangedAttribute`: `minecraft:bounciness` default 0, teto **1.0**; `air_drag_modifier`/`friction_modifier` default 1, teto 2048; mixins compilados de colisão, drag e atrito, cuja fórmula é `clamp(1−(1−rawFriction)*modifier,0,1)`. **Teto registral ≠ prova de valor final em player**; +2.5 das Slime Boots e +0.5 da magia não podem ser tratados como fatores físicos finais sem execução do host. SHA da instalação real desconhecido. +0 magias/perks/adapters, integração ⚠️/⛔.

## Slime Boots — modificadores de equipamento e cancelamento de queda (18/10/2026)

✅ [Java21 #39153448024](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39153448024) **SUCCESS**, 11/11 testes, SHA-1 publisher igual ao instalado, [JSON #12145728990](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39153448024/artifacts/12145728990). [Dossiê dedicado](EXACT-BINARY-SLIME-BOOTS-FALL-0.1.2.md): atributos declarados `JUMP_STRENGTH +0.1`, `FRICTION_MODIFIER +0.3`, `BOUNCINESS +2.5`, `AIR_DRAG_MODIFIER -0.5` com operações compiladas; handler seleciona Player com `SLIME_BOOTS` em `FEET` antes de `setCanceled(true)`. Nenhuma referência direta ao status da magia ou ao cooldown nesse método. Tooltip com fórmula de cooldown não demonstra período de recarga no evento. **Equipamento != 7ª magia**, nenhuma nova raiz. Gameplay/evento realmente invocado e stacking com `Slime Aspect` continuam ⚠️, mutação via perk ⛔.

## Slime Aspect — sexto feitiço com consumer compilado (18/10/2026)

✅ [Java 21 #39149742796](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39149742796) **SUCCESS**, 9/9 autotestes, SHA1 do publisher igual ao físico, `PASS_BACKPORTED_012_SLIME_BOUNDED_BYTECODE`. [Dossiê exato](EXACT-BINARY-SLIME-ASPECT-0.1.2.md): `onCast` contém duração `int(getSpellPower*20)`, amp `level-1` e um `LivingEntity.addEffect`; supplier `ModMobEffects.lambda$static$2` registra BOUNCINESS/JUMP_STRENGTH/AIR_DRAG_MODIFIER em operações ADD_VALUE/ADD_MULTIPLIED_TOTAL com operandos `double` derivados de constantes float. **Estado atual: 6/6 IDs, 6/6 fichas, 6/6 spells com uma prova binária específica delimitada (100% apenas dessa métrica).** Nenhum atributo efetivo, player, perk/hook ou config física validada. **Os 5/6 abaixo são o checkpoint anterior.** [Artefato JSON #12144269318](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39149742796/artifacts/12144269318).

## Sulfur Bomb e Pale Thorn: parâmetros no JAR exato (18/10/2026)

✅ [Java21 #39133252975](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39133252975) **SUCCESS** — 10/10 autotestes, hash físico/publisher conferido, `PASS_BACKPORTED_012_BOMB_THORN_BOUNDED_BYTECODE` sem desvios, [JSON #12138732504](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39133252975/artifacts/12138732504). [Dossiê de geometria, dano e targeting](EXACT-BINARY-BOMB-THORN-0.1.2.md): Sulfur Bomb tem raio `3+entityPowerMultiplier`, coeficiente de dano da nuvem `0.185`, expansão AABB seguida de distância²/`canHitEntity`/LOS, queda radial de dano, cloud com duração configurada em 200 ticks e contador de três colisões de bloco; Pale Thorn tem alcance `15.0f`, raycast `0.15f`, duração `(int)(spellPower*100)`, fontes de dano Nature/Eldritch e VFX descartada após `tickCount>30`. **Limite:** opcode não é efeito observado, nem demonstra segurança de PvP/claims, dano HP final ou hook externo de alteração.

**Cobertura agora:** 6/6 IDs estáticos ✅, 6/6 fichas de parâmetros source-pinned ✅, **5/6 spells com ao menos um caminho de código delimitado certificado em classfile** (as três anteriores + Sulfur Bomb + Pale Thorn). Slime Aspect aguarda prova de código de efeitos. +0 novas magias, +0 adapters.


## Três consumidores compilados delimitados (18/10/2026)

✅ [Java21 #39131725388](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39131725388) **SUCCESS**, hash publisher `747847c1f38c73250ebac05ea06b41a381187850` igual ao físico e **8/8 autotestes**, `PASS_BACKPORTED_012_BOUNDED_COMPILED_PERK_CONSUMERS` sem desvios; JSON [artefato 12138535465](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39131725388/artifacts/12138535465). [Dossiê de três métodos físicos](EXACT-BINARY-PERK-CONSUMERS-0.1.2.md): SulfurCloudProjectile faz dois `super.tick` compilados; SulfurReleaseSpell.getWitherAmplifier devolve `spellLevel-2`; ResinSpraySpell.onCast contém o fluxo host-native de sessão `MagicData` com reativação e alternativa de criação/registro de projétil. **Aprovou inspeção de callsites, não gameplay, duração efetiva, amp normalizado ou API de extensão.** 6/6 IDs de spells catalogados, 3/6 com foco neste novo gate, +0 roots/adapters.


## Atualização da catalogação técnica de perks (18/10/2026)

✅ [Matriz source-pinned 6/6](PERK-CAUSAL-SOURCE-MATRIX-0.1.2.md) e [seis fichas individuais enriquecidas](spells/README.md) com valores declarativos de rarity/max level/cooldown, cast type/time, mana defaults, `getSpellPower`, dano, área/alcance, geometria, lifecycle de projéteis/effects, causalidade e riscos de reexecução. A nova prova deriva do source público exato **`RedReaper28/BackportedSpellbooks-1.21.1@07cb65efca0c264762a21c2d6bce0f83e3947226`**, que é **alinhado à data da publicação, sem equivalência binária de implementação demonstrada**. A identidade das 6/6 spells continua ✅ pelo JAR publisher hash-matched, [Java21 #38318268989](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38318268989). **Não** inferir mana debitada, cooldown efetivo, runtime/config, hitbox do cone nem extensão segura de perks; ⚠️/⛔ até host Iron's 3.16.3 e full-modpack QA. Global atualmente com piso histórico 1.857 semânticos / 1.855 estritos, denominador final aberto, **+0** novas raízes.


**Nova prova física (2026-10-12):** [JAR 0.1.2, seis spells registradas](EXACT-BINARY-SPELLS-0.1.2.md), [auditoria Java 21 #38318268989](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38318268989). SHA físico/publicador igual; `COUNTED_EXACT` somente para registro estático 6/6. Campanha 7/39 exatos / 32/39 pendentes; +0 novos, 1851/1849 preservados. Metadata interno 0.1.0 permanece distinto. Sem gameplay/config/Survival aprovado.

Status: `EXACT PHYSICAL ARTIFACT + EXACT PUBLISHER 0.1.2 RELEASE / RELEASE-DAY OFFICIAL SOURCE CEILING / 6 IRON'S SPELL REGISTRATIONS / 1 SCHOOL / CONTENT+WORLDGEN+EQUIPMENT PROCS / EMBEDDED VERSION MISMATCH PRESERVED / BYTE+FULL-PACK QA FAIL-CLOSED`

## Installed identity

- physical JAR: `backportedspellbooks-0.1.2.jar`
- mod id: `backportedspellbooks`
- display name: `Backported Spellbooks`
- embedded/runtime metadata version: **`0.1.0`**
- physical SHA-1: `747847c1f38c73250ebac05ea06b41a381187850`
- Minecraft: `1.21.1`
- loader: NeoForge
- physical snapshot pack loader: NeoForge `21.1.250` (Black Arcana build baseline `21.1.248`)

The filename/release label and embedded metadata disagree. This catalog preserves both layers and does not normalize one into the other.

## Publisher release identity

CurseForge project/file `1543731 / 8158731` publishes `backportedspellbooks-0.1.2.jar` for NeoForge 1.21.1 on 2026-05-28. The exact 0.1.2 changelog adds:

- Miasmic Staff;
- Quicksilver Spellbook;
- Slime Boots;
- four new spells: Slime Aspect, Sulfur Clouds, Sulfur Bomb and Sulfur Release;
- Corroded Fossils and Quicksilver ore content in Sulfur Caves.

The project page labels the distributed project MIT and server-side. The publisher description is older than the exact file changelog and is not used as a complete current inventory.

## Official source ceiling

Official repository: `RedReaper28/BackportedSpellbooks-1.21.1`.

The repository has no useful exact-version tag/release. Its terminal commit is `07cb65efca0c264762a21c2d6bce0f83e3947226`, dated 2026-05-28, the same calendar day as CurseForge file 8158731. That source still declares `mod_version=0.1.0`, matching the physical embedded metadata rather than the publisher filename.

The prior May 18 source point `4149c37c77dda46ab0a8697c438101e07ff14d19` exposes two spells. The May 28 source head exposes six. The four added spell registrations are the same four identities named as new in the 0.1.2 publisher changelog. This release-day source alignment is strong semantic evidence but is **not** promoted to byte-for-byte identity with the physical JAR.

## Semantic spell inventory

The exact physical JAR now independently establishes six static Iron's spell registrations, with the same IDs as the release-day official source:

1. `backportedspellbooks:slime_aspect`
2. `backportedspellbooks:sulfur_bomb`
3. `backportedspellbooks:sulfur_clouds`
4. `backportedspellbooks:sulfur_release`
5. `backportedspellbooks:pale_thorn`
6. `backportedspellbooks:resin_spray`

Individual [spell cards](spells/README.md) document these six identities and keep source-only mechanics separate from physical registry proof.

The release-day source additionally registers one provider school: `backportedspellbooks:pale_flora`; this school was not the object of the six-spell binary-proof gate.

These are provider spell identities executed through Iron's spell infrastructure. Iron's remains authority for cast state, spell configuration plumbing, mana settlement, cooldown settlement and its network/runtime pipeline. Backported Spellbooks owns the semantic spell definitions and provider effects/projectiles/content attached to them.

Black Arcana must not copy the six spells into its own registry merely because their themes overlap BA domains, and it must not route BA-native casts through Iron's solely to inherit this addon.

## Closed provider surface at the source ceiling

Observed registrations/resources include:

- 6 spells;
- 1 school;
- 15 explicit non-block item registrations plus 4 block items = 19 item registry objects;
- 4 blocks;
- 5 entity types;
- 4 mob effects;
- 2 particles;
- 1 fluid and 1 fluid type;
- 19 recipe JSONs in the inspected source tree;
- 2 configured ore features, 2 placed ore features and 2 NeoForge biome modifiers;
- 0 mixin configurations;
- no provider custom payload registration observed;
- no provider-owned persistent player/world subsystem observed.

Asset-only names are not promoted to registry identities unless an actual registration surface exists.

## Worldgen boundary

Both exact biome modifiers target `minecraft:sulfur_caves` at `underground_ores`:

- `backportedspellbooks:corroded_fossil_ore_placed`;
- `backportedspellbooks:quicksilver_ore_placed`.

This agrees with the publisher's 0.1.2 note that the two ores appear in Sulfur Caves. Vanilla Backport remains authority for the referenced Sulfur Caves host content. Black Arcana must not synthesize that biome or substitute its own worldgen when the host is absent.

## Dependency evidence boundary

Exact source metadata formally declares only NeoForge `[21.1.216,)` and Minecraft `[1.21.1]` for the addon. However, the source directly imports and builds against Iron's Spells, Vanilla Backport and selected Ace's Spell Utils APIs; `build.gradle` also carries several development dependencies.

Therefore:

- Iron's / Vanilla Backport / Ace's are **source-level/build/runtime expectations observed in code**, not promoted into fabricated `neoforge.mods.toml` dependency declarations;
- physical presence of those providers is recorded separately;
- missing undeclared hosts must fail closed rather than being replaced by Black Arcana fallbacks.

## Equipment/proc boundary

Observed server-relevant provider behavior includes:

- Miasma Staff: post-damage proc that applies Sulfuric Poison for qualifying Nature/Hydro magic damage, with item cooldown handling;
- Garden Rapier: post-damage provider proc including a nature blastwave/Resin Poison path;
- Slime Boots: provider fall-event cancellation while equipped;
- Quicksilver Spellbook and Pale Guide Spellbook: Iron's spellbook objects whose attributes modify host casting/mana/stat surfaces.

These are provider equipment/proc semantics, not Black Arcana casts. BA Backlash or other BA damage must not be deliberately routed through these procs to create an offensive proc chain.

## Black Arcana authority result

Black Arcana retains its single server-authoritative cast pipeline, targeting, transactional costs, BA cooldowns/charges, hazards, rituals, Corruption, Strain, Arcane Danger, Backlash causality and `WorldEffectPolicy`.

Iron's retains its own casting/mana/cooldown runtime. Backported Spellbooks owns its addon spell/content identities and equipment procs. Vanilla Backport owns the referenced host content. Ace's owns its imported utility/attribute surfaces. RPG Skill Tree receives no magic-runtime authority from any of these relationships.

## Evidence ceiling / remaining QA

Still fail-closed:

- byte-for-byte source↔physical-JAR reproducibility;
- exact publisher ↔ physical JAR SHA equality and six-class spell-registry static parity are **now verified** in [run #38318268989](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38318268989); this is not proof of all resources or functional source↔binary equivalence;
- complete physical-JAR resource/behavior parity with release-day source remains unverified;
- runtime compatibility of source baseline NeoForge 21.1.216 / Iron's 3.15.4 against physical NeoForge 21.1.250 / Iron's 3.16.3;
- behavior if undeclared Vanilla Backport / Iron's / Ace's dependencies are absent or change API;
- full-modpack worldgen/recipe reload and server/client behavior;
- Slime Boots tooltip cooldown language versus the observed unconditional fall-event cancellation path;
- license reconciliation for reuse.

## License / clean-room

CurseForge labels the project MIT, while the release-day source `gradle.properties` declares `All Rights Reserved`. This conflict is retained. Source/data inspection is factual and read-only for cataloging/interoperability. No code, assets, models, textures, sounds or implementation are copied or adapted into Black Arcana.