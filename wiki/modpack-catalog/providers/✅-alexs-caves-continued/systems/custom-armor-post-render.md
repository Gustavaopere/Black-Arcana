# CustomArmorPostRender — apresentação de armaduras (1.0.10)

**Contrato técnico estático** `STATIC_TECHNICAL_CATALOG_ONLY` / `SHA_EXACT_BINARY_BEHAVIOR`. **Hooks mutadores** `NOT_VERIFIED`. **QA física** `NOT_TESTED`. **Perks executáveis** `NOT_CERTIFIED`. **Política** `NO_MUTATION`. Esta ficha acrescenta **um contrato de suporte e +0 raízes mágicas**. O provider permanece `OPEN`. [Evidência e reprodução do lote](../EXACT-DARKNESS-ITEMS-CATALOG-1.0.10.md)

## 1. Identidade

O publisher 8856293 de Alex's Caves Continued 1.0.10 para Minecraft 1.21.1 tem 75.279.314 bytes e SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`. A interface `com.github.alexmodguy.alexscaves.server.item.CustomArmorPostRender` tem SHA-256 `19c649b8fdd407e51049f8a98dd31dc348a022c148ad3d5a70f2295a544988fd`, zero campos, zero superinterfaces e uma declaração pública abstrata, `String getArmorTexture(ItemStack, Entity, EquipmentSlot, String)`.

## 2. Comportamento

`HumanoidArmorLayerMixin.ac_renderArmorPiece` injeta no `HEAD` de `HumanoidArmorLayer.renderArmorPiece`, com `cancellable=true` e `remap=true`. Lê a stack equipada (`@0–6`) e, se o item implementa a interface (`@13`), cancela a renderização original e guarda a stack no campo do renderer (`@21–27`). O desenho customizado prossegue quando o item é `ArmorItem` e o slot do item coincide com o slot recebido (`@39–59`). Usa o modelo pai quando ele é `HumanoidModel` e usa o modelo recebido pela injeção nos demais casos (`@77–105`). O mixin consulta `ClientHooks.getArmorModel` (`@114`), copia as propriedades para o modelo retornado quando é uma instância diferente (`@119–133`), chama o helper de animações (`@139`) e ajusta as partes visíveis pelo slot (`@151`).

`getACArmorResource` chama `getArmorTexture(stack, entity, slot, null)` no caminho da injeção (`@154–161` no chamador, `@4–12` no helper). Usa a string retornada como chave de `AC_ARMOR_LOCATION_CACHE` e, se faltar um valor, chama `ResourceLocation.parse` e grava a associação (`@19–59`). O chamador entrega a textura resolvida e o modelo a `ACArmorRenderProperties.renderCustomArmor` (`@182`).

## 3. Parâmetros e saídas

As seis classes abaixo são implementadoras diretas e concretas em `com.github.alexmodguy.alexscaves.server.item`. Os nomes de arquivo na tabela têm prefixo `alexscaves:textures/armor/`. Quatro corpos leem apenas o slot e selecionam `_1` para `EquipmentSlot.LEGS` e `_0` para os demais valores. Os outros dois retornam uma constante. Stack, entidade e string de tipo ficam sem leitura nos seis callbacks.

| Classe | Textura para `LEGS` | Textura para os demais slots |
|---|---|---|
| `DarknessArmorItem` | `darkness_armor.png` | `darkness_armor.png` |
| `DivingArmorItem` | `diving_suit_1.png` | `diving_suit_0.png` |
| `GingerbreadArmorItem` | `gingerbread_armor_1.png` | `gingerbread_armor_0.png` |
| `HazmatArmorItem` | `hazmat_suit_1.png` | `hazmat_suit_0.png` |
| `PrimordialArmorItem` | `primordial_armor_1.png` | `primordial_armor_0.png` |
| `RainbounceBootsItem` | `rainbounce_boots.png` | `rainbounce_boots.png` |

