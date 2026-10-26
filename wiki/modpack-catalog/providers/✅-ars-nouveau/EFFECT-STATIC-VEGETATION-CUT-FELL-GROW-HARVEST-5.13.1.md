# Ars Nouveau 5.13.1 — lote Effects: Cut, Fell, Grow e Harvest

**Escopo:** auditoria de quatro fichas existentes para contratos técnicos de perks e interoperabilidade. O estado ✅ neste recorte significa exclusivamente `STATIC_TECHNICAL_CATALOG_ONLY`, nunca validação de mutação externa ou gameplay em modpack. `mutating_hook=NOT_VERIFIED`; `physical_qa=NOT_TESTED`.

## Proveniência e autoridade

- Modlist física de `neoforge-rpg-skilltree`: `ars_nouveau-1.21.1-5.13.1.jar`, mod ID `ars_nouveau`, Minecraft 1.21.1/NeoForge, SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd`.
- Source imutável `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`; classes e IDs no [manifesto de 109 identidades compiladas](EXACT-BINARY-GLYPH-RITUAL-IDS-5.13.1.md). A verificação binária **não** certifica equivalência de métodos, side, config ou execução física.
- O player/pack conserva o comportamento provider-native; não copiar implementação, assets nem preparar Java que intercepte internals desconhecidos.

| Ficha | Surface causal observada | Risco que bloqueia mutating perks |
|---|---|---|
| [Cut](glyphs/effects/cut.md) (`EffectCut`) | `IShearable.isShearable/onSheared` com drops em `ItemEntity`, alternativa `IDamageEffect.attemptDamage` base1 + AMP1; `doStrip` com `DIAMOND_AXE`; `doShear` com `SHEARS`; `dupeCheck` em `Capabilities.ItemHandler.BLOCK`/`Container` | `doShear` emite drops de `onSheared` **antes de `dupeCheck`** e ainda pode executar dois caminhos `useItemOn/useOn` para fake player. `AOE/Pierce` são lidos no helper apesar de **não** serem augments listados como compatíveis; validar origem de bônus. |
| [Fell](glyphs/effects/fell.md) (`EffectFell`) | `DFSBlockstates` sobre tag `FELLABLE`, limite `(int)(GENERIC_INT+round(AOE_BONUS*AOE))` default50+50×AOE, checks de claim e harvest por posição | Com Extract/Silk ou Fortune, gera drops **antes** de `destroyBlockSafelyWithoutSound` cujo retorno não é conferido. Preflight `destroyRespectsClaim` e BreakEvent do destroy podem divergir. DFS/Set não dão ordenação ou quebra garantida. |
| [Grow](glyphs/effects/grow.md) (`EffectGrow`) | `SpellUtil.calcAOEBlocks`, `destroyRespectsClaim` e `ServerLevel`, `BoneMealItem.applyBonemeal`; fallback `BoneMealItem.growWaterPlant` na direção do hit após `isFaceSturdy` | Preflight de claim só no `blockpos` **original**, não repete em `relative`. Stack local `new ItemStack(Items.BONE_MEAL,64)` não prova consumo de 64 itens do caster; partículas não provam stage efetivo de growth. |
| [Harvest](glyphs/effects/harvest.md) (`EffectHarvest`) | `FarmBlock` pode redirecionar para cima; maduras Cocoa AGE2, Nether Wart AGE3, CropBlock isMaxAge→reset AGE1 e `HARVEST_STEMS`; `processAndSpawnDrops` com Fortune e filtro Mage Bloom | Drops gerados antes de `setBlockAndUpdate` (AGE0/1) ou de `destroyBlockSafely` para stems; retornos ignorados. Sem `destroyRespectsClaim` direto neste método para Cocoa/Wart/Crop. Atenção a ServerLevel cast dos auxiliares Cocoa/Wart sem guarda local. |

## Invariantes de integração

1. **Provider authority:** Ars Nouveau é dono de mana, spell resolver, aquisição, augments, drops, bonemeal, BlockEvent e lifecycle de mundo; `WorldEffectPolicy` do Black Arcana aplica-se às próprias alterações BA, não intercepta automaticamente os paths de Ars.
2. **RPG Skill Tree** é sibling de progressão, atributos, Mastery/perks/gates, sem ownership de cast/world mutation. O fato de existir `EffectResolveEvent.Pre` não comprova hook por-effect nem settlement com dedup.
3. **Confirmação causal:** não computar quebras com base em DFS nodes, maturações com base em partículas, drops com base em preflight, dois tool callbacks como ações independentes ou AOE candidates como plantas colhidas. Qualquer incentivo de Mastery precisa correlacionar sucesso provider-native com proteção e orçamento únicos, sem replay.
4. **Custo/caps:** defaults de mana Cut **0**, Fell **150**, Grow **70** e Harvest **10**; números carregados podem diferir; ausência de mana default não certifica cast grátis. Não inferir cooldown individual, taxa de XP ou receita.
5. **Clean-room e Stage:** nenhum método copiado ao BA, nenhuma transmutação nova implementada, nenhuma alteração de Stage 06.05 ou Stage 09.

## QA física pendente

Comparar corpo dos métodos no JAR exato se necessário; medir claims com `BlockEvent.BreakEvent`, handler fake player e blocos `IShearable`, `FELLABLE` de mods, Double UseOn, drops gerados apesar de veto, `growWaterPlant` adjacente, CropBlock AGE1, `MAGE_BLOOM_CROP`, side ServerLevel, chances de vanilla bonemeal, configs reais de mana/augment, chunks, TPS e multiplayer. `mutating_hook=NOT_VERIFIED`; `physical_qa=NOT_TESTED`.

**Contadores projetados após CI+merge:** Effects **47/67**, Glyphs **65/85**, fichas Ars **89/138**, global **89/2075**, providers fechados **0/164**. O denominador continua sendo somente as fichas candidatas reconhecidas, não um censo do universo mágico completo.
