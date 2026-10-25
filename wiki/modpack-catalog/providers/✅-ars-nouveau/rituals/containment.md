# Containment

Status: `SOURCE-PINNED 5.13.1 / MOB-JAR CAPTURE RITUAL`

- Registry id: `ars_nouveau:ritual_containment`
- Class: `RitualMobCapture`
- Source cost declaration: `500`
- Work cadence: every `60` game ticks
- Jar search cube: `±3` blocks around the ritual
- Entity search: AABB inflated `5` blocks around each eligible empty Mob Jar
- Exact release checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`

## Provider-native behavior

On each server work cycle, Containment scans nearby placed `MobJar` blocks. Only empty `MobJarTile` instances are eligible. For each, it searches entities around that jar using the provider `canJar` predicate.

Before serialization, the provider detaches passengers, drops valid leashes, removes active Raiders from raids and releases Villager POI memories. If `MobJarTile.setEntityData(e)` succeeds, the original entity is removed with `UNLOADED_TO_CHUNK`, a visual flying-item effect is spawned toward the jar and provider advancements may trigger for special captures.

Default capture admission:

- explicit provider jar whitelist always allowed;
- provider jar blacklist denied;
- multipart `PartEntity` denied;
- blacklisted ItemEntity stacks denied;
- otherwise living non-player, non-dead entities are allowed.

If at least one capture succeeds in the work cycle, the ritual calls `setNeedsSource(true)` once after scanning the jars.

## Description ↔ executable-radius mismatch

The provider description says mobs and jars must be within 3 blocks of the brazier. The pinned executable path enforces the 3-block cube for **jars**, but searches entities within an AABB inflated by **5 blocks around each jar**. This difference is preserved as runtime/UX QA rather than normalized by assumption.

## Authority / Black Arcana boundary

Entity serialization, removal, Mob Jar data, special jar behavior and Source settlement remain Ars Nouveau authority. Black Arcana must not create a parallel capture ledger or duplicate entity data.

## QA

Source entry path is pinned to 5.13.1. Effective Source batching, multipart/modded entity support and special Mob Jar behaviors remain runtime/provider QA.

## Engenharia para perks — contrato de ritual

- **Fonte:** [`RitualMobCapture.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/ritual/RitualMobCapture.java), `com.hollingsworth.arsnouveau.common.ritual.RitualMobCapture`, Ars 5.13.1.
- **Geometria/cadência:** a cada `60` ticks no servidor percorre posições `brazier±3` por eixo, isto é um cubo de `7×7×7` **candidatos a jarro** antes de filtro `MobJar`. Para cada `MobJarTile` vazio procura entidades em `AABB(jarPos).inflate(5)`, volume independente de 3 blocos do brazier. Divergência da descrição do provider deve permanecer explícita.
- **Elegibilidade:** `canJar` aceita whitelist `JAR_WHITELIST` antes da blacklist; em seguida bloqueia `JAR_BLACKLIST`, `PartEntity`, `ItemEntity` com tag de item `JAR_ITEM_CAPTURE_BLACKLIST`; fallback admite `LivingEntity` não-player e não morta. A ordem whitelist→blacklist é significativa e não deve ser invertida por um gate customizado.
- **Settlement:** desmonta passageiros/leash/raid/POI de Villagers antes de `tile.setEntityData(e)`; apenas após sucesso retira entidade com `RemovalReason.UNLOADED_TO_CHUNK` e cria efeitos visuais. Se ao menos uma captura teve sucesso marca `setNeedsSource(true)` ao final; `getSourceCost=500` não prova debit 500 por mob. Mesmo `MobJarTile` processa no máximo uma entidade por ciclo devido ao `break` interno.
- **Perks:** captura, descarte, persistência do jarro, Source e conquistas especiais pertencem ao Ars; não duplicar entity serialization nem award XP por VFX.
- **Estado:** ✅ source-pinned; ⚠️ tempo, recursos e proteção exigem observar config/JAR runtime. ⛔ não existe adapter RPG/Black Arcana demonstrado para reescrever Source, progresso, alvos ou world effects deste ritual.

## Certificação técnica estática de ritual — segundo lote (25/10/2026)

