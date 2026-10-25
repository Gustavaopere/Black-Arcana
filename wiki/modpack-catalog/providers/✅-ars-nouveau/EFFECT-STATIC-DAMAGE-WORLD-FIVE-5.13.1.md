# Ars Nouveau 5.13.1 — segundo lote de Effects (dano, área e mundo)

**Escopo: 5/67 Effects adicionais com contrato técnico estático documentado; 10/67 Effects certificados após este lote, 28/85 glyphs, 28/138 fichas Ars e 28/2.075 fichas globais. 0/164 providers completos.** Esses percentuais não medem hooks, mods integralmente verificados ou sucesso no cliente.

Source imutável: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`; artefato publisher `ars_nouveau-1.21.1-5.13.1.jar`, SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd`. A identidade dos glyphs foi conferida com o [roster compiled SHA-exato](EXACT-BINARY-GLYPH-RITUAL-IDS-5.13.1.md), mas isso **não** equivale a execução observada do source em profile físico.

| Glyph | Eixo causal para perks | Condição de bloqueio |
|---|---|---|
| [Harm](glyphs/effects/harm.md) | **Poison em vez de dano** quando houver Time augment e LivingEntity; damage via IDamageEffect em outro ramo; defaults 5+2×amp | ⛔ Sem branch-preserving adapter e confirmação de settlement |
| [Explosion](glyphs/effects/explosion.md) | Raio configurado separado de `ANExplosion.baseDamage` e exposure/dano; Extract muda BlockInteraction; onExplosionStart cancela | ⛔ Sem orçamento, proteção e event/geometry QA |
| [Lightning](glyphs/effects/lightning.md) | Spawna LightningEntity; dano wet/energy-capability por alvo, Shocked e hooks em tick; possível restauração de damage pendente após evento cancelado | ⛔ Sem contrato seguro de spawn/settlement |
| [Freeze](glyphs/effects/freeze.md) | Slowness LivingEntity versus grade AOE/Pierce×7 tentativas de water/ice/lava/fire e ShapersFocus | ⛔ Sem bound/claims/rollback verificados |
| [Ignite](glyphs/effects/ignite.md) | FireTicks em entidade; blocos Sensitive MAGIC_FIRE versus candle/campfire/fogo normal com claim helper no ramo normal | ⛔ Sem proteção de mundo auditada end-to-end |

**Auditorias de consumidores downstream existentes:** [ANExplosion](glyphs/effects/explosion.md), [LightningEntity](glyphs/effects/lightning.md), [SpellUtil](glyphs/effects/freeze.md), [IPotionEffect](glyphs/effects/harm.md) e [IDamageEffect](glyphs/effects/harm.md) são referenciados nas fichas e fonte imutável. Cada classe conserva sua responsabilidade. `SPELL_MODIFIER` ou qualquer outro evento público não valida automaticamente perk alterando world-effects ou settlement.

**Gates:** `STATIC_TECHNICAL_CATALOG_ONLY`, `PINNED_SOURCE_PLUS_SHA_EXACT_BINARY_IDENTITY`, `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`. Sem novo spell, versão, hook, Java, Stage, contrato entre sibling projects ou alteração de modlist. Testes documentais e CI não promovem Stage 06.05/09.
