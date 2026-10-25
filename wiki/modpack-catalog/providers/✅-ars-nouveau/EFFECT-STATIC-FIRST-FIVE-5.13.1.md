# Ars Nouveau 5.13.1 — Effects, primeiro lote de contratos estáticos (5/67)

**Escopo:** cinco Effects com revisão técnica individual e fontes imutáveis: Heal, Slowfall, Glide, Sense Magic, Knockback. `5/67` identifica somente fichas de Effects promovidas a ✅ técnico estático; não executa um perk. As 67/67 identidades de Effects já eram conhecidas antes deste lote e não aumentam.

**Fonte/versionamento:** `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`, `ars_nouveau-1.21.1-5.13.1.jar`, publisher SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd`. A auditoria compilada [85 glyphs +24 rituals](EXACT-BINARY-GLYPH-RITUAL-IDS-5.13.1.md) prova IDs/class, **não** o comportamento byte-a-byte do cast instalado.

| Effect | Contrato causal e divergência relevante para perks | Estado runtime |
|---|---|---|
| [Heal](glyphs/effects/heal.md) | alvo Player recebe exhaustion 2.5 no ramo cura; dano invertido via `IDamageEffect#attemptDamage`; base 3+3×amp default | ⛔ hook não verificado |
| [Slowfall](glyphs/effects/slowfall.md) | `MobEffects.SLOW_FALLING`, duration helper + config base30s / increment8; status é Minecraft-owned | ⛔ hook não verificado |
| [Glide](glyphs/effects/glide.md) | efeito Ars `GLIDE_EFFECT` ou perk **interna Ars** em `canGlide`; defaults 180/120 vs fallback 30/8 | ⛔ hook não verificado |
| [Sense Magic](glyphs/effects/sense-magic.md) | `MAGIC_FIND_EFFECT` para entidades ou pedestal highlight; 75 blocos só na descrição, não confirmado pelos callbacks | ⛔ hook não verificado |
| [Knockback](glyphs/effects/knockback.md) | ID real `glyph_gust`; resistência de knockback; branches Sensitive/Extract; block falling entity/propagation | ⛔ hook não verificado |

**Invariantes:** não duplicar casts, mana, exaustão, dano/loot, spawn de entidade, efeitos de mobilidade, discovery, Mastery ou emissão de mundo. `claim_scope=STATIC_TECHNICAL_CATALOG_ONLY`; `mutating_hook=NOT_VERIFIED`; `physical_qa=NOT_TESTED`; provider runtime fora de Black Arcana e RPG Skill Tree.

**Foco futuro:** evidência provider-native do evento de modificação por Effect (`EffectResolveEvent.Pre` ou seam comprovado) e dos consumidores efetivos de stats, order/side/cancelamento e clamps, então testes em modpack físico. Nenhum Stage promocionado.
