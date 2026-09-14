# Ars 'n' Spells 3.0.2 — catálogo mágico

Última auditoria: 2026-09-14

## Escopo e autoridade

Este catálogo cobre a superfície **fixa de spells/rituais pertencente ao addon `ars_n_spells` 3.0.2 para NeoForge 1.21.1**. Ele não duplica como conteúdo do addon os spells dinâmicos de Ars Nouveau ou Iron's Spells 'n Spellbooks que o bridge transporta, inscreve ou delega.

Presença/versão no inventário versionado do modpack:

- RPG Skill Tree sibling `docs/MODPACK_SCOPE.md`, derivado de `modlist(20260822-201255).txt`: `ars_n_spells` `3.0.2`.
- A modlist física/runtime atual continua sendo autoridade superior quando estiver disponível/versionada; este arquivo não afirma presença física posterior ao snapshot.

Fonte upstream exata auditada:

- repositório: `otectus/ars-n-spells`;
- branch NeoForge 1.21.1: `port/neoforge-1.21.1`;
- commit de release 3.0.2: `20953dda8cca4a167f31f3ef161079446c83c15b`;
- o `README.md` desse commit identifica explicitamente `v3.0.2, NeoForge 1.21.1` e descreve o projeto como bridge entre Ars Nouveau e Iron's Spells 'n Spellbooks.

## Resultado

Estado: ✅ **Catalogado para a superfície spell/ritual própria da versão 3.0.2**.

Resumo fechado:

- **8** registros reais no registry de `AbstractSpell`: `ars_n_spells:ars_cross_1` até `ars_n_spells:ars_cross_8`;
- **0** desses oito proxies possui efeito mágico próprio: todos delegam para um payload de spell de Ars Nouveau armazenado no spellbook/item;
- **5** rituais próprios registrados no `RitualRegistry` de Ars Nouveau;
- **13** registros mágicos fixos próprios do addon quando Iron's está carregado: 8 proxies + 5 rituais;
- sem Iron's carregado, os proxies não são registrados e somente `Spell Uninscription` é registrado entre os cinco rituais auditados;
- spells de Ars Nouveau e Iron's referenciados dinamicamente pela camada de cross-cast **não são contados novamente** como spells de Ars 'n' Spells.

## 1. Spell registry — proxy pool

`ArsCrossProxyRegistry` cria um `DeferredRegister<AbstractSpell>` no registry de spells do Iron's e registra um pool finito de oito IDs. `CrossModSpellComponents.PROXY_POOL_SIZE` fixa o tamanho em `8`.

| ID | Tipo | Efeito próprio | Semântica catalogada |
| --- | --- | --- | --- |
| `ars_n_spells:ars_cross_1` | proxy `AbstractSpell` | não | slot 1 para delegar ao payload Ars vinculado ao livro |
| `ars_n_spells:ars_cross_2` | proxy `AbstractSpell` | não | slot 2 para delegar ao payload Ars vinculado ao livro |
| `ars_n_spells:ars_cross_3` | proxy `AbstractSpell` | não | slot 3 para delegar ao payload Ars vinculado ao livro |
| `ars_n_spells:ars_cross_4` | proxy `AbstractSpell` | não | slot 4 para delegar ao payload Ars vinculado ao livro |
| `ars_n_spells:ars_cross_5` | proxy `AbstractSpell` | não | slot 5 para delegar ao payload Ars vinculado ao livro |
| `ars_n_spells:ars_cross_6` | proxy `AbstractSpell` | não | slot 6 para delegar ao payload Ars vinculado ao livro |
| `ars_n_spells:ars_cross_7` | proxy `AbstractSpell` | não | slot 7 para delegar ao payload Ars vinculado ao livro |
| `ars_n_spells:ars_cross_8` | proxy `AbstractSpell` | não | slot 8 para delegar ao payload Ars vinculado ao livro |

### Semântica dos proxies

`ArsCrossProxySpell` declara custo intrínseco zero (`baseManaCost = 0`, `manaCostPerLevel = 0` e `getManaCost(...) = 0`) e, no cast server-side, localiza o payload Ars correspondente ao `poolId` no item de casting e delega para `CrossCastingHandler.castArsSpell(...)`. Portanto:

