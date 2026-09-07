# Extend Time

- Registry ID: `ars_nouveau:glyph_extend_time`
- Source class: `AugmentExtendTime`
- Exact source: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`
- Default tier: **2**
- Default mana: **10**

## Source-pinned behavior

Adds **+1.0** to Ars Nouveau's duration modifier. Compatible effects use that stat for provider-owned duration behavior, including effects, summons and other timed spell results.

## Boundary

Duration scaling is provider-owned. Black Arcana durations/cooldowns remain separate server-owned policy values and cannot be silently multiplied by this Ars stat.

Status: `SOURCE-PINNED 5.13.1 / RUNTIME+CONFIG QA PENDING`.