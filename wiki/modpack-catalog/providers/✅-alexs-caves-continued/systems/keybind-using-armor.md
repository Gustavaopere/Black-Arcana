# Keybind Using Armor

**Estado:** ⚠️ PARCIAL / STATIC_DISCOVERY_ONLY. `static_contract=NOT_CERTIFIED`, `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `NO_MUTATION`; provider OPEN. Não representa nova raiz mágica ou cast certificado.

**Autoridade:** Alex's Caves Continued (`alexscaves`) 1.0.10; Minecraft 1.21.1 / NeoForge 21.1.250 documental / Java 21. Modlist física sibling #019; publisher `alexscaves-1.0.10-neoforge+1.21.1.jar`, 75.279.314 bytes, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c32e9f2e95bffae0e7c`. Não houve comparação nova com dump físico instalado nem observação do runtime transformado. [Dossiê de descoberta SHA-exata](../EXACT-JELLY-KEYBIND-LIMESTONE-1.0.10.md) e [replay](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45651673635/job/139337522318): 186.937 bytes, SHA-256 `61a6010adbe0c6f41968a6ffc8f85e8c4c6e013175007f6be93280d3cf2da0ed`, duas saídas byte-idênticas, seis checks. O dossiê detalha consumidores, hashes de métodos e offsets. Replay da HEAD consolidada obrigatório.

## Identidade e descrição funcional

Owner `com/github/alexmodguy/alexscaves/server/item/KeybindUsingArmor`, SHA-256 `6ed129bf051acf5b551e2e96ed898c818304fe99e0298fb9f0a5ebf226bc3b86`. Declara uma assinatura sem Code: `onKeyPacket(Entity,ItemStack,int)V`. Não há ID de item ou magia independente demonstrado para essa interface. DarknessArmorItem é implementador direto encontrado no censo; ArmorKeyMessage é consumidor tipado. Trata-se de candidato a contrato de suporte; não acrescentar uma habilidade independente pelo nome.

## Ativação e boundary

ArmorKeyMessage.lambda$handle$0, Code SHA `0641114dc3b38ccf47d158b49226b2d4afe39ab7bf8d104faa58686c052f0e60`: janelas observadas Player.getItemBySlot @80, getItem @87, instanceof @94, checkcast @102 e dispatch onKeyPacket @116 com entidade local 3, stack local 6 e type:I do pacote. Não demonstra o restante do handler, seleção inicial da entidade, slot, type, thread, autorização ou aceite do callback.

## Parâmetros, custos, autoria e integração

A interface em si declara apenas os argumentos acima; não define fórmula, alcance, AOE, dano, cooldown, custo, projétil, duração ou efeito. Os valores dependem do implementador e dos gates efetivos do dispatcher, ainda NÃO VERIFICADOS neste contrato. Fichas já existentes de DarknessArmorItem e cloak são evidência a reusar, sem transferir selo automaticamente. Ownership, persistência e autoridade de rede permanecem abertos. Não tratar dispatch como API mutadora segura ou permissão para enviar/repetir packets; sem Mastery e sem bypass de gates. Próximo gate: métodos completos do message, implementação, bootstrap, caminho de execução e limites de lado/autoridade.
