# Alex's Caves Continued 1.0.10 — reconciliação de fronteiras distribuídas

Base c2e9bcb6a395b1c85ef19bcd1763b349c22e439e; modlist sibling 18144e8318978b8904b584b80b4ddd630f22f8f0, entrada 019, NeoForge 21.1.250, Java 21. Publisher SHA-256 36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c. Não é nova extração física: reutiliza resultados binários rastreáveis já integrados e confronta hierarquias/caminhos sem importar comportamento de classes irmãs.

| Prova | Execução | SHA-256 do relatório |
|---|---|---|
| [Downstream 21.1.250](EXACT-FOUR-ITEMS-DOWNSTREAM-21.1.250.md) | [45471957912](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45471957912) | 5a5c4a201604224306a2b5cded87cb82523bce8cf0e82aaf998954125afe0c65 |
| [Impacto 21.1.250](EXACT-INK-BOMB-IMPACT-21.1.250.md) | [45535313661](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45535313661) | 642a25a85314108c189a2fc717e6e6678d122c2603e7fb4c5db6effacc135691 |
| [Defaults](EXACT-ITEM-ENTITY-DEFAULTS-21.1.250.md) | [45517751804](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45517751804) | 448111136166191329351f06376741dc040bb6a6ee9f8f624ae8b915d5fae944 |
| [Consumo/status](EXACT-FOOD-STATUS-SETTLEMENT-21.1.250.md) | [45479066017](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45479066017) | ac206f62678acd71876df7df3321eb16ee51832a15325515bf23db71bc566464 |

Projeções de máquinas: [PR 1236](https://github.com/Gustavaopere/Black-Arcana/pull/1236), job 139831911308, relatório SHA-256 137a0235d3e00a4fbbe947d6da01ffb50572f57a8a43f62da63847aa81034ff9. Receitas e campos retomados das projeções já realizadas e [registry](systems/item-registry.md). Crucible: [contrato individual](actions/conversion-crucible-biome-conversion.md).

## Fichas reconciliadas

- [chocolate-ice-cream-scoop](items/chocolate-ice-cream-scoop.md)
- [sweetberry-ice-cream-scoop](items/sweetberry-ice-cream-scoop.md)
- [vanilla-ice-cream-scoop](items/vanilla-ice-cream-scoop.md)
- [cinder-brick](items/cinder-brick.md)
- [guano](items/guano.md)
- [depth-charge](items/depth-charge.md)
- [seeking-arrow](items/seeking-arrow.md)
- [purple-soda-bottle-rocket](items/purple-soda-bottle-rocket.md)
- [quarry-smasher](items/quarry-smasher.md)
- [submarine](items/submarine.md)
- [green-soylent](items/green-soylent.md)
- [slam](items/slam.md)
- [spelunkie](items/spelunkie.md)
- [radiant-essence](items/radiant-essence.md)
- [licowitch-radiant-essence](items/licowitch-radiant-essence.md)

## Limites e próximo gate

- ThrowableProjectile: não confundir algoritmo herdado com override de DepthCharge; AbstractArrow/FireworkRocketEntity não herdam esse tick.
- Scoops: falta implementação cureWithMilk, parâmetros EntityType e autoridade real.
- Quarry/Submarine: corpos tick de 580/733 instruções ainda excederam projeção anterior; não declarar completos.
- Consumo: finish callback precede evento Finish; custo/status não constituem transação atômica comprovada.
- Essências: vínculo com ação já catalogada, zero novas raízes; recursos adicionais exigem atribuição por ID.
- Índices e ledger não mudam: 15 fichas parciais aprofundadas, zero certificados novos, zero hook, zero runtime, zero QA física.

Nenhuma implementação de terceiro copiada; somente semântica, localizadores e fronteiras.
