# ISS: Magic From The East 1.1.5 — 22 feitiços binários SHA-exatos

**✅ `COUNTED_EXACT` para 22/22 inscrições estáticas**: 11 Symmetry e 11 Spirit; **+0 novas raízes semânticas** (inventário prévio já incluía 22). Campanha de 39 providers **20/39 exatos / 19/39 pendentes**; mínimos estritos **1857 global / 1855 escopo** inalterados. Runtime, configuração e Survival **⚠️**.

## Autoridade do JAR e evidência reproduzível

- Modlist física sibling posição **#346**: `iss_magicfromtheeast-1.1.5.jar`, mod ID `iss_magicfromtheeast`, SHA-1 `e3552ea6b7b32b843c48bf0d857237d4b7129ab0`, NeoForge 1.21.1.
- [CurseForge file 7385201](https://www.curseforge.com/minecraft/mc-mods/magic-from-the-east/files/7385201), **1680780 bytes**, SHA-1 `e3552ea6b7b32b843c48bf0d857237d4b7129ab0` = registro físico.
- [Primeira auditoria Java 21 #38449337411](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38449337411) SUCCESS (fingerprint + enumeração); [prova estática Java 21 #38449995162](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38449995162) **SUCCESS** (22 classes, IDs literais, escolas e bootstrap).
- Workflow inspecionado permanece isolado em [`audit/iss-mfte-115-20261013`](https://github.com/Gustavaopere/Black-Arcana/tree/audit/iss-mfte-115-20261013); nenhum JAR nem código de terceiros incorporado ao runtime Black Arcana.

## Registry e bootstrap no bytecode

- `net.warphan.iss_magicfromtheeast.ISS_MagicFromTheEast` invoca `MFTESpellRegistries.register`.
- `net.warphan.iss_magicfromtheeast.registries.MFTESpellRegistries` usa `DeferredRegister<AbstractSpell>`, `SpellRegistry.SPELL_REGISTRY_KEY`, namespace `iss_magicfromtheeast` e wrapper `registerSpell(AbstractSpell)`.
- O inicializador realiza **22** chamadas de registro incondicionais na ordem abaixo, com **zero desvios condicionais** no bloco de declaração inspecionado.
- O construtor de cada classe fornece duas strings literais para o construtor de `ResourceLocation`, armazenadas em `spellId`; `getSpellResource()` retorna esse campo. A prova não presume que as strings apareçam diretamente no getter.
- As 11 classes Symmetry usam `MFTESchoolRegistries.SYMMETRY_RESOURCE`; as 11 classes Spirit usam `MFTESchoolRegistries.SPIRIT_RESOURCE` na configuração padrão compilada. Config efetiva em jogo ainda não foi certificada.

## Identidades exatas: 11 Symmetry + 11 Spirit

| # | Nome catalogado | ID compilado | Classe física e escola | Ficha |
|---:|---|---|---|---|
| 1 | Sword Dance | `iss_magicfromtheeast:sword_dance` | `symmetry.SwordDanceSpell` | [Ficha](symmetry/sword-dance.md) |
| 2 | Bagua Array Circle | `iss_magicfromtheeast:bagua_array_circle` | `symmetry.BaguaArrayCircleSpell` | [Ficha](symmetry/bagua-array-circle.md) |
| 3 | Dragon Glide | `iss_magicfromtheeast:dragon_glide` | `symmetry.DragonGlideSpell` | [Ficha](symmetry/dragon-glide.md) |
| 4 | Jade Judgement | `iss_magicfromtheeast:jade_judgement` | `symmetry.JadeJudgementSpell` | [Ficha](symmetry/jade-judgement.md) |
| 5 | Jiangshi Invoke | `iss_magicfromtheeast:jiangshi_invoke` | `symmetry.JiangshiInvokeSpell` | [Ficha](symmetry/jiangshi-invoke.md) |
| 6 | Underworld Aid | `iss_magicfromtheeast:underworld_aid` | `symmetry.UnderworldAidSpell` | [Ficha](symmetry/underworld-aid.md) |
| 7 | Punishing Heaven | `iss_magicfromtheeast:punishing_heaven` | `symmetry.PunishingHeavenSpell` | [Ficha](symmetry/punishing-heaven.md) |
| 8 | Drapes of Reflection | `iss_magicfromtheeast:drapes_of_reflection` | `symmetry.DrapesOfReflectionSpell` | [Ficha](symmetry/drapes-of-reflection.md) |
| 9 | Cloud Ride | `iss_magicfromtheeast:cloud_ride` | `symmetry.CloudRideSpell` | [Ficha](symmetry/cloud-ride.md) |
| 10 | Nephrite Slash | `iss_magicfromtheeast:nephrite_slash` | `symmetry.NephriteSlashSpell` | [Ficha](symmetry/nephrite-slash.md) |
| 11 | Jade Bullet | `iss_magicfromtheeast:jade_bullet` | `symmetry.JadeBulletSpell` | [Ficha](symmetry/jade-bullet.md) |
| 12 | Soul Catalyst | `iss_magicfromtheeast:soul_catalyst` | `spirit.SoulCatalystSpell` | [Ficha](spirit/soul-catalyst.md) |
| 13 | Soul Burst | `iss_magicfromtheeast:soul_burst` | `spirit.SoulBurstSpell` | [Ficha](spirit/soul-burst.md) |
| 14 | Spirit Challenging | `iss_magicfromtheeast:spirit_challenging` | `spirit.SpiritChallengingSpell` | [Ficha](spirit/spirit-challenging.md) |
| 15 | Bone Hands | `iss_magicfromtheeast:bone_hands` | `spirit.BoneHandsSpell` | [Ficha](spirit/bone-hands.md) |
| 16 | Calamity Cut | `iss_magicfromtheeast:calamity_cut` | `spirit.CalamityCutSpell` | [Ficha](spirit/calamity-cut.md) |
| 17 | Kitsune Pack | `iss_magicfromtheeast:kitsune_pack` | `spirit.KitsunePackSpell` | [Ficha](spirit/kitsune-pack.md) |
| 18 | Revenant of Honor | `iss_magicfromtheeast:revenant_of_honor` | `spirit.RevenantOfHonorSpell` | [Ficha](spirit/revenant-of-honor.md) |
| 19 | Ashigaru Squad | `iss_magicfromtheeast:ashigaru_squad` | `spirit.AshigaruSquadSpell` | [Ficha](spirit/ashigaru-squad.md) |
| 20 | Phantom Charge | `iss_magicfromtheeast:phantom_charge` | `spirit.PhantomChargeSpell` | [Ficha](spirit/phantom-charge.md) |
| 21 | Anchoring Kunai | `iss_magicfromtheeast:anchoring_kunai` | `spirit.AnchoringKunaiSpell` | [Ficha](spirit/anchoring-kunai.md) |
| 22 | Splitting Shuriken | `iss_magicfromtheeast:splitting_shuriken` | `spirit.SplittingShurikenSpell` | [Ficha](spirit/splitting-shuriken.md) |

**PHYSICAL_SPELL_REGISTRATIONS=22**
**NEW_SEMANTIC_ROOTS=0**
**EXACT_STATIC_REGISTRY_AUDIT=PASS**
**PUBLISHER_EQUALS_PHYSICAL_SHA1=PASS**
**RUNTIME_SURVIVAL_NOT_VERIFIED=TRUE**

## Exclusões e deduplicação

- `LaunchSpell` e `QigongControllingSpell` são protótipos comentados no source de referência, não surgem no inicializador ativo do JAR; a antiga escola Dune não cria um conjunto adicional.
- A descrição pública de release `Nephrite Splash` corresponde à identidade comprovada `iss_magicfromtheeast:nephrite_slash`; não contabilizar duas magias.
- Soulburn, soul proxy, reflection, projéteis e summons são subações ou efeitos das 22 identidades, sem novas raízes por instância/efeito visual.

## Gates físicos e de integração

**⚠️** A fonte compila contra Iron's 3.16.2; o modpack físico tem 3.16.3. A prova cobre somente registros/IDs/classes/escolas compilados, **não** cast no cliente/servidor, mana e cooldown efetivos, config implantada, receitas/aquisição Survival, mortes/reload, owner/team/PvP, lifecycle de summons, reflection, Soulburn e iFrame mutation. Os QA estáticos previamente anotados para Anchoring Kunai, Phantom Charge, Cloud Ride e Soul Catalyst não foram automaticamente corrigidos nem aprovados por essa prova.

**Autoridades:** ISS responde por escolas/efeitos/entidades/identidades; Iron's pelo casting e mana base; Black Arcana pelo seu próprio runtime de magia; RPG Skill Tree apenas por progressão, Mastery, perks e gates através de contratos reais. Deduplicação e custos provider-native são preservados; integrações sem seam comprovado permanecem fail-closed.

Clean-room: somente fatos do registry/bytecode são documentados; nenhum método/asset proprietário é reproduzido.
