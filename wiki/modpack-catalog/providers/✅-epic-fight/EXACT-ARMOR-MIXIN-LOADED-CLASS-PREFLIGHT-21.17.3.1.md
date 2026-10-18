# Epic Fight 21.17.3.1 — preflight físico do mixin de armadura na classe carregada

**18/10/2026 · ✅ `TRANSFORMED_HANDLER_PRESENT` no servidor dedicado isolado · ⚠️ handler não invocado, combate e cliente não testados · ⛔ perks/Mastery sem adapter homologado.**

## Evidência executada (NeoForge 21.1.250 / Java 21)

- [GitHub Actions #39098101364](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39098101364), job `connected_player_observer_no_client_guard`: **SUCCESS**. Compilou o companion `epicFightCatalogQa` e o Black Arcana em Java 21; verificou que o companion não entrou no JAR de produção.
- O runner usou Epic Fight **21.17.3.1**, CurseForge projeto **405076** / file **8175609**, JAR fixado por SHA-1 `fb199b7bbea2fc402da28ab586e73f47e32f8fc0` e SHA-256 `8b882554cf10086398340fbdc741819ee72a801a3adce516c7f4768326a39526`. Esses hashes correspondem ao publicador e ao snapshot físico histórico; não constituem uma releitura do perfil local.
- Servidor dedicado NeoForge **21.1.250** iniciou naturalmente **sem cliente**. No evento `ServerStartedEvent`, o companion QA consultou **`LivingEntity.class.getDeclaredMethods()` da classe carregada pela JVM**, sem carregar o classfile mixin do JAR para fingir resultado.
- Exigiu **um e somente um** método de nome `handler$...` contendo `epicfight$getDamageAfterArmorAbsorb`, retorno `void` e parâmetros **`DamageSource`, `float`, `CallbackInfoReturnable`**, sem candidatos divergentes. O log observado e aceito pelo CI foi:

```text
[BLACK_ARCANA_EPICFIGHT_ARMOR_MIXIN_QA] type=result status=TRANSFORMED_HANDLER_PRESENT handler_count=1 handler_invoked=false damage_tested=false client_connected=false mastery_tested=false
```

- A verificação positiva exige essa linha **exatamente uma vez** e rejeita os marcadores `HANDLER_SIGNATURE_NOT_EXACT` e `REFLECTION_OR_LINKAGE_UNAVAILABLE`. O workflow incluiu controle sintético positivo e negativo do matcher regex.
- JSON compacto publicado como artefato **#12125471763**, nome `epicfight-connected-player-no-client-preflight-d875dc4a143beddcc8d2d60e202a0719d7a15c08`. O relatório é **pré-gate**: `connected_players=0`, `has_proven_join_patch=false`, `skill_equipped=false`, `attribute_mutated=false`, `armor_mixin_handler_present_in_loaded_LivingEntity=true`, `armor_mixin_handler_invoked=false`, `armor_damage_tested=false`. A aprovação do marker de mixin não altera a negativa obrigatória da prova de jogador conectado.
- [Observer opt-in](../../../../src/epicFightCatalogQa/java/dev/gustavopere/blackarcana/qa/epicfight/EpicFightArmorMixinAppliedQa.java), [mod de QA que registra o observer](../../../../src/epicFightCatalogQa/java/dev/gustavopere/blackarcana/qa/epicfight/EpicFightCatalogQaMod.java), [workflow read-only](../../../../.github/workflows/epicfight-211731-connected-player-preflight-qa.yml). Ativação específica: `BLACK_ARCANA_EPICFIGHT_QA_ARMOR_MIXIN_PREFLIGHT=1`. Não muta atributos, mana, stamina, entidade, dano, animação ou mundo.

## Reprovação inicial e correção sem afrouxar gates

A tentativa inicial [#39097863144](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39097863144) **FAILED** na asserção. A investigação encontrou barras invertidas duplicadas no **regex do próprio workflow**, que não reconheceria nem um marcador positivo válido. Nenhuma ausência de mixin em runtime foi demonstrada por aquela tentativa. O matcher foi corrigido, e controles positivo/negativo foram acrescentados antes de aceitar a segunda execução **SUCCESS** #39098101364. Não houve remoção de validações nem aceitação presumida.

## O que mudou e o que não mudou

**Comprovado novo:** em um servidor dedicado isolado executando o Epic Fight exato, o alvo `LivingEntity` carregado pela JVM tem um handler de mixin com nome e assinatura esperados. Isso é evidência **de transformação/instalação do método** mais forte que a prova anterior do bytecode publisher e da configuração `common.MixinLivingEntity`.

**Não comprovado:** que um ataque atingiu o handler, que a `@Inject` intercepta corretamente `getDamageAfterArmorAbsorb` em todas as versões de alvo, que as operações de `CombatRules` reduziram HP de entidade real, que o evento foi cancelado, que `ServerPlayerPatch.initialized=true`, ou que uma perk externa possa mudar armadura/dano/alcance sem duplicação. A prova de consumo compilado anterior continua separada: [AttackPhase → ValueModifier → EpicFightDamageSource → MixinLivingEntity](EXACT-ATTACK-PHASE-CONSUMERS-21.17.3.1.md). A lógica de inscrição do handler não equivale à confirmação de comportamento do fluxo de combate.

## Próxima aceitação física e risco

1. Com o companion QA isolado e cliente real compatível: conectar e observar `CONNECTED_PATCH_INITIALIZED` após login e respawn; nenhum FakePlayer forçado, UUID/nome em log ou chamada manual a `onJoinWorld`.
2. Em ambiente descartável: instrumentar **outro** cenário para capturar antes/depois de ataque real, `DamageSource`, tag `BYPASSES_ARMOR`, redução por armadura, eventos, absorção e decréscimo de HP sem interferir no combat provider. Exigir controle vanilla e Epic Fight, cobertura de fonte/tag, dano/clamp e múltiplos modifiers.
3. Somente com boundary público ou integração provider-safe demonstrada, avaliar perks de dano/tipo/alvo/área/duração/cooldown e Mastery no sibling. Até lá **⛔**.

**Contagem:** 43/43 core skills Epic Fight documentadas; 3/3 ações sobrenaturais já contadas, 40 excluídas do numerador mágico e ainda relevantes para perks. **+0** roots, **+0** adapters. Catálogo global mínimo 1.857 semânticos / 1.855 estritos, denominador —%. Stage 06.05 🟡, Stage 09 físico PENDING. PR #825 draft; merge não realizado.
