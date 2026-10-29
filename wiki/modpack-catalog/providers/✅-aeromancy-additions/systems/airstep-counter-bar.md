# HUD — contador de Airstep

**Contrato:** suporte de Aeromancy Additions `1.2.8`, source fixo `snackerpirater/aero-additions@ae282b32d25ad76ef8d01c637ec05566a767ae4c`. Não é nova identidade de magia. `hooks=NOT_VERIFIED`; `physical_runtime=NOT_TESTED`; **0 certificações / +0 magias / +0 adapters aprovados**. O JAR oficial de publicação foi adquirido separadamente; isso não comprova paridade com o JAR instalado historicamente (SHA-1 histórico de 35 caracteres inválido). [Proveniência e limites](../SOURCE-CONTRACTS-1.2.8.md).

## Registro, gate e store

`AirstepCounterBar.instance` implementa `LayeredDraw.Layer`. `AAClientEvents.registerLayers` registra `aero_additions:airstep_counter` acima de `aero_additions:screen_effects` (o overlay é registrado acima de todas as camadas). A classe não envia C2S nem aplica salto.

`shouldRender` exige player local não nulo, MobEffect **AIRSTEPPING** ativo, GUI visível e player não espectador. Não exige contador positivo. Renderiza a textura `aero_additions:textures/gui/airstep_counter.png` em 12×12 e o texto branco `"x" + contador`, consultado em `AAClientData.getAeroSpellData(localPlayer).getAirStepHitsRemaining()`.

Coordenadas: `x=screenWidth/2+100`; `y=screenHeight-43-(creative?0:10)`; texto em `(x+13,y+2)`. São constantes da apresentação, sem config/perk no método. O contador apresentado é o **cache de snapshots S2C**; `canJump` lê a attachment da entidade. O source não mostra a recepção aplicando o snapshot à attachment. O getter chama `doSync`, porém objetos decodificados/fallback sem referência `ServerPlayer` não fazem envio nesse ramo.

| Eixo | Contrato para perks |
|---|---|
| Dano | N/A: elemento visual. |
| Alcance | N/A: tela local. |
| Alvo | Player local, entrada do cache pelo ID numérico. |
| Tempo | Consulta a cada render quando o gate passa; sem animação/TTL próprio ou decremento de carga. |
| Custo | N/A: não debita mana ou carga; só lê o contador. |

O HUD não é autoridade para cast/XP e seu render não é evento de progresso. [Cache](client-data-cache.md) · [wire S2C](../payloads/sync-magic-data.md) · [stateflow](state-lifecycle-network-ui.md). Aparência, posicionamento, latência e concordância cache/attachment permanecem `NOT_TESTED`.


**Fonte imutável:** [AirstepCounterBar.java](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/spells/airstep/AirstepCounterBar.java#L13-L26) · [Registro das camadas](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/AAClientEvents.java#L77-L80) · [Cache](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/network/AAClientData.java#L14-L26) · [Getter e distribuição](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/network/AeromancySpellData.java#L96-L126) · [Gate de salto](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/spells/airstep/AirstepSpell.java#L113-L124).
