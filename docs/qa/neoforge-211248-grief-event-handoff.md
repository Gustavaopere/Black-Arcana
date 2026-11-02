# Handoff — NeoForge `EventHooks.canEntityGrief` (21.1.248)

**Propósito:** continuar o recorte SHA-exato de Alex's Caves Continued 1.0.10 da [PR #1007](https://github.com/Gustavaopere/Black-Arcana/pull/1007), sem repetir os 24 testes já integrados. Aquele recorte comprovou `ACPlatform.canEntityGrief -> EventHooks.canEntityGrief` e o ramo de retorno antecipado do `TremorzillaEntity.breakBlocksAround`, mas não inspecionou a implementação NeoForge.

## Autoridades distintas

- A modlist física referenciada em `neoforge-rpg-skilltree/main@59ff2a0e827fd08faa603f4482f8104ac433383c` registra **NeoForge 21.1.250**. O **21.1.248** é o *baseline* de desenvolvimento do Black Arcana (README / `plans/DECISIONS.md` D014). O presente experimento audita 21.1.248 **sem extrapolar** sua validade para o loader físico 21.1.250.
- API pública de NeoForge 1.21.1: `canEntityGrief(Level, @Nullable Entity)` retorna a regra `mobGriefing` quando a entidade é `null`; quando existe entidade, emite `EntityMobGriefingEvent` no event bus e retorna `canGrief()`. O objeto de evento inicializa `canGrief` pelo valor da gamerule e pode ser modificado pelos listeners através de `setCanGrief(boolean)`. Isto está documentado no [Javadoc de EventHooks](https://lexxie.dev/neoforge/1.21.1/net/neoforged/neoforge/event/EventHooks.html) e [Javadoc do evento](https://aldak.netlify.app/javadoc/1.21.1-21.1.x/net/neoforged/neoforge/event/entity/entitymobgriefingevent).
- A inspeção independente do código da *branch* pública `NeoForged/NeoForge@1.21.1` é **evidência de fonte mutável**, não é uma verificação SHA-exata de 21.1.248. Por isso a [sonda de bytecode](neoforge_211248_grief_event_probe.py) e o [workflow](../../.github/workflows/neoforge-211248-grief-event.yml) exigem o artefato Maven da versão exata, `javap` do Java 21 e testes de regressão.

## Estados da auditoria

O workflow primeiro registra SHA-256 do JAR e hashes SHA-256 de duas classes e cinco métodos selecionados. Depois deve ser incorporado um manifesto `NEOFORGE-211248-GRIEF-EVENT-ABI.json` com os valores efetivamente observados. **Somente a execução subsequente em modo `--seal` pode atestar que o bytecode compilado continua idêntico.** O modo inicial sem manifesto é explicitamente exploratório. Testes sintéticos executados localmente não substituem a execução do JAR oficial.

Mesmo que a implementação confirme esse fluxo, a decisão do evento é dependente de listeners instalados. O evento **não é, isoladamente, um comprovante de autorização por posição, claim, dono ou proteção de terreno**, nem garante tratamento adequado de `BlockState.onBlockExploded`, `Level.destroyBlock` ou spawns. Não se deve alterar raio, volume, dano ou destruição em perks do Tremorzilla por esse recorte. A permissão de WorldEffectPolicy do Black Arcana também não pode ser presumida para uma mutação nativa do provider.

**Estado:** ⚠️ `NOT_CERTIFIED` / `NO_MUTATION` / `mutating_hook=NOT_VERIFIED` / `physical_qa=NOT_TESTED`; +0 fichas, +0 providers. Stage 06 permanece inalterado.