# Downstream de projéteis e máquinas — 1.0.10

**STATIC_DISCOVERY_ONLY / NO_MUTATION / NOT_CERTIFIED / NOT_TESTED.** Base main `8341321f98beafbc0b00e3f17bc16e0e6208f18e` após #1233 integrada com 78/78 workflows. Modlist sibling #19, publisher `alexscaves-1.0.10-neoforge+1.21.1.jar`, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`, 75.279.314 bytes. Nova coleta pendente. Não inventar os parâmetros a partir dos nomes de entidade.

## Objetos existentes e owners downstream

| Owner referenciado em ficha/factory exata | Fichas a aprofundar |
|---|---|
| CinderBrickEntity | [Cinder Brick](items/cinder-brick.md) |
| DepthChargeEntity | [Depth Charge](items/depth-charge.md) |
| GuanoEntity | [Guano](items/guano.md) |
| ThrownIceCreamScoopEntity | [Chocolate](items/chocolate-ice-cream-scoop.md), [Sweetberry](items/sweetberry-ice-cream-scoop.md), [Vanilla](items/vanilla-ice-cream-scoop.md) |
| LimestoneSpearEntity | [Limestone Spear](equipment/limestone-spear.md) |
| SeekingArrowEntity | [Seeking Arrow](items/seeking-arrow.md) |
| SodaBottleRocketEntity | [Purple Soda Bottle Rocket](items/purple-soda-bottle-rocket.md) |
| QuarrySmasherEntity | [Quarry Smasher](items/quarry-smasher.md) |
| SubmarineEntity | [Submarine](items/submarine.md) |

[Registro de itens](systems/item-registry.md), [helpers](EXACT-TERMINAL-ITEM-HELPERS-1.0.10.md), [itens finais](EXACT-LATE-CONCRETE-ITEMS-1.0.10.md), [Quarry](EXACT-QUARRY-RADIANT-FOOD-1.0.10.md) sustentam ligação inicial. Onze fichas, nove owners; sabores de scoop compartilham entidade sem presumir efeitos idênticos.

## Recorte da investigação

[Probe](../../../../docs/qa/alexscaves_1010_projectile_machine_downstream_probe.py) verifica identidade/roster publisher e exige owners únicos pelo basename comprovado, determina hierarquia nativa, projeta todos os corpos próprios e ancestrais nativos (registra explicitamente métodos fora do orçamento, não certifica lacunas), referências tipadas e janelas de ACEntityRegistry. Campos candidatos do registry são filtros de busca, não confirmação de registry IDs. A análise de recursos por filename é limitada. [Workflow](../../../../.github/workflows/alexscaves-1010-projectile-machine-downstream.yml) executa dois replays por grupo.

Projéteis: dano e DamageSource, targeting, owner, direção, homing, colisão, velocidade, física, hitbox, AOE, efeitos, tags, pickups e descarte, NBT, side e eventos, integração com perks e engine. Máquinas: movimento, inventário, estado, energia, acesso/controle, oxigênio/assentos, quebra de blocos, claims, persistence e callbacks; não presumir autorização de mineração nem custo liquidado. Nenhum novo certificado/raiz/índice nesta proposta, sem alteração de runtime. O ledger da #1235 é independente e não será tocado aqui.
