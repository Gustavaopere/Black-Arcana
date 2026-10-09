# Auditoria física cross-domain de candidatos mágicos — 2026-10-08

**Estado: 🟡 triagem documentada; ⚠️ varredura binária integral ainda não comprovada.**

## Autoridade e método

- Snapshot físico do sibling: `neoforge-rpg-skilltree@de80b186357cad20ba5b81892a8682777e96e35a`, índice `PROJECT-INSTRUCTIONS/modlist/modlist.md`; Black Arcana `main@9141a8ed1c345db4e995e5f2aa849df2c24769b9` antes do lote.
- A modlist tem **587 posições incluindo loader**, com **97** classificadas no campo de categoria física `Magic` e **490** fora dessa categoria.
- Uma busca lexical **no nome do mod** por famílias como `spell`, `ritual`, `magic`, `soul`, `cataclysm`, `boss`, `portal`, `enchant`, `malum` e afins gerou **46 candidatos de alta prioridade** entre as 490 entradas. A expressão é uma **heurística de triagem**, não um classificador de presença/ausência de registries.
- **35/46** correspondem, por identidade ou alias explícito, a diretórios de provider ✅ já existentes. **11/46** foram revisados contra seus dossiês físicos sibling; não foi demonstrada uma identidade nova de spell, glyph, rite ou ação sobrenatural player-owned nesses 11 pelo material analisado.
- **Não se conclui que as outras 444 entradas são semanticamente vazias**: não passaram por inspeção exaustiva de JAR ou source de cada versão. O denominador cross-domain global continua aberto.

## Segundo ciclo — catálogo físico integral e triagem por categoria (2026-10-08)

O inventário físico do sibling inclui o **NeoForge modloader como #001**. Assim, o conjunto real contém **587 = 97 JARs classificados Magic + 489 JARs fora de Magic + 1 loader**. Os 490 itens fora da categoria citados no primeiro ciclo incluíam inadvertidamente o loader: somente **489 são JARs de mods escaneáveis**. Isso não altera as 46 linhas lexicais do primeiro ciclo.

Novo [manifesto reproduzível dos 489 JARs](../../../docs/qa/nonmagic_physical_manifest_2026-10-08.json), fixado em `neoforge-rpg-skilltree@de80b186357cad20ba5b81892a8682777e96e35a`:

| Grupo de triagem (disjunto) | Entradas físicas JAR | Interpretação |
|---|---:|---|
| `LEXICAL_NAME` | **46** | Nome contém indicador de possível magia/sistema; 35 READMEs catalogados e 11 dossiês lidos no ciclo anterior |
| `RPG_GEAR_MOBS_DIMENSIONS` | **96** | Não passou no filtro lexical, mas categoria inclui RPG/equipamento/mobs/dimensões. Pode conter habilidades mágicas ou apenas tecnologia/estruturas |
| `OTHER` | **347** | Outros JARs; não classificados como semanticamente vazios e continuam dentro da varredura física |
| **Total** | **489** | **0/489** JARs inspecionados binariamente nesta execução; manifesto e ferramenta prontos |

Ferramenta [nonmagic_physical_jar_triage.py](../../../docs/qa/nonmagic_physical_jar_triage.py) e [procedimento](../../../docs/qa/nonmagic_physical_jar_triage.md) fazem fingerprint read-only e buscam candidatos pelos nomes das entradas ZIP (sem ler corpos, executar classes ou copiar código). ZIP filename matching **não estabelece registry, spell ID, autoria ou ausência de poder**.

### Sete dossiês da segunda passada conferidos

