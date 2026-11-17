# Alex's Mobs 2.1.13 — AMNetContext concrete bridge + registration bootstrap

**Status:** 🟡 SHA-exact JAR discovery candidate; `static_perk_contract=NOT_CERTIFIED`, `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `NO_MUTATION`.

## Why this pass is necessary

The merged [Transmutation C2S audit](alexsmobs-213-transmutation-c2s-handoff.md) and [sealed snapshot](../../wiki/modpack-catalog/providers/✅-alexs-mobs-continued/EXACT-TRANSMUTATION-C2S-2.1.13.json) establish the native message, handler, sender-ID comparison, active-menu type gate and the call to `transmute(Player,int)`. They **do not** establish which concrete object implements `AMNetContext`, whether `getSender()` is bound to the authenticated network connection, or which LambdaMetafactory handles are registered for the publisher's packet.

This follow-up adds a reproducible read-only probe rather than re-certifying the previously merged message receiver.

## Physical identity and bounded procedure

- Provider: `alexsmobs`; publisher JAR previously matched to the physical modlist: `alexsmobs-2.1.13-neoforge+1.21.1.jar`; Minecraft 1.21.1, NeoForge, Java 21.
- Reconfirmation against a newer physical modlist export remains required if the sibling changes; the current GitHub tree scan did not expose an Alex's Mobs-named modlist entry. This probe never upgrades the historical fingerprint into an unqualified current-version claim.\n- Publisher artifact CurseForge project/file `1635121/8856498`; SHA-1 `50ddafdf3d12b33331e4eecb4ab514ae451baadd`; SHA-256 `eef0b4d36f1e40292b23f90ad3052e2e9aace3a33c6a48c65b8b5f2b061ab6c8`; 27,452,738 bytes.
- [New auditor](alexsmobs_213_context_bridge_probe.py), [eight synthetic tests](alexsmobs_213_context_bridge_probe_test.py), [CI workflow](../.github/workflows/alexsmobs-213-context-bridge.yml).
- The auditor validates both hashes, file size, archive membership, classfile major version and bounded candidate cohort. It selects provider classfiles referencing `AMNetContext`, records only methods relevant to context/dispatch, identifies **direct** `implements AMNetContext` declarations, and extracts limited `AlexsMobs.setup` bootstrap-handle candidates.
- The generated JSON is a discovery **artifact**, not a sealed new certification. Do not mark the new evidence SHA-verified until the corresponding CI completes successfully on the publisher JAR.

## Evidence semantics / negatives

- Presence of `AMNetContext` in a class constant pool is **only a search signal**, not an implementation or caller proof.
- Direct implementation of the interface is stronger evidence but does **not** prove connection ownership, `getSender` authenticity or the absence of wrappers in external dependencies (e.g. CodxLib).
- `invokedynamic` and `BootstrapMethods` matches are **candidate** callback links; the exact `registerMessage` invocation's bootstrap indices, method handles, direction and actual execution order still require contextual reconciliation.
- No index, certificate or universe counters change from this auditor alone. The three semantic roots remain the observed denominator, with Item Transmutation ⚠️ partial/conditioned.
- Explicit outstanding negatives: sender spoofing, replay, concurrent settlement, wrong table/session, player dimension transition, choice out of range/clamp and item/XP double-processing in dedicated multiplayer.
- Black Arcana must not reapply provider-owned `Slot.set`, `giveExperienceLevels` or `postTransmute`. No perk XP discount, reroll, output or Mastery mutation can be enabled by this passive evidence.

## Next acceptance gates

1. Inspect and SHA-seal the CI JSON only after obtaining the real publisher result and reasoning about the concrete context implementation.
2. Trace the actual callback bindings and transport direction, and distinguish registered handlers from syntactic lambdas.
3. Design and run targeted negative tests for spoofing, stale menus, replay and concurrent settlement; complete physical modpack/NeoForge QA separately.
4. Only after the full individual static contract is evidenced may the certified count change; a mutating hook requires separate proof.

Stage 06 is not promoted by this catalog work. No modifications to Enshrouded or RPG Skill Tree.

## Resultado observado no JAR SHA-exato — CI #44167951912

O [workflow de descoberta](https://github.com/Gustavaopere/Black-Arcana/actions/runs/44167951912) executou os **10 testes sintéticos**, confirmou o JAR por SHA-256/tamanho e gerou o artifact `alexsmobs-213-context-bridge-readonly` (ID `14364944866`). Foram rastreadas **27 classes candidatas** e **uma implementação direta** de `AMNetContext`: `com/github/alexthe666/alexsmobs/message/AMNeoNetwork$1.class` (classfile SHA-256 `273b6ae4bf9190129efb5d249c672d5ef7d8ed0efb6d62c69a9b1f9f746889b6`). Isso é evidência estática da versão publisher; não constitui execução física de transmutação.

### Adaptador de identidade e ordem de execução

- `AMNeoNetwork.adapt(IPayloadContext)` constrói `AMNeoNetwork$1` com o contexto recebido (`new @0`, construtor `@5`).
- `AMNeoNetwork$1.getSender()` lê `IPayloadContext.player() @4` e testa `instanceof ServerPlayer @11`; caso verdadeiro faz `checkcast @18`, caso contrário o fluxo devolve `null @26`. Não utiliza `MessageTransmuteFromMenu.playerId` para produzir o remetente.
- `AMNeoNetwork$1.isClientSide()` lê `IPayloadContext.flow() @4` e `PacketFlow.isClientbound() @9`. Logo o nome local `isClientSide` está baseado na **direção do fluxo**; não comprova por si só uma sessão legítima.
- `AMNeoNetwork$1.enqueueWork(Runnable)` delega a `IPayloadContext.enqueueWork @5`. Já `setPacketHandled(boolean)` possui apenas `return @0` (no-op na implementação observada).
- `AMNeoNetwork.handle(AMPayload,IPayloadContext)` resolve uma entrada de `REGISTRATIONS` pelo índice do envelope, aplica `adapt @20` e invoca `Registration.handle @23`, que chama o `BiConsumer.accept @6` previamente armazenado.

### Codec, registro e semântica bidirecional

- `AlexsMobs.setup` contém a classe `MessageTransmuteFromMenu` no `ldc_w @375` e registra via `registerMessage @393`; o `invokedynamic @388` aponta para bootstrap **#64**. Os bootstraps **#62/#63/#64** são, respectivamente, os handles de `MessageTransmuteFromMenu.write`, `.read` e `MessageTransmuteFromMenu$Handler.handle`. Essa correspondência reduz a incerteza de ligação estática dos callbacks do registro.
- `AMNeoNetwork.register` anexa os callbacks `encoder/decoder/handler` à lista `REGISTRATIONS` e mapeia a classe para um índice de registro; `AMNeoNetwork.wrap` usa o índice do tipo de objeto registrado.
- `AMNeoNetwork.onRegisterPayloads` encaminha os handlers ao `AMNeoSend.registerPlay @17`. **`AMNeoSend.registerPlay` invoca `PayloadRegistrar.playBidirectional @4`**. Portanto o envelope nativo é registrado como **bidirecional**, mesmo que a transmutação de item seja uma intenção normalmente enviada do cliente ao servidor. Não classificar a registration global como C2S-only.
- `AMNeoNetwork.decodePayload` lê um **índice de tipo de mensagem** via `readVarInt @1` e rejeita valores negativos (`iflt @6 →21`) ou fora do tamanho de `REGISTRATIONS` (`if_icmplt @18 →35` ou exceção `@21..34`). **Não confundir este índice de envelope, validado na decodificação, com `MessageTransmuteFromMenu.choice`, que é encaminhado ao menu e pode sofrer clamp `0..2`.**
- Classfile SHA-256: `AMNeoNetwork.class` = `f57c8ca31569238bb73574c8c4493a884cfce33c895198c4d80d1f431d6c31b8`; `AMNeoNetwork$Registration.class` = `c838c162c106e895dd6d2165cbd050587547286e67643397730d978ac7e0f74b`; `AMNeoSend.class` = `a9ccf4e5ce81eb0492f0d6e2eae6ca701de482d85855b2ec0036e220b147f770`.

**Limite residual:** a ligação de métodos/registries no publisher é mais bem localizada e a origem do `ServerPlayer` está rastreada até `IPayloadContext.player()`; ainda não há testes reais de conexão autenticada, abuso de fluxo bidirecional, menu/tabela válida por sessão, replay, concorrência, efeitos persistidos, disconnect/reload, falhas de codec ou mixed client/server. A existência desses guardas não demonstra isolamento suficiente para mutações. Não promover `static_perk_contract`, `mutating_hook`, `physical_qa`, contadores ou Stage.
