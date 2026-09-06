# Paladin Spells — catálogo do provider

## Estado

`EXTERNAL PROVIDER / INSTALLED — SOURCE AUDIT 1.21.1 COMPLETE FOR SPELL REGISTRY; LIVE-JAR QA PENDING`

## Versão instalada

- JAR do pack: `paladin_spells-1.21.1-1.1.1.jar`
- mod id: `paladin_spells`
- fonte auditada: branch upstream `1.21`, commit `31f64ccdb39d062b21cc25d434cb62d6463b486e`
- upstream `gradle.properties`: Minecraft 1.21.1 / mod version 1.21.1-1.1.1.

## Papel

Addon de Iron's Spells focado em paladino/tank. Registra cinco spells Holy:

1. `paladin_spells:taunt`
2. `paladin_spells:bulwark`
3. `paladin_spells:sworn_protector`
4. `paladin_spells:bedrock_skin`
5. `paladin_spells:ram`

O próprio README upstream descreve Sworn Protector como `WIP`.

## Aquisição

O source tree 1.21 auditado não contém loot/acquisition data próprio dos spells; em `data/paladin_spells` foi encontrado apenas `damage_type`. Os spells são registrados diretamente no `SpellRegistry` do Iron's.

Portanto a Wiki **não afirma** ainda uma fonte de scroll/loot específica do addon. A aquisição deve ser validada contra o sistema genérico/config/loot do Iron's e contra o JAR/config do modpack antes de preencher `Como obter` como canônico.

## Fórmulas comuns

Os campos `baseManaCost`, `manaCostPerLevel`, `baseSpellPower` e `spellPowerPerLevel` vêm das classes 1.21 do provider. A fórmula final usada pelo Iron's para mana/power efetivos e modificadores do jogador deve ser documentada a partir da versão instalada do Iron's; não é reimplementada nesta Wiki por inferência.

## QA blockers encontrados na auditoria

### Sworn Protector

Na branch 1.21, `onCast` aplica persistent data e o efeito somente dentro de `if (level.isClientSide)`, enquanto o event handler de redirect roda apenas no servidor. Isso cria uma incompatibilidade aparente de authority. O spell permanece `QA BLOCKER — LIVE JAR VALIDATION` até teste no pack ou correção do provider/bridge.

### Bulwark

`BulwarkEffect` registra `Attributes.ARMOR` com operação `ADD_MULTIPLIED_TOTAL` e amount `0.0`, enquanto o spell usa um amplifier calculado. Sem outra lógica server-side não encontrada no provider, isso parece incapaz de produzir o aumento pretendido. O spell permanece `QA REQUIRED` antes de ser reutilizado como fundação de Magia Divina.

### Ram

A classe do spell aplica `mobAttack` a todos os `LivingEntity` encontrados no AABB do dash, exceto o caster, sem filtro de ally/friendly-fire dentro da própria classe. Uma camada global pode alterar o resultado, portanto comportamento PvP/party precisa de teste no modpack.

## Visual

O pack deve preservar a mecânica provider-native, mas a apresentação atual pode ser elevada quando houver método seguro. Taunt usa `ANGRY_VILLAGER` como partícula de feedback; isso é funcional, porém abaixo do novo padrão visual da Wiki e entra como `VFX UPGRADE CANDIDATE`.

## Deduplicação para Magia Divina

Não criar clones dos cinco papéis abaixo:

- self armor amplification → comparar primeiro com Bulwark;
- AoE threat/forced target → Taunt;
- damage redirection/protector link → Sworn Protector;
- rooted heavy mitigation → Bedrock Skin;
- armor-scaling holy charge → Ram.

Novos spells Divinos precisam oferecer outra decisão mecânica, por exemplo julgamento celeste, consagração, purificação, banimento ou Miracle-tier infrastructure.

## Páginas

- `bulwark.md`
- `taunt.md`
- `sworn-protector.md`
- `bedrock-skin.md`
- `ram.md`