| Física | Mod | Evidência declarada no dossiê físico | Disposição de catálogo |
|---:|---|---|---|
| #121 | Create Guardian Beam Defense | Turrets cinéticos e **Beam Reactor Helmet** (beam acionado por keybind); natureza tecnológica/combate definida pelo dossiê | ⚠️ Ação tecnológica real, não convertida sem prova em feitiço mágico Black Arcana; autoritatividade do addon |
| #334 | Integrated Simply Swords | Variantes de armas por material e integração com Simply Swords | ⚠️ Sem nova spell identity independente demonstrada; requer revisão de registries se surgir efeito ativo próprio |
| #404 | Modonomicon | Framework data-driven de livros/guias e previews de multibloco | ⚠️ Não é por si só um spell registry; consumidores/datapacks podem apresentar rituais |
| #395 | MineColonies | Colônias, IA/jobs, research e permissões | ⚠️ Research/skills não são feitiços propriamente ditos sem contrato de ação verificável |
| #320 | Integrated Dungeons Arise | Overhaul de estruturas, loot e spawners | ⚠️ Worldgen pode alterar obtenção de itens mágicos de terceiros; não provar spell própria |
| #335 | Integrated Stronghold | Megaestrutura vanilla de exploração, puzzles e traps | ⚠️ Estruturas/loot não equivalem a magia independente |
| #464 | Pufferfish's Skills | Framework data-driven de skill trees com requisitos, custos e rewards | ⚠️ Conteúdo efetivamente carregado depende de datapacks; ponte de progressão permanece sibling, não um novo runtime mágico |

Os sete dossiês acima são leitura de evidência documental da modlist, **não inspeção binária da build atual**. O filtro de categoria encontrou **96** linhas relevantes, das quais **7** receberam leitura específica nesta segunda passada; as restantes **89** continuam em revisão. Os **347** JARs do grupo OTHER também continuam no universo de auditoria. Total de dossiês individuais revisados nas duas passadas: **18** (11 + 7), sem promover nenhum novo feitiço a contagem semântica por mera interpretação.
## Terceiro ciclo — dez dossiês cross-domain adicionais (2026-10-08)

**Estado: ⚠️ triagem documental adicional, não certificação binária.** Estes dez itens pertencem ao grupo disjunto `RPG_GEAR_MOBS_DIMENSIONS`, excluem os sete já revisados no segundo ciclo e foram lidos na revisão física documental do sibling `de80b186357cad20ba5b81892a8682777e96e35a`. Os nomes, versões e JARs permanecem vinculados ao [manifesto fixado](../../../docs/qa/nonmagic_physical_manifest_2026-10-08.json). Os SHA-1 mencionados em alguns dossiês **não foram re-hasheados** nesta continuação.

