# Keybind Using Armor

**Contrato estático:** ✅ `CERTIFIED_STATIC_7_AXES` / `STATIC_TECHNICAL_CATALOG_ONLY` (candidato à CI e merge). **Runtime/hook:** `NOT_VERIFIED`. **Perk executável:** `NOT_CERTIFIED`. **QA física:** `NOT_TESTED`. `NO_MUTATION`; provider OPEN; zero novas raízes.

**Autoridade:** Alex's Caves Continued (`alexscaves`) 1.0.10; Minecraft 1.21.1 / NeoForge 21.1.250 documental / Java 21. Modlist física sibling #019; publisher `alexscaves-1.0.10-neoforge+1.21.1.jar`, 75.279.314 bytes, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c32e9f2e95bffae0e7c`. Não houve comparação nova com dump físico instalado nem observação do runtime transformado. [Dossiê de descoberta SHA-exata](../EXACT-JELLY-KEYBIND-LIMESTONE-1.0.10.md) e [replay](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45651673635/job/139337522318): 186.937 bytes, SHA-256 `61a6010adbe0c6f41968a6ffc8f85e8c4c6e013175007f6be93280d3cf2da0ed`, duas saídas byte-idênticas, seis checks. O dossiê detalha consumidores, hashes de métodos e offsets. Replay da HEAD consolidada obrigatório.

## Identidade e descrição funcional

Owner `com/github/alexmodguy/alexscaves/server/item/KeybindUsingArmor`, SHA-256 `6ed129bf051acf5b551e2e96ed898c818304fe99e0298fb9f0a5ebf226bc3b86`. Declara uma assinatura sem Code: `onKeyPacket(Entity,ItemStack,int)V`. Não há ID de item ou magia independente demonstrado para essa interface. DarknessArmorItem é implementador direto encontrado no censo; ArmorKeyMessage é consumidor tipado. Contrato de suporte; não acrescentar uma habilidade independente pelo nome.

## Ativação e boundary

ArmorKeyMessage.lambda$handle$0, Code SHA `0641114dc3b38ccf47d158b49226b2d4afe39ab7bf8d104faa58686c052f0e60`: janelas observadas Player.getItemBySlot @80, getItem @87, instanceof @94, checkcast @102 e dispatch onKeyPacket @116 com entidade local 3, stack local 6 e type:I do pacote. A seção complementar abaixo fecha o fluxo estático de seleção, slot, dispatch e seus limites de autorização; não comprova aceite físico.

## Parâmetros, custos, autoria e integração

A interface em si declara apenas os argumentos acima; não define fórmula, alcance, AOE, dano, cooldown, custo, projétil, duração ou efeito. Os valores pertencem ao implementador e à engine; o dispatcher nativo está delimitado abaixo. Fichas já existentes de DarknessArmorItem e cloak são evidência a reusar, sem transferir selo automaticamente. Ownership, persistência e autoridade de rede permanecem abertos. Não tratar dispatch como API mutadora segura ou permissão para enviar/repetir packets; sem Mastery e sem bypass de gates.

## Prova causal complementar: interface, wire e dispatch

[Run 45796533259 / job 139828495853](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45796533259/job/139828495853), dois replays 765.144 bytes SHA-256 `6c8e0c98af51b60fe40d3bd0b326fb909525f1780b2086740748e158b6bd20ea`. [Dossiê](../EXACT-FOOD-IDENTITY-KEYBIND-CLOSURE-1.0.10.md) e [selo](../EXACT-KEYBIND-USING-ARMOR-CONTRACT-1.0.10.json). Interface sem corpo executável, uma declaração abstrata; implementação nativa DarknessArmorItem, classe SHA `872fc610bac5be6010e3981b001c4088c7227e9cffe7938381c34c2f456c4e9a`; assertion de hierarquia transitiva na nova HEAD. ArmorKeyMessage classe SHA `ea27e9648b5c756d1e3487ecedc382c17e24c83e812ab8e81cb67fa962b5c33e`, seis declarações: dois construtores, read/write, handle e lambda. Três int serializados em ordem equipmentSlot/playerId/type, sem validação de valores na serialização. ACNetwork.registerPayloads solicita playBidirectional @22 e lambda despacha por ENTRIES; contexto getSender usa context.player(), retorna ServerPlayer ou null; isClientSide usa flow.isClientbound; enqueueWork delega IPayloadContext, descarta Future. handle enfileira @8 e marca handled @15; não comprova execução. Lambda escolhe sender ou client local Player, exige não nulo, resolve entidade no nível do contexto @35, clamp slot para 0..values.length−1 @53, exige entidade Player, lê slot @80, testa interface e despacha @116. Não existe comparação de igualdade entre sender e entidade resolvida, validação própria de type ou charge cheia nesse fluxo. Não considerar boundary de autorização de Black Arcana.

DarknessArmorItem.onKeyPacket, 56 instruções, Code SHA `89c7304d0aecfa82668ee6c50df9b63911773cac5363fa241278819ad1b12286`: testa LivingEntity e canChargeUp(entity,false) @16, exige ausência de luz pelo helper argumento 11, Hood no HEAD e ausência de Darkness Incarnate; ramo de criatividade não habilitado pelo false. Se elegível, reset CloakCharge da stack fornecida a 0 @33, ACCompat.setTag @39, solicita efeito DARKNESS_INCARNATE com duração de ACServerConfig.darknessCloakFlightTime, amp0 e três flags false @81, addEffect @84 com retorno descartado. Ramo inelegível exibe mensagem no Player cliente; sem guarda de lado no ramo de efeito. O int type não é lido. Não é recibo de custo ou efeito aceito. ACCompat.setTag escreve CUSTOM_DATA, null remove componente; getTag devolve copyTag. UpdateItemTagMessage trata mãos, não prova sincronização de armadura. [Cloak](../actions/cloak-darkness-incarnate.md) conserva charge, config, efeitos e lifecycle. Sem ação, fórmula, alcance, AOE, dano, projétil, mana ou cooldown próprios da interface. Sem hook seguro; não repetir mensagem, reset, efeito ou XP. O certificado delimita API/fluxo estático, não segurança de protocolo, execução instalada ou rede. Teste físico obrigatório.

| Método | Code SHA-256 |
|---|---|
| `ArmorKeyMessage.lambda$handle$0` | `0641114dc3b38ccf47d158b49226b2d4afe39ab7bf8d104faa58686c052f0e60` |
| `ArmorKeyMessage.handle` | `3dfa9769bbdbc6e6d5e5239e2904841e01683c735561e99885da8a83ff026905` |
| `ArmorKeyMessage.read` | `bfa0ff4d6c5f4739c08652943aa7e2bda6e6c9fe0584fe4f73c40c974356e88c` |
| `ArmorKeyMessage.write` | `953c1d44fac650e7d5a0216a589d50586469dcf757926a0816a98c826e6bc208` |
| `DarknessArmorItem.onKeyPacket` | `89c7304d0aecfa82668ee6c50df9b63911773cac5363fa241278819ad1b12286` |
| `ACNetwork.registerPayloads` | `de5583c030c814cc0056b433a84b017fd4a5e24de8c5953f4649a3649878bd7a` |
| `ACNetwork.lambda$registerPayloads$0` | `cfa43e477d3bb6eb24224f020fe26081e6aa032924e8378198ada9b9b6455697` |
| `ACNetwork$NeoForgeContext.getSender` | `ba5bee8479142d9291b2f653661e626c31c63a612cf3eb0b90f0bf4b674c4794` |
