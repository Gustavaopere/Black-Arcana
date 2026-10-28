# RibbonHandler — anexação, tracking e limpeza — Ace's Spell Utils 1.2.7.2

**Tipo:** superfície de manutenção/routing de VFX do provider · **Estado:** ⚠️ contrato source-pinned, QA física fail-closed.

## Arquivos exatos e responsabilidades

- [`utils/RibbonHandler.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/utils/RibbonHandler.java)
- [`events/AcesSpellUtilsServerEvents.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/events/AcesSpellUtilsServerEvents.java)
- [`network/TriggerRibbonPacket.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/network/TriggerRibbonPacket.java)
- [`vfx/ribbon/RibbonConfig.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/vfx/ribbon/RibbonConfig.java), [`ColorRamp.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/vfx/ribbon/ColorRamp.java), [`Curve.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/vfx/ribbon/Curve.java) e [`Easing.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/vfx/ribbon/Easing.java)
- [`client/ribbon/ActiveRibbon.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/client/ribbon/ActiveRibbon.java), [`RibbonManager.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/client/ribbon/RibbonManager.java), [`RibbonRenderer.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/client/ribbon/RibbonRenderer.java) e [`RibbonRenderTypes.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/client/ribbon/RibbonRenderTypes.java)

**Fluxo source:** `RibbonHandler` mantém `ConcurrentHashMap<UUID, Attached(Entity,RibbonConfig)>` no servidor. `attach` armazena entidade e envia `TriggerRibbonPacket(id,true,config)` via `sendToPlayersTrackingEntityAndSelf`; `detach` remove do mapa e envia `attach=false`. `resend(ServerPlayer,target)` reenvia config para novos espectadores; `pruneDead` remove registros de entidades não vivas; `clear` na parada do servidor. `AcesSpellUtilsServerEvents.onStartTracking(PlayerEvent.StartTracking)` chama `resend` para ServerPlayer e `onServerTick(ServerTickEvent.Post)` executa `pruneDead`.

**Targeting/range/tempo/consumo:** Entidade rastreada no mundo e cliente de espectadores; wire transmite `entityId` runtime e config. Não há damage source, spell ID, mana ou alcance de cast nesse canal.

**Risco e dependências:** O mapa é estático por UUID e usa igualdade de instância no `isAttached` e `resend`. Testar relog, id reuse, teleporte/dimensão, stop; ausência de reenvio pode desincronizar só o visual, não deve alterar estado server gameplay.

## Configuração e geometria reais

| Tipo/campo | Parâmetro local e unidade |
|---|---|
| `RibbonConfig.color` / `ColorRamp` | Null/vazio→branco; até **8 stops RGB**. Copia arrays na entrada e devolve clone. `at(t)` interpola canais arredondados em 0..255; t=0 é cauda, t=1 cabeça. |
| `width` | Null→`Curve.of(0.18)`; endpoints limitados a **0..4**. Renderer desloca essa medida para **cada lado** da linha antes do miter, não largura total fixa. |
| `alpha` | Null→`Curve.of(1)`; sem clamp 0..1 no record. Renderer limita `round(alpha(t)*255)` a 0..255. |
| `length` | **2..128 amostras de tick**, não blocos nem TTL do attachment. |
| `additive` | Factory `of(color,width,length)` usa false; true seleciona blend LIGHTNING, preservando alpha. |
| `Curve(head,tail,easing)` | Endpoints não finitos→0, easing null→LINEAR; `at(t)=tail+(head−tail)*ease(clamp(t,0,1))`. `of(head)` usa tail 0/LINEAR. |
| `Easing` | LINEAR, EASE_IN_QUAD, EASE_OUT_QUAD, EASE_IN_OUT_QUAD, EASE_IN_CUBIC, EASE_OUT_CUBIC; ordinal inválido→LINEAR. A ordem é parte do wire contract, sem significado de hit/cast. |

## Estado cliente, amostragem e orçamento

`RibbonManager` guarda `HashMap<Integer,ActiveRibbon>` por entityId; attach substitui a instância e zera histórico, detach remove imediatamente. No tick cliente retorna durante pausa; level null limpa tudo; entidade ausente/morta remove a entrada. Não há fila para packet que chegue antes da entidade nem TTL/NBT do attachment. `ActiveRibbon.sample` limpa a história em salto **>32 blocos**, adiciona a posição e limita aos últimos length pontos. `active()`/`points()` expõem coleções internas; isso não estabelece API estável de mutação para perks.

O renderer roda em AFTER_ENTITIES, exige ao menos dois pontos, interpola a cabeça com partialTick e descarta segmentos degenerados. Miter é limitado a **2**; cada segmento elegível emite **4 vértices**: no máximo 127 quads/508 vértices por ribbon com length 128. Há passes normal e additive separados e flush por tipo; ambos usam QUADS/POSITION_COLOR, NO_CULL, LEQUAL e escrita só de cor. O buffer 1536 de `RibbonRenderTypes` não é limite de entidades. Não existe cap global de ribbons; length limita histórico local, sem provar orçamento total de render.

## Interoperabilidade e QA

Esse sistema faz apresentação e manutenção do provider. Não cria `AbstractSpell` nem prova hit, gasto de mana, proc, ganho de Mastery ou atualização do mundo. Black Arcana permanece authority para seu próprio casting/hazards/domains/rituais/WorldEffectPolicy/Strain/Corruption/Arcane Danger; RPG Skill Tree só progressão com gates reais. Não implementar segundo handler de estado a partir de evento puramente visual.

Fonte `AceTheEldritchKing/Aces_Spell_Utils@a0b2f4c2fcfa938c8e47239279c77c2ef82647ac`, versão source `1.2.7.2-1.21.1`; arquivo físico catalogado `aces_spell_utils-1.2.7.2-1.21.1.jar` SHA-1 `8cbcd535a0b19bef49504c0b5ecafcbcd1cb1cca` sem verificação de classfile. Build source depende Iron's `3.16.2`; modpack declara `3.16.3`. **QA:** JAR e event handlers reais, client/dedicated server, tracking/clear/teleport, cenários multicaster, packet sequencing e budgets gráficos; `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `COMPLETE_PERK_READY=false`.
