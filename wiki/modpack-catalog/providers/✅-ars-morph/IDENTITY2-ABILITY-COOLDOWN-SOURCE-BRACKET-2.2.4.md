# Identity2 — cooldown de abilities de Ars Morph 2.0.0: inspeção cruzada do código oficial

## Novo gate de prova física — 17/10/2026

A branch da [PR #825](https://github.com/Gustavaopere/Black-Arcana/pull/825) contém um verificador Python fail-closed [`identity2_224_cooldown_binary.py`](../../../docs/qa/identity2_224_cooldown_binary.py) e um [workflow Java 21](https://github.com/Gustavaopere/Black-Arcana/blob/docs/catalog-perk-causality-20261015/.github/workflows/identity2-224-cooldown-binary.yml). O workflow `pull_request` **executa somente os seis autotestes sintéticos de parsing/fail-closed**, sem baixar JAR ou conferir compatibilidade. Seu ramo `workflow_dispatch` requer **file ID oficial do Identity2 2.2.4 para NeoForge Minecraft 1.21.1 e SHA-1 independente de 40 hex**: sem ambos, **nenhuma auditoria física é executada**. É proibido aproveitar arquivos de Fabric, Minecraft 1.21.11 ou a release 2.2.4.1 como se fossem a build exigida.

Quando explicitamente acionado com esses valores, o job obtém o JAR pelo Curse Maven, confere bytes e metadata `modId=identity2`, verifica as quatro assinaturas delimitadas de métodos nos classfiles por `javap -p -c` e publica **apenas JSON de referências e offsets**, nunca o binário de terceiros. Verifica `resolvePrimaryAbilityCooldown`, `handleIdentityAbilityPacket`, `EntityMixin.identity2$baseTick` e `Identity2Client.onClientTickEnd`. A ordem das chamadas e os opcodes **não provam caminhos de execução nem equivalência com o JAR instalado**. A comparação com o SHA-1 do JAR instalado e o teste em jogador conectado continuam necessários, mesmo se o relatório disser `PASS_BOUNDED_SIGNATURES`.

**Estado deste checkpoint:** script e workflow criados; teste local de seis gates do protótipo equivalente **PASS**; CI remoto e auditoria publisher **PENDING na criação**. O checksum e o file ID do JAR **instalado** ainda não foram fornecidos por snapshot físico. Nenhum contrato de perk liberado. Também foram eliminadas as sete linhas em branco finais apontadas pelo `git diff --check` no CI anterior, com reexecução completa do CI exigida para fechamento.

**Checkpoint 17/10/2026 · PR #825 draft · evidência `UPSTREAM_SOURCE_BRACKET`, runtime `⚠️`.** Investigação solicitada após fechar as 7/7 fichas de `ars_morph`. Não copia código para Black Arcana. A versão do modpack documentada é **Identity2 2.2.4, Minecraft 1.21.1/NeoForge** (e Ars Morph 2.0.0); o JAR físico específico de Identity2 **não foi extraído nem comparado** neste checkpoint. Não declarar `BINARY_EXACT`.

## Autoridade, proveniência e limitação de versão

Fonte oficial identificada a partir do link *Source* da página do projeto: [`xGabou/Identity2`](https://github.com/xGabou/Identity2). Dois snapshots **do ramo `1.21.1`** foram comparados:

- **Antes da publicação:** [`847202234ae89a1596c6039b473566e34231c213`](https://github.com/xGabou/Identity2/tree/847202234ae89a1596c6039b473566e34231c213), commit de **27/05/2026**. Usa esquema do cooldown em `ModPackets`, `Identity2Client` e `EntityMixin` descrito abaixo.
- **Depois da publicação:** [`c634278ee637e8b94949a685072c94d67c9b3d4a`](https://github.com/xGabou/Identity2/tree/c634278ee637e8b94949a685072c94d67c9b3d4a), commit de **02/10/2026**, com `gradle.properties` em `mod_version=2.2.4.1`, MC 1.21.1. Os blocos de execução/cooldown em análise retêm o **mesmo algoritmo**, embora os blobs Git **não sejam byte-idênticos** entre os dois snapshots.
- Release do publisher **Identity2 2.2.4 para NeoForge 1.21.1** foi publicada em **02/09/2026** ([files oficiais](https://www.curseforge.com/minecraft/mc-mods/identity2/files/all)). A existência da release intermediária não prova que o binário instalado corresponde a qualquer um dos commits. **Status: `SOURCE_BRACKET`, não `SOURCE_VERSION_EXACT` ou `BINARY_EXACT`.**

## Contrato de cooldown observado nos dois snapshots

1. `IdentityAbilityDefinition` declara `int cooldown` e `int useduration`, derivados dos JSONs `data/*/identity2/identity_ability/*.json`. O contador da habilidade primária no servidor é fixado por `resolvePrimaryAbilityCooldown = max(0, cooldown + useduration)` se definição presente; fallback = `20`. [Pré-release](https://github.com/xGabou/Identity2/blob/847202234ae89a1596c6039b473566e34231c213/common/src/main/java/net/Gabou/identity2/ModPackets.java#L225-L275) · [pós-release](https://github.com/xGabou/Identity2/blob/c634278ee637e8b94949a685072c94d67c9b3d4a/common/src/main/java/net/Gabou/identity2/ModPackets.java#L203-L253).
2. Em `handleIdentityAbilityPacket`, a ação primária `entityid==0` reobtém morph `getCurrentIdentity()`; se falta, aborta. Se `getAbilityCooldown()>0`, retorna. Caso contrário **define o cooldown antes** de executar o comando opcional ou `predefAbility.execute(player)`. `execute` não tem retorno de sucesso/fracasso. [Pré](https://github.com/xGabou/Identity2/blob/847202234ae89a1596c6039b473566e34231c213/common/src/main/java/net/Gabou/identity2/ModPackets.java#L215-L268) · [Pós](https://github.com/xGabou/Identity2/blob/c634278ee637e8b94949a685072c94d67c9b3d4a/common/src/main/java/net/Gabou/identity2/ModPackets.java#L188-L246).
3. `EntityMixin` usa campos `int abilityCooldown` e `int secondaryAbilityCooldown`, e cada `baseTick` decrementa `1` enquanto o campo é positivo. **Unidade operacional: contagem de ticks** no código, não segundos. [Pré](https://github.com/xGabou/Identity2/blob/847202234ae89a1596c6039b473566e34231c213/common/src/main/java/net/Gabou/identity2/mixin/EntityMixin.java#L636-L683) · [Pós](https://github.com/xGabou/Identity2/blob/c634278ee637e8b94949a685072c94d67c9b3d4a/common/src/main/java/net/Gabou/identity2/mixin/EntityMixin.java#L638-L685).
4. `Identity2Client` lê `identityAbility.cooldown` para `primaryCooldown`, `useduration` separadamente, inicia localmente `primaryCooldown+useDuration`, envia `ABILITY_ACTION_PRIMARY` (0) e, durante a faixa `primaryCd>primaryCooldown`, envia payload de progressão numérica para `BuiltinIdentityAbility.tick`. Envia também `ABILITY_ACTION_PASSIVE(_USED)` conforme input. Isso é **predição/solicitação de cliente**; o servidor decide sua própria admissão. [Pré](https://github.com/xGabou/Identity2/blob/847202234ae89a1596c6039b473566e34231c213/common/src/main/java/net/Gabou/identity2/Identity2Client.java#L363-L397) · [Pós](https://github.com/xGabou/Identity2/blob/c634278ee637e8b94949a685072c94d67c9b3d4a/common/src/main/java/net/Gabou/identity2/Identity2Client.java#L359-L394).
5. `ABILITY_ACTION_SECONDARY` usa `resolveSecondaryAbilityCooldown`, tipicamente `cooldown` sem somar `useduration` (exceto overrides hardcoded para Elder Guardian/Shulker). Não aplicar `cooldown + useduration` a ações secundárias por analogia. [Pós](https://github.com/xGabou/Identity2/blob/c634278ee637e8b94949a685072c94d67c9b3d4a/common/src/main/java/net/Gabou/identity2/ModPackets.java#L222-L267).

## Valores brutos do Ars Morph e contadores derivados

As onze atribuições `ars_morph` em `data/{ars_nouveau,ars_elemental}/identity2/identity_ability/*.json` foram lidas no [commit source-release-aligned](https://github.com/Alexthw46/Ars-Morph/tree/4a5a2c706fe5a316fc9ad03ac37a3ac1d1dc3c58). Cinco Weald Walkers (incluindo Flashing se Ars Elemental carregado) usam mesmo predef/classe Java, não criam cinco magias novas.

| Ability | Variante/assignment | `cooldown` | `use_duration` | Contador primário (`c+u`) | Contador secundário normal (`c`) |
|---|---|---:|---:|---:|---:|
| Weald Walker | blazing/cascading/flourishing/vexing + Flashing* | 100 | 20 | **120 ticks** | 100 ticks |
| Wilden Hunter | wilden_hunter | 800 | 20 | **820 ticks** | 800 ticks |
| Wilden Stalker | wilden_stalker | 800 | 100 | **900 ticks** | 800 ticks |
| Starbuncle | starbuncle | 100 | 20 | **120 ticks** | 100 ticks |
| Whirlisprig | whirlisprig | 400 | 20 | **420 ticks** | 400 ticks |
| Wixie | wixie | 200 | 20 | **220 ticks** | 200 ticks |
| Firenando* | firenando_entity | 120 | 40 | **160 ticks** | 120 ticks |

*Firenando/Flashing condicionais a `ars_elemental`, presente na modlist mas sujeito a teste físico. O `use_duration` não deve ser interpretado como a duração efetiva do efeito derivado: Starbuncle aplica Speed por 3000 ticks, Whirlisprig pode reaplicar Jump Boost por 40 ticks, e o canal de progressão envia valores `tick` que os callbacks podem ignorar.*

## Causalidade e risco para perks

- **A regra de cooldown é server-owned**, portanto um redutor de cooldown de perks **não** pode alterar apenas UI, JSON renderizado pelo cliente ou `AttributeInstance` de outro mod. Seria necessário um seam de pré-admissão configurável por usuário e aceito pelo Identity2 real; nenhuma API de alteração per-player foi homologada.
- **Contador inicia antes do efeito:** o caso Wixie (`goodEffectTable` tamanho 10, sorteio `nextInt(badEffectTable.size())` = 12) pode ter erro no callback após a cobrança do cooldown. `MorphBoundAbility.execute` captura/loga `Throwable`; requer reproduzir JAR e medir contador/falta de poção, sem afirmar bug em gameplay.
- **Cancelamento não equivale a refund:** habilidades que testam `resolver.postEvent().isCanceled()` abortam sua ação depois que Identity2 estabeleceu o cooldown; o corpo do handler não verifica sucesso do resolver para reembolsar. A persistência e duplicação de efeitos depende do host.
- **Passivo e progressão numérica:** a rota de `passiveTick` e `tick` recebe mensagens C2S; o trecho analisado não inclui gate de cooldown para esses cases como inclui para a ação primária. **QA de frequência, side e autenticação de morph** antes de aceitar qualquer evento como Mastery.
- **Survival/WorldSafety:** `Whirlisprig` faz Grow+AOE do Ars, não do Black Arcana. Não atribuir `WorldEffectPolicy` externo por suposição; Firenando e Weald Walker geram projéteis filhos provider-native com owner e DamageSource ainda condicionados.
- **Sem clone de Identity2:** progresso, aquisição/morph, `BuiltinIdentityAbility`, packet e cooldown são host-owned. RPG Skill Tree fornece gates/perks/Mastery somente por contrato real, sem duplicar o envio da ação e sem creditar uma única ativação e seu resolver Ars como dois casts.

## Checklist de homologação (não concluído)

1. Identificar e SHA-verificar o **JAR instalado do Identity2 2.2.4 para 1.21.1**, obter `ModPackets.class`, `EntityMixin.class`, `Identity2Client.class`, `ModRegistries.class` e comparar esse bytecode com o contrato acima. Não promover `SOURCE_BRACKET` a `BINARY_EXACT` sem esse gate.
2. Dedicated server + cliente real: valores de 120/820/900/120/420/220/160 ticks, qualidade do decremento em 20TPS vs lag, ações secundárias, tentativa enquanto ainda em cooldown, disconnect/relog, morrer/respawn e alterar morph durante cooldown.
3. Cancelamento de `postEvent`, morph errado/ausente, callback que lança exceção (Wixie crouch), entrada numérica C2S de progressão, múltiplos alvos, ausência de feedback de sucesso e possível progressão indevida.
4. Testar Identity2 2.2.4 com Ars Morph 2.0.0/Ars 5.13.1/Ars Elemental 0.7.10.1 e observar owner de ataques, passivos, PvP, claims e Mastery sem duplicação.

**Estado:** catálogo SOURCE_BRACKET avançado; ⚠️ runtime instalado não verificado; ⛔ adapters de cooldown/Mastery não homologados; +0 novas magias e +0 alteração do runtime BA. Stage 06.05 🟡 / Stage 09 físico pendente.
