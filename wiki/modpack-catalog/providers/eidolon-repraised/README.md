# Eidolon: Repraised

## Estado canônico

- mod id: `eidolon_repraised`
- JAR instalado: `eidolon_repraised-1.21.1-0.5.0.2.jar`
- versão instalada: `0.5.0.2`
- Minecraft: `1.21.1`
- loader: NeoForge
- source oficial: `Alexthw46/Eidolon-Repraised`
- source pin exato da versão: `696a47333e43970be7f697790eac0af76b6a04b8`
- estado: **SOURCE-PINNED 0.5.0.2 / SPELL REGISTRY 20/20 / OFFICIAL CHANTS 18/18 / CONVERSIONS 4/4 / GENERIC RITUAL PROTOTYPES 10/10 / OFFICIAL RITUAL RECIPES 24/24 / RESEARCH REGISTRY 16/16 INVENTORIADOS / RUNTIME QA + FULL SURVIVAL REACHABILITY PENDENTES**

O source pin acima é o commit que altera `mod_version` para `0.5.0.2`. O head atual da branch 1.21.1 já avançou para 0.5.0.3 e não é usado como autoridade para a build instalada.

A auditoria de source da superfície mágica principal desta versão está fechada em inventário. Isso **não equivale a runtime QA**: settlement de alguns spells, empacotamento exato do JAR, reachability survival e interações com o modpack ainda precisam ser testados.

## Arquitetura provider-native

Eidolon 0.5.0.2 é um provider completo de:

- mana própria;
- Light/Dark reputation/devotion;
- soul capability;
- research/knowledge;
- 11 Signs + SignSequence;
- chants data-driven;
- chant conversions;
- prayers/effigy/altar;
- rituais e sacrifícios;
- summons ritualísticos;
- crafting ritualístico com health requirement;
- estrutura/divination via ritual locator;
- `SpellCastEvent.Pre` cancelável e `SpellCastEvent.Post`;
- server config por spell para custo/delay e parâmetros específicos.

Black Arcana deve tratar cada eixo como provider-owned. Mana, soul e devotion do Eidolon não são intercambiáveis com Ars Source, Iron's mana, Goety Soul Energy, Malum spirits ou recursos próprios do Black Arcana.

## Inventários fechados no source 0.5.0.2

### Signs — 11/11

`wicked`, `sacred`, `blood`, `soul`, `mind`, `flame`, `winter`, `harmony`, `death`, `warding`, `magic`.

A sequência ordenada faz parte da identidade de chant e deve ser resolvida pelo provider.

### Spell registry — 20/20

`Spells.init()` registra 20 entradas técnicas:

1. `dark_prayer`
2. `darklight_chant`
3. `dark_animal_sacrifice`
4. `dark_touch`
5. `frost_touch`
6. `dark_villager_sacrifice`
7. `zombify_villager`
8. `enthrall_spell`
9. `light_prayer`
10. `fire_chant`
11. `light_chant`
12. `holy_touch`
13. `lay_on_hands`
14. `cure_zombie`
15. `smite_chant`
16. `sunder_armor`
17. `reinforce_armor`
18. `create_water`
19. `undead_lure`
20. `basic_incense`

O catálogo detalhado de custos, gates, delays, efeitos e anomalias está em `SPELL-CATALOG.md`.

### Official chant recipes — 18/18

`EidChantProvider` gera 18 chants normais. `undead_lure` e `basic_incense` não entram nesse datagen:

- `undead_lure` está registrado, custa 50 no source, mas seu `cast()` é vazio na versão exata auditada;
- `basic_incense` é marcado `// dummy` e pertence ao subsystem de incense.

Portanto **20 entries de registry != 20 chants survival**.

### Chant conversions — 4/4

- Gold Inlay -> Holy Symbol, Light devotion ≥10;
- Pewter Inlay -> Unholy Symbol, Dark devotion ≥10;
- Black Wool -> Top Hat, neutral, devotion 0;
- music-disc tag -> Parousia Disc, neutral, devotion 0.

Dark/Holy Touch resolvem essas conversões pelo RecipeManager. Black Arcana não deve duplicar output, gate ou preço.

### Rituals — 24/24 official recipes

O runtime possui 10 prototypes genéricos em `RitualRegistry`, mas o datagen oficial gera **24 receitas**:

- 10 generic rituals;
- 11 summon rituals;
- 2 brazier crafting rituals;
- 1 Catacombs location ritual.

Esse ponto corrige uma inferência anterior: os summon constants comentados em `RitualRegistry` não tornam os summons inativos. `SummonRitualRecipe` instancia `SummonRitual` diretamente a partir do entity id, e os 11 JSONs estão presentes nos generated resources do source pinado.

Ver `RITUAL-CATALOG.md` e `DATA-DRIVEN-CATALOG.md`.

### Research — 16/16 registry keys

`core`, `pewter_crucible`, `soul_enchanter`, `arcane_gold`, `shadow_gem`, `improved_crucible`, `candle`, `wooden_altar`, `deity_altar`, `chants`, `frost_spell`, `fire_spell`, `necrotic_touch`, `soulfire_wand`, `prestigious_palm`, `soulfire_ritual`.

