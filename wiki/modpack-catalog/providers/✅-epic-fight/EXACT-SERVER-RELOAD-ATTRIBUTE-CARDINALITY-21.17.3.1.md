# Epic Fight 21.17.3.1 — estabilidade do registry de modifiers após reload real (17/10/2026)

## Gate causal de datapack original e restauração — 17/10/2026

✅ [Actions #38999302329](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38999302329) **SUCCESS**: em servidor NeoForge 21.1.250 com Epic Fight físico 21.17.3.1, o datapack descartável original de QA substituiu `data/epicfight/skill_parameters/adaptive_skin.json` por um modifier moderno `id=black_arcana_epicfight_qa:adaptive_skin_control`, `operation=add_value`. Após reload, a coleção `Skill.attributes` de `adaptive_skin` mudou **0→1**; após remover o datapack e novo reload, voltou **1→0**. As outras sete skills controladas permaneceram **0/0/0/0 (legadas)** e **2/2/1 (modernas)**. [Prova de três fases e limites](EXACT-TEMPORARY-DATAPACK-OVERRIDE-RESTORE-21.17.3.1.md).

⚠️ Prova causal **somente do mapa carregado da skill** no servidor isolado. Não prova `AttributeInstance` aplicado no jogador, equip/unequip ou modpack completo de 587 entradas. Nenhum datapack de override de QA foi incluído no produto; nenhum adapter de perks/Mastery foi implementado. O gate anterior de reload sem override permanece válido como evidência histórica separada.

**Resultado:** ✅ `RESOURCE_RELOAD_COMPLETED_REGISTRY_COUNTS_STABLE_ISOLATED_SERVER`, com dados exatos para **8/8 skills** do provider carregado em servidor NeoForge **21.1.250**. Este rótulo é apenas uma **categoria documental de QA**, não enum de API e não significa `PLAYER_ATTRIBUTE_INSTANCE_VALIDATED` nem override de datapack.

## Artefato e prova

- **Build física:** Epic Fight `21.17.3.1` / `epicfight`, JAR oficial CurseForge `405076/8175609`, SHA-1 `fb199b7bbea2fc402da28ab586e73f47e32f8fc0`, SHA-256 `8b882554cf10086398340fbdc741819ee72a801a3adce516c7f4768326a39526`. Java **21**, Minecraft **1.21.1**, NeoForge do pack **21.1.250**. Workflow mantém o publisher JAR no runner e não o publica.
- **Execução:** [GitHub Actions #38998283536](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38998283536), job `exact_loaded_registry` — **SUCCESS**. O companion isolado `black_arcana_epicfight_qa` leu as oito coleções `Skill.attributes` após `ServerStartedEvent`, invocou o pipeline `MinecraftServer.reloadResources(server.getPackRepository().getSelectedIds())`, aguardou a conclusão do `CompletableFuture` e, na thread do servidor, voltou a consultar as coleções. O workflow **exige** o evento de conclusão `type=reload_end status=OBSERVED observed=5 controls=3` e oito cardinalidades exatas antes de publicar JSON limitado.
- **Fonte upstream adjacente, não substituta da evidência física:** [`SkillReloadListener.java` L99–136 na revisão 21.17.3](https://github.com/Antikythera-Studios/epicfight/blob/a78aa24b72e90a9d09f5fd61925e4369d117abaf/src/main/java/yesman/epicfight/api/data/reloader/SkillReloadListener.java#L99-L136) descreve o listener de recursos `skill_parameters` e a invocação de `loadDatapackParameters`. O JAR instalado é a revisão física posterior **21.17.3.1**; a existência desse código adjacente não comprova, sozinha, qual listener foi chamado no teste.

## Estado observado nas duas leituras

| Skill | Dados físicos (JSON) | `Skill.attributes` no boot | `Skill.attributes` após reload |
|---|---:|---:|---:|
| `epicfight:adaptive_skin` | 1 legado | **0** | **0** |
| `epicfight:adrenaline_fiend` | 2 legados | **0** | **0** |
| `epicfight:catharsis` | 2 legados | **0** | **0** |
| `epicfight:bonebreaker` | 1 legado | **0** | **0** |
| `epicfight:vengeance` | 2 legados | **0** | **0** |
| `epicfight:swordmaster` | 2 modernos | **2** | **2** |
| `epicfight:forbidden_strength` | 2 modernos | **2** | **2** |
| `epicfight:technician` | 1 moderno | **1** | **1** |

O teste distinguiu `type=reload_begin status=REQUESTED` de `type=reload_end status=OBSERVED` e exigiu o registro de todas as oito skills **após** a resolução do future. A cardinalidade dos **oito modificadores legados do JSON** continuou **0/8** no mapa carregado, enquanto os **cinco modificadores modernos de controle** permaneceram **5/5**.

## Limites e próximo gate

1. ✅ **Estabilidade do mapa carregado após reload de recursos** comprovada no servidor isolado, sem cliente, sem addon e sem outro script do modpack.
2. ⚠️ **Não foi aplicado override de datapack.** Com recursos inalterados, igualdade antes/depois não prova individualmente a execução nem o efeito específico de `SkillReloadListener.apply` em todos os caminhos. Para fechar causalidade da carga, criar um **datapack original de QA** com um modifier moderno substituindo um dos oito legados, testar cardinalidade alterada, remover override e restaurar estado. Não transportar esse override para a distribuição real.
3. ⚠️ **Não houve `AttributeInstance` de jogador**: equip/unequip, atributos reais, persistência, death/respawn e sincronização client/server seguem sem validação. Não autoriza afirmar que as cinco skills inteiras estejam desabilitadas; apenas o campo declarativo foi observado vazio.
4. ⛔ **Integração de Mastery/perks do RPG Skill Tree** permanece sem contrato seguro de evento/ABI de versão física. Epic Fight mantém autoridade sobre combate, animações, stamina e skill pipeline. Black Arcana mantém casting, rituais, hazards, custos e demais runtimes mágicos próprios.
5. 🟡 Stage 06.05 inalterado; Stage 09 físico pendente; não há merge.

**Catálogo:** Epic Fight core ✅ 43/43 IDs catalogados, 42/42 JSONs físicos, 28 dossiês técnico-causais preexistentes, três trident innates previamente contadas. **+0** magias, piso global **1.856 semânticos mínimos / 1.854 estritos**, denominador global ainda desconhecido.
