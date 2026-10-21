# Epic Fight — FakePlayer e elegibilidade para teste de atributos (17/10/2026)

**Resultado:** ✅ gate de diagnóstico executado, ⛔ FakePlayer avaliado **não elegível** para equip/unequip de skill como se fosse jogador conectado. A attachment nativa do Epic Fight criou um ServerPlayerPatch, porém seu campo EntityPatch.initialized estava **false**.

## Prova física

- [GitHub Actions #39003200555](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39003200555), job real_attachment_fake_player_preflight, **SUCCESS**; artifact JSON limitado **12090146205**. Servidor dedicado Java 21, Minecraft 1.21.1, NeoForge **21.1.250**.
- Epic Fight 21.17.3.1, modid epicfight, JAR físico da modlist sibling #260/587, CurseForge 405076/8175609. SHA-1 fb199b7bbea2fc402da28ab586e73f47e32f8fc0 e SHA-256 8b882554cf10086398340fbdc741819ee72a801a3adce516c7f4768326a39526; workflow revalidou o arquivo do publisher antes do boot.
- [QA Java](https://github.com/Gustavaopere/Black-Arcana/blob/docs/catalog-perk-causality-20261015/src/epicFightCatalogQa/java/dev/gustavopere/blackarcana/qa/epicfight/EpicFightFakePlayerEligibilityQa.java) e [workflow](https://github.com/Gustavaopere/Black-Arcana/blob/docs/catalog-perk-causality-20261015/.github/workflows/epicfight-211731-fake-player-eligibility-qa.yml) separados do JAR de produção, ativados somente por BLACK_ARCANA_EPICFIGHT_QA_FAKE_PLAYER_PREFLIGHT=1. Sem redistribuição do JAR do Epic Fight.

## Observação direta sem mutação

O QA usou a FakePlayerFactory do NeoForge para obter um FakePlayer. Consultou seu AttributeInstance de minecraft:generic.max_health e a attachment do próprio Epic Fight registrada sob EpicFightAttachmentTypes.ENTITY_PATCH. Inspecionou os campos de identidade e inicialização do patch, sem criar manualmente uma instância do provider nem fazer reflexão ampla sobre métodos potencialmente client-only.

| Item verificado | Resultado |
|---|---|
| FakePlayer do NeoForge | Presente |
| AttributeInstance máximo de vida | Base **20.0** |
| Attachment nativa do Epic Fight | Presente |
| Classe do patch | yesman.epicfight.world.capabilities.entitypatch.player.ServerPlayerPatch |
| Campo EntityPatch.original | Mesma instância FakePlayer |
| Campo EntityPatch.initialized | **false** |
| Status observável | PATCH_ATTACHED_UNINITIALIZED_REQUIRES_JOIN_LIFECYCLE |
| Chamada a SkillContainer.setSkill | **Não executada** |
| Modificação de atributos de jogador | **Não executada** |

A [fonte upstream adjacente 21.17.3, EntityPatch.java](https://github.com/Antikythera-Studios/epicfight/blob/a78aa24b72e90a9d09f5fd61925e4369d117abaf/src/main/java/yesman/epicfight/world/capabilities/entitypatch/EntityPatch.java#L19-L46) indica que onJoinWorld realiza a transição do booleano de inicialização. A [CommonEntityPatchProvider adjacente](https://github.com/Antikythera-Studios/epicfight/blob/a78aa24b72e90a9d09f5fd61925e4369d117abaf/src/main/java/yesman/epicfight/world/capabilities/provider/CommonEntityPatchProvider.java) registra o tipo PLAYER. Essas referências são **source-adjacent**, não prova de equivalência do JAR compilado físico; a prova efetiva é a observação do servidor com o JAR 21.17.3.1 carregado.

## Gate Stage 09 — jogador conectado real, ainda pendente

1. Inicializar servidor com release exata e um cliente de testes, verificando mod IDs, dependências e composição.
2. Conectar um ServerPlayer real, observar sua attachment ServerPlayerPatch e comprovar inicialização pelo lifecycle de entrada no mundo (**initialized=true**) antes de usar a capability.
3. Confirmar categoria/slot Epic Fight exatos e medir o AttributeInstance generic.max_health ao equipar e remover adaptive_skin com datapack **original e temporário** de QA; verificar ID e amplitude do modifier, duplicação, remoção e restauração do valor.
4. Validar reconexão/respawn, sincronização entre cliente/servidor, efeitos de addons do modpack e limpeza/restauração integral dos dados temporários.
5. Se o cliente conectado, patch inicializado ou contrato seguro não estiver disponível, manter **⛔ bloqueado**; nunca chamar onJoinWorld artificialmente, nunca construir um PlayerPatch manualmente nem declarar gameplay homologado por um FakePlayer.

Oito modificadores modernizados foram provados **somente no mapa das skills** durante o gate anterior [#39001996512](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39001996512) (0→8→0, JSON artifact 12089431494). Este novo gate não promove a integração de perks/Mastery e não altera o resultado 43/43 IDs Epic Fight, 42/42 JSONs, +0 magias. Piso global 1.856 semânticas mínimas / 1.854 estritas; Stage 06.05 🟡 e Stage 09 físico pendente; PR #825 draft e sem merge.