| Posição física | Mod / dossiê sibling exato | Sinal documentado | Disposição para Black Arcana |
|---|---|---|---|
| #071 | [BetterEnd: New Dawn](https://github.com/Gustavaopere/neoforge-rpg-skilltree/blob/de80b186357cad20ba5b81892a8682777e96e35a/PROJECT-INSTRUCTIONS/modlist/Biomes%20%2B%20Cosmetic%20%2B%20Mobs%20%2B%20Structures%20%2B%20World%20Gen/%E2%9C%85-betterend-new-dawn%20v21.0.34.md) | `Resonance I/II` em ferramentas de mineração e conteúdos do End; nenhum feitiço autônomo demonstrado. | ⚠️ Ação de equipamento/encantamento; somente promover com registry/owner de magia confirmado. |
| #074 | [BetterNether: New Dawn](https://github.com/Gustavaopere/neoforge-rpg-skilltree/blob/de80b186357cad20ba5b81892a8682777e96e35a/PROJECT-INSTRUCTIONS/modlist/Biomes%20%2B%20Cosmetic%20%2B%20Mobs%20%2B%20Structures%20%2B%20World%20Gen/%E2%9C%85-betternether-new-dawn%20v21.0.26.md) | Brewing, equipamentos e criaturas de Nether; nenhuma lista de feitiços player-owned encontrada no dossiê. | ⚠️ Conferir receitas/efeitos efetivos antes de considerar qualquer ação mágica independente. |
| #084 | [Born in Chaos](https://github.com/Gustavaopere/neoforge-rpg-skilltree/blob/de80b186357cad20ba5b81892a8682777e96e35a/PROJECT-INSTRUCTIONS/modlist/Adventure%20and%20RPG%20%2B%20Armor%2C%20Tools%2C%20and%20Weapons%20%2B%20Mobs%20%2B%20Structures%20%2B%20World%20Gen/%E2%9C%85-born-in-chaos%20v1.7.6.md) | Missionary: teleporte, summons e projéteis mágicos **de mob**; equipamentos Frostbitten/Icy têm efeitos descritos, mas não roster/registro exato nesta release. | ⚠️ Prioridade alta: distinguir ações de criatura, equipamentos ativáveis e eventuais poderes de jogador, com JAR/config exatos. |
| #193 | [Create Mechanical Companion](https://github.com/Gustavaopere/neoforge-rpg-skilltree/blob/de80b186357cad20ba5b81892a8682777e96e35a/PROJECT-INSTRUCTIONS/modlist/Addons%20%2B%20Adventure%20and%20RPG%20%2B%20Create%20%2B%20Mobs%20%2B%20Technology/%E2%9C%85-create-mechanical-companion%20v1.9.md) | Mechanical Wolf equipado via Link; `Quantum Drive` teleporta o companion e outros módulos dão efeitos ofensivos/utilitários. | ⚠️ Ação de companion tecnológico, sem identidade de feitiço autônoma demonstrada; preservar ownership de Create/Curios/addon. |
| #260 | [Epic Fight](https://github.com/Gustavaopere/neoforge-rpg-skilltree/blob/de80b186357cad20ba5b81892a8682777e96e35a/PROJECT-INSTRUCTIONS/modlist/Adventure%20and%20RPG%20%2B%20API%20and%20Library%20%2B%20Armor%2C%20Tools%2C%20and%20Weapons/%E2%9C%85-epic-fight%20v21.17.3.1.md) | Battle mode, weapon innate/special attacks, stamina, dodge/guard/passivas e frameworks de skills. | ⚠️ Combat-framework; nenhum número de spells inferido da quantidade de skills. Examinar conteúdo mágico somente por ID/ação concreta. |
| #321 | [Integrated Dungeons and Structures (IDAS)](https://github.com/Gustavaopere/neoforge-rpg-skilltree/blob/de80b186357cad20ba5b81892a8682777e96e35a/PROJECT-INSTRUCTIONS/modlist/Adventure%20and%20RPG%20%2B%20Armor%2C%20Tools%2C%20and%20Weapons%20%2B%20Create%20%2B%20Structures%20%2B%20World%20Gen/%E2%9C%85-integrated-dungeons-and-structures-idas%20v1.13.7%2B1.21.1-neoforge.md) | Templates/loot/structures com integrações opcionais, inclusive Ars Nouveau; propriedade dos itens/spells permanece com providers de origem. | ⚠️ Estrutura composta não prova nova magia IDAS-owned; verificar scripts/loot/referências sem duplicar registries. |
| #371 | [Legendary Monsters](https://github.com/Gustavaopere/neoforge-rpg-skilltree/blob/de80b186357cad20ba5b81892a8682777e96e35a/PROJECT-INSTRUCTIONS/modlist/Armor%2C%20Tools%2C%20and%20Weapons%20%2B%20Mobs%20%2B%20Structures/%E2%9C%85-legendary-monsters%20v2.2.2.md) | Bosses/mobs com projéteis/AI e integração separada Legendary Spellbooks; source publicado citado no dossiê está defasado da 2.2.2. | ⚠️ Prioridade intermediária: reconciliar habilidade de mob e integração Spellbooks por versão exata, sem somar duas vezes. |
| #433 | [ParCool!](https://github.com/Gustavaopere/neoforge-rpg-skilltree/blob/de80b186357cad20ba5b81892a8682777e96e35a/PROJECT-INSTRUCTIONS/modlist/Adventure%20and%20RPG%20%2B%20Miscellaneous%20%2B%20Utility%20%26%20QoL/%E2%9C%85-parcool%20v4.0.0.3.md) | Parkour/mobilidade (wall movement, vault, dodge etc.) com estado de skill próprio. | ⚠️ Movimentação não é feitiço por si; sem evidência de nova ação mágica. |
| #452 | [Portable Hole](https://github.com/Gustavaopere/neoforge-rpg-skilltree/blob/de80b186357cad20ba5b81892a8682777e96e35a/PROJECT-INSTRUCTIONS/modlist/Armor%2C%20Tools%2C%20and%20Weapons%20%2B%20Player%20Transport/%E2%9C%85-portable-hole%20v21.1.0.md) | Ferramenta acionada por jogador cria passagem temporária/restaurável em blocos, com duração, profundidade e cooldown configuráveis. | ⚠️ Prioridade alta para classificação semântica: ferramenta especial é observável, mas classificação como magia/ritual não está comprovada. |
| #568 | [Weapons of Miracles](https://github.com/Gustavaopere/neoforge-rpg-skilltree/blob/de80b186357cad20ba5b81892a8682777e96e35a/PROJECT-INSTRUCTIONS/modlist/Addons%20%2B%20Adventure%20and%20RPG%20%2B%20Armor%2C%20Tools%2C%20and%20Weapons/%E2%9C%85-weapons-of-miracles%20v2.0.178.md) | Addon Epic Fight publica **27 skills**, além de 11 armas, 4 artefatos e entidade companion; nomes/registries das 27 skills não enumerados no dossiê. | ⚠️ Prioridade alta: obter identidade e natureza de cada skill da release exata, e separar especiais de combate de spell roots. |

