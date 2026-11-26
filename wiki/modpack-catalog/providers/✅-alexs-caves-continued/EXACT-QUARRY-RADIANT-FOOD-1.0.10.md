# Quarry Smasher, Radiant Essence e alimentos antirradiação — descoberta 1.0.10

**DISCOVERY_ONLY / NO_MUTATION / NOT_CERTIFIED / NOT_TESTED.** Base canônica `2f4d5c0b296039a7afa701e8465d89c4b8394e78`. Modlist sibling #19, publisher `alexscaves-1.0.10-neoforge+1.21.1.jar`, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c32e9f2e95bffae0e7c`, 75.279.314 bytes. Nova coleta pendente; sem novo dump físico.

## Reconciliação alfabética anterior

PrimordialArmorItem possui três fichas estáticas certificadas na main: [Helmet](items/primordial-helmet.md), [Tunic](items/primordial-tunic.md), [Pants](items/primordial-pants.md). Factories $42/$43/$44, slots HEAD/CHEST/LEGS. Classfile SHA-256 `8833c162d1507aba795b1ff809f5a6f6ddb846da308d809795cf80e69be5d09e`; quatro métodos próprios, dois consumidores relevantes, PlayerMixin.ac_eat e DinosaurChopBlock.eat. Contador por identidade e slot. [Contrato existente](EXACT-PRIMORDIAL-ARMOR-THREE-PIECES-1.0.10.md). Não duplicar fichas, certificados, hooks, efeitos, raízes ou runtime. Inventário anterior 55/81 classes com disposição documentada; após esta reconciliação, 56/81 no recorte proposto, não certificação de classes nem universo semântico integral.

## Próximas três classes e seis factories

| ID | Classe | Factory | Code SHA-256 |
|---|---|---|---|
| `alexscaves:green_soylent` | `RadiationRemovingFoodItem` | `lambda$static$66` | `aaf8577259d92e748676d4b3a21900a43c36ee085c844bc9c7f8ddf9185d7ef2` |
| `alexscaves:licowitch_radiant_essence` | `RadiantEssenceItem` | `lambda$static$182` | `4695bc463cfdbffb43121cd3c2adb63f7dedb49c54784503528a9123ef96a062` |
| `alexscaves:quarry_smasher` | `QuarrySmasherItem` | `lambda$static$16` | `8eedb42718de2b1062ad616449d83c8b6577741845712c901bd1fbb73a7c70f6` |
| `alexscaves:radiant_essence` | `RadiantEssenceItem` | `lambda$static$181` | `4695bc463cfdbffb43121cd3c2adb63f7dedb49c54784503528a9123ef96a062` |
| `alexscaves:slam` | `RadiationRemovingFoodItem` | `lambda$static$65` | `a2ed034a1d56a99a005cfae5480389ac42ac12aaff2b62885fa0f41b1217211e` |
| `alexscaves:spelunkie` | `RadiationRemovingFoodItem` | `lambda$static$64` | `1ee7980eccd745100779b6563c43ddf9cb8c0f8184a61b2d52b8c7bee1f6a338` |

Fonte: [registro](systems/item-registry.md). Factories de Radiant Essence e Licowitch Radiant Essence compartilham hash Code, mas são identidades registradas distintas; isso não prova equivalência de todos os consumidores ou loot.

## Eixos a fechar

- Quarry Smasher: ativação, spawn/entidade ou bloco, posição, targeting, colisão, custo e autoridade de alterações de mundo, proteção de claims, lifecycle/owner, sem atribuição antecipada de dano ou Mastery.
- Radiant Essence e Licowitch Radiant Essence: distinguir callbacks e consumidores por ID, gates, efeitos, aquisição, custos e estado; não deduzir cura, luz ou radiação do nome.
- RadiationRemovingFoodItem: [ACFoods](systems/foods.md) comprova SLAM N=4, m=0.5, meat, DAMAGE_BOOST 400 ticks p=1; SPELUNKIE N=2, m=0.1, fast, sem efeito declarado pelo builder. Green Soylent deve ter identidade e perfil conferidos na factory e downstream; não inferir seu valor a partir dos demais. Investigar o caminho de redução/remoção de radiação, efeitos, amplifier, ordem de consumo, autoridade, recipiente, persistência e falha.

## Reprodução proposta

[Auditor](../../../../docs/qa/alexscaves_1010_quarry_radiant_food_probe.py) verifica hash/tamanho/roster do JAR, seis factories Code SHA-exatas e seus targets, corpos próprios, referências tipadas e recursos JSON delimitados por nome. [Workflow](../../../../.github/workflows/alexscaves-1010-quarry-radiant-food.yml) exige dois relatórios idênticos. O limite de recursos por filename não prova todos os JSONs transitivos; consumidores tipados não excluem reflexão ou transforms. Sem novas fichas/certificados, índices, hooks, Stage ou QA física nesta proposta. Próximo após coleta: RadioactiveBlockItem, RadioactiveItem e RadioactiveOnDestroyedBlockItem. NO_MUTATION / fail-closed.
