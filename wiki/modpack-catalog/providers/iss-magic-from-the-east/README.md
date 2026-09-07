# ISS: Magic From The East — provider canônico

Status: `INSTALLED 1.1.5 / SOURCE-PINNED / 22 ACTIVE SPELLS / SYMMETRY 11/11 / SPIRIT 11/11 / PROVIDER 22/22 CATALOGED`

- **JAR do pack:** `iss_magicfromtheeast-1.1.5.jar`
- **Mod ID:** `iss_magicfromtheeast`
- **Version authority:** modlist atual + Notion + upstream `WarPhan78/ISS_MagicFromTheEast-1.21.x`
- **Source pin:** `13208302c9fdf5beb171a328558cbef07a25ba46`
- **`gradle.properties`:** Minecraft `1.21.1`, mod `1.1.5`
- **Iron's dependency declared upstream:** `1.21.1-3.16.2`; pack currently uses Iron's `3.16.3`.

## Registry exato 1.1.5

`MFTESpellRegistries` registra **22 spells ativos**:

- Symmetry: 11/11 catalogados
- Spirit: 11/11 catalogados

`LaunchSpell` e `QigongControllingSpell` permanecem comentados no registry e NÃO contam. A escola Dune também está comentada no `MFTESchoolRegistries`, com nota upstream para só ser habilitada quando seu desenvolvimento começar.

## Escolas próprias

- `iss_magicfromtheeast:symmetry`
- `iss_magicfromtheeast:spirit`

Ambas têm focus tags, school power, magic resist, cast sound e damage type próprios. Não são aliases temáticos de escolas do Iron's base.

## Symmetry — 11/11

`sword_dance`, `bagua_array_circle`, `dragon_glide`, `jade_judgement`, `jiangshi_invoke`, `underworld_aid`, `punishing_heaven`, `drapes_of_reflection`, `cloud_ride`, `nephrite_slash`, `jade_bullet`.

## Spirit — 11/11

`soul_catalyst`, `soul_burst`, `spirit_challenging`, `bone_hands`, `calamity_cut`, `kitsune_pack`, `revenant_of_honor`, `ashigaru_squad`, `phantom_charge`, `anchoring_kunai`, `splitting_shuriken`.

## Deduplicação — contracts ocupados

### Symmetry

Delayed sword swarm; anti-undead circle + damage-to-healing inversion; multi-hit jade dragon; falling judgement blade + AoE; triple Jiangshi summon; missing-health verdict circle; heavy Jade Executioner summon; projectile-reflection shield; rideable cloud; weapon-scaled slash + delayed crystal line; direct projectile + radial shockwave.

### Spirit

Multi-skull Soulburn volley; radial Spirit+Soulburn burst; ExtractedSoul linked proxy damage; durable self-healing Bone Hands summon; non-interruptible weapon-scaled line cut; Kitsune pack + mountable alpha; Spirit Samurai companion; mixed melee/ranged Ashigaru formation; advancing cavalry debuff wall; teleport-triggered damage-proxy soul; entity-hit-triggered radial shuriken split.

Esses contracts são provider-native first e não devem virar novos spells Black Arcana apenas com outro nome/VFX.

## QA estático relevante

Ver `TECHNICAL-AUDIT.md`. Há divergências comprovadas entre tooltip e runtime-path em Anchoring Kunai e Phantom Charge, além de findings de Cloud Ride/Soul Catalyst. Esses pontos ficam explicitamente pendentes de runtime QA; o catálogo não normaliza valores contraditórios.
