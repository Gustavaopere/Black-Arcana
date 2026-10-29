# Contrato integrado — estado, lifetime, rede e UI

**Contrato:** suporte de Aeromancy Additions `1.2.8`, source fixo `snackerpirater/aero-additions@ae282b32d25ad76ef8d01c637ec05566a767ae4c`. Não é nova identidade de magia. `hooks=NOT_VERIFIED`; `physical_runtime=NOT_TESTED`; **0 certificações / +0 magias / +0 adapters aprovados**. O JAR oficial de publicação foi adquirido separadamente; isso não comprova paridade com o JAR instalado historicamente (SHA-1 histórico de 35 caracteres inválido). [Proveniência e limites](../SOURCE-CONTRACTS-1.2.8.md).

## Stores e autoridade

A fonte demonstra três stores distintos: **MobEffects** da entidade (presença, amplifier, duração); **attachment `aeromancy_magic_data`** (flags/cargas); **map cliente `AAClientData`** (snapshots recebidos por entity ID). Não são aliases. Iron's governa o cast, mana, cooldown e dados adicionais de cast; o provider governa seus callbacks, attachment, input Airstep e visuais. RPG Skill Tree não recebe neste código uma API de mutação ou settlement aprovada.

A attachment padrão conserva `livingEntity` somente para `ServerPlayer`. Serialização salva flags como Long, contador como **Float** e lê como **Int**; esse desacordo é anomalia de fonte, sem prova de perda física. Os construtores de dados recebidos por rede conservam apenas ID/campos, sem referência. O registro não declara `copyOnDeath`; não há handler Clone que use os métodos `clone/getPersistentData`, e esses métodos não copiam valores. Respawn sync não prova retenção de estado.

## Airstep — escritores, gates e resets

| Momento | Store/lado demonstrado | Operação |
|---|---|---|
| `onCast` | Callback de magia; sem side guard local no método | Aplica AIRSTEPPING por `(int)(getSpellPower(level,caster)*30)` ticks com amplifier `level-1`; grava `1+level` cargas na attachment. Chama `super.onCast`. |
| Input em `PlayerTickEvent.Pre` | Cliente local | Não espectador; nova tecla Jump; airborne; não fall-flying; `canJump`. Executa predição e envia `deltaX,deltaZ`. |
| `canJump` | Tanto predição quanto callback servidor | Lê attachment, exige `>0`, efeito AIRSTEPPING e `!onGround`. Leitura chama `doSync`. Não consulta o map do HUD. |
| Handler C2S | Trabalho enfileirado do servidor | Usa `ctx.player()`; mesmos três gates de `canJump`. Não revalida borda de tecla/espectador/fall-flying/ritmo ou intervalo dos ints. |
| Salto aprovado | Callback usado por ambos lados | Substitui movimento por horizontal normalizado ×0.5 + Y `JUMP_STRENGTH+JumpBoost`; reseta fall distance; impulse/som; decremente carga. Partículas SPIT só no lado não cliente. |
| `LivingFallEvent` | Evento, sem gate universal de side no método | Se AIRSTEPPING ativo e distância ≥ SAFE_FALL_DISTANCE e havia carga, zera multiplicador de dano, toca som, partículas só não cliente. **Sempre recarrega `1+spellLevel` cargas quando o efeito está ativo**, mesmo sem passar o gate de proteção. Não debita carga na proteção. |
| `MobEffectEvent.Remove` / `Expired` | Evento, sem side guard local | Se effect instance é AIRSTEPPING, grava contador 0. |
| `ServerGamePacketListenerImpl.tick` | Mixin servidor | Leituras de `clientIsFloating` retornam falso com AIRSTEPPING, independentemente do contador. |

As cargas não decrescem por tick; não são mana. Duração pertence ao MobEffect e à infraestrutura do engine. Nenhum handler deste fluxo é evidência de aquisição/XP; queda, tick, render ou pacote recebido não equivalem a novo cast.

## Propagação e recepção

`set/subtract/getAirStepHitsRemaining` e `add/removeEffects` chamam `doSync`. Se há referência `ServerPlayer`, envia `sync_magic_data` a tracking players e self. O getter sincronizante faz leituras servidor gerarem tentativas de envio; isto é propriedade do código, sem medida de tráfego/custo no pack. `syncToPlayer(recipient)` oferece envio direto.

Login, dimension change e respawn enviam a attachment do próprio player a ele. `StartTracking` literalmente obtém **dados do tracker `event.getEntity()` e envia ao target `event.getTarget()`**, ambos `ServerPlayer`. Não corrigir essa direção na documentação. Não há limpeza explícita de cache nem sync de mob efetivo nestes handlers.