**Cobertura de leitura até este ciclo:** **28 dossiês** individuais no universo de 142 candidatos priorizados: 11 candidatos `LEXICAL_NAME` e 17 de `RPG_GEAR_MOBS_DIMENSIONS` (7 anteriores + 10 nesta tabela). Permanecem **79** do grupo de 96 por categoria sem leitura individual nesta auditoria, além de 347 `OTHER` sem encerramento exaustivo. Os 35 outros candidatos lexicais possuem pasta ✅ já mapeada, o que não implica releitura binária. **0/489 JARs não-Magic inspecionados fisicamente nesta sequência; 0 novas identidades mágicas certificadas.** Os 39 providers source/release-bounded, 14 rotas de Survival e bloqueio de Stage 06.05 permanecem inalterados.

Para uma triagem ZIP read-only focada nos dez arquivos, quando os bytes da instância estiverem disponíveis, usar `--physical-numbers "71,74,84,193,260,321,371,433,452,568"`. Os nomes ZIP podem direcionar investigação; não comprovam registry, casting nem estado habilitado no pack. Classificar habilidade `mob-owned`, arma/artefato, movimento e magia `player-owned` separadamente antes de qualquer ficha ou alteração no mínimo semântico.

## Candidatos lexicais, estado por linha física

| Linha física | Mod | JAR registrado | Disposição nesta rodada |
|---:|---|---|---|
| #003 | Ace's Spell Utils | `aces_spell_utils-1.2.7.2-1.21.1.jar` | ✅ Catálogo existente [aces-spell-utils](../providers/✅-aces-spell-utils/README.md) |
| #021 | Alex's Mobs Continued | `alexsmobs-2.1.13-neoforge+1.21.1.jar` | ✅ Catálogo existente [alexs-mobs-continued](../providers/✅-alexs-mobs-continued/README.md) |
| #031 | Apotheotic Creation | `apotheoticcreation-2.0.0.jar` | ✅ Catálogo existente [apotheotic-creation](../providers/✅-apotheotic-creation/README.md) |
| #032 | Apothic Category Compat | `apothic_compat-2.0.2.jar` | ✅ Catálogo existente [apothic-compat](../providers/✅-apothic-compat/README.md) |
| #033 | Apothic Compats | `apothic_compats-0.2.4.2.jar` | ✅ Catálogo existente [apothic-compats](../providers/✅-apothic-compats/README.md) |
| #034 | Apothic Attributes | `ApothicAttributes-1.21.1-2.10.1.jar` | ✅ Catálogo existente [apothic-attributes](../providers/✅-apothic-attributes/README.md) |
| #036 | Apothic Spawners | `ApothicSpawners-1.21.1-1.4.0.jar` | ✅ Catálogo existente [apothic-spawners](../providers/✅-apothic-spawners/README.md) |
| #051 | Ars Nouveau: Two-Way Portals (with immersive portal support) | `ars_two_way_portals-2.0.0.jar` | ✅ Catálogo existente [ars-two-way-portals](../providers/✅-ars-two-way-portals/README.md) |
| #055 | Artifacts | `artifacts-neoforge-13.2.5.jar` | ✅ Catálogo existente [artifacts](../providers/✅-artifacts/README.md) |
| #079 | Bosses'Rise - Epic Souls like boss fights | `block_factorys_bosses-2.1.2-neo-1.21.1.jar` | ✅ Catálogo existente [bosses-rise](../providers/✅-bosses-rise/README.md) |
| #082 | Bosses of Mass Destruction [Forge \| NeoForge] | `BOMD-NeoForge-1.21-1.3.3.jar` | ✅ Catálogo existente [bosses-of-mass-destruction](../providers/✅-bosses-of-mass-destruction/README.md) |
| #088 | Cataclysm x YUNG's Better Nether Fortresses Compat | `cataclysmfortresses-1.21.1-NeoForge.jar` | ⚠️ Dossiê físico revisado; ver tabela de 11 abaixo |
| #120 | Create: Enchantment Industry | `create-enchantment-industry-2.5.3b.jar` | ✅ Catálogo existente [create-enchantment-industry](../providers/✅-create-enchantment-industry/README.md) |
| #141 | Create: Deep Dark | `create_deep_dark-3.0.2-neoforge-1.21.1.jar` | ✅ Catálogo existente [create-deep-dark](../providers/✅-create-deep-dark/README.md) |
| #149 | Create: Mobile Packages | `create_mobile_packages-1.21.1-0.7.7.jar` | ✅ Catálogo existente [create-mobile-packages](../providers/✅-create-mobile-packages/README.md) |
| #182 | Create: Dragons Plus | `CreateDragonsPlus-1.11.8b.jar` | ✅ Catálogo existente [create-dragons-plus](../providers/✅-create-dragons-plus/README.md) |
| #183 | Create: Enchantable Machinery | `createenchantablemachinery-3.6.0+mc1.21.1-neoforge.jar` | ✅ Catálogo existente [create-enchantable-machinery](../providers/✅-create-enchantable-machinery/README.md) |
| #184 | Create: Ender Transmission | `createendertransmission-2.1.1-1.21.1.jar` | ✅ Catálogo existente [create-ender-transmission](../providers/✅-create-ender-transmission/README.md) |
| #215 | Deeper and Darker | `deeperdarker-neoforge-1.21.1-1.4.1.jar` | ✅ Catálogo existente [deeper-and-darker](../providers/✅-deeper-and-darker/README.md) |
| #219 | Dimensional Sable | `dimensional_sable-1.0.5.jar` | ✅ Catálogo existente [dimensional-sable](../providers/✅-dimensional-sable/README.md) |
| #245 | Epic Fight x Iron's Spells: Enhanced Animations | `efiscompat-3.1.0.jar` | ✅ Catálogo existente [efiscompat](../providers/✅-efiscompat/README.md) |
| #249 | EMF Compat: Iron's Spells 'n Spellbooks | `emf_compat_iron_spells_1.21.1_2.0.0.jar` | ✅ Catálogo existente [emf-compat-iron-spells](../providers/✅-emf-compat-iron-spells/README.md) |
| #251 | Ender's Delight | `endersdelight-1.3.1.jar` | ⚠️ Dossiê físico revisado; ver tabela de 11 abaixo |
| #253 | Enhanced Boss Bars | `enhancedbossbars-1.0.0.jar` | ⚠️ Dossiê físico revisado; ver tabela de 11 abaixo |
| #265 | Ender's Spells and Stuff: Requiem | `ess_requiem-0.1.7.jar` | ✅ Catálogo existente [enders-spells-and-stuff-requiem](../providers/✅-enders-spells-and-stuff-requiem/README.md) |
| #273 | FamiliarsLib | `familiarslib-1.21.1-1.7.1.jar` | ✅ Catálogo existente [familiarslib](../providers/✅-familiarslib/README.md) |
| #300 | Gaze - A Malum Addon | `gaze-1.1.7.1.jar` | ✅ Catálogo existente [gaze](../providers/✅-gaze/README.md) |
| #310 | GTBC's SpellLib/API | `gtbcs_spell_lib-2.2.0-1.21.1.jar` | ✅ Catálogo existente [gtbcs-spelllib](../providers/✅-gtbcs-spelllib/README.md) |
| #315 | Ice And Fire: Dragon Care | `Ice and Fire - Dragon Care-1.3.1 - 1.21.1v.jar` | ✅ Catálogo existente [dragon-care](../providers/✅-dragon-care/README.md) |
| #317 | Ice and Fire X Epic Fight | `iceandfire-ce-epicfight-armor-compat-1.0.0.jar` | ⚠️ Dossiê físico revisado; ver tabela de 11 abaixo |
| #318 | Ice And Fire: Dread Land | `iceandfire_dreadland-0.1.2.jar` | ✅ Catálogo existente [ice-and-fire-dread-land](../providers/✅-ice-and-fire-dread-land/README.md) |
| #323 | Cataclysm: Ignis Soulfires | `ignissoulfires-1.8.0.jar` | ✅ Catálogo existente [ignis-soulfires](../providers/✅-ignis-soulfires/README.md) |
| #325 | Integrated Mowzie's Mobs | `IMM v1.3.0-1.21.1.jar` | ⚠️ Dossiê físico revisado; ver tabela de 11 abaixo |
| #327 | Immersive Aeronautics - Immersive Portals + Create: Aeronautics | `Immersive-Aeronautics1.1.4-1.21.1-NeoForge.jar` | ⚠️ Dossiê físico revisado; ver tabela de 11 abaixo |
| #330 | Immersive Portals: True Immersion | `immersive_portals_true_immersion-2.0.4.jar` | ✅ Catálogo existente [immersive-portals-true-immersion](../providers/✅-immersive-portals-true-immersion/README.md) |
| #333 | Integrated Cataclysm | `integrated_cataclysm-1.0.6+1.21.1-neoforge.jar` | ⚠️ Dossiê físico revisado; ver tabela de 11 abaixo |
| #368 | L_Ender's Cataclysm | `L_Ender's Cataclysm 1.21.1-3.33.jar` | ✅ Catálogo existente [cataclysm](../providers/✅-cataclysm/README.md) |
| #381 | Loot Integrations: L_Ender 's Cataclysm | `lootintegrations_cataclysm-1.2.jar` | ⚠️ Dossiê físico revisado; ver tabela de 11 abaixo |
| #382 | Loot Integrations: Ice and Fire | `lootintegrations_iceandfire-1.2.jar` | ⚠️ Dossiê físico revisado; ver tabela de 11 abaixo |
| #383 | Loot Integrations: Integrated Dungeons, Villages & Strongholds & Cataclysm | `lootintegrations_integrated-1.5.jar` | ⚠️ Dossiê físico revisado; ver tabela de 11 abaixo |
| #399 | Ragdoll mob corpses | `mob_ragdoll_corpse-1.1.5.jar` | ⚠️ Dossiê físico revisado; ver tabela de 11 abaixo |
| #400 | Mobstein : Revive animals and necromancy! | `mobstein-5.4.4-neoforge-1.21.1.jar` | ✅ Catálogo existente [mobstein](../providers/✅-mobstein/README.md) |
| #475 | Reliquified L_Ender 's Cataclysm new relics fix | `reliquified-lenders-cataclysm-new-relics-fix-1.0.2.jar` | ✅ Catálogo existente [reliquified-lenders-cataclysm-new-relics-fix](../providers/✅-reliquified-lenders-cataclysm-new-relics-fix/README.md) |
| #511 | Snow! Real Magic! ⛄ (Neo/Forge) | `SnowRealMagic-1.21.1-NeoForge-12.2.2.jar` | ✅ Catálogo existente [snow-real-magic](../providers/✅-snow-real-magic/README.md) |
| #521 | Soul fire'd | `soul-fire-d-neoforge-1.21-6.1.0.jar` | ✅ Catálogo existente [soul-fire-d](../providers/✅-soul-fire-d/README.md) |
| #585 | YUNG's Better Witch Huts (NeoForge) [1.20.4 - 1.21.1 ONLY] | `YungsBetterWitchHuts-1.21.1-NeoForge-4.1.1.jar` | ✅ Catálogo existente [yungs-better-witch-huts](../providers/✅-yungs-better-witch-huts/README.md) |

