# Cloak of Darkness — Darkness Incarnate

- Provider: **Alex's Caves Continued** (`alexscaves`)
- Version: `1.0.10`
- Exact physical/publisher SHA-1: `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`
- Owner: `alexscaves:cloak_of_darkness` with the provider Darkness armor condition
- Trigger: provider armor key after charge/eligibility is satisfied
- State: `COUNTED_EXACT`

## Semantic identity

The provider consumes cloak charge and applies the active Darkness Incarnate state, including its provider flight behavior. Charge time, duration, light checks and HUD state are parameters/gates of the same action.

## Exact acquisition

Exact provider data closes Cloak and Hood of Darkness through provider recipes.

## Boundary

Numerical tuning, cooldowns, targeting, entities, effects, particles, sounds and world settlement remain provider authority. Black Arcana catalogs the identity and must not replay provider settlement.

Sources: `../EXACT-1.0.10-ARTIFACT-AUDIT.md`, `../ITEM-ACTION-DISPOSITION-1.0.10.md`.

## Contrato causal de carga, ativação e voo — fonte pública fixada (não homologado no JAR físico)

**Teto de evidência (2026-10-28).** As identidades são `COUNTED_EXACT` pelo relatório de auditoria da versão instalada `alexscaves` 1.0.10, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`. Os parâmetros abaixo resultam de inspeção **read-only** do fonte público `Codx-org/AlexsCavesContinued@523308608422ab8e31974befa7111ecdf495dd37`; a igualdade binária desse commit com o JAR físico **não foi demonstrada**. Rotular esses parâmetros `SOURCE_SNAPSHOT_ONLY`, e **não** `COMPLETE_PERK_READY`. Configs efetivas, chamadas packet/runtime, hooks mutadores e QA física permanecem `NOT_VERIFIED`.

| Parâmetro / seam | Evidência method-pinned do snapshot |
|---|---|
| Elegibilidade | `DarknessArmorItem.canChargeUp(living, false)` requer **Hood of Darkness**, ausência de `DARKNESS_INCARNATE` ativo e **não estar na luz** segundo `DarknessIncarnateEffect.isInLight(living, 11)`. O teste consulta luz do bloco e céu/horizonte |
| Charge e config | Item usa NBT `CloakCharge`, flag `CanCharge` e configs `darknessCloakChargeTime` e `darknessCloakFlightTime`. Esses valores são configuração do provider; **não há quantidade fixa de ticks certificada aqui** |
| Leitura do medidor | `getMeterProgress` calcula `CloakCharge / darknessCloakChargeTime`; `hasMeter` exige Cloak no CHEST, Hood no HEAD e ausência do efeito |
| Ciclo de item | `acInventoryTick` reconhece o cloak equipado e reavalia `CanCharge` periodicamente (**intervalo >10 ticks** pelo timestamp), com `UpdateItemTagMessage` como suporte. O snapshot contém ponte de compatibilidade 1.21 comentada pelo pré-processador para `acArmorTick`; não assumir que todos os caminhos comentados são executados no JAR |
| Intent de ativação | Quando o **cliente** detecta medidor `>=1.0F` e tecla `2`, envia `ArmorKeyMessage(CHEST ordinal, wearer id, 2)` e chama também `onKeyPacket` localmente |
| Aplicação | `onKeyPacket` zera `CloakCharge` e adiciona efeito `DARKNESS_INCARNATE` com duração configurável quando `canChargeUp(living,false)` passa. **Nesse método isolado não aparece teste de carga completa nem do inteiro `key`**; é requisito auditar o pipeline servidor `ArmorKeyMessage.handle`, sem presumir falha ou segurança física |
| Roteamento de mensagem | `ArmorKeyMessage.handle` obtém `context.getSender()`, resolve entidade por `message.playerId`, valida `instanceof Player`, obtém armadura no slot informado e despacha `KeybindUsingArmor.onKeyPacket`. Neste trecho não há comparação explícita entre o UUID do remetente e o jogador resolvido; **risco de autorização a investigar**, não exploração confirmada na versão instalada |
| Voo/efeito | `DarknessIncarnateEffect.tick` chama `toggleFlight(...,true)`, que para `ServerPlayer` liga `mayfly/flying` e ajusta flying speed a `0.05F*4=0.2F`; `onEffectEnd` retorna a speed a `0.05F` e desativa voo para não criativos fora de spectator |
| Compatibilidade | A restauração direta de `mayfly/flying` pode colidir com fontes de voo de outros mods/perks; não há contrato compartilhado de lease/ownership de voo demonstrado neste snapshot |

### Gates de segurança e compatibilidade

Não inferir `cooldown` a partir do tempo de carga nem gravar `CloakCharge` pelo Black Arcana. Antes de qualquer perk de recarga, duração, voo ou restrição de luz, verificar o bytecode **exatamente instalado** 1.0.10, o caminho final do packet server-side (identidade do player, slot e charge), o `darknessCloakChargeTime` efetivo, sincronização de tags, retorno de voo após morte/remoção/remoção do efeito, coexistência com flight providers e dedicated server. **⛔ Fail-closed** sem hook mutador público/suportado e teste físico.

**Fontes:** [`DarknessArmorItem`](https://github.com/Codx-org/AlexsCavesContinued/blob/523308608422ab8e31974befa7111ecdf495dd37/src/main/java/com/github/alexmodguy/alexscaves/server/item/DarknessArmorItem.java), [`ArmorKeyMessage.handle`](https://github.com/Codx-org/AlexsCavesContinued/blob/523308608422ab8e31974befa7111ecdf495dd37/src/main/java/com/github/alexmodguy/alexscaves/server/message/ArmorKeyMessage.java), [`DarknessIncarnateEffect`](https://github.com/Codx-org/AlexsCavesContinued/blob/523308608422ab8e31974befa7111ecdf495dd37/src/main/java/com/github/alexmodguy/alexscaves/server/potion/DarknessIncarnateEffect.java); [relatório de identidade exata](../EXACT-1.0.10-ARTIFACT-AUDIT.md).
