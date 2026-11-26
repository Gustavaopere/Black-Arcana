# Thrown projectile and terminal item helpers — descoberta 1.0.10

**STATIC_DISCOVERY_ONLY / NO_MUTATION / NOT_CERTIFIED / NOT_TESTED.** Base main `9eeb5db432e5c9c552e8866214d34ec9fd20da73`, modlist sibling #19, publisher `alexscaves-1.0.10-neoforge+1.21.1.jar`, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`, 75.279.314 bytes. Novo replay pendente. Não há dump da instalação nem confirmação de runtime.

## Roster de classes físicas selecionadas

- `server/item/SpearItem`
- `server/item/ThrownProjectileItem`
- `server/item/UpdatesStackTags`
- `server/item/dispenser/FluidContainerDispenseItemBehavior`

## Factories diretas previamente seladas

| ID | Owner | Factory | Code SHA-256 |
|---|---|---|---|
| `alexscaves:chocolate_ice_cream_scoop` | `ThrownProjectileItem` | `ACItemRegistry.lambda$static$168` | `4c62609bf9f25265d90a3f88bffd4493e6362f978abda2161d7f97ea9ec9ac28` |
| `alexscaves:cinder_brick` | `ThrownProjectileItem` | `ACItemRegistry.lambda$static$63` | `6170bbfd08b2836ed9e776a6faf4682e4f9708646716c0160e13bcc32986c125` |
| `alexscaves:depth_charge` | `ThrownProjectileItem` | `ACItemRegistry.lambda$static$113` | `5b5396ac73dc271445003cefeda4e6066978b2df1997228de0b035949d3a39f8` |
| `alexscaves:guano` | `ThrownProjectileItem` | `ACItemRegistry.lambda$static$121` | `279cb235c5eba0d207bae281636c396354915b06416eb9bec09335bdb108cd6d` |
| `alexscaves:sweetberry_ice_cream_scoop` | `ThrownProjectileItem` | `ACItemRegistry.lambda$static$170` | `b8243502eff7adfa97638db4839e654631ff1cf86a89b85cbba221b3a5be8052` |
| `alexscaves:vanilla_ice_cream_scoop` | `ThrownProjectileItem` | `ACItemRegistry.lambda$static$166` | `b1207d3c3493cba9f22a6a9f795d105ae5176c5ba075726e0b9f4280c72d1609` |

[Registro](systems/item-registry.md). Owners sem factory direta nessa tabela são helpers/abstrações ou consumidores que requerem reconciliação separada. Não presumir que um owner equivale a um novo objeto ou raiz semântica. Itens de arremesso existentes podem já ter fichas; nenhuma duplicação automática.

## Recorte e validação

[Probe](../../../../docs/qa/alexscaves_1010_terminal_item_helpers_probe.py) fixa o artefato e roster de 1555 classfiles, Code das factories, todos os corpos próprios das classes selecionadas, censo tipado e janelas de consumidores, JSONs por filename. [Workflow](../../../../.github/workflows/alexscaves-1010-terminal-item-helpers.yml) exige dois replays idênticos. O relatório distingue owners abstratos/interfaces e helpers; consumidores e recursos indiretos podem escapar do recorte, sem fechar universo. Não copia implementação de terceiros.

SpearItem: base herdada, escala, construção de projéteis e consumidores já mapeados; ThrownProjectileItem: seis factories, suppliers, lançamento, uso, custos e retornos; UpdatesStackTags: interface, callsites e persistência; FluidContainerDispenseItemBehavior: dispenser, débito, fallback e efeitos de mundo. Reconciliar fichas existentes antes de criar quaisquer outras.

Sem novas fichas ou certificados, sem alteração dos índices compartilhados e sem Stage promotion nesta proposta; integração somente após CI e consolidação com a PR #1233.

## Resultado observado e disposições técnicas

[Run 45794089646/job 139820166475](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45794089646/job/139820166475), HEAD `27c5bbc7780abbb2efe9bf2c4db615be5d0e7b3c`, 23 declarações (17 próprias e 6 factories), 16 owners tipados, 134 JSON, 8 checks e dois replays 439138 bytes SHA-256 `7d70e29eb4bd2df5df5fe73720d1bd6213b61e7a950b43494f3efd416830e66f`. Seis fichas parciais de arremesso, sem novos certificados. SpearItem base: construtor ADD_VALUE dano D e velocidade −3D, MAINHAND, SPEAR 72000 ticks, use gate damageable/damageValue<maxDamage−1, power min(1,(t²+2t)/3), t=elapsed/20F, desgaste 1 ataque/2 mineração não zero. [Limestone](equipment/limestone-spear.md) atualizado sem promover, [Extinction](equipment/extinction-spear.md) e [Frostmint](equipment/frostmint-spear.md) preservados. UpdatesStackTags interface class SHA `1ba03e1d244a0a6ad49a888cb406bf518858c52988b4210db204c0bbd1e6e0ad`, único updateTagFromServer(Entity,ItemStack,CompoundTag)V Code SHA `267fbf3a7bc6d8051ff1a014921b5df941f947a2165ac0e63b211a55f2d14144`: ACCompat.setTag(stack,tag), entity não lida, não autentica rede; consumers UpdateItemTagMessage e owners concretos. Não autoriza mutação. FluidContainerDispenseItemBehavior class SHA `b34847a98cdcd38c1ac2b5b3a7dbaa3f95fb76d4646086991a63ee794da850fb`, execute Code SHA `0c5d847b5a05432239667abb0c4a9a8147c41be4dd2bf55f22d64004bd96a252`: cast DispensibleContainerItem, bloco em frente do dispenser, emptyContents @50, se true checkExtraContent @68 e retorna new bucket @80; false DefaultDispenseItemBehavior.dispense @90. Sem shrink explícito, engine/callbacks determinam débito e alterações de mundo. Sem hook. Helpers não são novos objetos de magia; documentados no dossiê e vinculados às fichas.

- [Chocolate Ice Cream Scoop](items/chocolate-ice-cream-scoop.md)
- [Cinder Brick](items/cinder-brick.md)
- [Depth Charge](items/depth-charge.md)
- [Guano](items/guano.md)
- [Sweetberry Ice Cream Scoop](items/sweetberry-ice-cream-scoop.md)
- [Vanilla Ice Cream Scoop](items/vanilla-ice-cream-scoop.md)