**✅ `STATIC_TECHNICAL_CATALOG_ONLY` — contrato estático completo da ficha; ⛔ `mutating_hook=NOT_VERIFIED`; ⚠️ `physical_qa=NOT_TESTED`.** Prova não cobre hook seguro, config implantada nem aceitação do modpack.

| Campo de perk | Evidência estática no provider |
|---|---|
| Identidade e release | `ars_nouveau:ritual_containment`; `RitualMobCapture`; Ars Nouveau 5.13.1. [Source imutável](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/ritual/RitualMobCapture.java) e [registry exato do publisher](../EXACT-BINARY-GLYPH-RITUAL-IDS-5.13.1.md). |
| Execução, ramificações e settlement | No servidor a cada `gameTime%60==0`, varre **cubo de posições brazier±3 em cada eixo** e considera `MobJar` cujo `MobJarTile` exista e esteja vazio. Para cada jar, busca `Entity` em `AABB(jarPos).inflate(5)` filtrado por `canJar`. Antes de serializar, interrompe riding de passageiros, remove leash quando aplicável, retira `Raider` de raid ativa e libera POIs de Villagers. **Só se `tile.setEntityData(e)` retornar true** remove o original com `RemovalReason.UNLOADED_TO_CHUNK`, cria FX/`EntityFlyingItem`, pode premiar advancements Starbuncle/LightningBolt/Clock, e dá `break` (no máximo 1 entidade/jar/ciclo); qualquer sucesso sinaliza `setNeedsSource(true)` **uma vez após a varredura**. |
| Fórmulas, parâmetros, limites e caps | Busca de jars é cubo **7×7×7 posições** (343 candidatas, nem todas são jars), não esfera de radius3. Busca de entidades usa **AABB inflate 5 ao redor de cada jar**, o que diverge da descrição 'mobs e jars within 3 blocks'. `canJar` admite `EntityTags.JAR_WHITELIST` **antes** da blacklist, rejeita blacklist, `PartEntity`, `ItemEntity` com `JAR_ITEM_CAPTURE_BLACKLIST`; fallback admite LivingEntity não Player, não morta. Whitelist pode introduzir outros tipos, inclusive não-LivingEntity. |
| Targeting, área/volume, duração, dano e projétil | Captura e serialização de entidades no `MobJarTile`; a apresentação `EntityFlyingItem` **não é projectile de spell nem outra entidade capturada**, e advancements condicionais não representam XP de cast. Sem DamageType/duração de buff/raycast de Form; persistência binária e estado de jar são provider-owned. |
| Resource cost, cooldown, receita/admissão | `getSourceCost()=500 Source`, solicitado com `setNeedsSource(true)` se houver pelo menos uma captura com `setEntityData` bem-sucedido; não é automaticamente 500 por mob, por jar ou por FX. Transferências e custo de jars precisam de QA do runtime de brasier. Custo de magia `SpellResolver` de Form/Effect é N/A neste ritual. |
| Política de mundo e integração entre projetos | Bloqueados replay, duplicação de item/NBT de criatura, rollback personalizado do Black Arcana e Mastery por advancement. Entidades modded/chefe, passageiros, aldeões e raiders exigem testes de integração: whitelist tem precedência sobre blacklist e deve permanecer como comportamento Ars. Autoridade de execução e fonte/Source pertence ao Ars; RPG Skill Tree fornece progressão/atributos/Mastery/gates mediante contrato real, Black Arcana detém seu runtime/rituais e WorldEffectPolicy para suas mutações próprias, sem interceptar automaticamente este ritual. |
| Grau de evidência/QA | `PINNED_SOURCE_PLUS_SHA_EXACT_BINARY_IDENTITY`: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157` para métodos e publisher `ars_nouveau-1.21.1-5.13.1.jar` SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd` para **ID/classe registrada**. Não foi comprovada equivalência byte-a-byte dos métodos, configuração atual, side/claims reais, multiplayer ou QA físico. |

**Gate fail-closed:** alteração de geometria, itens, persistência, energia/Source ou consumer exige hook real, orçamento, transação e deduplicação provados; o ✅ é documental, não implementação de perk ou promoção de Stage 06.05/09.
