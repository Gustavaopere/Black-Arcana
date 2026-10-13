# Fire's Ender Expansion 2.4.1 — onze IDs de spell em binário SHA exato

**✅ `COUNTED_EXACT` para registro estático:** **11/11** spell identities próprias e previamente contabilizadas; **+0** raízes semânticas. Campanha física 39 providers: **17/39 exact / 22/39 pending**, mínimo estrito **1857 global / 1855 escopo** inalterado. Gameplay e Survival permanecem ⚠️.

## Proveniência física e teste Java 21

- JAR da modlist sibling: `firesenderexpansion-2.4.1.jar`, mod ID `firesenderexpansion`, versão instalada `2.4.1` (ordem física **#281**); Minecraft 1.21.1 / NeoForge.
- Artefato oficial [CurseForge file 8167304](https://www.curseforge.com/minecraft/mc-mods/fires-ender-expansion/files/8167304), obtido por CurseMaven, **2442013 bytes**, SHA-1 `da87a4a0c926dd75236766584cddbae69c6aeff7`, **correspondente ao SHA-1 físico informado pela modlist**. Uma publicação 2.5.x mais recente não altera a versão física 2.4.1.
- [Auditoria binária de 11/11 identidades Java 21 #38434192044](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38434192044) **SUCCESS**, após [descoberta da versão exata #38433992026](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38433992026). A primeira [tentativa #38433875258](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38433875258) falhou fechada por não encontrar o file ID exato; a página CurseForge identificou `8167304`, resolvendo a origem sem usar binário não conferido.
- `FiresEnderExpansion.<init> → SpellRegistries.register(modEventBus) → SPELLS.register(eventBus)`. `SpellRegistries.<clinit>` cria `DeferredRegister<AbstractSpell>` para Iron's `SpellRegistry.SPELL_REGISTRY_KEY`, namespace literal `firesenderexpansion`, com **11** invocações incondicionais de `registerSpell(new ConcreteSpell)`; wrapper usa `DeferredRegister.register(spell.getSpellName(), Supplier)`.
- Verificações por `javap -p -c`: classe, ordem de construção, cardinalidade das chamadas, ausência de branches no initializer, método `getSpellResource`, `ResourceLocation.fromNamespaceAndPath` com sufixo literal e `SchoolRegistry.ENDER_RESOURCE` em cada spell compilado. `PHYSICAL_SPELL_REGISTRATIONS=11`, `EXACT_STATIC_REGISTRY_PROOF=PASS`, `NEW_SEMANTIC_ROOTS=0`. O source pin histórico 2.4.1 permanece separado da evidência compilada.

## Registry exato (11/11)

| # | ResourceLocation | Classe no JAR 2.4.1 | Catálogo |
|---:|---|---|---|
| 1 | `firesenderexpansion:arcane_slice` | `net.fireofpower.firesenderexpansion.spells.ArcaneSliceSpell` | [Ficha](ender/arcane-slice.md) |
| 2 | `firesenderexpansion:aspect_of_the_shulker` | `net.fireofpower.firesenderexpansion.spells.AspectOfTheShulkerSpell` | [Ficha](ender/aspect-of-the-shulker.md) |
| 3 | `firesenderexpansion:hollow_crystal` | `net.fireofpower.firesenderexpansion.spells.HollowCrystalSpell` | [Ficha](ender/hollow-crystal.md) |
| 4 | `firesenderexpansion:dimensional_adaptation` | `net.fireofpower.firesenderexpansion.spells.DimensionalAdaptationSpell` | [Ficha](ender/dimensional-adaptation.md) |
| 5 | `firesenderexpansion:obsidian_rod` | `net.fireofpower.firesenderexpansion.spells.ObsidianRodSpell` | [Ficha](ender/obsidian-rod.md) |
| 6 | `firesenderexpansion:infinite_void` | `net.fireofpower.firesenderexpansion.spells.InfiniteVoidSpell` | [Ficha](ender/infinite-void.md) |
| 7 | `firesenderexpansion:dragons_fury` | `net.fireofpower.firesenderexpansion.spells.DragonsFurySpell` | [Ficha](ender/dragons-fury.md) |
| 8 | `firesenderexpansion:gate_of_ender` | `net.fireofpower.firesenderexpansion.spells.GateOfEnderSpell` | [Ficha](ender/gate-of-ender.md) |
| 9 | `firesenderexpansion:displacement_cage` | `net.fireofpower.firesenderexpansion.spells.DisplacementCageSpell` | [Ficha](ender/displacement-cage.md) |
| 10 | `firesenderexpansion:binary_stars` | `net.fireofpower.firesenderexpansion.spells.BinaryStarsSpell` | [Ficha](ender/binary-stars.md) |
| 11 | `firesenderexpansion:scintillating_stride` | `net.fireofpower.firesenderexpansion.spells.ScintillatingStrideSpell` | [Ficha](ender/scintillating-stride.md) |

**Família:** Ender, via configuração padrão de Iron's. A classificação source-pinned de risco, XP/perks, raridade, eventos/efeitos e custo não foi promovida automaticamente por esta prova de registro.

## Exclusões e riscos de runtime

- Entidades auxiliares, efeitos, animações, estruturas, items, curios, buffs, projéteis e máquinas **não** são novos spells só porque aparecem no mesmo JAR.
- A descrição pública antiga de dez spells não prevalece contra o inicializador compilado de **onze** identidades.
- `BinaryStarEntity`: teleport/slam AoE aparece comentado no source-pinned do provider; sem declarar execução dessa fase.
- `NovaBurnEffect`: risco de amplifier 0 na aplicação e dano calculado 0, exige teste no runtime.
- `ScintillatingStrideSpell`: ausência de filtro explícito de aliados no trecho ofensivo requer observação do pipeline de dano.
- `InfiniteVoidEffect`: retorno a `(0,100,0)` no Overworld quando a posição não está recuperada, risco de lifecycle/permissões.
- **⚠️ Pendente:** compatibilidade efetiva do host Iron's `3.16.3` contra o source 2.4.1 originalmente compilado em `3.15.6`, config aplicada, crafting/loot, casting, resource/cooldown settle, domains, teleport cross-dimension, anti-magic, claims e multiplayer/Survival. O CI Black Arcana não constitui teste do pack cliente real.
- **Clean-room/authority:** Fire's Ender Expansion/Iron's controlam seus próprios casts, mana/cooldowns, efeitos, projectiles, teleport e domains; Black Arcana não os processa nem debita de novo; RPG Skill Tree permanece sibling/provider de progressão sob contrato. Stage 06.05 🟡.
