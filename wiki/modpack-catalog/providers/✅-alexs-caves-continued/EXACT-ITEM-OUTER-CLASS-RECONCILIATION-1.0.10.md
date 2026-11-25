# Reconciliação do inventário de classes externas de itens — checkpoint documental 1.0.10

**Escopo de reconciliação, não certificado novo.** Base canônica Black Arcana `712fd0bed3d3cdd126720405d1901a67bb9743be`. Fonte: [inventário SHA-exato](INTEGRATION-SCOPE-INVENTORY-1.0.10.json), [ledger canônico](../../meta/PERK-READY-CERTIFICATIONS.json) e fichas individuais indicadas. JAR publisher 1.0.10 SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`; 81 classes externas de item no recorte do inventário. O prefixo de 37 disposições históricas até FrostmintSpearItem é preservado. A reconciliação abaixo consulta o estado real do ledger e a identidade de classe em cada ficha na base indicada; não substitui provas binárias individuais.

## Sete classes seguintes

| Classe | Fichas existentes na base | Disposição |
|---|---|---|
| `server/item/GalenaGauntletItem` | [equipment/galena-gauntlet.md](equipment/galena-gauntlet.md) | ✅ fichas certificadas no recorte individual |
| `server/item/GazingPearlItem` | [items/gazing-pearl.md](items/gazing-pearl.md) | ✅ fichas certificadas no recorte individual |
| `server/item/GingerbreadArmorItem` | [items/gingerbread-boots.md](items/gingerbread-boots.md); [items/gingerbread-chestplate.md](items/gingerbread-chestplate.md); [items/gingerbread-helmet.md](items/gingerbread-helmet.md); [items/gingerbread-leggings.md](items/gingerbread-leggings.md) | ✅ fichas certificadas no recorte individual |
| `server/item/HazmatArmorItem` | [items/hazmat-boots.md](items/hazmat-boots.md); [items/hazmat-chestplate.md](items/hazmat-chestplate.md); [items/hazmat-leggings.md](items/hazmat-leggings.md); [items/hazmat-mask.md](items/hazmat-mask.md) | ✅ fichas certificadas no recorte individual |
| `server/item/HolocoderItem` | [items/holocoder.md](items/holocoder.md) | ⚠️ ficha parcial; candidato #1227 ainda não integrado |
| `server/item/HotChocolateBottleItem` | [items/hot-chocolate-bottle.md](items/hot-chocolate-bottle.md) | ✅ fichas certificadas no recorte individual |
| `server/item/InkBombItem` | [items/glow-ink-bomb.md](items/glow-ink-bomb.md); [items/ink-bomb.md](items/ink-bomb.md) | ✅ fichas certificadas no recorte individual |

São sete classes e 14 fichas vinculadas, 13 certificadas no ledger e uma parcial (Holocoder). Esses certificados já estavam contabilizados na base. Não confundir uma classe com uma peça/variante individual: GingerbreadArmorItem e HazmatArmorItem correspondem cada uma a quatro fichas, e InkBombItem a duas. Não elevar o prefixo contíguo de certificação além de Holocoder enquanto sua PR estiver pendente.

## Próxima fronteira

A posição 45 do inventário histórico é JellyBeanItem, seguida por KeybindUsingArmor e LimestoneSpearItem. [Coleta delimitada](EXACT-JELLY-KEYBIND-LIMESTONE-1.0.10.md) em andamento; nenhum novo contrato foi certificado. As 37 classes a partir de JellyBeanItem ainda não têm disposição reconciliada neste checkpoint específico; isso não significa que todas careçam de fichas (algumas têm ações/consumidores previamente auditados). O roster físico de classes não é o universo de objetos mágicos, nem deve ser somado aos 138 objetos observados. O inventário integral do provider segue OPEN.

`NO_MUTATION / NOT_VERIFIED / NOT_TESTED / semantic_magic_roots_delta=0`.
