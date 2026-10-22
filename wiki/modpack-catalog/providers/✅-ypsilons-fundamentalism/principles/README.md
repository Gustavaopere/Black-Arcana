# Principles — 13 fichas individuais para engenharia de perks

**22/10/2026 — 13/13 categorias enum com ficha individual source-pinned.** Este numerador mede fichas deste lote; não é completude técnica global, 13 spells novos ou aceite físico. A [visão agregada](../PRINCIPLES.md) continua índice dos sistemas; as 15 magias permanecem nas escolas existentes. Não se alteram mínimos mágicos ou campanha binária.

| Principle | Chave do ledger | Ficha |
|---|---|---|
| Concentratio | `createEntity` | [Concentratio](concentratio.md) |
| Potentia | `usesShoot` | [Potentia](potentia.md) |
| Vitale | `usesSummon` | [Vitale](vitale.md) |
| Locus | `usesTargeting` | [Locus](locus.md) |
| Repetitio | `hasRecasts` | [Repetitio](repetitio.md) |
| Apparitio | `usesTeleport` | [Apparitio](apparitio.md) |
| Pertinacia | `addEffects` | [Pertinacia](pertinacia.md) |
| Expansio | `createsAoeEntities` | [Expansio](expansio.md) |
| Motus | `usesMobility` | [Motus](motus.md) |
| Perceptio | `usesRaycast` | [Perceptio](perceptio.md) |
| Remedium | `usesHealing` | [Remedium](remedium.md) |
| Augere | `usesPotentiation` | [Augere](augere.md) |
| Certum | `immutable` | [Certum](certum.md) |

## Reprodutibilidade e provenance

Source consultado: `ypsilonM/FundamentalPrinciples-1.21.1@a9b8f8222fb2a800edece8c1568984bd2a764fc2`, release correlacionada em gradle.properties 1.1.7.1, Iron's 3.16.2. Identidade física versionada: `ypfundamentals-1.1.7.1.jar`, SHA-1 `a2855c253202a8fcc2925fcf5b1bf86d64fbe4da`; a [modlist RPG](https://github.com/Gustavaopere/neoforge-rpg-skilltree/blob/ffd1f1ede5bf46ce3425a5c17bc5d279d8c572dc/PROJECT-INSTRUCTIONS/modlist/Addons%20%2B%20Adventure%20and%20RPG%20%2B%20Magic%20%2B%20Mobs/%E2%9C%85-fundamental-principles-irons-spells-addon%20v1.1.7.1.md) confirma #575. Não houve acesso à instalação de jogo ao vivo ou equivalência integral source→JAR. O pin dos 15 IDs físicos comprova registry, não esse lote de métodos.

[gradle.properties](https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/gradle.properties#L32) declara `mod_license=MIT`. O repositório contém [TEMPLATE_LICENSE.txt](https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/TEMPLATE_LICENSE.txt#L5), que explicita aplicação aos templates NeoForged/MDK, não demonstra sozinho licença de todos os arquivos específicos do addon. Esta entrega resume comportamento e símbolos, sem importar source/arte; redistribuição ou derivação exige esclarecer licença aplicável.

## Contratos comuns de progressão

[PrinciplesLevelsAttachment#setLevel](https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/src/main/java/com/ypsi/fundamentalism/attachments/customAtt/PrinciplesLevelsAttachment.java#L88) limita nível 0–20; CODEC serializa mapas de nível e XP e não deve ser tratado como esquema autorizado para escrita de outro mod. `addExperience` avalia XP exigido para currentLevel+1, e o helper usa cast int sobre valores positivos. Primeiro nível exige 46 XP. O incremento vem do SpellOnCastEvent conforme categorias/raridade/tipo de cast; eventos de cast não demonstram dano confirmado ou Mastery externa.

[YpsAttachments#PRINCIPLES_LEVELS](https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/src/main/java/com/ypsi/fundamentalism/attachments/YpsAttachments.java#L44) registra `ypfundamentals:spell_category_levels` com serialize(CODEC) e copyOnDeath. [PrinciplesProgressionManager#getCategoryLevel](https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/src/main/java/com/ypsi/fundamentalism/attachments/PrinciplesProgressionManager.java#L34) lê attachment no servidor ou ClientCategoryLevelsData no cliente; player null retorna 10, um fallback que não prova nível real. Métodos públicos source não são integração homologada para atribuição de XP/escrita de níveis. [addCategoryExperience](https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/src/main/java/com/ypsi/fundamentalism/attachments/PrinciplesProgressionManager.java#L94) sincroniza ao ServerPlayer após alteração; logins/transições têm rotas próprias. Clone, death/restart e config implantada ainda precisam QA.

[PowerSpellsMixin#multiplySpecificSpellPower](https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/src/main/java/com/ypsi/fundamentalism/mixins/principlesMixins/PowerSpellsMixin.java#L35) é consumer separado das passivas e soma modificadores de várias categorias antes da razão de fatigue. `SUBCATEGORIES_HALF` também inclui usesTargeting no código, embora comentário de configuração enumere só três subcategorias. Config tem worldRestart; não presumir refresh por jogador ou hot reload de toda passiva.

[lista de mixins registrada](https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/src/main/resources/ypfundamentals.mixins.json#L15) inclui os oito mixins de Principles descritos nas fichas. Isso prova declaração source; matching dos injection targets em Iron's 3.16.3 requer inicialização/QA com o provider.

## Limites de integração e validação

- Config global suportada (`NATIVE`) não é setter por player/perk.
- Callback/mixin de consumo source-confirmado não é uma API pública mutadora para Black Arcana ou RPG.
- Preservar uma autoridade para cooldown, mana, food, XP e effects; não replicar settlement.
- Não converter melhoria de raio em volume ou precisão em hitbox. Os detalhes de Perceptio/Locus, Potentia e Expansio nas fichas importam para os consumidores reais.
- Source não comprova montagem de mixins, ordem de listeners, config efetiva, Survival ou aceite de cliente/modpack. Nenhum desses gates recebe PASS aqui.

A validação deste lote confere 13 fichas e localizadores contra o pin, além de links locais. Nenhum novo teste de gameplay ou adapter foi criado. Stage 06/09, matrizes físicas e contagem de magias permanecem independentes.