- o proxy existe para satisfazer a identidade de spell exigida pela roda nativa do Iron's;
- o efeito real continua sendo o spell Ars armazenado no payload;
- custo/efeito não devem ser atribuídos ao proxy como um spell original do addon;
- a contagem `8` mede **slots de registry**, não oito novos efeitos mágicos.

## 2. Ritual registry

`RitualRegistryHandler.registerRituals()` fecha o conjunto de rituais registrado pela versão auditada.

| Ritual / ID | Condição | Semântica observável no código auditado |
| --- | --- | --- |
| Spell Uninscription — `ars_n_spells:spell_uninscription` | sempre registrado | remove o componente de cross-cast de exatamente um item inscrito; é deliberadamente independente de Iron's |
| Mana Infusion — `ars_n_spells:mana_infusion` | requer `irons_spellbooks` carregado | ao terminar, adiciona a quantidade configurada de mana do Iron's ao jogador mais próximo no raio fixo do ritual |
| Spell Transcription — `ars_n_spells:spell_transcription` | requer `irons_spellbooks` carregado | consome uma fonte spell-bearing Ars/Iron's e grava seu spell em um alvo como payload de cross-cast |
| Mana Well — `ars_n_spells:mana_well` | requer `irons_spellbooks` carregado | durante o tick do ritual, adiciona mana do Iron's aos jogadores na área configurada |
| Spellbook Binding — `ars_n_spells:spellbook_binding` | requer `irons_spellbooks` carregado | vincula um spell Ars exportado em carrier scroll a um spellbook real do Iron's e aloca um proxy `ars_cross_n` para a roda nativa |

A condição acima deriva do próprio `RitualRegistryHandler`: `SpellUninscriptionRitual` é registrado antes do gate `ModList.get().isLoaded("irons_spellbooks")`; os outros quatro são registrados apenas depois desse gate.

## 3. Sistemas mágicos relacionados, sem contagem como spells próprios

O README da release 3.0.2 documenta sistemas de integração que afetam casting e progressão — mana unification, spell scaling, resonance, cooldown categories, progression, affinity e cross-mod spell casting. Eles são semanticamente relevantes para interoperabilidade, mas **não aumentam a contagem de spell IDs próprios** deste catálogo.

Em particular:

- o cross-cast pode carregar spells existentes de Ars Nouveau ou Iron's em itens;
- o Spell Loom/export/binding pode fazer um spell Ars aparecer na roda do Iron's;
- essa aparição usa um dos oito IDs-proxy e não transfere ownership do spell original para `ars_n_spells`.

## 4. Evidência técnica upstream

Commit exato auditado: `20953dda8cca4a167f31f3ef161079446c83c15b`.

Arquivos usados para fechar o inventário:

- `README.md` — versão, propósito do bridge e descrição dos sistemas/cross-cast;
- `src/main/java/com/otectus/arsnspells/spell/irons/ArsCrossProxyRegistry.java` — registro do pool de proxies;
- `src/main/java/com/otectus/arsnspells/spell/irons/ArsCrossProxySpell.java` — semântica de delegação e custo zero do proxy;
- `src/main/java/com/otectus/arsnspells/spell/CrossModSpellComponents.java` — `PROXY_POOL_SIZE = 8` e sidecar/payload de cross-cast;
- `src/main/java/com/otectus/arsnspells/rituals/RitualRegistryHandler.java` — conjunto e gates dos cinco rituais;
- classes dos cinco rituais para IDs e comportamento individual.

## 5. Limite clean-room

A inspeção de fonte upstream foi usada somente para **enumerar registries, IDs, gates e comportamento público relevante à catalogação/interoperabilidade**. Nenhuma implementação, código, asset, texto de UI, modelo ou lógica proprietária é incorporada ao runtime do Black Arcana por este catálogo.

Este documento não cria bridge, adapter ou dependência de runtime. Qualquer integração futura continua sujeita à versão física instalada, contrato real do provider, autoridade do Black Arcana e fail-closed quando não houver hook seguro.
