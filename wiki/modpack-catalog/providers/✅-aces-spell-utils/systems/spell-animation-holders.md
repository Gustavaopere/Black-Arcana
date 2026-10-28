# ASSpellAnimations — 27 holders de animação

**Classe:** `spells/ASSpellAnimations.java`. **Tipo:** metadados `AnimationHolder` de apresentação de spells/combat; **não** 27 magias ou 27 registros de skills. **Estado:** ⚠️ source-pinned, sem certificação de interoperabilidade Epic Fight.

## Identidade Java → resource path

Todos são `new AnimationHolder(AcesSpellUtils.id(path), boolean)`; `AcesSpellUtils.MOD_ID=aces_spell_utils` no source. A coluna final reproduz o booleano do construtor, sem inferir significado não documentado.

| Constante Java | ResourceLocation | Bool |
|---|---|---|
| `ANIMATION_CLAP` | `aces_spell_utils:clap` | `true` |
| `ANIMATION_GAOLER_SUMMON` | `aces_spell_utils:gaoler_summon` | `true` |
| `ANIMATION_MALEVOLENT_HAND_SIGN` | `aces_spell_utils:malevolent_hand_sign` | `true` |
| `ANIMATION_MALEVOLENT_HAND_SIGN_RELEASE` | `aces_spell_utils:malevolent_hand_sign_release` | `true` |
| `ANIMATION_CHARGE_GUN` | `aces_spell_utils:charge_gun` | `true` |
| `ANIMATION_CHARGE_GUN_RELEASE` | `aces_spell_utils:charged_gun_release` | `true` |
| `ANIMATION_CHARGE_GUN_FULL` | `aces_spell_utils:full_gun_shoot` | `true` |
| `ANIMATION_SIMPLE_SHOOT` | `aces_spell_utils:simple_shoot` | `true` |
| `ANIMATION_CHARGED_GROUND_SLAM` | `aces_spell_utils:charged_ground_slam` | `true` |
| `ANIMATION_CONSTRUCT_SUMMON` | `aces_spell_utils:construct_summon` | `true` |
| `ANIMATION_WRATH_ROAR` | `aces_spell_utils:wrathful_roar` | `true` |
| `ANIMATION_DEFENSIVE_SWORD_STANCE_START` | `aces_spell_utils:sword_stance_start` | `true` |
| `ANIMATION_DEFENSIVE_SWORD_STANCE_FINISH` | `aces_spell_utils:sword_stance_finish` | `true` |
| `ANIMATION_POWERFUL_SWORD_SLASH` | `aces_spell_utils:powerful_sword_slash` | `true` |
| `ANIMATION_RIGHT_HORIZONTAL_SWORD_SLASH` | `aces_spell_utils:right_horizontal_slash_one_handed` | `true` |
| `ANIMATION_LEFT_HORIZONTAL_SWORD_SLASH` | `aces_spell_utils:left_horizontal_slash_one_handed` | `true` |
| `ANIMATION_RUDE_BUSTER_SLASH` | `aces_spell_utils:rude_buster_slash` | `true` |
| `ANIMATION_GROUND_FIST_SLAM` | `aces_spell_utils:ground_fist_slam` | `true` |
| `ANIMATION_SNOWGRAVE_START` | `aces_spell_utils:snowgrave_spell_cast_start` | `true` |
| `ANIMATION_SNOWGRAVE_STOP` | `aces_spell_utils:snowgrave_spell_cast_stop` | `true` |
| `ANIMATION_SPELL_PUNCH` | `aces_spell_utils:impact_punch` | `true` |
| `ANIMATION_OVERHEAD_SWING_START` | `aces_spell_utils:overhead_swing_start` | `true` |
| `ANIMATION_OVERHEAD_SWING_FINISH` | `aces_spell_utils:overhead_swing_finish` | `true` |
| `ANIMATION_RIGHT_HANDED_PUNCH` | `aces_spell_utils:right_handed_punch` | `true` |
| `ANIMATION_LEFT_HANDED_PUNCH` | `aces_spell_utils:left_handed_punch` | `true` |
| `ANIMATION_RAPID_PUNCH_LOOP` | `aces_spell_utils:punch_flurry` | `false` |
| `ANIMATION_SPIN_SLASH_LOOP` | `aces_spell_utils:spin_slash_loop` | `false` |

## Limites para perks, animação e Epic Fight

A classe fornece identificadores/holders; **não** especifica range, alvo, hitbox, dano, mana, cooldown ou duração. Não comprova que todos os paths possuem asset carregável no JAR físico nem que Epic Fight os aceita diretamente. O par `ANIMATION_CHARGE_GUN_RELEASE` → `charged_gun_release` é a grafia efetiva (não `charge_gun_release`). Os dois últimos holders têm bool `false`; não traduzir automaticamente isso para permissão de loop ou condição de interrupção sem conferir consumidor e contrato do Iron's.

**Fonte exata:** [`spells/ASSpellAnimations.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/spells/ASSpellAnimations.java). Próxima QA: assets, consumidor, prioridade/overrides, blending, multiplayer, sincronização servidor-cliente e compatibilidade Epic Fight 1.21.1.

**Proveniência:** AceTheEldritchKing/Aces_Spell_Utils @ `a0b2f4c2fcfa938c8e47239279c77c2ef82647ac`, source `1.2.7.2-1.21.1`. O catálogo físico referencia `aces_spell_utils-1.2.7.2-1.21.1.jar`, sem prova independente de paridade classfile. Build desta revisão usa Iron's `3.16.2`, versus pack `3.16.3`.

**Gate:** `source_pinned=true`; `mutating_hook=NOT_VERIFIED`; `physical_qa=NOT_TESTED`; `COMPLETE_PERK_READY=false`. Não gera spell registrado, proc, atributo, perk ou adapter novo. Black Arcana preserva seu runtime mágico; Iron's controla casting/mana/cooldown dos seus spells; RPG Skill Tree controla progressão somente via contrato real.
