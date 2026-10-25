# Ars Nouveau 5.13.1 — cinco Effects de mobilidade, teleporte e controle

**Escopo:** 5 novas fichas auditadas e certificadas apenas como contrato técnico estático: Blink, Leap, Launch, Pull e Snare. Total depois deste lote: **15/67 Effects**, **33/85 glyphs**, **33/138 fichas Ars** e **33/2.075 fichas globais**; **0/164 providers com todo o universo fechado**.

Identidade por publisher JAR `ars_nouveau-1.21.1-5.13.1.jar` SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd` na [auditoria exata do registry](EXACT-BINARY-GLYPH-RITUAL-IDS-5.13.1.md). Semântica por fonte pública imutável `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`. A primeira evidência NÃO comprova equivalência binária total da segunda; config/pack físicos nunca foram testados nesta etapa.

| Effect | Operação que interessa à perk | Limite de autoridade |
|---|---|---|
| [Blink](glyphs/effects/blink.md) | Self forward 8+3×amp default, block adjacent validation; scroll/rune/turret/dim são ramos diferentes e podem ter regras de destino próprias | ⛔ sem mutação segura de teleporte/claims |
| [Leap](glyphs/effects/leap.md) | **substitui** motion na direção do olhar; clamp em living vs sem clamp em nonliving; force_ground só self airborne | ⛔ sem hook de motion/gates |
| [Launch](glyphs/effects/launch.md) | **soma** velocity vertical; defaults entity 0,8 + 0,25×amp, falling block 0,48 + 0,25×amp | ⛔ sem hook de conversion |
| [Pull](glyphs/effects/pull.md) | **substitui** velocity da entidade pela direção caster−target; bloco usa normal da face com ruído ±0,05, +0,1Y | ⛔ sem hook de alvo ou RNG |
| [Snare](glyphs/effects/snare.md) | Living aplica status, zero motion e duração 8s+1 por unidade; EnchantedFallingBlock tenta groundBlock(true), sem buff | ⛔ sem hook de assentamento/persistência |

**Invariantes:** não universalizar a geometria ou o sinal entre ramos, não tratar `canOcclude()` como validação integral de destino, não duplicar entidade `EnchantedFallingBlock`, casts, cooldowns, mana ou Mastery. Glyphs source-pinned podem ter custos/compatibilidades config-dependent e o target depende também da Form e do SpellResolver. Inspeção de source/jar não equivale a QA de cliente/servidor ou jogo Survival.

**Gate:** `STATIC_TECHNICAL_CATALOG_ONLY`, `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`. A implementação de perks permanece bloqueada sem seam real, lado do servidor e deduplicação garantidos; nenhum Stage, registry, Java ou projeto sibling foi alterado.
