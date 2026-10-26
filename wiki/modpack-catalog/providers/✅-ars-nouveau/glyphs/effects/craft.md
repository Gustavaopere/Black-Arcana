# Ars Nouveau — Craft

Status: `SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / RUNTIME CONFIG QA PENDING`

- Registry id: `ars_nouveau:glyph_craft`
- Display name: Craft
- School: Manipulation
- Default tier: 1
- Default mana cost: 50
- Compatible augments: none

## Provider-native behavior

Opens a remote crafting menu for a real player caster. Ars provides a crafting menu whose validity is not tied to remaining near a workstation.

## Acquisition / learning

- Provider-generated Glyph recipe: `minecraft:crafting_table`.
- Source-default recipe XP: **27 XP** (Tier I).
- Starter default: **no**.
- Learning is Ars-owned and consumes the Glyph in survival after a successful server-side unlock; runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Authority / deduplication

This provider already owns generic remote crafting. Black Arcana should not add another plain crafting-access spell unless the mechanic materially changes into a forbidden-magic contract rather than duplicating utility.

Source checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157` (`EffectCraft`).

## Engenharia para perks — caminho causal individual

- **Fonte versionada:** [`EffectCraft.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectCraft.java), Ars Nouveau 5.13.1.
- **Admissão:** `onResolve(HitResult,...,shooter,...)` abre menu somente se `shooter instanceof Player` **e** `isNotFakePlayer(shooter)`; não há branch por alvo nem resultado de craft associado ao glyph.
- **UI real:** `SimpleMenuProvider` instancia `CustomWorkbench extends CraftingMenu` com `ContainerLevelAccess.create(player.world,player.blockPosition())`. O override `CustomWorkbench.stillValid(Player)` retorna sempre `true`: a validade do menu não depende da proximidade de uma mesa. Sem augments; mana default 50.
- **Perks:** evento de cast/menu aberto não comprova crafting efetivo, remoção de ingredientes nem concessão de receita. Não reimplementar inventário, nem recompensar Mastery por cada clique de crafting sob a identidade do spell.
- **Estado:** ✅ source pin com métodos/fórmulas; ⚠️ auxiliaries, config real e Survival QA pendentes. API de `EffectResolveEvent.Pre` existe, mas adapter RPG para este glyph não foi implementado/testado; sem duplicação de custo/efeito/WorldEffectPolicy.

## Certificação técnica estática — Craft (26/10/2026)

**✅ `STATIC_TECHNICAL_CATALOG_ONLY` · ⛔ `mutating_hook=NOT_VERIFIED` · ⚠️ `physical_qa=NOT_TESTED`.** Identidade publisher `ars_nouveau:glyph_craft` → `EffectCraft` verificada no manifesto binário do JAR `ars_nouveau-1.21.1-5.13.1.jar`, SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd`; sem equivalência provada dos métodos. Código upstream `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`: [EffectCraft.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectCraft.java).

| Campo técnico | Contrato source-pinned e limite |
|---|---|
| Entrada e targeting | `EffectCraft.onResolve(HitResult,...)` não diferencia `onResolveBlock` ou `onResolveEntity`; verifica **`shooter instanceof Player playerEntity && isNotFakePlayer(shooter)`**. Não abre menu a partir de `FakePlayer`, turret ou entidade não-jogadora no método inspecionado. O `HitResult` não é usado para procurar bancada/alvo; não existe AOE, range adicional nem projétil de craft. |
| Menu remoto | Com caster elegível, `playerEntity.openMenu(new SimpleMenuProvider(...,CONTAINER_NAME))`; nome `Component.translatable("container.crafting")`. O factory instancia `new CustomWorkbench(id,inventory,ContainerLevelAccess.create(player.getCommandSenderWorld(),player.blockPosition()))`, onde `CustomWorkbench extends CraftingMenu`. |
| Condição de validade | Override `CustomWorkbench.stillValid(Player)` retorna **`true`** incondicionalmente: a validade do menu não exige continuar próximo à mesa. Isso não implica sobrevivência do menu depois de logout, cross-dimension teleport, morte ou sincronização de inventário garantida. `openMenu` não prova craft completado ou consumo real de ingredientes. |
| Outputs, custos e limites | Não há branch da classe que produza items/receitas diretamente, nem manipulação própria de `RecipeManager`, `BlockState`, `DamageType`, cooldown ou criação de `ItemEntity`. `getCompatibleAugments()` retorna `augmentSetOf()` vazio; `getDefaultManaCost()=50`, school `MANIPULATION`; Tier do glyph não deve ser inferido desta classe sem consultar config/defaults herdados (o dossiê existente registra Tier I). O custo carregado pode divergir do default. |
| Integração/causalidade | Ars e `CraftingMenu`/vanilla são donos de menu e receitas. Não recompensar Mastery por cada clique ou cada receita “vista” a partir de EffectResolveEvent; o efeito garantido aqui é **pedido para abrir UI**, não objeto craftado. `WorldEffectPolicy` do Black Arcana não tem mutação de mundo neste método; a criação de um sistema de autocrafting pelo BA ou RPG Skill Tree não decorre de EffectCraft. Apenas progressão/gates por bridge verificada, sem duplicar receitas ou slots. |

**QA pendente:** abertura efetiva de menu com servidor/client, perda de conexão, troca de dimensão, inventários integrados por mods, custo de mana no cast, feedback de sucesso, spoofing/fake player, sobrevivência de container e configs. `mutating_hook=NOT_VERIFIED`; `physical_qa=NOT_TESTED`. Nenhum Stage alterado.
