# Slowfall

- Registry ID: `ars_nouveau:glyph_slowfall`
- Source class: `EffectSlowfall`
- School: Elemental Air
- Default tier: **2**
- Default mana: **30**
- Default duration config: base **30**, Extend Time increment **8**
- Exact source: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`

## Source-pinned behavior

Applies Minecraft Slow Falling through Ars Nouveau's configurable potion-effect path.

Compatible augments: Extend Time, Reduce Time.

## Acquisition / learning

- Provider-generated Glyph recipe: `ars_nouveau:air_essence` + `ars_nouveau:wilden_wing` + `minecraft:feather` ×3 + `#c:rods/blaze` + `#c:crops/nether_wart`.
- Source-default recipe XP: **55 XP** (Tier II).
- Starter default: **no**.
- Learning is Ars-owned and consumes the Glyph in survival after a successful server-side unlock; runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Boundary

Ars Nouveau owns duration/config and effect application. Black Arcana mobility/fall-safety mechanics remain independent unless a supported adapter explicitly consumes provider state.

Status: `SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / RUNTIME+CONFIG QA PENDING`.

## Engenharia para perks — caminho causal individual

- **Source pin:** [`EffectSlowfall.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectSlowfall.java) do Ars 5.13.1.
- **Efeito/targeting:** `onResolveEntity` aceita `LivingEntity` e chama `IPotionEffect.applyConfigPotion(living,MobEffects.SLOW_FALLING,spellStats)`. `EffectSlowfall` não ajusta o vetor de movimento diretamente; gravidade/queda são providas pelo efeito Minecraft.
- **Config:** `buildConfig` define 30s base e 8s por duration unit; com defaults carregados, `ticks=600+8*(int)(20*getDurationMultiplier())`, amplifier `(int)getAmpMultiplier()` do helper. Compatible somente Extend Time e Duration Down. **Perks:** não usar a mesma regra para reduzir dano de queda por outra magia sem hook e teste específicos.
- **Estado:** ✅ classe/método do source pin; ⚠️ scripts de addons, config física e QA Survival pendentes; ⛔ bridge de perks RPG e mutação de `SpellStats` sem validação de causalidade e limites.

## Certificação estática de Effect — 25/10/2026

**✅ Documentação técnico-causal estática completa deste Effect; ⛔ hook de mutação por perks `NOT_VERIFIED`; ⚠️ QA físico/config `NOT_TESTED`.** O ✅ não concede implementação de perk; aplica-se ao source fixo do Ars Nouveau 5.13.1 e identidade binária do glyph, não à equivalência integral dos métodos do JAR instalado.

| Campo para implementação de perks | Prova / fronteira de autoridade |
|---|---|
| ID, versão e classe | `ars_nouveau:glyph_slowfall`, classe `EffectSlowfall`, escola Elemental Air, tier padrão 2. [Implementação em commit exato](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectSlowfall.java); [ID/class no JAR SHA-exato](../../EXACT-BINARY-GLYPH-RITUAL-IDS-5.13.1.md). |
| Ação, ramo, consumidor e settlement | `onResolveEntity` só aplica `MobEffects.SLOW_FALLING` se o hit for uma `LivingEntity`, chamando `IPotionEffect.applyConfigPotion`. O próprio glyph não faz `setDeltaMovement` ou aplica dano direto. O efeito vanilla é a autoridade da queda real. |
| Parâmetros/fórmulas/compatibilidade/caps | `buildConfig` define base 30 segundos e contribuição Extend Time 8; getters têm fallback 30/8 quando não inicializados. Helper: `ticks=20*baseDurationSeconds+durationBuffSeconds*stats.getDurationInTicks()`, amplifier `(int)getAmpMultiplier()`. Duração final depende de `SpellStats`, mods/servidor e config real. Compatíveis `AugmentExtendTime` e `AugmentDurationDown`, nenhum outro inferido. |
| Alvo, área, projétil, tipo de dano e duração | Somente entidade viva recebida de `EntityHitResult`, sem projétil próprio, área, linha de visão, Range, DamageType ou alteração direta de física nesta classe; entrega e permissão pertencem à Form e ao resolver. |
| Mana, cast, cooldown, aquisição e aprendizado | Mana default 30, tier II, 55 XP de recipe gerada; recipe `ars_nouveau:air_essence` + `ars_nouveau:wilden_wing` + `minecraft:feather` ×3 + `#c:rods/blaze` + `#c:crops/nether_wart`. Starter default não; custo/cooldown efetivos são da magia Ars composta. [Inventário de acquisition 85/85](../../ACQUISITION.md). |
| Integração e policy | Não tratar os ticks de Slow Falling ou a gravidade do Minecraft como casts ou como bônus genérico de redução de dano; não substituir com buff Black Arcana sem contrato. Compatibilidade com voo de Iron's/Epic Fight exige QA. Ars Novo detém `SpellResolver`, `SpellStats`, custos, targets e resultado; RPG Skill Tree é sibling de progresso/perks, não proprietário de runtime. A existência de API de evento pública do Ars não prova um adapter RPG/Black Arcana seguro. Efeitos independentes Black Arcana têm seu próprio `WorldEffectPolicy`. |
| Evidência e limites | Source `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`, JAR publisher Ars 5.13.1 SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd` para **identidade registrada**; métodos/consumidores **somente source-pinned**, checksum de instalação corrente e configuração em jogo **não auditados** nesta etapa, gameplay Survival/cliente/servidor `NOT_TESTED`. |

**Fail-closed:** mudança de build/config, hooks efetivos, ordem de eventos e contrapartes de addons precisam de prova antes de mutar mana/alcance/alvo/duração/hitbox ou interpretar FX/estados persistentes como casts extras. Este Effect não aumenta o número de objetos do catálogo — sua ficha já existia.
