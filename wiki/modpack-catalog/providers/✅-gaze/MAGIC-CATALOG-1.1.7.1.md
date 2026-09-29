# Gaze 1.1.7.1 — catálogo canônico de magias e ritos

## Escopo

Ledger objeto-a-objeto do conteúdo mágico metricamente relevante confirmado no artefato físico exato `gaze-1.1.7.1.jar` (SHA-1 `a8cb3190bde157f78160ce65c202ce2d47fb2041`).

O artefato fecha **27 ações mágicas identificáveis** no escopo atual: **1 spell Gaze-owned para Iron's + 26 Spirit Rites**. O spell é `COUNTED_EXACT`; os 26 rites continuam `CONDITIONAL` apenas porque o valor efetivamente implantado de `disableGazeRites` não está presente na evidência do projeto.

## Spell standalone

| Registry identity | Substrato | Gate comprovado | Estado |
|---|---|---|---|
| `SOULWARD_SHIELD` | Iron's Spells 'n Spellbooks | `irons_spellbooks` presente no pack | `COUNTED_EXACT` |

O artefato expõe `SOULWARD_SHIELD` como `Supplier<AbstractSpell>` no registry de compatibilidade do Gaze. Nenhum disable gate específico do Gaze foi observado para esse spell. Mana, cooldown, nível, escola, fórmulas e aquisição detalhada permanecem provider-owned salvo evidência específica posterior.

## Spirit Rites

Todos os 26 holders abaixo são identidades player-facing comprovadas pelo registry e pela superfície de progressão do Gaze. O gate comum é o mesmo: `disableGazeRites` precisa estar comprovadamente `false` na configuração efetivamente implantada para promoção semântica estrita.

| # | Rite identity | Estado |
|---:|---|---|
| 1 | `gaze_lesser_arcane_rite` | `EXACT_REGISTRY / CONFIG_CONDITIONAL` |
| 2 | `gaze_greater_arcane_rite` | `EXACT_REGISTRY / CONFIG_CONDITIONAL` |
| 3 | `gaze_lesser_sacred_rite` | `EXACT_REGISTRY / CONFIG_CONDITIONAL` |
| 4 | `corrupt_gaze_lesser_sacred_rite` | `EXACT_REGISTRY / CONFIG_CONDITIONAL` |
| 5 | `gaze_greater_sacred_rite` | `EXACT_REGISTRY / CONFIG_CONDITIONAL` |
| 6 | `corrupt_gaze_greater_sacred_rite` | `EXACT_REGISTRY / CONFIG_CONDITIONAL` |
| 7 | `gaze_lesser_aerial_rite` | `EXACT_REGISTRY / CONFIG_CONDITIONAL` |
| 8 | `corrupt_gaze_lesser_aerial_rite` | `EXACT_REGISTRY / CONFIG_CONDITIONAL` |
| 9 | `gaze_greater_aerial_rite` | `EXACT_REGISTRY / CONFIG_CONDITIONAL` |
| 10 | `corrupt_gaze_greater_aerial_rite` | `EXACT_REGISTRY / CONFIG_CONDITIONAL` |
| 11 | `gaze_lesser_aqueous_rite` | `EXACT_REGISTRY / CONFIG_CONDITIONAL` |
| 12 | `corrupt_gaze_lesser_aqueous_rite` | `EXACT_REGISTRY / CONFIG_CONDITIONAL` |
| 13 | `gaze_greater_aqueous_rite` | `EXACT_REGISTRY / CONFIG_CONDITIONAL` |
| 14 | `corrupt_gaze_greater_aqueous_rite` | `EXACT_REGISTRY / CONFIG_CONDITIONAL` |
| 15 | `gaze_lesser_earthen_rite` | `EXACT_REGISTRY / CONFIG_CONDITIONAL` |
| 16 | `corrupt_gaze_lesser_earthen_rite` | `EXACT_REGISTRY / CONFIG_CONDITIONAL` |
| 17 | `gaze_greater_earthen_rite` | `EXACT_REGISTRY / CONFIG_CONDITIONAL` |
| 18 | `corrupt_gaze_greater_earthen_rite` | `EXACT_REGISTRY / CONFIG_CONDITIONAL` |
| 19 | `gaze_lesser_infernal_rite` | `EXACT_REGISTRY / CONFIG_CONDITIONAL` |
| 20 | `corrupt_gaze_lesser_infernal_rite` | `EXACT_REGISTRY / CONFIG_CONDITIONAL` |
| 21 | `gaze_greater_infernal_rite` | `EXACT_REGISTRY / CONFIG_CONDITIONAL` |
| 22 | `corrupt_gaze_greater_infernal_rite` | `EXACT_REGISTRY / CONFIG_CONDITIONAL` |
| 23 | `gaze_lesser_wicked_rite` | `EXACT_REGISTRY / CONFIG_CONDITIONAL` |
| 24 | `corrupt_gaze_lesser_wicked_rite` | `EXACT_REGISTRY / CONFIG_CONDITIONAL` |
| 25 | `gaze_greater_wicked_rite` | `EXACT_REGISTRY / CONFIG_CONDITIONAL` |
| 26 | `corrupt_gaze_greater_wicked_rite` | `EXACT_REGISTRY / CONFIG_CONDITIONAL` |

## Conteúdo mágico identificado mas excluído da métrica de ações

O artefato também fecha dois `GeasEffectType` Gaze-owned — `pact_of_encroaching` e `domain_of_swords` — e oito rune items. Eles permanecem catalogados como superfícies mágicas do provider, mas adicionam **0** ao numerador de spell/rite actions pela definição semântica canônica: Geas effect types são efeitos/status-like, e runes são itens/equipamentos/passivos.

## Config authority

`disableGazeRites` é um boolean COMMON do provider. O default de código é `false`, porém defaults não substituem a configuração implantada. Sem cópia autoritativa do COMMON config efetivo, os 26 rites não são promovidos para `COUNTED_EXACT`.

## Proveniência e autoridade

Fonte interna primária: `EXACT-1.1.7.1-ARTIFACT-AUDIT.md`, baseado em artefato hash-matched. Gaze permanece All Rights Reserved; este catálogo retém somente identidades, tipos, gates e relações necessárias à interoperabilidade/contagem clean-room.

Malum continua authority do runtime de Spirit Rites/Geas e dos recursos espirituais; Iron's continua authority do seu framework/settlement; Gaze possui as identidades addon que registra; Black Arcana não duplica nenhum desses pipelines.
