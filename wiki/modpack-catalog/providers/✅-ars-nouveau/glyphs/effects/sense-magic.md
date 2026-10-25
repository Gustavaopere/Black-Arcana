# Ars Nouveau — Sense Magic

Status: `SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / RUNTIME CONFIG QA PENDING`

- Registry id: `ars_nouveau:glyph_sense_magic`
- Display name: Sense Magic
- School: Abjuration
- Default tier: 2
- Default mana cost: 50
- Compatible augments: Extend Time, Reduce Time (`glyph_duration_down`)
- Source config default duration: 60 s
- Source config default Extend Time increment: 15 s

## Provider-native behavior

Applies Ars' Magic Find effect. Provider documentation states that Magic Find reveals magical mobs by glow within 75 blocks and reveals spells inscribed on Runes. When targeting a block entity implementing `IPedestalMachine`, the spell invokes that provider highlighting path.

## Acquisition / learning

- Provider-generated Glyph recipe: `ars_nouveau:abjuration_essence` + `ars_nouveau:dowsing_rod` + `ars_nouveau:starbuncle_shards`.
- Source-default recipe XP: **55 XP** (Tier II).
- Starter default: **no**.
- Learning is Ars-owned and consumes the Glyph in survival after a successful server-side unlock; runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Authority / deduplication

Ars Nouveau owns this magical sensing/reveal capability. Black Arcana Familiars & Divination must provide a materially distinct forbidden/divinatory contract rather than duplicate Magic Find.

Source checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157` (`EffectSenseMagic`).

## Engenharia para perks — caminho causal individual

- **Source exato:** [`EffectSenseMagic.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectSenseMagic.java), `com.hollingsworth.arsnouveau.common.spell.effect.EffectSenseMagic` no Ars Nouveau 5.13.1.
- **Alvos:** `onResolveEntity` aplica `ModPotions.MAGIC_FIND_EFFECT` exclusivamente a `LivingEntity` por `IPotionEffect.applyConfigPotion`. No bloco, só executa `IPedestalMachine.lightPedestal(world)` quando o BlockEntity atingido implementa essa interface.
- **Config vs fallback:** `buildConfig` usa duração base **60 segundos** e `Extend Time` **15 segundos**. Porém `getBaseDuration()` retorna fallback 30 segundos e `getExtendTimeDuration()` fallback 8 segundos quando os campos `POTION_TIME/EXTEND_TIME` são nulos. Registrar separadamente: default configurado 60/15; fallback pré-config 30/8, não os fundir. O helper calcula ticks usando os getters efetivos.
- **Resto do comportamento:** glow a mobs mágicos dentro de 75 blocos e revelação de runas são especificações do `MAGIC_FIND_EFFECT`/renderização, não callbacks explícitos da classe do glyph. Mana declarada 50, tier II, compatível Extend Time e Duration Down.
- **Perks:** detectar alvo mágico e renderizar glow não comprovam descoberta persistida, cast bem-sucedido por alvo, nem concessão de XP. Sem um resultado oficial observável, não criar source paralelo de progressão.
- **Estado:** ✅ classe/fórmulas source-pinned; ⚠️ outcomes downstream, config física e Survival pendentes; ⛔ nenhuma alteração por RPG Skill Tree implementada ou testada. Avaliar a interface `EffectResolveEvent.Pre` per-effect com clamps e causalidade.

## Certificação estática de Effect — 25/10/2026

**✅ Documentação técnico-causal estática completa deste Effect; ⛔ hook de mutação por perks `NOT_VERIFIED`; ⚠️ QA físico/config `NOT_TESTED`.** O ✅ não concede implementação de perk; aplica-se ao source fixo do Ars Nouveau 5.13.1 e identidade binária do glyph, não à equivalência integral dos métodos do JAR instalado.

| Campo para implementação de perks | Prova / fronteira de autoridade |
|---|---|
| ID, versão e classe | `ars_nouveau:glyph_sense_magic`, classe `EffectSenseMagic`, escola Abjuration, tier padrão 2. [Implementação em commit exato](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectSenseMagic.java); [ID/class no JAR SHA-exato](../../EXACT-BINARY-GLYPH-RITUAL-IDS-5.13.1.md). |
| Ação, ramo, consumidor e settlement | `onResolveEntity` aplica `ModPotions.MAGIC_FIND_EFFECT` por `IPotionEffect` apenas a LivingEntity. `onResolveBlock` chama `IPedestalMachine.lightPedestal(world)` só quando o BlockEntity atingido implementa essa interface. O glow de mobs mágicos em **75 blocos** e a revelação de runas constam da **descrição da classe**, não são implementados por esses dois callbacks de glyph; prova runtime em renderer/effect é separada. |
| Parâmetros/fórmulas/compatibilidade/caps | `buildConfig`: 60s base e 15s por unidade de duração; getters sem config têm fallback 30s/8s. Helper usa `ticks=base*20+bonus*getDurationInTicks()` e amplifier `(int)amp`. Compatíveis apenas Extend Time e Reduce Time. Não alegar varredura real de 75 blocos ou duração da interface pedestal sem verificar seu consumidor. |
| Alvo, área, projétil, tipo de dano e duração | Entidade viva recebe status Magic Find; bloco recebe apenas side effect de highlight via `IPedestalMachine`, se implementado. Sem dano, projétil, AoE ou seleção de entidades mágicas própria do glyph; Forms definem delivery. |
| Mana, cast, cooldown, aquisição e aprendizado | Mana default 50, tier II, 55 XP recipe; `ars_nouveau:abjuration_essence` + `ars_nouveau:dowsing_rod` + `ars_nouveau:starbuncle_shards`. Starter default não; efeitos visuais ou runas reveladas não constituem cast adicional. [Inventário de acquisition 85/85](../../ACQUISITION.md). |
| Integração e policy | Não atribuir Mastery por glow/varredura por tick, nem criar duplicação de estado de detecção/divinação entre Ars e Black Arcana. Ars Novo detém `SpellResolver`, `SpellStats`, custos, targets e resultado; RPG Skill Tree é sibling de progresso/perks, não proprietário de runtime. A existência de API de evento pública do Ars não prova um adapter RPG/Black Arcana seguro. Efeitos independentes Black Arcana têm seu próprio `WorldEffectPolicy`. |
| Evidência e limites | Source `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`, JAR publisher Ars 5.13.1 SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd` para **identidade registrada**; métodos/consumidores **somente source-pinned**, checksum de instalação corrente e configuração em jogo **não auditados** nesta etapa, gameplay Survival/cliente/servidor `NOT_TESTED`. |

**Fail-closed:** mudança de build/config, hooks efetivos, ordem de eventos e contrapartes de addons precisam de prova antes de mutar mana/alcance/alvo/duração/hitbox ou interpretar FX/estados persistentes como casts extras. Este Effect não aumenta o número de objetos do catálogo — sua ficha já existia.
