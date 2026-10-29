# Payload S2C — aero_additions:dash_particles

**Contrato:** suporte de Aeromancy Additions `1.2.8`, source fixo `snackerpirater/aero-additions@ae282b32d25ad76ef8d01c637ec05566a767ae4c`. Não é nova identidade de magia. `hooks=NOT_VERIFIED`; `physical_runtime=NOT_TESTED`; **0 certificações / +0 magias / +0 adapters aprovados**. O JAR oficial de publicação foi adquirido separadamente; isso não comprova paridade com o JAR instalado historicamente (SHA-1 histórico de 35 caracteres inválido). [Proveniência e limites](../SOURCE-CONTRACTS-1.2.8.md).

## Wire, produtor e efeito

`DashParticlesPacket` é registrado `playToClient`. Codec: **`Vec3 pos1` → `Vec3 pos2`**, usando `writeVec3`/`readVec3`. Apesar do nome `pos2`, o produtor de `DashSpell.onCast` envia `entity.position()` e **o vetor do impulso `vec`**, não uma posição de destino. `vec=look.multiply(2,1,2).normalize().scale((15+getSpellPower)/12f)`. Distribuição: `sendToPlayersTrackingEntityAndSelf(entity, packet)`.

O handler enfileirado obtém o player local e só cria partículas se não for nulo. Usa `pos1` como centro e `pos2.scale(0.2)` como velocidade base. Executa 20 iterações de `SPIT` com `force=true`: posição X/Z no intervalo relativo `[-0.5,+0.5)`, Y em `[-1.2,+1.2)`; adiciona ruído `[0,0.1)` à velocidade de cada eixo e passa os três componentes negados a `level.addParticle`. Os limites provêm de `Utils.random.nextDouble()` e constantes locais, sem scaling por delta time.

O pacote não move a entidade, não concede invulnerabilidade, não causa dano e não cobra custo. A movimentação de Dash, `ImpulseCastData` de Iron's e `invulnerableTime=20` estão no callback da magia, separados deste S2C visual. Um comentário sobre `ClientSpellCastHelper.handleClientboundTeleport` está desativado: não há teleporte ativo no handler.

| Eixo | Contrato para perks |
|---|---|
| Dano | N/A: puramente visual. |
| Alcance | 20 partículas em torno de `pos1`; tracking/self define receptores, sem raio de dano. |
| Alvo | Clientes que recebem a distribuição; não transporta entity ID. |
| Tempo | Uma emissão de 20 partículas por pacote; lifetime de partículas pertence ao engine. |
| Custo | N/A: mana/cooldown pertencem ao cast de [Dash](../spells/dash.md). |

Nenhum perk deve reenviar o pacote para reproduzir o dash. Packet delivery, partículas e sincronização do impulso em multiplayer permanecem `NOT_TESTED`.


**Fonte imutável:** [Codec e handler](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/spells/dash/DashParticlesPacket.java#L18-L69) · [Registro S2C](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/network/AAPayloadHandler.java#L14-L20) · [Produtor e estado separados](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/spells/dash/DashSpell.java#L51-L85).
