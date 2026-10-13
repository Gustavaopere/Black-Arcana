# Companions! 1.3.4 — nove Magic Books binários exatos

**✅ `COUNTED_EXACT` somente para as nove identidades estáticas de itens `AbstractMagicBook`.** Black Arcana não os trata como spell registrations de Iron's: o registry observado pertence ao provider/KNIGHTLIB (`CompanionsItems.ITEMS` / `ResourceRegistry<Item>`). A campanha de 39 providers passa a **23/39 exatos / 16/39 pendentes**, novos objetos semânticos **+0**; mínimos estritos **1857 global / 1855 escopo** preservados. Runtime/Survival ⚠️.

## Evidência binária direta

- Modlist física do sibling: `#104`, `companions-neoforge-1.21.1-1.3.4.jar`, mod ID `companions`, SHA-1 `23f6e4f27a457a8d016412e495e417c0b36fdcc1`, KnightLib físico **2.0.1**.
- [CurseForge file 8857294](https://www.curseforge.com/minecraft/mc-mods/companions-mod/files/8857294), **7.189.704 bytes** (valor exato: `7189704`), SHA-1 `23f6e4f27a457a8d016412e495e417c0b36fdcc1` = JAR físico.
- [Discovery Java21 #38457728494](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38457728494), [vínculos de classe e factory #38457998766](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38457998766), [asserções completas Java21 #38458161666](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38458161666): **SUCCESS**.
- Workflow externo clean-room isolado na branch [`audit/companions-134-20261013`](https://github.com/Gustavaopere/Black-Arcana/tree/audit/companions-134-20261013); sem JAR, código ou assets copiados à `main`.

## Registry compilado, identificação das fábricas

- `dev.xylonity.companions.registry.CompanionsItems` utiliza `dev.xylonity.knightlib.api.registrar.ResourceRegistry` para registrar nove nomes `book_*` com nove `ResourceEntry<Item>`.
- Cada nome possui `ResourceRegistry.register(String, Supplier)`, um bootstrap LambdaMetafactory próprio (#17–#25) e uma factory compilada cujo `new` aponta à classe física correspondente.
- As nove classes concretas estendem `dev.xylonity.companions.common.item.book.AbstractMagicBook`, todas presentes no JAR. O trecho de registros dos nove itens não contém desvio condicional.
- ID de item estático = uma ação mágica provider-native identificada pelo catálogo source-pinned; **não** transformar as nove ações em spells Iron's nem criar segundo objeto para o item/caster Soul Mage.

## Inventário canônico 9/9

| # | Identidade | Item ID compilado | Classe concreta binária | Ficha |
|---:|---|---|---|---|
| 1 | Ice Shard Magic Book | `companions:book_ice_shard` | `dev.xylonity.companions.common.item.book.books.IceShardBook` | [Ficha](magic-books/ice-shard.md) |
| 2 | Ice Tornado Magic Book | `companions:book_ice_tornado` | `dev.xylonity.companions.common.item.book.books.IceTornadoBook` | [Ficha](magic-books/ice-tornado.md) |
| 3 | Fire Mark Magic Book | `companions:book_fire_mark` | `dev.xylonity.companions.common.item.book.books.FireMarkBook` | [Ficha](magic-books/fire-mark.md) |
| 4 | Heal Ring Magic Book | `companions:book_heal_ring` | `dev.xylonity.companions.common.item.book.books.HealRingBook` | [Ficha](magic-books/heal-ring.md) |
| 5 | Stone Spikes Magic Book | `companions:book_stone_spikes` | `dev.xylonity.companions.common.item.book.books.StoneSpikesBook` | [Ficha](magic-books/stone-spikes.md) |
| 6 | Brace Magic Book | `companions:book_brace` | `dev.xylonity.companions.common.item.book.books.BraceBook` | [Ficha](magic-books/brace.md) |
| 7 | Magic Ray Magic Book | `companions:book_magic_ray` | `dev.xylonity.companions.common.item.book.books.MagicRayBook` | [Ficha](magic-books/magic-ray.md) |
| 8 | Black Hole Magic Book | `companions:book_black_hole` | `dev.xylonity.companions.common.item.book.books.BlackHoleBook` | [Ficha](magic-books/black-hole.md) |
| 9 | Naginata Magic Book | `companions:book_naginata` | `dev.xylonity.companions.common.item.book.books.NaginataBook` | [Ficha](magic-books/naginata.md) |

**PUBLISHER_EQUALS_PHYSICAL_SHA1=PASS**

**EXACT_PHYSICAL_ITEM_MAGIC_REGISTRATIONS=9**

**PROVIDER_NATIVE_MAGIC_BOOK_CLASSES=9**

**STATIC_ITEM_REGISTRATION_CONDITIONS=0**

**NEW_SEMANTIC_ROOTS=0**

**EXACT_STATIC_REGISTRY_AUDIT=PASS**

**RUNTIME_SURVIVAL_NOT_VERIFIED=TRUE**

## Autoridade, deduplicação e pendências

- Os nove Magic Books usam engine e cooldown próprios do Companions!/KnightLib. A reutilização pela IA do Soul Mage, projectiles, VFX, summons e efeitos downstream **não** multiplicam as identidades.
- A [fonte oficial 1.3.4 pinada](SOURCE-1.3.4-MAGIC-BOOK-INVENTORY.md) ainda é a referência *source-pinned* para cooldowns default, efeito e rotas de aquisição. A prova binária não certifica os valores das configs instaladas nem sucesso das rotas do Survival.
- **⚠️** Faltam boot e cast real de client/dedicated-server com KnightLib 2.0.1, comportamento de damage/heal/block-grief, rota de loot/recipe real, persistência, multiplayer, cooldowns e integração com Black Arcana.
- Companions! mantém autoridade sobre ações, itens, efeitos, loot e estados nativos. Black Arcana conserva seu runtime mágico e RPG Skill Tree é provider sibling de progressão/Mastery/perks/gates, somente via contratos reais. Sem API/boundary comprovado, integração permanece fail-closed.
