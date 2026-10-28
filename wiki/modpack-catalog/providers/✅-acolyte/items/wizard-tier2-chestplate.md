# wizard_tier2_chestplate — roupa de equipamento

**Release auditada:** Acolyte 1.0.3, publisher file `8098233`; SHA-256 `73fe745bbb0016fbc00af9ba14c0ecfe0a1d8a7d72a7892557739182b3486256`.
**Estado:** documentação de contrato binário; mutação `NOT_VERIFIED`; pack físico `NOT_TESTED`; igualdade do hash instalado não comprovada; certificações **0**.

Fonte: [contratos e proveniência](../BINARY-CONTRACTS-1.0.3.md) e [manifesto](../ARTIFACT-CATALOG-MANIFEST-1.0.3.json). Referências PC indicam offsets de método no publisher, não código reproduzido. O conflito publisher ARR / metadado TOML MIT permanece aberto; só fatos de interoperabilidade são retidos.

## Identidade e contrato

- Registry exato: `acolyte:wizard_tier2_chestplate`; classe `net.raptorzizi.acolyte.item.armor.WizardArmorItem`; superclass Iron's `ExtendedArmorItem`.
- Slot passado ao host: **CHESTPLATE** (peitoral). Tier **2** identifica a família visual, sem multiplicador de atributo local por tier.
- Propriedades: `ItemPropertiesHelper.hidden(1)`, raridade **COMMON**. Não inferir durabilidade/dano ou inventário criativo sem conferir o helper do host instalado.
- Material `acolyte:cosmetic`: defesa de todos os slots **0**, enchantability **15**, toughness **0**, knockback resistance **0**, som de couro; ingrediente de reparo é a tag NeoForge `LEATHERS`.
- O construtor entrega um array **vazio** de `AttributeContainer` a `ExtendedArmorItem`: não há bônus customizado de mana, escola, ataque, resistência ou velocidade nesta classe. Os 15 registros de roupa possuem esse mesmo comportamento; a ficha mantém este ID individual.
- Não há trigger de cast, ataque ativo, custo, cooldown, targeting/owner ou persistência customizada na classe. Equipamento, atributos derivados e stack pertencem ao contrato herdado; não usar o nome/tier como perk implícito.

## Apresentação e aquisição

`modelName=wizard_armor`, `textureName=wizard_armor_tier2`; `supplyRenderer` fornece `GenericCustomArmorRenderer` do host com `CosmeticModel`. Referência de animação do host: `irons_spellbooks:animations/wizard_armor_animation.json`. Nenhum asset é copiado. Não existe receita com este ID no publisher auditado; equipamento de mobs e acesso por comandos não demonstram uma aquisição normal pelo jogador.

## Evidência reproduzível

- `ModItemsRegistry.<clinit>` PC 302–319, `lambda$static$18` PC 0–24: ID, slot, helper, raridade e seleção visual.
- `WizardArmorItem.<init>` PC 0–24: material e array vazio; `supplyRenderer` PC 0–22: renderer.
- `ModArmorMaterialRegistry.<clinit>` PC 11–38; `makeArmorMap` PC 0–65; `lambda$static$1` PC 0–6: propriedades/reparo.
- `CosmeticModel.getAnimationResource(ExtendedArmorItem)` PC 0–7.

## Boundary de integração e validação

Acolyte possui o item e sua política local; Iron's possui atributos, efeitos, recipientes e magias do host; Minecraft/NeoForge possui inventário, equipamento e liquidação vanilla. Não há hook mutador homologado. Nomes de métodos/registries são candidatos de observação, sem garantia de API estável. Perks não devem alterar mana, repetir consumo, aplicar atributos em outro slot ou liquidar recompensas por esta ficha.

`NOT_TESTED`: conferir o hash instalado, uso/equipamento no servidor dedicado, criativo/sobrevivência, troca de slot, relog, morte e multiplayer; confirmar uma única aplicação e um único consumo no pack real. Ausência de cooldown explícito na classe não certifica ausência de cooldown herdado/do host.
