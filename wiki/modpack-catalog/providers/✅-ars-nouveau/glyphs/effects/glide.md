# Ars Nouveau — Glide

Status: `SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / RUNTIME CONFIG QA PENDING`

- Registry id: `ars_nouveau:glyph_glide`
- Display name: Glide
- School: Elemental Air
- Default tier: 3
- Default mana cost: 100
- Compatible augments: Extend Time, Reduce Time (`glyph_duration_down`)
- Source config default duration: 180 s
- Source config default Extend Time increment: 120 s

## Provider-native behavior

Applies Ars' Glide effect, allowing elytra-like flight behavior. The source also exposes `canGlide`, which treats either the Glide effect or Ars' Gliding Perk as sufficient for provider gliding eligibility.

## Acquisition / learning

- Provider-generated Glyph recipe: `ars_nouveau:air_essence` + `minecraft:elytra` + `#c:gems/diamond` ×3.
- Source-default recipe XP: **160 XP** (Tier III).
- Starter default: **no**.
- Learning is Ars-owned and consumes the Glyph in survival after a successful server-side unlock; runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Authority / deduplication

Ars Nouveau already owns temporary elytra-like gliding and a perk-based alternative path. Black Arcana mobility/familiar content should not add a generic duplicate glide buff or take over Ars' glide eligibility state.

Source checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157` (`EffectGlide`).

## Engenharia para perks — caminho causal individual

- **Fonte versionada:** [`EffectGlide.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectGlide.java), Ars Nouveau 5.13.1.
- **Ramo status:** `onResolveEntity` aplica `ModPotions.GLIDE_EFFECT` a LivingEntity via `IPotionEffect`. Config declarada base 180 segundos e ExtendTime 120; getters sem config têm fallbacks 30/8, uma divergência de inicialização que deve ser mantida separada. Após carga default, `ticks=3600+120*(int)(20*durationMultiplier)` pelo helper.
- **Caminho alternativo:** `EffectGlide.canGlide(LivingEntity)` retorna `hasEffect(GLIDE_EFFECT) || PerkUtil.countForPerk(GlidingPerk.INSTANCE,entity)>0.0`. **Este `GlidingPerk` é do Ars Nouveau**, não API de perks do sibling RPG Skill Tree; integração externa não pode reutilizar o nome para afirmar compatibilidade.
- **Perks:** glide por potion e por perk interna Ars representam condições distintas para uma checagem provider; sem hook RPG que declare equivalência, manter fail-closed para novo gate.
- **Estado:** ✅ source pin com métodos/fórmulas; ⚠️ auxiliaries, config real e Survival QA pendentes. API de `EffectResolveEvent.Pre` existe, mas adapter RPG para este glyph não foi implementado/testado; sem duplicação de custo/efeito/WorldEffectPolicy.

## Certificação estática de Effect — 25/10/2026

**✅ Documentação técnico-causal estática completa deste Effect; ⛔ hook de mutação por perks `NOT_VERIFIED`; ⚠️ QA físico/config `NOT_TESTED`.** O ✅ não concede implementação de perk; aplica-se ao source fixo do Ars Nouveau 5.13.1 e identidade binária do glyph, não à equivalência integral dos métodos do JAR instalado.

| Campo para implementação de perks | Prova / fronteira de autoridade |
|---|---|
| ID, versão e classe | `ars_nouveau:glyph_glide`, classe `EffectGlide`, escola Elemental Air, tier padrão 3. [Implementação em commit exato](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectGlide.java); [ID/class no JAR SHA-exato](../../EXACT-BINARY-GLYPH-RITUAL-IDS-5.13.1.md). |
| Ação, ramo, consumidor e settlement | `onResolveEntity` aplica `ModPotions.GLIDE_EFFECT` via `IPotionEffect.applyConfigPotion` a `LivingEntity`. `EffectGlide.canGlide(entity)` reconhece `hasEffect(GLIDE_EFFECT)` **ou** `PerkUtil.countForPerk(GlidingPerk.INSTANCE, entity)>0` — o `GlidingPerk` aqui é **interno ao Ars Nouveau**, não uma API do sibling RPG Skill Tree. |
| Parâmetros/fórmulas/compatibilidade/caps | `buildConfig` registra defaults base 180 s e bônus Extend Time 120 s, mas `getBaseDuration/getExtendTimeDuration` retornam fallback 30/8 quando campos ainda estão nulos; não confundir fallback com default carregado. `IPotionEffect` calcula ticks por base*20 + bonus*getDurationInTicks e amplifier `(int)amp`. Apenas Extend Time e Reduce Time são augments compatíveis. |
| Alvo, área, projétil, tipo de dano e duração | Recebe `LivingEntity` do hit; sem projétil/área/dano intrínsecos. Eligibility de planagem e movimento do cliente dependem de outros componentes do Ars/Minecraft, não deste `onResolveEntity` isolado. |
| Mana, cast, cooldown, aquisição e aprendizado | Mana default 100, tier III, 160 XP recipe default `ars_nouveau:air_essence` + `minecraft:elytra` + `#c:gems/diamond` ×3. Starter default não. Glide effect duration não equivale a cooldown do cast. [Inventário de acquisition 85/85](../../ACQUISITION.md). |
| Integração e policy | Não criar estado paralelo de Elytra ou perk de voo no Black Arcana; conflito com Iron's Angel Wings, mixins e teleporte exige QA de cliente/servidor sem inferir prioridade de provider. Ars Novo detém `SpellResolver`, `SpellStats`, custos, targets e resultado; RPG Skill Tree é sibling de progresso/perks, não proprietário de runtime. A existência de API de evento pública do Ars não prova um adapter RPG/Black Arcana seguro. Efeitos independentes Black Arcana têm seu próprio `WorldEffectPolicy`. |
| Evidência e limites | Source `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`, JAR publisher Ars 5.13.1 SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd` para **identidade registrada**; métodos/consumidores **somente source-pinned**, checksum de instalação corrente e configuração em jogo **não auditados** nesta etapa, gameplay Survival/cliente/servidor `NOT_TESTED`. |

**Fail-closed:** mudança de build/config, hooks efetivos, ordem de eventos e contrapartes de addons precisam de prova antes de mutar mana/alcance/alvo/duração/hitbox ou interpretar FX/estados persistentes como casts extras. Este Effect não aumenta o número de objetos do catálogo — sua ficha já existia.
