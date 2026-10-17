# Epic Fight 21.17.3.1 — todos os oito modificadores legados convertidos em QA e restaurados

**Data do checkpoint:** 17/10/2026. **Evidência:** ✅ `ALL_FIVE_MODERNIZED_MAPS_LOAD_AND_RESTORE` — rótulo documental, não API nem enum de produção. Cenário: servidor dedicado isolado Minecraft 1.21.1 / **NeoForge 21.1.250** / Java21, com JAR exato `epicfight` versão **21.17.3.1** carregado.

## Prova física do publisher e execução

- Artefato oficial CurseForge `405076 / 8175609`, SHA-1 `fb199b7bbea2fc402da28ab586e73f47e32f8fc0`, SHA-256 `8b882554cf10086398340fbdc741819ee72a801a3adce516c7f4768326a39526`. Os hashes foram validados pelo workflow antes de iniciar o servidor. O JAR só foi montado no servidor descartável.
- [GitHub Actions #39001996512](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39001996512) **SUCCESS**: job `all_five_attribute_modernization` executou as três fases e publicou **JSON de QA limitado, sem assets/JAR do publisher**, artefato GitHub **12089431494**. A falha do upload no primeiro experimento [#39001791151](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39001791151) foi corrigida com caminho explícito e `if-no-files-found: error`; o primeiro run também tinha **SUCCESS** na verificação de logs, mas **não havia artefato publicado**. O segundo passou com o upload obrigatório.
- [`EpicFightOverrideCycleQa.java`](https://github.com/Gustavaopere/Black-Arcana/blob/docs/catalog-perk-causality-20261015/src/epicFightCatalogQa/java/dev/gustavopere/blackarcana/qa/epicfight/EpicFightOverrideCycleQa.java) contém fixtures **originais de QA**, criadas a partir de tipos de atributos, operações e quantias auditadas no JAR, sem copiar código ou assets de terceiros. As operações foram substituídas por `add_value` ou `add_multiplied_total` e os oito `id` são gerados sob o namespace QA `black_arcana_epicfight_qa:`. O datapack temporário contém cinco recursos `data/epicfight/skill_parameters/{adaptive_skin,adrenaline_fiend,catharsis,bonebreaker,vengeance}.json`, sempre gerados em runtime e removidos no mesmo processo.
- O gate é **opt-in**, ativado por `BLACK_ARCANA_EPICFIGHT_QA_OVERRIDE_CYCLE=1` junto com `BLACK_ARCANA_EPICFIGHT_QA_ALL_LEGACY=1`. [Workflow isolado](https://github.com/Gustavaopere/Black-Arcana/blob/docs/catalog-perk-causality-20261015/.github/workflows/epicfight-211731-all-five-modifier-override-qa.yml) faz dois `MinecraftServer.reloadResources`, exige as **oito identidades** em `baseline`, `override` e `restored` com cardinalidade exata; falha caso a limpeza do datapack não seja confirmada. O workflow de regressão de uma skill permanece separado.

## Matriz observada em `Skill.attributes` do provider carregado

| Skill core | Entradas originais no publisher | Baseline | Durante datapack QA | Após remoção e reload |
|---|---:|---:|---:|---:|
| `epicfight:adaptive_skin` | 1 | **0** | **1** | **0** |
| `epicfight:adrenaline_fiend` | 2 | **0** | **2** | **0** |
| `epicfight:catharsis` | 2 | **0** | **2** | **0** |
| `epicfight:bonebreaker` | 1 | **0** | **1** | **0** |
| `epicfight:vengeance` | 2 | **0** | **2** | **0** |
| **Total das cinco skills** | **8** | **0** | **8** | **0** |
| `epicfight:swordmaster` | 2 (moderno) | 2 | 2 | 2 |
| `epicfight:forbidden_strength` | 2 (moderno) | 2 | 2 | 2 |
| `epicfight:technician` | 1 (moderno) | 1 | 1 | 1 |

O teste inclui a entrada própria do Epic Fight `epicfight:stamina_regen` na skill `catharsis`, além de atributos vanilla como `generic.max_health`, `generic.attack_speed` e `generic.attack_damage`. O controle positivo de `catharsis=2` confirma que **os dois modifiers modernos sintéticos** foram aceitos na coleção do registry, não o efeito de stamina aplicado em jogador.

## Conclusão de escopo

**Comprovado no servidor isolado:** o pipeline de recurso e o codec do provider conseguem materializar **oito modificadores em cinco skills** se os campos de identidade e operação usarem formato moderno, e desfazer a carga após remover o datapack de QA. O cenário reproduz a diferença entre os campos legados e os modernos sem inferir que todos os efeitos de skill estejam inoperantes.

**Não comprovado:** efeito em `AttributeInstance` de um `ServerPlayer`, equipar e remover a skill em `SkillContainer`, respawn/persistência, segurança em cliente remoto, presença dos addons do modpack completo de 587 entradas ou comportamento de Mastery/perks. A referência de código upstream `21.17.3` é adjacente, não fonte exata da API física `21.17.3.1`; a prova compilada do provider não autoriza hooks de integração.

**Próximo gate físico:** instrumentar, em cenário descartável com jogador real conectado (ou substituto cuja API exata seja comprovada), o ciclo `SkillContainer.setSkill` e a mudança de `AttributeInstance`, além de remoção/deduplicação, e classificar tudo como Stage 09 manual/phys quando necessário. É indispensável validar autorização, lifespan e origem da capability de `PlayerPatch`; não fabricar um proxy e não chamar `onInitiate` com executor nulo.

**Estado global preservado:** Epic Fight ✅ 43/43 identidades core, 42/42 JSONs físicos, 28 dossiês de perks, três trident innates sobrenaturais previamente catalogadas e **+0 magias** nesta etapa. Piso global **1.856 semânticas mínimas / 1.854 estritas**, denominador aberto. Stage 06.05 🟡 e Stage 09 físico pendente. PR #825 em draft, sem merge.
