# Demon Horns 0 — equipamento de cabeça

**Release auditada:** Acolyte 1.0.3, publisher file `8098233`; SHA-256 `73fe745bbb0016fbc00af9ba14c0ecfe0a1d8a7d72a7892557739182b3486256`.
**Estado:** documentação de contrato binário; mutação `NOT_VERIFIED`; pack físico `NOT_TESTED`; igualdade do hash instalado não comprovada; certificações **0**.

Fonte: [contratos e proveniência](../BINARY-CONTRACTS-1.0.3.md) e [manifesto](../ARTIFACT-CATALOG-MANIFEST-1.0.3.json). Referências PC indicam offsets de método no publisher, não código reproduzido. O conflito publisher ARR / metadado TOML MIT permanece aberto; só fatos de interoperabilidade são retidos.

## Identidade e equipamento

- Registry exato: `acolyte:demon_horns_0`; classe `DemonHornsItem extends ExtendedArmorItem` de Iron's.
- Tipo recebido pelo construtor: **HELMET** (slot de cabeça). Propriedades: `ItemPropertiesHelper.hidden(1)` e raridade **COMMON**; o efeito exato desse helper requer o host instalado. Não há ativação por clique, cast ou cooldown customizado nesta classe.
- Material `acolyte:cosmetic`: defesa por slot **0**, toughness **0**, knockback resistance **0**, enchantability **15**, som de equipar couro; reparo usa a tag NeoForge `LEATHERS`. São parâmetros do material, não evidência de redução de dano.
- O construtor entrega ao host **MAX_MANA +125**, operação **ADD_VALUE**, e **MANA_REGEN +0,35**, operação **ADD_MULTIPLIED_BASE**. A segunda é multiplicação da base, não +0,35 mana/tick; cálculo final e aplicação ao slot pertencem a `ExtendedArmorItem`/atributos do host. Não somar quatro variantes simultaneamente nem presumir integração com slot cosmético/Curios.
- As quatro formas possuem o mesmo contrato de atributo; identificadores e recursos visuais são distintos. Sem owner, alvo externo, gasto de mana, ticking ou persistência customizada no item.

## Aquisição e apresentação

O recurso `data/acolyte/recipe/demon_horns.json` é crafting shaped de duas Demon Horns adjacentes horizontalmente, resultado uma unidade desta forma. Não há receita equivalente das formas 1–3 no publisher auditado.

Modelo/texture usam a identidade `demon_horns_0`; `supplyRenderer` fornece o renderer genérico do host com `CosmeticModel`. A animação é referenciada no host `irons_spellbooks:animations/wizard_armor_animation.json`. Os assets não foram copiados.

## Evidência reproduzível

- `ModItemsRegistry.<clinit>` PC 40–53; `lambda$static$2` PC 0–24: ID, HELMET e argumentos do renderer.
- `DemonHornsItem.<init>` PC 0–62, especialmente 16–47: atributos e operações; `supplyRenderer` PC 0–22.
- `ModArmorMaterialRegistry.<clinit>` PC 11–38, `makeArmorMap` PC 0–65 e `lambda$static$1` PC 0–6: material/reparo.
- `CosmeticModel.getAnimationResource(ExtendedArmorItem)` PC 0–7: referência de animação do host.

## Boundary de integração e validação

Acolyte possui o item e sua política local; Iron's possui atributos, efeitos, recipientes e magias do host; Minecraft/NeoForge possui inventário, equipamento e liquidação vanilla. Não há hook mutador homologado. Nomes de métodos/registries são candidatos de observação, sem garantia de API estável. Perks não devem alterar mana, repetir consumo, aplicar atributos em outro slot ou liquidar recompensas por esta ficha.

`NOT_TESTED`: conferir o hash instalado, uso/equipamento no servidor dedicado, criativo/sobrevivência, troca de slot, relog, morte e multiplayer; confirmar uma única aplicação e um único consumo no pack real. Ausência de cooldown explícito na classe não certifica ausência de cooldown herdado/do host.
