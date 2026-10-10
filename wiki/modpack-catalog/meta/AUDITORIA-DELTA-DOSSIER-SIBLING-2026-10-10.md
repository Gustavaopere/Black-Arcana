# Reconciliação de 20 dossiês alterados na modlist sibling — 2026-10-10

**Escopo documental, não nova varredura de JARs.** Comparação GitHub:
`neoforge-rpg-skilltree@de80b186357cad20ba5b81892a8682777e96e35a` → `neoforge-rpg-skilltree@f85c9acf2d50c6d8fd9a7fa2f0912c9f03ba42f8` (main observada nesta auditoria). O diff relata **22 commits à frente**, **20 arquivos de dossiê modificados**, **0 arquivos adicionados** e **nenhuma alteração ao índice físico numerado `PROJECT-INSTRUCTIONS/modlist/modlist.md` nesse diff**. Todas as 20 alterações são em fichas Markdown já existentes; `modified` descreve o Git diff, **não** um mod instalado/atualizado. A modlist vigente continua sem novo dump físico além de `modlist(1).txt`.

Base Black Arcana: `main@5783034ca83834b6610aad0a5fd975edd1331743` (PR #733 incorporado). Snapshot de referência fixado em `de80b186357cad20ba5b81892a8682777e96e35a`. Fonte: [comparação no GitHub](https://github.com/Gustavaopere/neoforge-rpg-skilltree/compare/de80b186357cad20ba5b81892a8682777e96e35a...f85c9acf2d50c6d8fd9a7fa2f0912c9f03ba42f8).

## Seis fichas mágicas/adjacentes já presentes no catálogo

| Dossiê atualizado no sibling | Posição no snapshot 587 | Evidência existente no Black Arcana | Disposição semântica desta revisão |
|---|---:|---|---|
| Ace's Spell Utils 1.2.7.2-1.21.1 | #003 | [✅-aces-spell-utils](../providers/✅-aces-spell-utils/README.md) | API / escolas / atributos de Iron's. Não converter utilitários ou escolas em spells novos |
| Apothic Enchanting 1.6.2 | #035 | [✅-apothic-enchanting](../providers/✅-apothic-enchanting/README.md) | Enchantments e sistemas de enchanting; não promover automaticamente a spell action |
| Ars Sable 1.1.2 | #049 | [✅-ars-sable](../providers/✅-ars-sable/README.md) | Bridge espacial Ars↔Sable; compatibilidade real com Sable 2.0.5 ainda condicionada |
| Ars Nouveau's Flavors & Delight 2.2.2 | #053 | [✅-arsdelight](../providers/✅-arsdelight/README.md) | Conteúdo culinário/efeitos; não contar alimentos, efeitos ou Enchanter's Knife como novo spell registrado |
| Hexalia 1.3.7 | #314 | [✅-hexalia](../providers/✅-hexalia/README.md) | Rituais/receitas/magia natural já com dono definido; registro binário e execução físicos não revalidados |
| Mobstein 5.4.4 | #400 | [✅-mobstein](../providers/✅-mobstein/README.md) | Necromancia/ressurreição documentada; sem novo registry exato ou crédito semântico derivado da edição da ficha |

Os seis providers constavam **antes** destas edições na árvore canônica; o marcador ✅ indica **dossiê estrutural presente**, não 100% de completude binary-exact, implementação Black Arcana ou aprovação Survival.

## Outras 14 fichas modificadas — nenhuma promoção mágica

A comparação também inclui 14 dossiês já existentes em categorias de API, logística, automação, cosmética, utilidade, transporte, estruturas e storage:

| Categoria | Dossiês existentes atualizados | Conclusão desta revisão |
|---|---|---|
| API / Library | Fragmentum 2.4.4; Puzzles Lib 21.1.60 | Nenhuma identidade de feitiço comprovada pelo diff documental |
| Addons / Create e Storage | Create Aeronautics x Curios API Compat 2.2; Create Filters Anywhere 2.6.0; Sophisticated Storage Create Integration 0.1.21 | Não assumir nova magia por compatibilidade, receitas ou transferência |
| Gameplay / Automação | MineColonies 1.1.1387-1.21.1-snapshot; Parcool 4.0.0.3; Create Mobile Packages 0.7.7 | Não equiparar AI/logística/movimento a spell registry |
| Storage | Sophisticated Backpacks 3.26.3; Sophisticated Storage 1.5.91 | Itens, upgrades e armazenamento não são conjurações adicionais sem registry específico |
| Cosmética / cliente | Subtle Effects 1.14.3; Polytone 1.21-4.4.0; Create Cyber Goggles 8.6.3; EntityCulling 1.10.5 | Efeitos visuais, integração e renderização não autorizam incremento do ledger mágico |

Esta triagem **não é prova de ausência** de magia nos JARs, sobretudo onde há addons ou automação configurável. Todos continuam dentro da auditoria física 489-JAR quando aplicável. Uma edição de `.md` não altera `modId`, versão instalada, hash, registro de feitiços nem acesso em Survival.

## Não promoção e próximos gates

- **587** entradas físicas certificadas = 97 Magic + 489 JARs fora de Magic + 1 loader. As duas adições pós-snapshot declaradas (Cold Sweat: Altitude, Create: Bionics) levam a **589** entradas conhecidas declaradas, mas **sem novo dump físico**. A substituição Alcubierre → AeroWarptics não foi fisicamente comprovada.
- **164** pastas canônicas estruturais, **453** dossiês cross-domain revisados e **346/347** OTHER: preservados; **#272** continua ⛔ sem dossiê físico verificável.
- **39** registries de providers com prova binary-exact pendente e **14** rotas de configuração/Survival pendentes: preservados.
- Mínimo semântico: **1851** global / **1849** escopo; **zero novo objeto certificado nesta revisão**.
- PR #733 de ritual foi incorporado na Black Arcana main; isso não certifica o novo altar com Malum/Eidolon na instância. Stage 06.05 segue 🟡 condicionada à aceitação real; não há autorização para avançar Stage 07.
- É necessário ler JARs reais, obter metadata, SHA/registries, execução e evidências de Survival conforme os coletores existentes antes de qualquer alteração de contagem ou estado físico.

**Resultado:** os 20 arquivos alterados eram dossiês `modified` no Git e não provam uma única adição de mod ou spell ao pack. Esta revisão fecha somente o delta **documental** comparado, mantendo a fronteira física e semântica fail-closed.
