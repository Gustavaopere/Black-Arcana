# Payload C2S — aero_additions:airstep

**Contrato:** suporte de Aeromancy Additions `1.2.8`, source fixo `snackerpirater/aero-additions@ae282b32d25ad76ef8d01c637ec05566a767ae4c`. Não é nova identidade de magia. `hooks=NOT_VERIFIED`; `physical_runtime=NOT_TESTED`; **0 certificações / +0 magias / +0 adapters aprovados**. O JAR oficial de publicação foi adquirido separadamente; isso não comprova paridade com o JAR instalado historicamente (SHA-1 histórico de 35 caracteres inválido). [Proveniência e limites](../SOURCE-CONTRACTS-1.2.8.md).

## Wire e consumidor

`AirstepPacket` é a única rota provider-owned `playToServer`. Codec: **`int deltaX` → `int deltaZ`**; não contém entidade, ID de magia, nível, mana, velocidade ou contador. O decoder usa `readInt` sem clamp local. O handler enfileira `AirstepSpell.airstepJump(packet, ctx.player())`: a entidade vem do contexto autenticado da conexão, não do corpo do pacote.

O produtor cliente é `AAClientEvents.Game.handleJump(PlayerTickEvent.Pre)`: apenas player local não espectador; borda de tecla de pulo pressionada; airborne; não fall-flying; `AirstepSpell.canJump`. Calcula `deltaX=(up?1:0)+(down?-1:0)` e `deltaZ=(right?1:0)+(left?-1:0)`, portanto o produtor normal emite `-1..1`. Executa o salto local primeiro e depois envia o mesmo pacote ao servidor.

## Validação efetivamente chamada no servidor

`airstepJump` retorna falso se `canJump` falhar. O gate é exatamente **contador da attachment > 0, MobEffect AIRSTEPPING ativo e `!onGround()`**. O servidor não revalida borda de tecla, espectador, fall-flying, limite `-1..1`, spell level, mana ou cooldown nessa rota; também não há rate limit explícito. Os gates adicionais do produtor cliente não são gates C2S de servidor.

Com gate aprovado, cria `Vec3(deltaX,0,deltaZ)`, gira por `-atan2(look.z,look.x)`, normaliza e escala a `0.5`; a componente Y é `JUMP_STRENGTH + getJumpBoostPower()`. `setDeltaMovement` **substitui** o vetor, reseta fall distance, marca `hasImpulse`, toca Breeze jump e decrementa a attachment em 1. Partículas SPIT (10) são pedidas apenas no lado não cliente. Não há ajuste de mana nesta ação. Normalização limita magnitude horizontal dos inputs não nulos, mas não constitui validação de intervalo/ritmo do wire.

| Eixo | Contrato para perks |
|---|---|
| Dano | N/A: salto não inflige dano direto; reseta queda. |
| Alcance | Sem raycast/raio; impulso horizontal `0.5`, Y delegado ao atributo/Jump Boost. |
| Alvo | `ctx.player()` exclusivamente no servidor. |
| Tempo | Um salto aceito consome uma carga; sem timer/cooldown local adicional. Lifetime é AIRSTEPPING. |
| Custo | Uma carga, sem mana por pacote; mana/cooldown do cast pertencem a Iron's. |

[Estado e resets](../systems/state-lifecycle-network-ui.md), [mixin anti-floating](../mixins/server-packet-listener.md), [magia](../spells/airstep.md). Replays, inputs extremos, latência, predição/cache e side validation permanecem `NOT_TESTED`; não existe autorização de adapter para alterar esse wire.


**Fonte imutável:** [Codec e handler](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/spells/airstep/AirstepPacket.java#L10-L37) · [Registro C2S](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/network/AAPayloadHandler.java#L14-L20) · [Produtor cliente](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/AAClientEvents.java#L82-L102) · [Gate e movimento](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/spells/airstep/AirstepSpell.java#L98-L130) · [Decremento/sync](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/network/AeromancySpellData.java#L96-L108).
