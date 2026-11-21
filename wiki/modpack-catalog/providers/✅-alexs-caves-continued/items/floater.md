# Floater — `alexscaves:floater`

**Catálogo:** ⚠️ ficha individual detectada, contrato estático `PARTIAL`; hook `NOT_VERIFIED`, QA física `NOT_TESTED`, `NO_MUTATION`, provider `OPEN`. É um item utilitário de transporte/flutuação; não cria uma segunda raiz semântica de magia.

## 1. Identidade e fonte

Provider Alex's Caves Continued, mod ID `alexscaves`, versão publisher **1.0.10**, Minecraft 1.21.1/NeoForge/Java 21. Modlist identifica `alexscaves-1.0.10-neoforge+1.21.1.jar`. Artefato publisher 75.279.314 bytes, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`. Não há novo snapshot do cliente instalado. `ACItemRegistry.FLOATER` → `lambda$static$103` (Code SHA-256 `a9bfbdf9d227839dbb872f120c68e9df77c8723eed98d8e146c790aa3f395613`) → `FloaterItem()`. Classfile SHA-256 `30d98e6b5db3fc977c8e8e66adb82576c934d5a7cdc423bbd258f1e7a3224a05`; construtor usa `Item.Properties()` sem alterações locais.

## 2. Descrição, uso e targeting

Descrição funcional derivada do método `FloaterItem.use(Level,Player,InteractionHand)`: oferece uma entidade flutuadora no ponto atual do jogador quando ele está **na água ou em bolha**, exceto se estiver agachado. Seu `use` (Code SHA-256 `4a1d004b4ebb4270900189a914b01ee0a8ad927ec18a4848d6129668baecef46`) solicita `ACCompat.createEntity(ACEntityRegistry.FLOATER,level)`, `entity.copyPosition(player)` e, em servidor, `Level.addFreshEntity`. Então solicita `player.getRootVehicle().startRiding(floater)` e, se `!player.isCreative()`, `stack.shrink(1)`; termina em `ACCompat.useSidedSuccess`. Os retornos de spawn e de `startRiding` são **descartados**. Nada no corpo verifica proteção de claims, colisão/aceitação, autorização adicional ou restaura a stack em caso de falha. Esse é o limite causal do item; não assumir que colocar e montar tiveram sucesso.

## 3. Efeito e parâmetros da entidade

`FloaterEntity` (SHA-256 `b675ebd726fc8045610a48fbd310abbd5f6762fe68e1158badd8026e47ac2c30`) estende `Entity` e declara `timeOutOfWater:int`. `tick()` (Code SHA-256 `4189b44505454cce8089021252d762b641ad024925a2b07a3aebe1db4dc38beb`) aplica `ΔY=-0.04` por tick se gravidade permitida, soma `+0.2` a Y se `wasEyeInWater`, desloca via `MoverType.SELF`, depois multiplica velocidade por `0.9`. Fora da água, no servidor, incrementa `timeOutOfWater` e solicita descarte após o limiar do código. O contador **não é resetado** no ramo aquático; portanto tempo seco acumulado, e não necessariamente tempo consecutivo. Solicita evento de entidade 3 e partículas no cliente após descartar. Não inferir aceleração final, velocidade terminal, floating height, passenger count nem survival em correnteza sem engine/QA.

`interact(Player,Hand)` solicita montar no servidor: `CONSUME` se `startRiding` retorna true, `PASS` caso contrário; cliente retorna `SUCCESS`. `positionRider` para passageiro vivo de mesmo veículo, quando chunks necessários estão carregados, aplica `Y+0.699999988079071+ACPlatform.myRidingOffset` e `fallDistance=0`. `causeFallDamage` e `isAttackable` devolvem false. `getPickResult` usa o próprio item. `shouldBeSaved` retorna `!isRemoved`, porém `addAdditionalSaveData` e `readAdditionalSaveData` são vazios, **sem persistência local de `timeOutOfWater`**. Testar save/reload do veículo e passageiro.

## 4. Aquisição, custos e parâmetros N/A

Receita publisher `data/alexscaves/recipe/floater.json` (SHA-256 `379259801117cfd1aba2045bec78b19d55c913f47d33b1e925b4e241f0c0ce51`): `minecraft:crafting_shaped`, padrão `" B "/"BBB"/"PPP"` com **4 alexscaves:bioluminesscence** e **3 alexscaves:ping_pong_sponge** por item. Advancement `floater` usa `minecraft:inventory_changed`. Custo por ativação: solicita redução de uma stack para jogador não criativo; não há mana, duração de cast, cooldown, dano ofensivo, alvo remoto, AOE ou projétil **no corpo local** — `N/A` nesse escopo, efeitos de outros mods não verificados.

## 5. Integração, evidência e pendências

[Relatório causal](../EXACT-FLOATER-FROSTMINT-1.0.10.md) · [manifesto](../EXACT-FLOATER-FROSTMINT-DISCOVERY-1.0.10.json) · [probe SHA-exato](../../../../../docs/qa/alexscaves_1010_floater_frostmint_discovery.py). Candidatos conceituais: custos/consumo, flutuação, movimentação, proteção de passageiros e vida útil. **Sem hook mutador seguro**: `NO_MUTATION`, não solicitar segundo spawn nem reembolsar gasto por conta própria. Pendentes: registry de dimensões/capacidade, contextos cliente/servidor, aceite de spawn/montagem, extração/retorno ao inventário, save/reload, config/recipe overrides, claims, multiplayer e compatibilidade.