## Onze casos sem pasta específica de provider mágico

**Essas 11 linhas possuem dossiês físicos na modlist, mas não são automaticamente novos feitiços.** A observação abaixo reproduz a função documentada, sem prometer auditoria binária exaustiva ou configurar seu runtime como aprovado.

| Física | Função documentada no dossiê sibling | Estado semântico |
|---:|---|---|
| #88 | Ponte de tag de estruturas Berserker; o dossiê não aponta spell próprio | ⚠️ Nenhuma identidade mágica própria demonstrada pelo dossiê; JAR não inspecionado neste lote |
| #251 | Addon de receitas/cozinha do End; nenhuma identidade mágica independente indicada | ⚠️ Nenhuma identidade mágica própria demonstrada pelo dossiê; JAR não inspecionado neste lote |
| #253 | Camada client de boss bars; sem autoria de habilidades | ⚠️ Nenhuma identidade mágica própria demonstrada pelo dossiê; JAR não inspecionado neste lote |
| #317 | Compatibilidade visual de armadura Ice and Fire CE/Epic Fight; sem autoria de golpe | ⚠️ Nenhuma identidade mágica própria demonstrada pelo dossiê; JAR não inspecionado neste lote |
| #325 | Overhaul de worldgen/estruturas de Mowzie's Mobs; pendência física de Integrated Patches registrada no sibling | ⚠️ Nenhuma identidade mágica própria demonstrada pelo dossiê; JAR não inspecionado neste lote |
| #327 | Rewrite de core Immersive Portals/Create, transferência/infra; sem spell registry indicado | ⚠️ Nenhuma identidade mágica própria demonstrada pelo dossiê; JAR não inspecionado neste lote |
| #333 | Overhaul de estruturas/loot/recipes de Cataclysm; sem ação mágica independente evidenciada | ⚠️ Nenhuma identidade mágica própria demonstrada pelo dossiê; JAR não inspecionado neste lote |
| #381 | Injeção de loot de Cataclysm; não registrar novo spell por loot | ⚠️ Nenhuma identidade mágica própria demonstrada pelo dossiê; JAR não inspecionado neste lote |
| #382 | Injeção de loot de Ice and Fire; não registrar novo spell por loot | ⚠️ Nenhuma identidade mágica própria demonstrada pelo dossiê; JAR não inspecionado neste lote |
| #383 | Injeção de loot em Integrated Structures; não registrar novo spell por loot | ⚠️ Nenhuma identidade mágica própria demonstrada pelo dossiê; JAR não inspecionado neste lote |
| #399 | Física pós-morte de cadáveres (ragdoll); não confundir corpse effect com necromancia intencional | ⚠️ Nenhuma identidade mágica própria demonstrada pelo dossiê; JAR não inspecionado neste lote |

