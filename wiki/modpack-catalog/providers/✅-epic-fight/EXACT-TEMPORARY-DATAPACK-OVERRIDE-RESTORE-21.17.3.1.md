# Epic Fight 21.17.3.1 — datapack original temporário: alterar e restaurar o modifier após reload

## Cobertura causal ampliada: oito modifiers e cinco skills no provider carregado (17/10/2026)

✅ [CI de oito modificadores #39001996512](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39001996512) **SUCCESS**, com JSON de QA efetivamente publicado como artefato **12089431494**. Servidor Java21 / NeoForge físico **21.1.250**, JAR do Epic Fight **21.17.3.1** verificado por dois hashes. Cinco datapacks de substituição temporária escritos **somente no runner**, usando campos modernos e oito IDs QA distintos: `adaptive_skin 0→1→0`, `adrenaline_fiend 0→2→0`, `catharsis 0→2→0`, `bonebreaker 0→1→0`, `vengeance 0→2→0`; controles modernos `swordmaster/forbidden_strength/technician` estáveis **2/2/1** em três fases. Inclui `epicfight:stamina_regen`, aceito na coleção carregada. [Relatório e escopo](EXACT-ALL-FIVE-LEGACY-MODIFIER-OVERRIDE-RESTORE-21.17.3.1.md).

⚠️ Evidência de **mapa do provider**, não de atributos efetivos de jogador; sem `SkillContainer.setSkill`, equip/unequip, client ou modpack completo. Nenhum artefato QA foi transferido à produção; ⛔ hooks de perks e Mastery ainda sem contrato homologado. Core catalogado ✅ 43/43, **+0** magia.

**Data:** 17/10/2026. **Evidência:** ✅ `OVERRIDE_APPLY_AND_RESTORE_OBSERVED` em servidor dedicado isolado Java21 / Minecraft 1.21.1 / NeoForge **21.1.250**. **Provider:** Epic Fight `21.17.3.1`, mod ID `epicfight`, JAR CurseForge file `8175609` / project `405076`; SHA-1 `fb199b7bbea2fc402da28ab586e73f47e32f8fc0` e SHA-256 `8b882554cf10086398340fbdc741819ee72a801a3adce516c7f4768326a39526`.

## Procedimento realmente executado

[Workflow #38999302329](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38999302329), job `exact_datapack_override_restore`, terminou **SUCCESS**. A instalação do JAR físico e a verificação de ambos os hashes ocorreram antes do boot; o companion `black_arcana_epicfight_qa` foi compilado e instalado **somente no servidor descartável de QA**, não no JAR de produção.

No servidor, [`EpicFightOverrideCycleQa.java`](https://github.com/Gustavaopere/Black-Arcana/blob/docs/catalog-perk-causality-20261015/src/epicFightCatalogQa/java/dev/gustavopere/blackarcana/qa/epicfight/EpicFightOverrideCycleQa.java) executou, em sequência:

1. **Baseline real:** releitura de `EpicFightRegistries.SKILL` e do campo `Skill.attributes` das oito skills. Cinco legadas `0/0/0/0/0`; três controles modernos `swordmaster=2`, `forbidden_strength=2`, `technician=1`.
2. **Override original de QA:** criou temporariamente em `world/datapacks/black_arcana_epicfight_override_qa` um `pack.mcmeta` de formato 48 e o arquivo `data/epicfight/skill_parameters/adaptive_skin.json`. O **conteúdo de QA próprio**, sem copiar o código ou assets do publisher, declara somente um atributo `minecraft:generic.max_health` com modifier `id=black_arcana_epicfight_qa:adaptive_skin_control`, `operation=add_value`, `amount=6.0`. O `PackRepository` descobriu o pack como `file/black_arcana_epicfight_override_qa`, ele foi selecionado e `MinecraftServer.reloadResources` foi concluído. A skill `adaptive_skin` passou a ter **1** entrada em `Skill.attributes`. As outras sete permaneceram estáveis.
3. **Remoção e restauração:** o companion apagou apenas seu próprio diretório temporário, atualizou a seleção de packs e executou outro `MinecraftServer.reloadResources`. `adaptive_skin` voltou de **1 para 0**, com os mesmos sete controles estáveis. O workflow verificou que o diretório temporário não existia ao final.

O log apresentou `type=phase_end phase=baseline status=OBSERVED observed=8`, `override_begin status=REQUESTED`, `type=phase_end phase=override status=OBSERVED observed=8`, `restore_begin status=REQUESTED`, `type=phase_end phase=restored status=OBSERVED observed=8` e `type=end status=OBSERVED phases=baseline,override,restored`. O JSON de evidência (com somente cardinalidades de QA) foi publicado pelo workflow; **JAR e assets originais do provider não foram publicados**.

## Matriz de cardinalidade diretamente observada

| Skill | Baseline | Override aplicado | Após remover override |
|---|---:|---:|---:|
| `epicfight:adaptive_skin` | **0** | **1** | **0** |
| `epicfight:adrenaline_fiend` | 0 | 0 | 0 |
| `epicfight:catharsis` | 0 | 0 | 0 |
| `epicfight:bonebreaker` | 0 | 0 | 0 |
| `epicfight:vengeance` | 0 | 0 | 0 |
| `epicfight:swordmaster` | 2 | 2 | 2 |
| `epicfight:forbidden_strength` | 2 | 2 | 2 |
| `epicfight:technician` | 1 | 1 | 1 |

## Conclusão delimitada

O teste demonstra **causalidade da leitura do datapack de override para o mapa de atributos da skill** no servidor isolado. No baseline físico, os oito modificadores legados embutidos nos cinco arquivos permaneceram ausentes nas coleções; após substituir **apenas** a skill `adaptive_skin` por uma declaração moderna de QA, a coleção registrou um modifier; ao retirar o pack de QA, a coleção voltou ao estado inicial. Portanto, a coleção **respondeu** à mudança real de recurso, não apenas a um reload vazio.

**Não homologado:** o teste não equipou a skill em jogador, não consultou `AttributeInstance`, não confirmou max health efetivamente aplicado, não verificou morte/respawn, sincronização cliente/servidor ou behavior dos addons do modpack completo. É um **datapack de QA temporário**; não publicar a alteração de balanceamento como fix e não supor que todas as skills com JSON legado se comportam identicamente.

O teste de override foi opt-in por `BLACK_ARCANA_EPICFIGHT_QA_OVERRIDE_CYCLE=1`; a rotina original de estabilidade após reload permanece separada. A prova não autoriza adaptar perks, duplicar dano ou alterar o pipeline de combate: Epic Fight segue autoridade de skills/combate, Black Arcana segue authority do runtime mágico, RPG Skill Tree apenas provider de Mastery/progressão por contrato real.

**Métricas de catálogo inalteradas:** Epic Fight ✅ 43/43 identidades core classificadas e 42/42 JSONs físicos, três trident innates previamente contadas, **+0 magias novas**. Piso global **1.856 objetos semânticos mínimos / 1.854 estritos**, denominador global aberto. Stage 06.05 🟡 e Stage 09 físico pendente; PR #825 draft, sem merge.