A árvore completa de tasks/prerequisites e a reachability no pack ainda precisam de validação integral. Ver `PROGRESSION.md`.

## Cobertura semântica já provada

### Healing / purification

- `lay_on_hands`: heal base 5 + `0.05 × Light reputation`, com limpeza de efeitos harmful curáveis por leite;
- `purify`: conversões de Zombie Villager/Zombified Piglin/Zoglin;
- `cure_zombie`: prayer/cast Light que converte Zombie Villager.

### Holy / dark / devotion

- Light/Dark prayers;
- Holy/Dark Touch;
- Smite;
- deity-specific reputation gates;
- altar-driven reputation/mana loop.

### Soul / death

- soul capability própria;
- Crystal ritual produz 1–3 Soul Shards por valid undead kill bem-sucedido;
- Absorption captura/serializa entidades em Summoning Staff;
- summons consomem Soul Shard em suas receitas.

### Summons

11 official summon ritual recipes: Zombie, Skeleton, Phantom, Creeper, Wither Skeleton, Husk ×3, Drowned ×3, Stray, Wraith, Slimy Slug ×3 e Raven ×3.

`SummonRitual` usa `MobSpawnType.MOB_SUMMONED`, mas não estabelece por si só ownership/taming. Não inferir servant/familiar ownership apenas pela spawn cause.

### Time

`daylight` e `moonlight` alteram `PrimaryLevelData.dayTime` em +100 por tick durante suas janelas provider-native.

### AI / attraction / repulsion

`allure` e `repelling` injetam goals provider-native em animais/monstros. `enthrall_spell` possui um contrato separado de enthrall/taming para undead válidos.

### Divination

`ritual_locate_catacombs` materializa `LocationRitual` para a tag de Catacombs com Map + Compass + Magic Ink + Raven Feather.

### Ritual crafting / life-cost

Sapping Sword usa health requirement 20; Sanguine Amulet usa health requirement 40. Esses custos são parte da transação ritual do Eidolon e não devem ser debitados novamente.

## Pontos fail-closed / QA

### Settlement de mana não provado em alguns paths

O framework base valida mana, mas não centraliza o gasto. As implementações concretas normalmente chamam `IMana.expendMana(...)`. No exact source 0.5.0.2 permanecem ambíguos:

- `smite_chant` — custo declarado 40, sem gasto direto visível em `cast()`;
- `sunder_armor` — custo 50 via `ApplyPotionSpell`, sem gasto direto visível;
- `reinforce_armor` — custo 50 via `ApplyPotionSpell`, mesma condição;
- `create_water` — air-placement gasta mana, branch `LiquidBlockContainer` não mostra gasto direto;
- `undead_lure` — custo 50 e `canCast=true`, mas `cast()` vazio.

Black Arcana não deve corrigir isso externamente nem assumir cast grátis.

### Dynamic Enthrall cost

`enthrall_spell` usa custo efetivo `2 × baseCost × healthRatio`; com base 50, `100 × currentHealth/maxHealth`. Nunca substituir por custo fixo 50.

### Command chant extension surface

`CommandChantRecipe` existe e pode materializar `ExecCommandSpell`. Com command blocks habilitados, comandos configurados são executados server-side usando permission level 2. O datagen oficial auditado não gera command chant, mas datapacks podem fornecer um.

Integrações Black Arcana devem tratar command chants como uma superfície privilegiada/untrusted e nunca repetir comandos, elevar permissões ou inferir efeito seguro sem inspecionar a receita carregada.

## Authority / deduplication

Provider-native first:

- Eidolon liquida mana/reputation/soul/health/ritual inputs;
- Eidolon resolve SignSequence e recipes;
- Eidolon aplica efeitos e progressão;
- Eidolon decide prayer cooldown, altar power/capacity e effigy readiness;
- Eidolon decide entity capture/summon/conversion.

Black Arcana pode observar para perks/quests/integrations, mas deve preservar uma única causal identity por ação e deduplicar `SpellCastEvent`, world deltas, kills, captures, time mutation e effect application.

## Arquivos desta auditoria

- `SPELL-CATALOG.md` — 20 registry entries com números e gates;
- `RITUAL-CATALOG.md` — 10 generic prototypes + 24 official ritual recipes e semântica;
- `DATA-DRIVEN-CATALOG.md` — 18 chants, 4 conversions, 24 ritual recipes e command-chant extension;
- `PROGRESSION.md` — research/devotion/soul;
- `TECHNICAL-AUDIT.md` — authority, settlement anomalies e runtime QA;
- `INTEGRATION-RULES.md` — contrato Black Arcana.

## Proveniência / confiança

- presença/JAR/versão: modlist 612 + Auditoria Mestre do Notion, reconciliadas em 2026-09-07 — HIGH;
- version pin: commit `696a47333e43970be7f697790eac0af76b6a04b8` declara `mod_version=0.5.0.2` — HIGH;
- registries/classes/datagen/generated resources: source oficial no mesmo pin — HIGH para semântica de source;
- byte-for-byte equality com o JAR instalado: ainda não verificada;
- dedicated-server/runtime behavior: ainda não testado nesta fase.