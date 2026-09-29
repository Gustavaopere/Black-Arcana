# Ozymandias Sundries 0.0.5 — fichas canônicas de spells

Este índice materializa em fichas individuais as **2 identidades de spell provider-owned** fechadas pela auditoria clean-room do artefato físico/publisher exato `ozymandias_sundries-0.0.5.jar`.

O provider permanece **✅ catalogado / COUNTED_EXACT / +2 strict**. A divergência entre distribuição `0.0.5` e metadata interna `0.0.1` é preservada e esta materialização não altera o contador global.

## Spells — 2

- [Levitate](spells/levitate.md)
- [Lightning Warp](spells/lightning-warp.md)

## Registry authority

O registrar exato possui:

- 2 campos finais `Supplier<AbstractSpell>`;
- 2 chamadas `registerSpell(...)`;
- 0 branches condicionais no initializer;
- exatamente duas classes instanciadas e registradas: `LevitateSpell` e `LightningWarpSpell`.

Classes ou localization roots não registrados não criam uma identidade semântica.

## Exclusões

Contribuem **+0**:

- `solar_ray`, porque não possui field/call no registrar atual;
- `PerfectWarriorSpell`;
- `DeathWard`;
- `SolarRay`;
- `SunBurstSpell`;
- `SparkSpell`;
- `WolfPackSpell`;
- equipamentos/spellbooks que apenas embutem ou referenciam spells pertencentes ao host Iron's.

## Authority boundary

Ozymandias Sundries é authority apenas para estas duas identidades adicionais. Iron's Spells 'n Spellbooks continua authority de casting, mana, cooldowns, schools e configuração genérica de spells.

Fontes canônicas: [EXACT-0.0.5-ARTIFACT-AUDIT.md](EXACT-0.0.5-ARTIFACT-AUDIT.md), [SPELL-INVENTORY-EXACT.md](SPELL-INVENTORY-EXACT.md) e [README.md](README.md).
