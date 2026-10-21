# Epic Fight — cinco modifiers legados no registry carregado 21.17.3.1 (16/10/2026)

## Gate posterior: reload real de recursos e nova leitura (17/10/2026)

✅ [GitHub Actions #38998283536](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38998283536) **SUCCESS**. Depois do `ServerStartedEvent`, o companion QA iniciou `MinecraftServer.reloadResources`, aguardou o future e consultou novamente `Skill.attributes`. As cinco skills legadas mantiveram **0/0/0/0/0** e os três controles modernos mantiveram **2/2/1**. [Relatório de estabilidade pós-reload](EXACT-SERVER-RELOAD-ATTRIBUTE-CARDINALITY-21.17.3.1.md). Ainda não houve override real de datapack, comparação de atributos de jogadores ou equip/unequip.

**Estado:** ✅ `PROVIDER_LOADED_REGISTRY_OBSERVED` no ambiente **servidor isolado NeoForge 21.1.250**, com cinco skills legadas **0/0/0/0/0 modificadores em `Skill.attributes`** e três controles modernos positivos **2/2/1**. **Não** é medição de `AttributeInstance` do jogador, nem equivalência com o modpack completo de 587 entradas.

## Prova executada

- [GitHub Actions #38990309407](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38990309407), job `exact_loaded_registry`, **SUCCESS**. O run buscou o JAR CurseForge **405076/8175609**, validou SHA-1 `fb199b7bbea2fc402da28ab586e73f47e32f8fc0` e SHA-256 `8b882554cf10086398340fbdc741819ee72a801a3adce516c7f4768326a39526` antes de instalá-lo na pasta `runs/server/mods`; compilou o companion QA sob **Minecraft 1.21.1, NeoForge 21.1.250, Java 21** e iniciou o servidor dedicado. Asserts exigem `ModList.get().isLoaded("epicfight") == true`, cinco skills do registro presentes, três controles do registro presentes e cardinalidades positivas exatas.
- [`EpicFightCatalogQaMod.java`](https://github.com/Gustavaopere/Black-Arcana/blob/docs/catalog-perk-causality-20261015/src/epicFightCatalogQa/java/dev/gustavopere/blackarcana/qa/epicfight/EpicFightCatalogQaMod.java) é mod de **QA somente**, ID `black_arcana_epicfight_qa`, em source set e JAR separados; a tarefa [`epicFightCatalogQaJar`](https://github.com/Gustavaopere/Black-Arcana/blob/docs/catalog-perk-causality-20261015/build.gradle) nunca entra no JAR de produção. A consulta resolve `EpicFightRegistries.SKILL` por reflexão para consultar skills registradas; observa **somente** o tamanho do campo interno `Skill.attributes`, sem ler ataques, resources, jogador ou estados de cliente. O gate valida que a classe QA não vazou ao JAR de produção.
- [Workflow de bootstrap e reconciliação](https://github.com/Gustavaopere/Black-Arcana/blob/docs/catalog-perk-causality-20261015/.github/workflows/epicfight-211731-loaded-registry-qa.yml) publica apenas JSON de cardinalidades, nunca o JAR do publisher ou classes protegidas. Não há adapter, hook de perk ou cast implementado.

## Oito skills observadas após ServerStartedEvent

| Skill física | Formato `attribute_modifiers` no publisher JAR | Entradas efetivamente encontradas em `Skill.attributes` |
|---|---:|---:|
| `epicfight:adaptive_skin` | Legado: 1 | **0** |
| `epicfight:adrenaline_fiend` | Legado: 2 | **0** |
| `epicfight:catharsis` | Legado: 2 | **0** |
| `epicfight:bonebreaker` | Legado: 1 | **0** |
| `epicfight:vengeance` | Legado: 2 | **0** |
| `epicfight:swordmaster` | Moderno: 2 | **2** |
| `epicfight:forbidden_strength` | Moderno: 2 | **2** |
| `epicfight:technician` | Moderno: 1 | **1** |

**Conclusão estrita:** no cenário observado, os oito modifiers serializados legados **não foram materializados na coleção base de atributos das cinco skills**, apesar de o mesmo provider materializar os cinco registros modernos de três skills de controle. O fato de os controles passarem elimina a hipótese de que **todas** as coleções estivessem vazias porque nenhum datapack tivesse sido aplicado. Não demonstra por si só que os oito modifiers sejam excluídos em todo modpack, em overrides, sob outro ponto do lifecycle ou por outra via de atributo.

## Diagnóstico fechado de reflection sidedness

- [Run #38989149726](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38989149726) **FAIL_CLOSED**: servidor iniciado, entrada esperada não observada.
- [Run #38989380450](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38989380450) **FAIL_CLOSED**: `PROVIDER_ABI_UNAVAILABLE`, posteriormente localizado no mesmo caminho.
- [Run #38989820824](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38989820824) **FAIL_CLOSED**: `Class.getMethod("getModfierEntry")` tentou resolver `net/minecraft/client/gui/GuiGraphics` em `DEDICATED_SERVER`, e `RuntimeDistCleaner.processClassWithFlags` lançou `RuntimeException`. **Não atribuir essa falha ao runtime normal do Epic Fight.**
- [Run #38990047892](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38990047892) **SUCCESS** após trocar introspecção de métodos por leitura restrita do campo `attributes`, com cinco observações vazias; [#38990309407](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38990309407) adicionou os **três controles positivos**, todos observados com cardinalidade exata.

## Limites de autoridade e próximos gates

1. ✅ **JAR e mod IDs físicos**: `epicfight` / 21.17.3.1 / hashes pinados; ✅ **registry loaded mínimo isolado**, sujeito a event/lifecycle e configuração desse servidor.
2. ⚠️ **Modpack completo**: não foram instalados os 587 componentes do snapshot físico, addons Epic Fight, cliente ou KubeJS/script overrides. Ainda exigidos provider-loaded QA na composição real e datapack reload.
3. ⚠️ **Atributos efetivos do jogador**: não se equipou/desmontou skill, não se compararam `AttributeInstance`, mortes, troca de dimensão ou persistência. Uma coleção vazia na skill não permite declarar que a skill inteira está desabilitada: ela pode executar lógica própria independente do campo `attribute_modifiers`.
4. ⛔ **Integração de perks/Mastery/RPG Skill Tree**: nenhum ABI/hook seguro homologado. Não duplicar dano, stamina, stun, resource budget, guards, weapon innates ou costs. Black Arcana preserva seu runtime mágico e `WorldEffectPolicy`; Epic Fight controla combate.
5. 🟡 **Stage 06.05** continua pendente de aceite físico, Stage 09 segue bloqueado para release; PR permanece draft, sem merge.

**Métrica global inalterada:** ✅ 43/43 core skill IDs Epic Fight classificados; 42/42 JSONs físicos; 28 dossiês; +0 novas magias; piso 1.856 objetos mágicos semânticos mínimos / 1.854 estritos, denominador desconhecido.
