# Ars Nouveau 5.13.1 — Effects status e Dispel: cinco contratos estáticos

**5 novos Effects no catálogo técnico estático:** Invisibility, Wither, Hex, Bounce, Dispel; após este lote são **20/67 Effects, 38/85 glyphs, 38/138 fichas Ars e 38/2075 fichas candidatas globais**. Ainda **0/164 providers inteiramente certificados**. São fichas, não perks implementadas.

**Proveniência:** fonte pública `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`; publisher `ars_nouveau-1.21.1-5.13.1.jar` SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd`. Auditoria [85 glyphs + 24 rituais](EXACT-BINARY-GLYPH-RITUAL-IDS-5.13.1.md) é de identidades compiladas, sem equivalência integral de bytecode ou execução em cliente.

| Effect | Contrato causal relevante para perks | Limite de integração |
|---|---|---|
| [Invisibility](glyphs/effects/invisibility.md) | `MobEffects.INVISIBILITY`; sem partículas via parâmetro false; duração 30s + 8 por duration multiplier | ⛔ invisibilidade não garante indetectabilidade universal |
| [Wither](glyphs/effects/wither.md) | Status vanilla Wither; Amplify cap default 4, duration helper 30/8; DoT downstream | ⛔ não duplicar dano/XP por tick |
| [Hex](glyphs/effects/hex.md) | `HEX_EFFECT`; descrição de debuffs não comprova fórmula de heal/mana/damage no callback da classe | ⛔ consumidor precisa de evidência isolada |
| [Bounce](glyphs/effects/bounce.md) | `BOUNCE_EFFECT`; alteração de movimento só downstream, não em EffectBounce.onResolveEntity | ⛔ não somar impulso em paralelo |
| [Dispel](glyphs/effects/dispel.md) | `DispelEvent.Pre` cancelável em entity/block, Post condicional em entity e incondicional após block sem cancelamento; `IDispellable` | ⛔ veto source-verified **não** é perk bridge genérica |

**Dispel:** `Pre` em `EntityHitResult` de não-living não garante `Post`; entidade viva morta/removida após remoção de effects retorna antes de Post; `onResolveBlock` publica Post após o possível callback, mesmo se nenhum IDispellable existir. Campos públicos de `DispelEvent` são inspeccionáveis, mas o `EffectDispel` usa valores locais. Pre pode cancelar somente este Dispel; não intercepta rituais/corrupção Black Arcana. `ICancellableEvent` apenas em Pre.

**IPotionEffect:** `ticks=base*20+extend*stats.getDurationInTicks()`, `amplifier=(int)getAmpMultiplier()`; defaults 30/8 nestes quatro status. Somente Invisibility passa `showParticles=false`; os outros usam default true. Durations são do status; sem cooldown adicional autônomo.

**Gates:** `STATIC_TECHNICAL_CATALOG_ONLY`, `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`. Nenhuma validação em Survival, runtime, adapter RPG Skill Tree, Black Arcana Stage 06.05 ou Magic From The East foi alterada. Evitar deduplicação falsa por FX/tick/Post.
