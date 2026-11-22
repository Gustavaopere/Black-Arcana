# Galena Gauntlet — mineração, progresso e efeitos de destruição (Alex's Caves Continued 1.0.10)

**Estado:** ⚠️ **subcontrato estático SHA-exato, somente leitura**. A ficha individual `equipment/galena-gauntlet.md` permanece `static_contract=NOT_CERTIFIED`, `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `perks_executable=NOT_CERTIFIED`, `provider_universe_closed=false`, `NO_MUTATION`. A evidência abaixo prova **instruções e fluxo local do publisher**; não comprova aceitação de proteção territorial, alteração efetiva do bloco, drops, experiência final, segurança de eventos ou viabilidade de hook.

## 1. Artefato, origem e reprodução

- **Identidade física registrada no sibling `neoforge-rpg-skilltree`:** `alexscaves`, Alex's Caves Continued **1.0.10**, Minecraft **1.21.1**, NeoForge, Java 21, `alexscaves-1.0.10-neoforge+1.21.1.jar`, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`. Modlist física datada de 22/09/2026; não houve novo confronto dos bytes do JAR extraído do cliente/servidor instalado.
- **Publisher efetivamente inspecionado no CI:** JAR de **75.279.314 bytes**, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`. `installed_dump_parity=NOT_VERIFIED`. O SHA-1 do publisher coincide com o declarado no inventário físico, mas isso **não substitui** uma comparação de arquivos extraídos da instância.
- **Classe nativa:** `com/github/alexmodguy/alexscaves/server/entity/item/MagneticWeaponEntity`, classfile SHA-256 `a26794c9eba89c554e812078886beda6129d5298219f685f6d0e2be315fbf071`; 24 métodos executáveis e 17 campos no censo exato; `tick()V`: 744 instruções, atributo `Code` SHA-256 `eaf08e761f108f4e5f15816ca7f72807c068e51376ec9ed27588d65a6385a699`. O novo recorte audita o trecho causal da mineração **dentro de `tick`** e pinna as identidades bytecode de `getDigSpeed(Player,BlockState,BlockPos)` e `damageItem(int)` como dependências. Sua semântica interna já possui [auditoria separada](EXACT-GALENA-GAUNTLET-DAMAGE-DIGSPEED-1.0.10.md), que **não** autoriza contratos mutadores.
- **Relatório original da descoberta** `report.json`: **1.780.492 bytes**, SHA-256 `c91a48f9892be09c4ab951c8083703b0c5ffbb026fc43e7d808c2033dde8bba9`, obtido da execução [#45071358036](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45071358036), artefato GitHub Actions **#14773961125**. A sonda `docs/qa/alexscaves_1010_galena_gauntlet_discovery.py` o reconstrói a partir do JAR publisher.
- **Prova específica:** [manifesto SHA-exato](EXACT-GALENA-GAUNTLET-MINING-WORLD-EFFECT-1.0.10.json), [verificador de CFG/bytecode](../../../../docs/qa/alexscaves_1010_galena_mining_world_effect_checks.py) e [workflow de reprodução](../../../../.github/workflows/alexscaves-1010-galena-mining-world-effect.yml). O verificador prende **222 pivôs JVM tipados**, descritores, hashes, branches, constantes e a cardinalidade de callsites; rejeita **35 mutações adversariais** de opcodes/operandos com digests do relatório e método recalculados. Os resultados de CI devem ser associados à HEAD final da PR, não antecipados neste dossiê.

## 2. Origem do alvo e guardas antes da mineração

O método `tick` obtém `getController` e `getTarget` @20–29. O ramo de player é escolhido por `controller instanceof Player` @470–481, e consulta `isOwnerWearingGauntlet` @540–544 antes do raycast. A definição de distância nominal dessa consulta já foi documentada no [subcontrato de targeting](EXACT-GALENA-GAUNTLET-PLAYER-TARGETING-1.0.10.md): `30.0f + 5.0f × nível FIELD_EXTENSION`; não representa autorização de mineração ou alcance efetivo do bloco. `ProjectileUtil.getHitResultOnViewVector` é solicitado @649–659.

A rota de bloco @802–928 exige um `BlockHitResult` @862–872. O `BlockPos` para mineração é selecionado em @877–901 somente se `MagneticWeaponEntity.distanceToSqr(Vec3.atCenterOf(blockPos)) < 2.25d`: **1,5 blocos de distância da entidade arma ao centro**, não do jogador ao bloco. Se a posição local permanece nula @928–930, o ramo de mineração não executa. A rotina também consulta `BlockState.isAir` @912–918 para a posição de hit e ajusta um vetor de deslocamento. A verificação de ar nesse ponto **não prova** que toda posição selecionada será reaprovada como bloco não-ar no início da destruição.

**Não demonstrados nessa rota:** verificação direta de claim/permissão do jogador, evento `BlockEvent.BreakEvent`, `WorldEffectPolicy` do Black Arcana, alcance do jogador até o bloco, raycast final da arma para o centro em todos os ramos e aceitação do hit pelo servidor. Podem existir proteções nos métodos externos, eventos NeoForge ou configurações; portanto é incorreto concluir que o provider *bypassa* proteções apenas pela ausência de chamadas diretas aqui.

## 3. Progresso calculado e apresentação do bloco

Quando `lastSelectedBlock` é nulo ou difere de `selectedBlock`, a rota pode limpar a animação anterior com `Level.destroyBlockProgress(player.getId(), oldPos, -1)` @952–973 e zera `destroyBlockProgress` @982–984. Ela obtém:

- `H = BlockState.getDestroySpeed(level, pos)` @1005–1016, isto é, velocidade de destruição/dureza fornecida pelo estado do bloco no contexto da chamada;
- `S = MagneticWeaponEntity.getDigSpeed(player, state, pos)` @1018–1028, que depende de stack, encantamentos, efeitos, ambiente da arma e `EventHooks.getBreakSpeed`, auditados separadamente;
- `F = 8` se a variável local de **Ferrous Haste** é verdadeira, ou `F = 10` em outro caso @1119–1132 (o flag foi derivado de `ACCompat.enchantLevel` @606–622 e só é verdadeiro quando o resultado é positivo).

Após exigir `S > 1.0f` pelo branch @1030–1034, a atualização JVM local é:

`P_novo = P_anterior + ((S / H) / F)`.

A matemática em float ocorre em @1114–1143. **Não há guarda explícita local de `H > 0` nessa janela antes de `fdiv`**; a resposta de blocos indestrutíveis, `H=0`, valores negativos, `NaN`/infinito e qualquer proteção ou transformação exterior são **NÃO VERIFICADAS**. Isto não é evidência de que tais blocos sejam realmente destruídos.

`totalMiningTime` aumenta uma unidade por passagem @1075–1082; o som de impacto é solicitado quando `totalMiningTime % 4 == 0` @1037–1072. `strikeProgress` é atualizado por uma função oscilatória de `tickCount` @1085–1111, **não** representa sucesso da mineração. O feedback de trinca é solicitado via `Level.destroyBlockProgress(player.getId(), lastSelectedBlock, int(P*10))` @1146–1168. O efeito gráfico e o armazenamento desse progresso após reload/remoção da entidade permanecem não testados.

## 4. Solicitação de destruição e ordem dos efeitos

Somente quando `P >= 1.0f` @1171–1177 e `Level.isClientSide() == false` @1180–1187, o método entra na rota de alteração do mundo. Essa guarda de servidor é local ao bloco de conclusão; não torna **todas** as atualizações gráficas do método exclusivamente server-side.

A ordem de callsites observada é:

1. `damageItem(1)` da **arma controlada** @1190–1192; em seguida `getItemStack()` e `ItemStack.mineBlock(level,state,pos,player)` @1195–1213. São solicitações distintas. A interação com desgaste próprio da stack, encantamentos e possível remoção da entidade exige a semântica de helpers/engine; **não somar custos assumindo dois danos efetivos** nem assumir rollback.
2. Lê `Enchantments.FORTUNE` e `Enchantments.SILK_TOUCH` via `ACCompat.enchantLevel` @1216–1234 e armazena os resultados em locais 17 e 18. Não há `iload` desses dois locais no restante de `tick`, portanto **esses dois valores locais não alimentam outra instrução desse método**. Não inferir que encantamentos são ignorados por `mineBlock`, `playerDestroy` ou métodos externos.
3. Solicita `BlockState.getExpDrop(level,pos,blockEntity,player,weaponStack)` @1236–1260 **antes** da tentativa de destruição, e `EventHooks.onPlayerDestroyItem(player,weaponStack,MAIN_HAND)` @1262–1269, também **antes** do retorno de `destroyBlock`. O uso de `MAIN_HAND` é o argumento literal do callsite, não prova de qual mão contém a arma ou de um evento confirmado de quebra.
4. **Se `BlockState.getBlock() instanceof ShulkerBoxBlock`** @1272–1280: chama `Level.destroyBlock(pos,true)` @1283–1290 e armazena o booleano no local 20 @1293. **Sem testar localmente esse booleano**, solicita `Player.awardStat(BLOCK_MINED[state.getBlock()])` @1295–1308 e `Player.causeFoodExhaustion(0.005f)` @1311–1316; depois salta a @1363. O parâmetro `true` é o argumento *drop* da API; não comprova drops reais nem sucesso.
5. **Outros blocos:** chama `Level.destroyBlock(pos,false)` @1322–1329, guarda o booleano no local 20 @1332 e solicita `Block.playerDestroy(level,player,pos,state,level.getBlockEntity(pos),weaponStack)` @1334–1360 **sem consultar esse booleano antes da chamada**. O argumento `false` é o flag da API, não prova de supressão final de todo item/drop gerado em hooks ou `playerDestroy`.
6. **Experiência:** após ambos os ramos, `iload 20; ifeq @1408` @1363–1365 exige `destroyBlock == true`; `exp > 0` @1368–1370 e `level instanceof ServerLevel` @1379–1384 são guardas adicionais antes de `Block.popExperience(serverLevel,pos,exp)` @1394–1405. A experiência real coletada, alterações externas e XP/Mastery do Black Arcana continuam não medidos. O progresso local é zerado @1408–1410.

O fato verificável de **`awardStat` e `playerDestroy` não estarem sob a guarda local do booleano de destruição** impede usá-los como marcadores universais de um bloco efetivamente removido. Não conclui, isoladamente, que cada uma dessas chamadas sempre produza efeitos ou configure falha do jogo. O retorno de `Level.destroyBlock` e a implementação do NeoForge/outros mods não estão abertos nesse relatório.

## 5. Saída, autoria e questões de segurança

- O progresso de trinca recebe `player.getId()` como identificador visual @1152, e o branch usa um controller do tipo `Player`; nenhum desses callsites prova um **evento seguro de crédito de Mastery**. `Player.awardStat`, `Block.playerDestroy`, `onPlayerDestroyItem`, dano da ferramenta e callback de experiência são consumidores **não transacionais entre si** nesta janela local.
- Ao sair da rota ativa e retornar, o código pode limpar o feedback anterior via `destroyBlockProgress(player.getId(),lastSelectedBlock,-1)` @1441–1467. Persistência de `lastSelectedBlock` e `destroyBlockProgress` não foi demonstrada nos overrides NBT, conforme [dossiê de sincronização](EXACT-GALENA-GAUNTLET-PERSISTENCE-SYNC-1.0.10.md); isto **não** prova inexistência de persistência herdada ou erro visual pós-reload.
- Não se observou chamada **direta** a um `WorldEffectPolicy` do Black Arcana no método provider-nativo; arquiteturalmente, **qualquer mutador novo do Black Arcana** precisaria respeitar a política configurável do próprio projeto (decisão D007). A execução autônoma do provider não pode ser confundida com autorização implícita para adaptadores ou perks alterarem blocos.
- Potenciais pontos conceituais de perks: aceleração de `S`, custo/desgaste, elegibilidade de alvo, sucesso de mineração e telemetria de progressão. **Nenhum hook mutador, API de compensação, transação de drop, deduplicação de evento ou integração real com Mastery foi demonstrado.** `NO_MUTATION`/fail-closed.

## 6. Validação, limites e próximos gates

Reprodução do recorte no mesmo publisher, após obter o JAR com SHA exato:

```sh
python3 docs/qa/alexscaves_1010_galena_gauntlet_discovery.py --jar /caminho/alexscaves-1.0.10-neoforge+1.21.1.jar --javap /caminho/java21/bin/javap --output build/galena-mining-1010/report.json
python3 docs/qa/alexscaves_1010_galena_mining_world_effect_checks.py --report build/galena-mining-1010/report.json --manifest 'wiki/modpack-catalog/providers/✅-alexs-caves-continued/EXACT-GALENA-GAUNTLET-MINING-WORLD-EFFECT-1.0.10.json' --adversarial
python3 scripts/catalog/generate_perk_ready_indexes.py --check
python3 scripts/catalog/check_perk_ready_indexes.py
```

**Validação local do relatório publisher previamente autenticado:** 222 pivôs/744 instruções de `tick`, 2 referências de métodos dependentes, 35 alterações forjadas re-seladas rejeitadas; `python3 -m py_compile` aprovado. A CI dedicada deve executar as mesmas provas depois de reconstruir o relatório a partir do JAR; essa execução **não** é teste físico de mundo.

**Pendências:** (a) código/métodos da engine 1.21.1/NeoForge para `Level.destroyBlock`, `Block.playerDestroy`, eventos de autorização e claims; (b) testes físicos Survival/multiplayer/claims/TileEntity e Shulker com sucesso e falha forçada; (c) retorno de `mineBlock`, durabilidade e drops em cancelamentos; (d) chunk unloaded/reload, troca de dimensão, controller ausente e duplicação/perda; (e) engine de experiência, requisitos `WorldEffectPolicy`, governança e deduplicação de Mastery; (f) comprovar paridade do JAR realmente extraído da instância; (g) revisão do universo completo do provider. Todos mantidos `NÃO VERIFICADO`, sem promoção de índice, contrato estático total, hook, integração ou QA.
