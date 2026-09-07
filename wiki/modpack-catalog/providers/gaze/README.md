# Gaze — A Malum Addon

## Estado canônico

- JAR instalado: `gaze-1.1.7.1.jar`
- versão runtime: `1.1.7.1`
- Minecraft: `1.21.1`
- loader: NeoForge
- CurseForge project: `1273454`, file `7261638`
- Modrinth project: `NlvaJ5WE`, version `od4ltbRo`
- dependências públicas da release Modrinth: Malum `1.8.2`, Lodestone `1.8.2`; Iron's opcional.
- source público exato: **NÃO LOCALIZADO**.
- bytecode/JAR extraction: **PENDENTE**.

## Classificação

Gaze é um addon de **Malum**, não um spell provider Iron's. Ele amplia a Spirit Arcana por progressão, Geas, Spirit Rites, armas, runes, Curios e utilitários. Não criar fichas de “spell” artificiais para conteúdo que pertence aos registries de Malum/Gaze.

## Inventário público 1.1.7.1

A página oficial declara:

- nova progression screen;
- **2 novos Geas**;
- novo conjunto de **Rites**;
- **6 armas**;
- **8 Runes**;
- **5 Curios**;
- Spirit-Channel pouch.

A publicação não expõe a tabela completa de registry IDs/names. Portanto esses números são **escala pública**, não prova de inventário interno individualizado.

## Nomes observados em changelogs públicos

### Geas / sistemas
- `Domain of Swords` — adicionado em 1.1.7;
- `Pact of Encroaching Malice` — citado em correção 1.1.7; categoria registry exata: **NÃO VERIFICADO**.

### Rites citados
- Corrupted Greater Wicked — passou a ativar spawners;
- Corrupted Greater Sacred — ampliou compatibilidade com cakes modded;
- Aqua Rite — rework/toggle behavior;
- Corrupted Wicked Rite — reworked.

Não assumir que estes quatro constituem o registry total.

### Runes citadas
- Fafnir — bônus com full Malignant armor;
- WorldAnchor — buffado;
- Eir — buffado + indicador visual;
- uma rune de damage mitigation — nome final **NÃO VERIFICADO**.

A release informa 8 runes no total e que foram renomeadas para tema nórdico; os outros nomes exigem JAR/book data.

### Armas/itens citados
- Seidhr;
- Spirit Saber;
- Veil's Edge;
- Splintered World;
- Replica Dharmachakra;
- Spirit-Channel pouch.

A classificação item/weapon/curio final de cada entrada e o inventário completo devem vir do artefato.

## Fail-closed

Não usar números de versões 1.1.6/1.1.7 como se fossem internals 1.1.7.1. A release 1.1.7.1 afirma permanecer para Malum 1.8 e contém ajustes/fixes, mas não fornece source/registry completo.

## Próximo gate

Extrair `gaze-1.1.7.1.jar` ou localizar source exato; então individualizar Geas, Rites, Runes, Curios e armas com IDs, receitas, spirit costs, rites inputs/outputs, authority e anti-abuso.