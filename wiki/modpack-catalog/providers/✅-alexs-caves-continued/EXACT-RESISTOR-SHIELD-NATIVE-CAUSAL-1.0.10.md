# Resistor Shield — censo e causalidade do JAR publisher 1.0.10

**Objeto:** `alexscaves:resistor_shield`; classe `com/github/alexmodguy/alexscaves/server/item/ResistorShieldItem`. **Estado:** ⚠️ análise estática avançada, **não certificada**. `static_contract=NOT_CERTIFIED`; `mutating_hook=NOT_VERIFIED`; `physical_qa=NOT_TESTED`; `NO_MUTATION`; provider `OPEN`. Não adiciona nova raiz/cast, nem aumenta o numerador de certificações.

## Proveniência e limites

- **Instalado segundo a modlist sibling:** `alexscaves-1.0.10-neoforge+1.21.1.jar`, Minecraft 1.21.1, NeoForge, Java 21; SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`. Identidade da **cópia física instalada** contra o publisher: `NOT_VERIFIED`.
- **JAR publisher analisado pelo workflow:** 75.279.314 bytes; SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`; 1.555 classfiles. `ResistorShieldItem.class` SHA-256 `ffd3fddd74f8d44049886e9013de2e3d67cbd2a721015369175e8442c5044741`.
- **Relatório nativo recuperado do workflow** [#44977634651](https://github.com/Gustavaopere/Black-Arcana/actions/runs/44977634651), [artifact #14737940344](https://github.com/Gustavaopere/Black-Arcana/actions/runs/44977634651/artifacts/14737940344): `report.json` **971.863 bytes**, SHA-256 `260dcbe481e14dad250cfd7ea453b1a8a81a69efc8e0203126220ed5b30c304f`, medido de novo a partir do ZIP recuperado. A extração do publisher passou, mas o checker desse run falhou por uso de `fingerprint` antes de defini-lo; verificador corrigido na PR, **CI da HEAD final ainda necessária**. O artifact é efêmero: reproduzir pelo script, hash e JAR pinados.
- **Cobertura estritamente observada no JAR:** 20 métodos próprios executáveis; 0 campos próprios listados, 5 owners com referências tipadas (27 sites no total, incluindo autorreferências), 4 recursos JSON localizados por nome. Herança `ShieldItem`, mais `ACClientExtensionItem`, `ACEnchantableItem`, `ACRepairableItem` e `ACTickingItem` como interfaces declaradas. **Sem cobertura dos métodos herdados fora do JAR, do runtime do NeoForge ou dos consumidores por reflexão e eventos não tipados.**

## Ativação, estado e callbacks

- `<init>()`: propriedades declaradas `stacksTo(1)` @9, `durability(1000)` @15, `rarity(UNCOMMON)` @21, antes do `ShieldItem.<init>` @24. Uso/consumo real de durabilidade não decorre só do construtor.
- `use(Level,Player,InteractionHand)`: lê stack @2; `Player.startUsingItem(hand)` @9; **se** `isShiftKeyDown()` @13, inverte `isScarlet(stack)` usando `setPolarity` @34. Solicita som `RESITOR_SHIELD_SPIN` @37–49 e delega resultado a `ACCompat.useConsume(stack)` @54. **Não contém guarda de lado cliente/servidor própria**. Resultado real do helper, sincronização do toggle e cooldown herdado não examinados.
- `Polarity`: campo booleano em tag da stack; `isScarlet` retorna `false` quando tag nula. `setPolarity` grava `Polarity` via `ACCompat.getOrCreateTag/ setTag`. Helpers de `UseTime/PrevUseTime` e `SwitchTime/PrevSwitchTime` leem/gravam tags; `getLerpedUseTime` e `getLerpedSwitchTime` interpolam `prev + partialTick * (current - prev)`, sem clamp próprio no método.
- `acInventoryTick`: antes do branch de lado @59, se `UseTime != 0`, entidade viva e stack não igual a `getUseItem()`, pede reset `UseTime=0` @34 e `PrevUseTime=0` @45–55. No ramo cliente, `SwitchTime` cresce +1 até limite 5 na polaridade scarlet e diminui -1 até 0 na outra, guardas @120–160.
- `releaseUsing`: chama `ShieldItem.releaseUsing` @6 e `CommonProxy.clearSoundCacheFor(entity)` @13. `appendHoverText` adiciona `item.alexscaves.resistor_shield.desc` em cinza; não se reproduz texto proprietário.
- `getEnchantmentValue()` retorna 1; `isEnchantable(stack)` exige `count==1`. `acExtraRepairMaterials` retorna os dois ingots Neodymium; `isValidRepairItem` testa `ACRepairableItem.isExtraRepairMaterial` e faz fallback a `ShieldItem.isValidRepairItem`. Aceitação/consumo real em bigorna permanece condicionado.
- `shouldCauseReequipAnimation` retorna `false` somente quando ambas as stacks são do `RESISTOR_SHIELD` (teste de identidade), caso contrário `true`, independentemente do booleano passado nesse override. `initializeClient` encaminha `CommonProxy.getISTERProperties` ao consumidor de extensões visuais.

## Pulso ofensivo — `onUseTick`, 276 instruções

Fluxo de bytecode próprio, **sem garantia de que as solicitações sejam aceitas pela engine**:

1. Super `ShieldItem.onUseTick` @6; `elapsed = getUseDuration(stack,null) - remainingTicks` @9–18. `scarlet = isScarlet(stack)` @20–24; `strong = (elapsed >= 10 && elapsed <= 12)` @26–45; `heavySlamLevel = ACCompat.enchantLevel(stack, HEAVY_SLAM)` @47–54; `radius = 5.0F` @56.
2. Ramo `Level.isClientSide` @60–64: grava `UseTime=elapsed` @70; toca `RESITOR_SHIELD_SLAM` quando `elapsed == 10` @73–92. Para `elapsed >= 10 && elapsed % 5 == 0`, solicita som local/proxy e partículas polarizadas `SCARLET_SHIELD_LIGHTNING` ou `AZURE_SHIELD_LIGHTNING` (5 + `random.nextInt(5)` iterações), @95–362. As posições aleatórias e direção de renderização não constituem alvo de dano.
3. **Depois** da saída do ramo cliente @365, se `elapsed >= 10 && elapsed % 5 == 0`, obtém `LivingEntity` em `caster.getBoundingBox().inflate(5.0, 1.0, 5.0)` @379–403. Itera na lista sem limite próprio observado @406–581. Descarta entidades aliadas ao caster (`caster.isAlliedTo(target)`), o próprio caster e distâncias `target.distanceTo(caster)>5.0` @435–462. O filtro de distância é tridimensional; a caixa é expandida separadamente em X/Z/Y.
4. Em cada alvo aceito solicita `target.hurt(target.damageSources().mobAttack(caster), amount)` @465–495, com **`amount = strong ? (6 + 3*heavySlamLevel) : 2`**. O resultado booleano de `hurt` é descartado com `pop @495`. Não presumir dano final aplicado, dano PvP aprovado, bypass de imunidades ou rank/atributo em outro provider.
5. Independentemente do retorno de `hurt`, solicita `ACCompat.knockback(target, strength, dx, dz)`: `strength = strong ? 0.5 : 0.2`, `scarlet` usa `dx=target.x-caster.x` e `dz=target.z-caster.z` @501–537; `azure` usa **`dx=caster.x-caster.x=0`**, `dz=caster.z-target.z` @543–578. Essa diferença está nos operandos do JAR; efeito final e eventual bug exigem auditar `ACCompat.knockback` e QA.
6. Somente no `elapsed==10 && !level.isClientSide` @584–595 solicita `ACCompat.hurtAndBreakUsedHand(stack,1,caster)` @598–601. Este é débito solicitado de **1 ponto de durabilidade nesse instante**, não cobrança garantida nem cooldown.

**Observação de boundary crítica:** há guarda client-only para animação @60–64, mas **não há guarda server-only própria envolvendo o loop de `hurt`/`knockback` @365–581**; esse loop é alcançável pelo fluxo de ambos os lados. Não concluir, sem verificar engine/`ACCompat`/rede, que duas aplicações reais aconteçam. Para perks, não duplicar a chamada de `onUseTick` ou o loop de dano. Testar mundo dedicado, integridade de PvP, claims, event cancellation e causalidade de hit/durabilidade.

## Métodos próprios — fingerprints de instruções do relatório

| Método | Instruções | SHA-256 normalizado |
|---|---:|---|
| `<init>` | 12 | `b998827c74b378bf4ceab37241709c2f1bca3defee255f9d8099150db2c99d16` |
| `acExtraRepairMaterials` | 15 | `b1c165d8b02b3531e59afa61434eb1da01506822154ef3a4d9db9cc34f60812e` |
| `acInventoryTick` | 79 | `3cec5ec860390c581f2795f6c2f128c2c1507593934eb6b40db608bf6d182b20` |
| `appendHoverText` | 8 | `f1d51a225066a01d40e4007c660f90f54ee87aca37278015cb3b8cdfc2cf79e5` |
| `getEnchantmentValue` | 2 | `d943c5fe0bd38038ce70963c73b8759ba3d76c8c00d31c1a2141268dc4e0ee0a` |
| `getLerpedSwitchTime` | 29 | `2b596a6e1fd948380b3afa27536d03e15147b74b1ce2626edac364e1dd4680bd` |
| `getLerpedUseTime` | 29 | `3bf9be409b9b6d5cb4414c966a0cd27b7b5f5bb89650c7edf4ccaee672d91845` |
| `getSwitchTime` | 11 | `dd7de29ec565120099306b77dee7d87f2ddb4fb9d7951584ffceb803cfb3e5e2` |
| `getUseTime` | 11 | `fe8cd54d443d0f8217dfcab40bcfafd4d1e89b31203423840e1301b11b1ec087` |
| `initializeClient` | 6 | `3a6c2d33865c1d1707dcbd93e1f9e0bd3bd706c9817ddb988b4e0589ebb14cf4` |
| `isEnchantable` | 8 | `9cd84b0255be269f2bf50fce0095c14fa5d484831fd35063e71f4c9814aa6b4f` |
| `isScarlet` | 11 | `0120856259e8808d6984bbf32e027806ce18b55f48b968a4d8cc0cd31466f25a` |
| `isValidRepairItem` | 13 | `56ef4089abe5ca807759ea066eaab7be291dd520d357c2fab2a6de913f3fa597` |
| `onUseTick` | 276 | `91abe64167b12b90bbdb14a3792f2c25a273444303ca928df0ae378d5ed7f117` |
| `releaseUsing` | 10 | `060b90ea58c4220856ab82b2a6ed4cb7e6948aba77ef9ed69a1c7f756835355b` |
| `setPolarity` | 11 | `99cf6b8ca3b1854f35ccacb7a6134c2334a8ba796748e389dcbff0648c6f3106` |
| `setSwitchTime` | 16 | `8230f61088a45eebc80b500e579737bc42824385ecb633ee3799fc8fb5284d5a` |
| `setUseTime` | 16 | `14cdd83df5a99a5b39d424d15ab530141740c1e17afe79b2b7edc7938cc27701` |
| `shouldCauseReequipAnimation` | 16 | `3e00d35cc9b87936c41e5bc8d92b876c67d1df83ae7e0bef4a637ec674f56c60` |
| `use` | 26 | `ecdff4ab3bec4f7f57b488a358d7dc40ff72e2570625bbb81496b1929a060c8a` |

Além dos hashes normalizados acima, `onUseTick` tem Code SHA-256 `193bebed4088805aed9cc0da12b8daca41f0889787505c7780c28529387aa3b8` e tamanho de `Code` 605 bytes; `use` Code SHA-256 `f04b9b493f488d61a9d71121b1d994a87d1430dae8727ab5562d633d0fee8f81`. Conferir também o método de fábrica `ACItemRegistry.lambda$static$20` no manifesto parcial: Code SHA-256 `6be6cb4de8570768436590ecdd12cfd11e44f1c9b8e76b7eb58a324d6b4d63ce`, instruções SHA `d5746049d40ac0bafdb3b78aac9a4134cba1f81838a06bb5866b30c3143402bc`.

## Consumidores tipados e recursos — limites

| Owner | Sites tipados | Corpo(s) exposto(s) |
|---|---:|---|
| `client/event/ClientEvents` | 6 | `onPoseHand`; usa `getLerpedUseTime` para pose |
| `client/render/item/ACItemstackRenderer` | 2 | `renderByItem`; apresentação/modelo |
| `client/sound/ResistorShieldSound` | 3 | `isValidItem` e `tickVolume`; verifica classe, polaridade e interpolação |
| `server/item/ACItemRegistry` | 2 | `lambda$static$20`; fábrica |
| `server/item/ResistorShieldItem` | 14 | autorreferências em cinco corpos, não contar como consumidor externo |

Todos os owners acima possuem prefixo `com/github/alexmodguy/alexscaves/`. Censo busca sites de tipos registrados no publisher; sem prova de completude para consumers implícitos. `ClientEvents`, renderer e som são apresentação nativa, **não hooks mutadores**.

Recursos filename-matched (conteúdo e semântica **NÃO AUDITADOS**, apenas hash e tamanho):
- `assets/alexscaves/models/item/resistor_shield.json` — 1.275 bytes; SHA `90e6f55395b5da2c68cb0d858aa9b8a773e46a7cd3027500f5249d0f675acb47`.
- `data/alexscaves/advancement/alexscaves/resistor_shield.json` — 735 bytes; SHA `0a4dae9d1e074b98ae2127ea855c9684cd9e18d56fbd8c2f4c7049924508936f`.
- `data/alexscaves/recipe/resistor_shield.json` — 433 bytes; SHA `2d2c648cc1db20b024ba3643c4e3c281b270039299d32ea8a3e9b8e8262f77af`.
- `data/alexscaves/tags/item/enchantable/resistor_shield.json` — 55 bytes; SHA `2b5d57ffc709293f994b472c07cd44ed34647efec41106b819621c060366f3e0`.

## Certificação, integração e próxima prova

**Comprovado pelo bytecode publisher:** valores imediatos, guards, invocações, parâmetros declarados e grafos enumerados acima. **NÃO VERIFICADO:** resultado de `ACCompat.hurt/knockback/hurtAndBreakUsedHand` e `useConsume`, defesa herdada do `ShieldItem`, persistência física de componentes, comportamento durante reload/respawn, custo aceito, resultado de recursos JSON, callbacks por mixin/eventos, efeitos do lado cliente em servidor, multiplayer e comparação do JAR instalado. Nenhum override seguro por jogador/rank/atributo/Mastery foi identificado.

Reproduzir a descoberta e o checker com os scripts `docs/qa/alexscaves_1010_resistor_shield_discovery.py` e `docs/qa/alexscaves_1010_resistor_shield_discovery_checks.py`, sobre JAR SHA-exato e com teste negativo. Validar a CI inteira da **última HEAD**, além de auditar as bibliotecas/consumidores e executar QA física quando aplicável. O relatório não substitui essas etapas. Até então, **⚠️ parcial / NO_MUTATION / fail-closed**.