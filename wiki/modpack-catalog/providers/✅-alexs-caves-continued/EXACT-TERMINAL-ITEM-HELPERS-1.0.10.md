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
