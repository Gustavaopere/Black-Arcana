# Ars Nouveau 5.13.1 — quatro Effects de mutação de mundo

**Escopo:** certificado de documentação técnica estática de 4 glyph Effects adicionais: Break, Place Block, Conjure Water e Evaporate. Não há alteração do runtime Black Arcana nem do provider Ars, hook de mutação implementado, QA física, Stage ou status integral do mod.

**Proveniência:** versão física `ars_nouveau-1.21.1-5.13.1.jar`, mod ID `ars_nouveau`, SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd`; upstream `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`. O publisher identifica os 85 glyphs e 24 rituais em [auditoria de registry/class](EXACT-BINARY-GLYPH-RITUAL-IDS-5.13.1.md). **A identidade compilada não prova equivalência dos métodos nem integração no pack.**

| Effect e ficha | Superfícies físicas / contratos para perk | Limite que bloqueia mutação externa |
|---|---|---|
| [Break](glyphs/effects/break.md) (`EffectBreak`) | `onResolveBlock` / `SpellUtil.calcAOEBlocks`: AOE+Pierce, nível de harvest `3+AMP` truncado, Mining Fatigue, tool simulado shears/pickaxe, Fortune+Extract, `BlockTagProvider.BREAK_BLACKLIST` | `BlockUtil.destroyRespectsClaim` posta preflight, `BlockUtil.breakExtraBlock` posta outro `CommonHooks.fireBlockBreak`; somente quebra confirmada por retorno positivo propaga via `ShapersFocus`. Não multiplicar loot/XP ou criar segundo break. |
| [Place Block](glyphs/effects/place-block.md) (`EffectPlaceBlock`) | `SpellUtil.calcAOEBlocks`, evento `BlockEvent.EntityPlaceEvent`, `InventoryManager.extractItem/extractRandomItem`, `BlockItem.place`, `ExtractedStack.returnOrDrop`; `Sensitive` reflete fake player orientation | `world.isInWorldBounds` é checado **antes** do `pos1.relative(hitDirection)`; não há segunda guarda local. Propagação em `InteractionResult != FAIL` não é prova independente de cada placement/consumo. |
| [Conjure Water](glyphs/effects/conjure-water.md) (`EffectConjureWater`) | Água em `LiquidBlockContainer`, água adjacente via `setBlockAndUpdate`, extinguish fogo, `SOAKED_EFFECT`, Sensitive e AOE/Pierce | O `destroyRespectsClaim` e o `isInWorldBounds` checam **o BlockPos original**, não repetem no destino adjacente; retorno de `setBlockAndUpdate` ignorado. `buildConfig` 20s vs fallback `getBaseDuration` 30s (somente config null). |
| [Evaporate](glyphs/effects/evaporate.md) (`EffectEvaporate`) | Para cada posição AOE, 1 centro + 6 `Direction.values()` = **7 tentativas**; `LiquidBlock` com FluidState não vazio vira AIR, ou `SimpleWaterloggedBlock` com WATERLOGGED vira false | Não há `destroyRespectsClaim` ou event gate explícito nessa classe, e `world.setBlock` não tem retorno inspecionado antes de propagar `ShapersFocus`. 7 chamadas não equivalem a 7 conversões bem-sucedidas. |

## Regras comuns de geometria

O overload `SpellUtil.calcAOEBlocks(shooter,pos,hit,aoeMultiplier,pierceCount)` utiliza largura `1+floor(AOE)`, altura `1+ceil(AOE)`, profundidade `1+Pierce`, e orientação pelo hit/caster. Isso **não** é um único parâmetro `range` ou `projectile_size`; interações por bloco, fluidos, inventários e loots têm perfis distintos. Cada candidate e branch deve ser testado sob orçamento de work, chunks carregados, claims e proteção da posição **efetiva de mutação**.

`Break` declara custo mana default **10**, `Place Block` **10**, `Conjure Water` **80**, `Evaporate` **50**. Defaults não provam valor carregado, custo por target ou cooldown individual. `Conjure Water` tem configuração padrão `POTION_TIME=20` s / `EXTEND_TIME=10` s e fallback base 30 somente com config nula; distinguir **duração configurada** da duração fallback.

## Arquitetura e QA

- **Ars Nouveau** mantém seus custos de mana, resolver, casting, aquisição de glyph, inventories, `ShapersFocus`, loot, liquidações de itens, chamadas vanilla/NeoForge e modificações nativas do mundo.
- **Black Arcana** mantém seu próprio runtime de casts, rituais, hazards, Corruption/Strain, persistência e `WorldEffectPolicy`. Esta policy não é interceptor universal do Ars.
- **RPG Skill Tree** é sibling/provider de Mastery, perks, atributos e gates exclusivamente por contrato real. A existência de `EffectResolveEvent.Pre` não é prova de mutator de parâmetros destes Effects.
- **Bloqueio:** `STATIC_TECHNICAL_CATALOG_ONLY`; `mutating_hook=NOT_VERIFIED`; `physical_qa=NOT_TESTED`. Sem adapter, bônus de raio, volume, loot, manipulação do status nem double-processing.

**QA pendente:** confirmar semântica do classfile 5.13.1, configurações efetivas, drops/enchants, retorno de `BlockItem.place`, fake-player + callback de claim, props waterlogged, `BlockPos` adjacente, ShapersFocus, limites do mundo, performance AOE e multiplayer. GameTests/CI do Black Arcana não substituem validação no modpack.

**Contadores previstos após os gates e merge:** Effects **39/67**, Glyphs **57/85**, Ars Nouveau **81/138**, global **81/2075**, providers com escopo integral **0/164**. Denominadores são o recorte de fichas detectadas — não um censo de toda capacidade mágica do pack. Stages 06.05 e 09 não promovidos.