## Fontes exatas dos 11 dossiês revisados

- #88: [dossiê físico do sibling](https://github.com/Gustavaopere/neoforge-rpg-skilltree/blob/de80b186357cad20ba5b81892a8682777e96e35a/PROJECT-INSTRUCTIONS/modlist/Addons%20%2B%20Bug%20Fixes/%E2%9C%85-cataclysm-yungs-better-nether-fortresses-compat%20v1.21.1.md)
- #251: [dossiê físico do sibling](https://github.com/Gustavaopere/neoforge-rpg-skilltree/blob/de80b186357cad20ba5b81892a8682777e96e35a/PROJECT-INSTRUCTIONS/modlist/Addons%20%2B%20Farming%20%2B%20Food/%E2%9C%85-enders-delight%20v1.3.1.md)
- #253: [dossiê físico do sibling](https://github.com/Gustavaopere/neoforge-rpg-skilltree/blob/de80b186357cad20ba5b81892a8682777e96e35a/PROJECT-INSTRUCTIONS/modlist/Adventure%20and%20RPG%20%2B%20Cosmetic%20%2B%20Miscellaneous%20%2B%20Mobs/%E2%9C%85-enhanced-boss-bars%20v1.0.0.md)
- #317: [dossiê físico do sibling](https://github.com/Gustavaopere/neoforge-rpg-skilltree/blob/de80b186357cad20ba5b81892a8682777e96e35a/PROJECT-INSTRUCTIONS/modlist/Addons%20%2B%20Armor%2C%20Tools%2C%20and%20Weapons%20%2B%20Bug%20Fixes%20%2B%20Cosmetic/%E2%9C%85-ice-and-fire-ce-epic-fight-armor-compat%20v1.0.0.md)
- #325: [dossiê físico do sibling](https://github.com/Gustavaopere/neoforge-rpg-skilltree/blob/de80b186357cad20ba5b81892a8682777e96e35a/PROJECT-INSTRUCTIONS/modlist/Adventure%20and%20RPG%20%2B%20Structures%20%2B%20World%20Gen/%E2%9C%85-integrated-mowzies-mobs%20v1.3.0.md)
- #327: [dossiê físico do sibling](https://github.com/Gustavaopere/neoforge-rpg-skilltree/blob/de80b186357cad20ba5b81892a8682777e96e35a/PROJECT-INSTRUCTIONS/modlist/Create/%E2%9C%85-immersive-aeronautics%20v1.1.4.md)
- #333: [dossiê físico do sibling](https://github.com/Gustavaopere/neoforge-rpg-skilltree/blob/de80b186357cad20ba5b81892a8682777e96e35a/PROJECT-INSTRUCTIONS/modlist/Addons%20%2B%20Adventure%20and%20RPG%20%2B%20Armor%2C%20Tools%2C%20and%20Weapons%20%2B%20Create%20%2B%20World%20Gen/%E2%9C%85-integrated-cataclysm%20v1.0.6%2B1.21.1-neoforge.md)
- #381: [dossiê físico do sibling](https://github.com/Gustavaopere/neoforge-rpg-skilltree/blob/de80b186357cad20ba5b81892a8682777e96e35a/PROJECT-INSTRUCTIONS/modlist/Addons%20%2B%20Structures/%E2%9C%85-loot-integrations-cataclysm%20v1.2.md)
- #382: [dossiê físico do sibling](https://github.com/Gustavaopere/neoforge-rpg-skilltree/blob/de80b186357cad20ba5b81892a8682777e96e35a/PROJECT-INSTRUCTIONS/modlist/Addons%20%2B%20Structures/%E2%9C%85-loot-integrations-ice-and-fire%20v1.2.md)
- #383: [dossiê físico do sibling](https://github.com/Gustavaopere/neoforge-rpg-skilltree/blob/de80b186357cad20ba5b81892a8682777e96e35a/PROJECT-INSTRUCTIONS/modlist/Addons%20%2B%20Structures/%E2%9C%85-loot-integrations-integrated-structures%20v1.5.md)
- #399: [dossiê físico do sibling](https://github.com/Gustavaopere/neoforge-rpg-skilltree/blob/de80b186357cad20ba5b81892a8682777e96e35a/PROJECT-INSTRUCTIONS/modlist/Addons%20%2B%20Mobs/%E2%9C%85-sable-mob-ragdoll-corpses%20v1.1.5.md)

## Próximos gates

1. Auditar de modo físico/binary-exact os 11 candidatos quando houver acesso aos JARs exatos; cruzar registries, metadata, recursos e eventos player-owned sem reutilizar implementação de terceiros.
2. Confrontar as 444 outras entradas com classificação explícita de ownership e eventuais datapacks, scripts ou efeitos mágicos não identificados lexicalmente; nenhuma inferência negativa por ausência da palavra magic.
3. Adicionar ficha e ajustar ledger **apenas** quando uma nova identidade semântica comprovada for encontrada. Catálogo de infraestrutura +0 não equivale a ação mágica provider-owned.
4. Conservar Traveloptics e o Deeper and Darker base fora do escopo operacional do usuário, preservando seus dossiês históricos; Deeper & Darker Spellbooks segue em escopo.
