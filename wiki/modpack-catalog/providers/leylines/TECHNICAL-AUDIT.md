# Leyline Spellbooks 1.0.3 — auditoria técnica

## Proveniência fechada

- Pack: `leylines-1.0.3.jar`
- Mod ID observado na modlist: `leylines`
- Runtime: `1.0.3`
- CurseForge: Project `1636676`, File `8565076`
- Publicação: Release, NeoForge, Minecraft 1.21.1, 429.7 KB, publicada em 2026-08-02
- Curse Maven: `curse.maven:leylines-irons-spells-n-spellbooks-addon-1636676:8565076`
- SHA-1 corroborado: `dfa6908731f432905caaaa1e53b4aedeaa26ed59`
- CDN resolvido: file path oficial ForgeCDN para `leylines-1.0.3.jar`

O artefato exato está identificado. O bloqueio atual não é de identidade/versionamento; é de **conteúdo binário ainda não extraído** neste ambiente.

## Source

Nenhum repositório público com source pinável da build 1.0.3 foi localizado nas buscas realizadas. A ausência de resultado público não prova que o source não exista; significa apenas que ele não está disponível como provenance utilizável no catálogo atual.

## Inventário público vs registry

A página oficial confirma nove nomes de `Signature Spells`: Blink Step, Rift Gate, Chrono Tether, Temporal Stutter, Fissure, Anchor Recall, Beam, Ley Blast e Eclipse. O mesmo trecho termina em `and more`.

Consequência: `9` é **lower bound público**, não total de spells. Registry IDs, classes, quantidade total, ordem de registro e qualquer spell não citada permanecem `NÃO VERIFICADO`.

## Matriz de campos bloqueados até bytecode

Para todos os spells públicos, salvo nova evidência exata:

- registry ID: `NÃO VERIFICADO`
- classe Java / inheritance: `NÃO VERIFICADO`
- escola efetiva por registro/nível: `NÃO VERIFICADO` (o provider como um todo anuncia a escola Leyline)
- min/max level: `NÃO VERIFICADO`
- rarity: `NÃO VERIFICADO`
- mana formula: `NÃO VERIFICADO`
- cooldown: `NÃO VERIFICADO`
- cast type/time/channel/recast: `NÃO VERIFICADO`
- spell power / damage / healing / damage type: `NÃO VERIFICADO`
- range/radius/duration/caps: `NÃO VERIFICADO`
- target rules / PvP / ally / boss behavior: `NÃO VERIFICADO`
- crafting / loot / scroll acquisition: `NÃO VERIFICADO`
- exact particles/sounds/animations/resources: `NÃO VERIFICADO`
- server authority / packets / persistence: `NÃO VERIFICADO`
- public API/hooks/events: `NÃO VERIFICADO`

## Rift contract confirmado publicamente em 1.0.3

A release 1.0.3 é explicitamente uma atualização de confiabilidade/regras de arena:

- morrer durante encontro ativo falha imediatamente a luta e impede completion loot/crystal;
- boss bar da wave é limpa em morte, respawn, logout e mudança de dimensão;
- afastar-se mais de 60 blocos do rift ativo colapsa o encontro;
- mobs de wave a mais de 40 blocos são puxados de volta à arena;
- mobs persistem após uma morte breve para evitar falso clear;
- `/leylines spawnpillar` exige permission level 2; variante `here` tenta a coluna atual primeiro.

Esses são contratos semânticos/changelog, não assinaturas de classe. O ponto exato onde cada regra é implementada continua bytecode-pending.

## Deduplicação e fail-closed

Black Arcana não deve implementar uma segunda máquina de estado para rifts, waves, abandonment, death failure ou loot. Também não deve inferir que `Rift Gate` usa qualquer API específica de portal, nem que as spells temporais usam tick rate, attributes, potion effects ou event cancellation específicos.

Qualquer integração futura precisa descobrir o boundary real do JAR e observar a authority provider-native. Se não houver hook estável comprovado, a integração deve falhar fechada em vez de reproduzir comportamento por aproximação.

## Estado

`EXACT ARTIFACT IDENTIFIED / 9 PUBLIC SIGNATURE NAMES DOCUMENTED / COMPLETE REGISTRY UNKNOWN / BYTECODE EXTRACTION REQUIRED`