As dez texturas e `darkness_armor_glow.png` estão empacotadas. `renderCustomArmor` desenha Darkness com `entityTranslucent` na luz recebida e uma segunda passada de glow com luz empacotada `240` (`@0–102`). Rainbounce usa `getTeslaBulb` com luz empacotada `240` (`@105–177`). Os demais usam `armorCutoutNoCull` na luz recebida (`@180–208`). Os três caminhos consultam `ItemStack.hasFoil()` para o brilho visual de encantamento.

## 4. Seleção de alvo

O portador e o slot vêm da chamada de renderização. A seleção se limita à peça equipada, ao modelo, às partes visíveis e à textura. Dano, vítima, área, alcance, linha de visão e colisão são inaplicáveis a este contrato de apresentação.

## 5. Custos

Mana, consumo de item, desgaste, cooldown e cobrança de perk são inaplicáveis. As escritas observadas no caminho delimitado pertencem à apresentação do cliente, incluindo a referência à última stack no renderer, as propriedades e a visibilidade do modelo e o cache de recursos por textura.

## 6. Integração

O censo tipado das **1.555 classes** encontra oito classes com referência à interface, contando a própria declaração, as seis implementadoras e `HumanoidArmorLayerMixin`. A hierarquia do JAR tem seis classes concretas atribuíveis à interface. Há sete declarações de `getArmorTexture` e uma referência de método com esse nome, `InterfaceMethodref #82` no mixin, usada em `getACArmorResource @12`. `alexscaves.mixins.json` lista o mixin em `mixins` e em `client`. Seu alvo é a camada de armadura do cliente e o JAR registra essa configuração em `META-INF/neoforge.mods.toml`.

A seleção de modelos por tipo de item tem evidência na ficha de extensão de cliente. A transformação do Cloak e seus efeitos de jogo pertencem ao contrato da ação. [Client Extension](client-extension.md) · [Cloak of Darkness](../actions/cloak-darkness-incarnate.md)

## 7. Validação e localizadores JVM

| Método | Descritor e localizador |
|---|---|
| `CustomArmorPostRender.getArmorTexture` | `(Lnet/minecraft/world/item/ItemStack;Lnet/minecraft/world/entity/Entity;Lnet/minecraft/world/entity/EquipmentSlot;Ljava/lang/String;)Ljava/lang/String;` · `ACC_PUBLIC`, `ACC_ABSTRACT` |
| Os seis `getArmorTexture` concretos | Mesmo descritor. Darkness `@0–3`, Rainbounce `@0–2`, os outros quatro `@0–12` |
| `HumanoidArmorLayerMixin.ac_renderArmorPiece` | `(Lcom/mojang/blaze3d/vertex/PoseStack;Lnet/minecraft/client/renderer/MultiBufferSource;Lnet/minecraft/world/entity/LivingEntity;Lnet/minecraft/world/entity/EquipmentSlot;ILnet/minecraft/client/model/HumanoidModel;FFFFFFLorg/spongepowered/asm/mixin/injection/callback/CallbackInfo;)V` · `@0–185` |
| `HumanoidArmorLayerMixin.getACArmorResource` | `(Lnet/minecraft/world/entity/LivingEntity;Lnet/minecraft/world/item/ItemStack;Lnet/minecraft/world/entity/EquipmentSlot;Ljava/lang/String;)Lnet/minecraft/resources/ResourceLocation;` · `@0–61` |
| `ACArmorRenderProperties.renderCustomArmor` | `(Lcom/mojang/blaze3d/vertex/PoseStack;Lnet/minecraft/client/renderer/MultiBufferSource;ILnet/minecraft/world/item/ItemStack;Lnet/minecraft/world/item/Item;Lnet/minecraft/client/model/Model;ZLnet/minecraft/resources/ResourceLocation;)V` · `@0–211` |

O contrato usa inspeção do JAR identificado por SHA, censo tipado, corpos de bytecode e recursos empacotados. Aplicação do mixin, desenho efetivo no cliente, reload de recursos e compatibilidade com os renderers do pack permanecem `NOT_TESTED`. [Evidência e reprodução do lote](../EXACT-DARKNESS-ITEMS-CATALOG-1.0.10.md)
