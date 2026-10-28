# EmissiveGenericCustomArmorRenderer — camada visual de armadura Geo

**Provider:** Ace's Spell Utils `1.2.7.2-1.21.1` · **tipo:** API de render cliente · **estado:** ⚠️ `SOURCE_VERSION_ONLY`, integração `CONDITIONAL`, sem certificação de perk.

O renderer e sua camada são reutilizáveis; não representam novos itens/spells registrados. A composição de atributos e o ciclo do provider estão em [ExtendedGeoArmorItem](geo-armor-attribute-helper.md); os [itens de exemplo](../examples/example_armor_helmet.md) são consumidores concretos. Esta ficha cobre a seleção de RenderType, buffer, luz e recursos, sem atribuir efeitos de gameplay à apresentação.

## Construtor, desenho e parâmetros efetivamente usados

[`EmissiveGenericCustomArmorRenderer<T extends Item & GeoItem>`][renderer] estende o `GenericCustomArmorRenderer<T>` de Iron's. O construtor `(GeoModel<T> model,ResourceLocation glowLayer,RenderType renderType)` encaminha o modelo ao super e adiciona `new GeoArmorGlowmaskLayer<>(this,glowLayer,renderType)`. Seu `getRenderType(...)` retorna **`RenderType.entityTranslucent(getTextureLocation(animatable))`**: o parâmetro `texture` recebido pelo override não escolhe a textura dessa chamada.

[`GeoArmorGlowmaskLayer<T extends GeoAnimatable>`][glow] recebe `GeoRenderer<T>`, `ResourceLocation glowMask` e `RenderType`; conserva os dois últimos em campos públicos finais `GLOW_LAYER` e `RENDER_TYPE`. No callback `render(...)`, chama `getRenderer().reRender(...)` com:

| Argumento de desenho | Valor no source |
|---|---|
| Modelo | `getDefaultBakedModel(animatable)` |
| Pose, buffer source, animatable, partial tick | Valores recebidos pelo callback |
| RenderType e VertexConsumer | `RENDER_TYPE` armazenado e `bufferSource.getBuffer(RENDER_TYPE)` |
| Luz | `packedLight` recebido, sem substituição local por constante fullbright |
| Overlay e cor | `OverlayTexture.NO_OVERLAY`, `0xFFFFFFFF` |

O callback não consulta diretamente `GLOW_LAYER`; a textura efetiva da camada depende do RenderType fornecido pelo consumidor. Também não usa os parâmetros `bakedModel`, `renderType`, `buffer` e `packedOverlay` recebidos como substitutos desses valores. O nome Glowmask/Emissive não prova luz de bloco, aura, imunidade ou alteração de dano; as propriedades do RenderType/host e o resultado visual exigem QA.

## Consumidor e recursos concretos

[`ExampleWarlockArmorItem.supplyRenderer()`][example] constrói `RenderType.breezeEyes(aces_spell_utils:textures/models/armor/evil_armor_tips.png)` e o passa ao renderer junto a `new ExampleWarlockMaskModel()`. O [modelo][model] resolve:

| Papel | ResourceLocation |
|---|---|
| Geometria | `aces_spell_utils:geo/evil_armor.geo.json` |
| Textura principal | `aces_spell_utils:textures/models/armor/evil_armor.png` |
| Camada fornecida pelo consumidor | `aces_spell_utils:textures/models/armor/evil_armor_tips.png` |
| Animação | **`irons_spellbooks:animations/wizard_armor_animation.json`**, pertencente ao host |

O [asset geométrico local][geometry] declara atlas `128×128`, `visible_bounds_width=3`, `visible_bounds_height=3.5`, offset `(0,1.25,0)`. Esses números são bounds de apresentação; não alteram hitbox, alcance, colisão ou área de spell. Animação do host e recursos locais precisam existir no cliente; os caminhos não provam fidelidade visual em outra versão.

## Lifecycle, rede, custos e integração

O renderer é fornecido pelo callback lazy de [ExtendedGeoArmorItem](geo-armor-attribute-helper.md); a base retorna null até um consumidor sobrescrever `supplyRenderer()`. Estas duas classes de render não registram payload, não enviam estado de magia, não gravam componentes e não executam evento de equipamento/dano. O callback redesenha o modelo no ciclo cliente. Não há duração, cooldown, custo de mana, seleção de alvo, RNG, projétil ou proc próprio; o wearer/modelo visível não é um alvo ofensivo.

Modelo/RenderType são argumentos nativos de construção, mas mudança por perk requer um consumidor cliente e contrato de sincronização/classloading comprovado. Não iniciar cast, aplicar atributo ou conceder Mastery por frame/reRender. A camada não substitui a autoridade de equipamento/atributos do host; RPG Skill Tree conserva progressão e Black Arcana conserva seus efeitos/regras de mundo. Nenhuma bridge foi implementada.

QA pendente: carregamento em cliente/dedicado, lazy provider e renderer null, recursos ausentes, textura principal versus camada, transparência, luz recebida, clipping/bounds, animação host e remoção/troca de equipamento. Não houve execução física nem demonstração de paridade do JAR nesta ficha.

Pin oficial `AceTheEldritchKing/Aces_Spell_Utils@a0b2f4c2fcfa938c8e47239279c77c2ef82647ac`; JAR anotado `aces_spell_utils-1.2.7.2-1.21.1.jar`, SHA-1 `8cbcd535a0b19bef49504c0b5ecafcbcd1cb1cca`. Source Ace depende de Iron's `3.16.2`, pack anota `3.16.3`; o renderer de Iron's/GeckoLib não foi certificado nessa combinação. `source_pinned=true` · `mutating_hook=NOT_VERIFIED` · `physical_qa=NOT_TESTED` · `COMPLETE_PERK_READY=false` · **+0 magias registradas, +0 perks implementadas.**

[renderer]: https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/entity/render/armor/EmissiveGenericCustomArmorRenderer.java#L12-L22
[glow]: https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/entity/render/armor/GeoArmorGlowmaskLayer.java#L15-L41
[example]: https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/items/example/items/armor/ExampleWarlockArmorItem.java#L20-L30
[model]: https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/entity/armor/ExampleWarlockMaskModel.java#L9-L29
[geometry]: https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/resources/assets/aces_spell_utils/geo/evil_armor.geo.json#L1-L12
