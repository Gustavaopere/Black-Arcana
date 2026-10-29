# Integração cliente — AAClientEvents

**Contrato:** suporte de Aeromancy Additions `1.2.8`, source fixo `snackerpirater/aero-additions@ae282b32d25ad76ef8d01c637ec05566a767ae4c`. Não é nova identidade de magia. `hooks=NOT_VERIFIED`; `physical_runtime=NOT_TESTED`; **0 certificações / +0 magias / +0 adapters aprovados**. O JAR oficial de publicação foi adquirido separadamente; isso não comprova paridade com o JAR instalado historicamente (SHA-1 histórico de 35 caracteres inválido). [Proveniência e limites](../SOURCE-CONTRACTS-1.2.8.md).

## Eventos e ownership

`AAClientEvents` e sua classe interna `Game` são `@EventBusSubscriber(modid=aero_additions,value=Dist.CLIENT)`. As ações de render e input pertencem ao provider, sem hook próprio de RPG Skill Tree.

| Callback | Ação ativa |
|---|---|
| `rendererRegister(RegisterRenderers)` | Renderer Curios de Updraft Tome (`SpellBookCurioRenderer` de Iron's); renderers de MagicWindCharge, UpdraftVisualEntity, SummonedBreeze, WindBladeProjectile e Tornado. São entidades/visuais auxiliares; não novos spells. |
| `registerRenderers(AddLayers)` | Adiciona `WindySwirlRenderer.Vanilla` às skins player SLIM e WIDE quando renderer é `LivingEntityRenderer`, passando `AeromancySpellData.WIND_SHIELD` (=2). Iteração para Geo mob renderers está comentada. |
| `registerLayers(RegisterGuiLayersEvent)` | [Overlay Breathless](breathless-overlay.md) acima de tudo e [contador Airstep](airstep-counter-bar.md) acima desse overlay. |
| `Game.handleJump(PlayerTickEvent.Pre)` | Input do player local e predição de [Airstep C2S](../payloads/airstep.md), detalhado abaixo. |

`wasJumping` é booleano estático. O callback só o atualiza dentro do gate de player local não nulo, entidade do evento igual ao player local e não espectador. Ao detectar subida da tecla Jump, se airborne e não fall-flying, consulta `AirstepSpell.canJump`, monta os eixos direcionais `-1..1`, chama o salto local e envia o pacote ao servidor. Não há reset explícito de `wasJumping` em logout/mudança de mundo neste source. Essas restrições do input não acrescentam gates ao handler servidor.

A constante `WIND_SHIELD=2` passada ao renderer funciona como seletor de MobEffect: o renderer consulta `entity.hasEffect(WIND_SHIELD)` ou `BREATHLESS`; não lê a bitmask da attachment. O bloco de shapeshift e o ramo Geo de registro estão comentados; não os catalogar como integração ativa.

| Eixo | Contrato para perks |
|---|---|
| Dano | N/A nos callbacks cliente; não autorizam dano ou XP. |
| Alcance | N/A visual; input Airstep produz impulso de `0.5` horizontal no callback delegado. |
| Alvo | Renderers registrados; input e GUI usam player local. |
| Tempo | Registro por eventos; input em `PlayerTickEvent.Pre`; GUI por render. Sem timer de spell próprio. |
| Custo | N/A nos handlers; salto delegado consome carga, casting/mana/cooldown são de Iron's. |

[Stores e sides](state-lifecycle-network-ui.md). Renderers ativos não comprovam execução ou compatibilidade física com o cliente do pack.


**Fonte imutável:** [Registro e skins](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/AAClientEvents.java#L41-L80) · [Input cliente](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/AAClientEvents.java#L82-L102) · [Shapeshift desativado](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/AAClientEvents.java#L104-L129) · [Gate visual real](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/spells/wind_shield/WindySwirlRenderer.java#L139-L143) · [Salto delegado](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/spells/airstep/AirstepSpell.java#L98-L124).
