# Epic Fight 21.17.3.1 — observabilidade read-only de dano nativo para Stage 09

**18/10/2026 — ✅ Observador de QA compilado, separado da produção e armado no servidor sem cliente; ⚠️ nenhuma amostra de ataque de jogador conectado; ⛔ perks/Mastery e mudanças de dano sem homologação.**

## Evidência executada

- [Workflow #39098965924](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39098965924): **SUCCESS** no job `connected_player_observer_no_client_guard`. O runner validou hashes publisher, compilou `epicFightCatalogQaJar` sob NeoForge 21.1.250/Java 21, confirmou que as classes de QA não entram no JAR de produção, iniciou dedicated server com Epic Fight 21.17.3.1 e validou o preflight com **zero jogadores**.
- O CI exigiu o marcador exato `[BLACK_ARCANA_EPICFIGHT_NATIVE_DAMAGE_QA] type=armed status=AWAIT_NATIVE_PLAYER_ATTACK source_class_available=true connected_players=0 incoming_count=0 post_count=0 no_client_proof=false` uma única vez. O teste rejeita toda linha `type=sample` sem cliente e exige, em paralelo, `TRANSFORMED_HANDLER_PRESENT` de armadura e `AWAIT_CONNECTED_PLAYER` do observer de lifecycle. **Nenhum ataque de jogador, HP ou handler invocado foi observado**.
- Evidência JSON publicada: artefato GitHub Actions **#12126200760**, incluindo `native_damage_telemetry_armed_without_client=true`, `native_damage_player_samples_observed=0` e `native_damage_health_loss_validated=false`. Não contém JAR do publicador.
- A assinatura dos eventos foi confirmada **por compilação real** contra a versão NeoForge 21.1.250 no workflow, além do source de NeoForge 1.21.1 consultado anteriormente.

## Objeto da auditoria

Preparar observação **somente passiva** dos valores realmente emitidos pelo pipeline de dano NeoForge/Epic Fight, para não confundir:

- o argumento declarado de `AttackPhaseProperty` com perda efetiva de HP;
- a presença de `epicfight$getDamageAfterArmorAbsorb` em `LivingEntity` transformada com a invocação do handler durante um ataque;
- o campo `ARMOR_NEGATION_MODIFIER` com uma porcentagem líquida invariável;
- a presença de `ServerPlayerPatch` com uma skill executada/cobrada.

As evidências já aprovadas são [consumidores de propriedades compilados](EXACT-ATTACK-PHASE-CONSUMERS-21.17.3.1.md) e [handler do mixin presente na classe transformada](EXACT-ARMOR-MIXIN-LOADED-CLASS-PREFLIGHT-21.17.3.1.md). O próximo critério exige observação de ação provider-native realmente originada por jogador conectado.

## Implementação opt-in, não produtiva

- Classe independente [`EpicFightNativeDamageTelemetryQa.java`](../../../../src/epicFightCatalogQa/java/dev/gustavopere/blackarcana/qa/epicfight/EpicFightNativeDamageTelemetryQa.java), registrada no companion `EpicFightCatalogQaMod` **somente** com `BLACK_ARCANA_EPICFIGHT_QA_NATIVE_DAMAGE_PREFLIGHT=1`.
- Assinaturas NeoForge obtidas da árvore **1.21.1** de `neoforged/NeoForge@00c6a3fd23d80ce54ec834a7e25d09fba37927e9`: `LivingIncomingDamageEvent` fornece `getSource`, `getOriginalAmount` e `getAmount`; `LivingDamageEvent.Post` fornece `getSource`, `getOriginalDamage`, `getNewDamage` e `getReduction`; `DamageContainer.Reduction` distingue `ARMOR` de `ABSORPTION`. **A compilação do QA contra 21.1.250 exato é teste separado**: o código-fonte consultado na branch NeoForge não é prova de versão binária idêntica.
- No `ServerStartedEvent`, carrega a classe `yesman.epicfight.world.damagesource.EpicFightDamageSource`; se indisponível, emite `PROVIDER_DAMAGE_CLASS_UNAVAILABLE`, nunca simula um ataque.
- Um evento só é elegível se sua fonte for desse tipo e o atacante `DamageSource.getEntity()` for `ServerPlayer` **não FakePlayer e ainda presente na player list** do servidor.
- Registra **no máximo 12 amostras de entrada e 12 de `Post` por execução**, sem identificadores, usernames, UUIDs, posições ou IDs de entidade. Coleta valor original, valor de entrada ou HP reduzido segundo contrato do `Post`, ARMOR e ABSORPTION reductions, tag `BYPASSES_ARMOR` e booleano `victim_is_player`.
- **Não** usa `setAmount`, `setNewDamage`, `hurt`, `onJoinWorld`, spawn de entidade, `AttributeInstance` mutation ou qualquer outro mecanismo de escrita/cobrança.
- `Incoming` e `Post` são **observações distintas**; sem um ID causal de hit compartilhado, não se calcula a diferença entre duas amostras como se fossem necessariamente do mesmo ataque. Mesmo o evento Post não prova, isoladamente, a execução do handler particular do mixin.

## Matriz objetiva de aceitação

| Cenário | Evidência requerida | Resultado atual |
|---|---|---|
| Compilação Java 21 do companion com NeoForge 21.1.250 | `epicFightCatalogQaJar`, JAR de produção sem classes QA | ✅ #39098965924 SUCCESS, separação QA/produção comprovada |
| Servidor dedicado sem cliente | marcador `AWAIT_NATIVE_PLAYER_ATTACK`, contagens 0/0, zero linhas `type=sample` | ✅ #39098965924 PASS, zero amostras de player e observer armado |
| Jogador conectado, login natural | `ServerPlayerPatch.initialized=true` no observer de lifecycle independente | ⚠️ ainda não observado |
| Dano nativo do Epic Fight | ao menos um `type=sample phase=post source=EPICFIGHT_CONNECTED_PLAYER` por ataque real autorizado | ⚠️ ainda não observado |
| Mitigação de armadura | observar samples `Post` em alvos/armaduras distintos, com `bypasses_armor`, reductions e controle vanilla | ⚠️ não mensurado |
| Passagem por handler específico | instrumentação causal adicional para demonstrar invocação, além da presença de método | ⚠️ não mensurado |
| Reconnect, respawn e full modpack | observer de lifecycle + regressão em servidor real e provas de compatibilidade | ⚠️ não mensurado |
| Adapter de dano, alcance, tipo, hitbox ou Mastery | API pública/contract efetivo + QA provider-native sem duplicar dano ou custo | ⛔ bloqueado |

**Procedimento físico futuro:** usar servidor descartável e cliente real com versão exata; confirmar login/respawn com observer de patch; realizar ataques provider-native separados por tempo suficiente para a lógica de invulnerabilidade; comparar cenários sem armadura, com armadura e tags específicas; coletar logs sem dados de identificação. Registrar separadamente uma transação de ataque/dano em ferramenta capaz de correlacionar identidade causal; não inferir correlação a partir do índice `sample`. Não executar/desenvolver método que burle reivindicações/claims PvP ou proteções do servidor.

## Autoridade e cobertura

Epic Fight mantém autoridade sobre `AttackAnimation`, `EpicFightDamageSource`, `ValueModifier`, handlers Mixin, recursos e animações. Black Arcana mantém seu próprio runtime mágico, e RPG Skill Tree só define progressão/perks/Mastery sob contrato real. Este QA não é bridge de gameplay.

**Inventário:** Epic Fight ✅ 43/43 identidades core, 3/3 ações sobrenaturais do tridente já contabilizadas e 40 habilidades não mágicas relevantes às perks; +0 magias, +0 adapters. Global mínimo histórico 1.857 objetos semânticos (1.855 estritos), denominador ainda aberto, **—%**. Stage 06.05 🟡; Stage 09 físico PENDING; PR #825 draft, sem merge.
