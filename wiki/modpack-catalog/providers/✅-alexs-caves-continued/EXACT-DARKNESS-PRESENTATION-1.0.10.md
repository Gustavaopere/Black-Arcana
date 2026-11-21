# CustomArmorPostRender e CustomTabBehavior — interfaces de apresentação (1.0.10)

**Disposição:** ⚠️ componentes técnicos nativos inspecionados; **zero novos casts ou magias**, zero certificados de objeto mágico e zero hooks mutadores. `NO_MUTATION`, `NOT_VERIFIED` para hooks, `NOT_TESTED` para QA física e provider `OPEN`. Estas duas interfaces não são fichas de feitiço e não alteram os denominadores de objetos mágicos. Manter separados de [Cloak Darkness Incarnate](actions/cloak-darkness-incarnate.md), [efeito Darkness Incarnate](effects/darkness-incarnate.md) e [inventário de itens](items/INDEX.md).

## Identidade e cadeia de prova

Publisher `alexscaves-1.0.10-neoforge+1.21.1.jar`, Minecraft 1.21.1, Java 21, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c` (75.279.314 bytes, 1.555 classfiles). Auditor [read-only](../../../../docs/qa/alexscaves_1010_darkness_presentation_probe.py), [manifesto SHA-exato](EXACT-DARKNESS-PRESENTATION-DISCOVERY-1.0.10.json), CI [run 44864573972](https://github.com/Gustavaopere/Black-Arcana/actions/runs/44864573972), job `136725251381`, artefato `14691630395`, ZIP SHA-256 `7cf08c60fd02de05d3a735a365ecc3c8a95bf481fe5f4ccecd5c40aea1313c15` (expira 05/12/2026). Os 18 transcripts integrais `javap -p -c -v -s` ficam no CI, sem copiar código de terceiros para o repo.

### 1. CustomArmorPostRender

- Owner `com/github/alexmodguy/alexscaves/server/item/CustomArmorPostRender.class`; SHA-256 `19c649b8fdd407e51049f8a98dd31dc348a022c148ad3d5a70f2295a544988fd`.
- Uma única declaração abstrata, **sem corpo executável ou estado**: `getArmorTexture(ItemStack, Entity, EquipmentSlot, String): String`. Não executa render, ataque, cast, dano ou efeito.
- Censo tipado em **todas as 1.555 classes**: seis implementadores nativos — `DarknessArmorItem`, `DivingArmorItem`, `GingerbreadArmorItem`, `HazmatArmorItem`, `PrimordialArmorItem`, `RainbounceBootsItem`; um consumidor do método `HumanoidArmorLayerMixin`, SHA-256 `383fbea50413635447bb3fdbf77f06298007f42e3254e40d5ef0b94a8277e048`. Seus implementadores devolvem uma string de textura em cada caso, com efeitos de gameplay pertencendo às classes de item, não à interface.
- O mixin consulta a textura via `invokeinterface` no caminho de material/recurso da camada de armadura e pode acionar `ACArmorRenderProperties.renderCustomArmor`. A classe do mixin é evidência **estática**, não prova de aplicação bem-sucedida por mixin, renderizador cliente nem textura carregada no modpack.
- **Perks/Mastery:** sem parâmetro de dano, mana, cooldown, targeting ou servidor; `N/A` para mutação de magia. Não transformar um selector de textura em boundary de gameplay.

### 2. CustomTabBehavior

- Owner `com/github/alexmodguy/alexscaves/server/item/CustomTabBehavior.class`; SHA-256 `6a77f884be2f7556f8c5085a534bd70968628c52d83687be2efde8237dba6cbe`.
- Uma declaração abstrata, **sem implementação própria**: `fillItemCategory(CreativeModeTab.Output): void`. Nenhum implementador direto encontrado nas 1.555 classes deste JAR; isto não exclui implementadores de mods externos ou execução condicionada.
- Consumidor tipado `ACCreativeTabRegistry` (SHA-256 `e73ea47bee91ada022b06c5c73eebf454f68cfe769bbc7e7a22b2561cc23822d`): se o `ItemLike` consultado implementa `CustomTabBehavior`, delega a `fillItemCategory`; caso contrário solicita `CreativeModeTab.Output.accept`. É seleção de **conteúdo criativo**, não uso/cast, gate de progressão, aquisição Survival ou efeito.
- **Perks/Mastery:** `N/A` para parâmetros mágicos da interface; nenhum hook server-authoritative suportado. A existência de um `instanceof` não prova implementador carregado.

## Limites e próximos owners

As interfaces não recebem fichas extras no contador semântico: continuam componentes técnicos de suporte. A cadeia de gameplay relevante é [Darkened Apple](items/darkened-apple.md), [Hood of Darkness](items/hood-of-darkness.md) e [Cloak of Darkness](items/cloak-of-darkness.md), com `DarknessIncarnateEffect` já certificado separadamente no recorte. Faltam QA cliente do render/mixin, resource reload, seleção de modelos e testes contra implementadores externos; esses testes **não** são homologação do runtime mágico de Black Arcana.
