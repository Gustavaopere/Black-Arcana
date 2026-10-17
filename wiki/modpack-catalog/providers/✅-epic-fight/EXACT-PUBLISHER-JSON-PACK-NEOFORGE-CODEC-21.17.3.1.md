# Epic Fight — JAR físico → codec Minecraft no NeoForge exato do pack

**Status da prova nova:** `PENDING_WORKFLOW`, sujeito ao resultado do gate de GitHub Actions. **Não** declarar `provider-loaded`, atributo aplicado ou controle de fluxo/condição testado. Este é um probe opcional e isolado do codec **vanilla Minecraft**, não um teste de skill ativada do Epic Fight.

## Evidência-fonte e motivo

- Modlist física sibling, posição **#260/587 entradas**: `epic-fight-21.17.3.1-mc1.21.1-neoforge.jar`, `modid epicfight`, CurseForge `405076 / 8175609`, SHA-1 `fb199b7bbea2fc402da28ab586e73f47e32f8fc0` e SHA-256 `8b882554cf10086398340fbdc741819ee72a801a3adce516c7f4768326a39526`, NeoForge físico **21.1.250**. A branch main do Black Arcana usa NeoForge **21.1.248**: essas versões não devem ser tratadas como intercambiáveis.
- [Teste isolado de publisher JAR](https://github.com/Gustavaopere/Black-Arcana/blob/docs/catalog-perk-causality-20261015/src/test/java/dev/gustavopere/blackarcana/integration/epicfight/EpicFightPublisherJarAttributeCodecTest.java) lê **literalmente** `data/epicfight/skill_parameters/{adaptive_skin,adrenaline_fiend,catharsis,bonebreaker,vengeance}.json` do arquivo zip baixado após verificar **os dois hashes**. Usa `JsonOps` → `NbtOps` e `AttributeModifier.MAP_CODEC` do Minecraft real. Exige oito registros físicos distribuídos como **1 + 2 + 2 + 1 + 2**.
- [Workflow isolado de NeoForge 21.1.250](https://github.com/Gustavaopere/Black-Arcana/blob/docs/catalog-perk-causality-20261015/.github/workflows/epicfight-211731-publisher-attribute-codec.yml) pinou `-Pneo_version=21.1.250`, Java 21, e exige **2/2 testes não ignorados** no XML JUnit; retorna somente XML de QA com retenção curta, **jamais** o JAR do publisher.
- **Testes desenhados (se e somente se o workflow passar):** a primeira asserção inspeciona os 5 recursos empacotados, verifica 8/8 linhas `name/uuid`, ausência de `id`, `operation` legada e resultado de parse vazio para o codec do modifier, inclusive a lista composta por `Codec.list`. A segunda reconstrói apenas controles modernos `id/add_value|add_multiplied_total` preservando os **amounts do publisher**, exigindo parse individual e de lista.
- **Isolamento:** o teste JUnit somente ativa quando `EPICFIGHT_PUBLISHER_JAR` existe no ambiente. O job independente verifica explicitamente a execução não ignorada no XML. O teste não injeta o Epic Fight no gameTestServer nem classpath de produção, não altera spells/perks/runtime, não redistribui código/asset/JAR de terceiros.

## Limites e próximos gates

Ainda não executa o `Skill.ATTRIBUTE_ENTRY_CODEC` da classe Epic Fight, o reload do datapack no mod instalado ou o lifecycle `Skill.onInitiate/onRemoved` em entidades reais. Mesmo com `SUCCESS`, a classificação dos cinco modifiers continua **⚠️ `RAW_ONLY_NOT_PROVEN_LOADED` no provider**, e perks/atributos não são homologados. Teste realmente **provider-loaded** requer pack com dependencies exatas, inicialização dedicada, equipar/desabilitar skill, comparação de `AttributeInstance`, recarregamento e consistência client/server.

**Identidades mágicas:** nenhum novo feitiço — core Epic Fight segue 43/43 registros, 42/42 JSONs, 3 trident innates previamente contadas. Piso global 1.856 semânticas mínimas / 1.854 estritas, denominador desconhecido. Stage 06.05 🟡; Stage 09 físico pendente, sem merge.