`sync_magic_data` decodifica int ID/long flags/int cargas e **substitui a entrada do map cliente**. Não aplica o snapshot à attachment cliente. Assim, o source fecha que HUD e `canJump` leem stores diferentes; não fecha que a predição e o número apresentado convergem em runtime. Reconnect, reuso de entity ID, tracking tardio, ordem de pacotes e recarga/save exigem QA físico.

O ramo `IMagicEntity` de `doSync` cria `sync_entity_data`, mas essa classe **não está registrada** e seu handler enfileirado é vazio. O callback auxiliar de mob no cache também não aplica dados. Não contar esta classe como quarta rota ativa ou suporte completo a mobs.

## UI e flags realmente usadas

`AirstepCounterBar` é registrado acima de `screen_effects`, só aparece com AIRSTEPPING, GUI visível e player não espectador, e mostra `x<cache.cargas>`, inclusive quando zero. `AAOverlay` aparece com BREATHLESS e usa a mesma textura da camada de Wind Shield, com offset animado e alpha `0.1`. O overlay consulta o MobEffect diretamente.

Constantes de flags `ASPHYXIATING=1`, `WIND_SHIELD=2`, `AIR_STEP=4` existem no estado, mas não há escritor/leitor externo ativo da bitmask no provider auditado. As chamadas antigas em Breathless/WindShield estão comentadas. `WindySwirlRenderer.shouldRender` seleciona entre MobEffect WIND_SHIELD e BREATHLESS usando o número recebido; não testa as flags armazenadas. O lifetime visual segue a presença de MobEffect, sem flag-sync funcional demonstrado.

## Matriz de responsabilidade para perks

| Eixo | Responsabilidade efetiva | Limite de integração |
|---|---|---|
| Dano | Airstep não causa dano; proteção de queda altera multiplicador no evento. Breathless e projéteis têm callbacks próprios. | Não alterar dano genérico usando sync/HUD. MagicWindCharge tem mixin separado para flag da impulsão. |
| Alcance | Airstep: impulso horizontal 0.5, sem seleção espacial. Tracking determina receptores de snapshot/partículas. | Tracking não é range de spell ou AoE. |
| Alvo | C2S controla `ctx.player()`; snapshots usam ID numérico; visuais locais usam player/effect. | Nenhum payload de cast/target arbitrário ou API de perks de alvo. |
| Tempo | MobEffect controla duração; quedas recarregam; remoção/expiração zera; input por Pre tick e UI por render. | Sem cobrança/recompensa de progresso por tick, pacote, render ou recarga. |
| Custo | Cast/mana/cooldown são de Iron's; salto consome uma carga. | Não duplicar cast settlement, mana ou cooldown no mod do pack. |

## Navegação e QA pendente

[Attachment/serializer](../attachments/aeromancy-magic-data.md) · [classe de dados](aeromancy-spell-data.md) · [cache](client-data-cache.md) · [registrador](payload-registration.md) · [Airstep C2S](../payloads/airstep.md) · [sync player](../payloads/sync-magic-data.md) · [sync entidade incompleto](../payloads/sync-entity-data.md) · [Dash visual S2C](../payloads/dash-particles.md) · [eventos servidor](server-events.md) · [eventos cliente](client-events.md) · [contador](airstep-counter-bar.md) · [overlay](breathless-overlay.md) · [mixin anti-floating](../mixins/server-packet-listener.md) · [mixin fall damage](../mixins/server-player.md).

Salvar/reabrir, morte/respawn, logout/relogin, mudança de mundo/dimensão, predição cliente, replay/inputs extremos e interações de mixins precisam execução no pack para estabelecer resultado. Este contrato registra implementações e lacunas da fonte; **não certifica comportamento no modpack físico**.


**Fonte imutável:** [Factory](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/network/AADataAttachments.java#L13-L21) · [NBT/codec](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/network/AeromancySpellData.java#L28-L71) · [Mutação e envio](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/network/AeromancySpellData.java#L79-L143) · [Airstep callbacks](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/spells/airstep/AirstepSpell.java#L77-L145) · [Input/layers](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/AAClientEvents.java#L70-L102) · [Lifecycle](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/AAServerEvents.java#L92-L119) · [Aplicação S2C](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/network/AASyncPlayerDataPacket.java#L26-L33) · [Cache](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/network/AAClientData.java#L10-L40) · [Registros ativos](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/network/AAPayloadHandler.java#L11-L21) · [Handler entidade](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/network/AASyncEntityDataPacket.java#L18-L35) · [MobEffects visuais](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/spells/wind_shield/WindySwirlRenderer.java#L139-L143) · [Overlay](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/AAOverlay.java#L19-L55) · [HUD](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/spells/airstep/AirstepCounterBar.java#L13-L26).
