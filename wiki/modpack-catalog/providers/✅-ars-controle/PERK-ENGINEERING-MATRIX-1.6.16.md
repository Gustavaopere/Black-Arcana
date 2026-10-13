# Ars Controle 1.6.16 — matriz de engenharia por glifo (9/9)

**✅ 9/9 glifos com fichas individuais source-located em PR #796**: 1 effect e 8 filters. Versão física `ars_controle-1.21.1-1.6.16.jar`, SHA-1 `795567371450debec83fe634fd0114c295f7da5a`, IDs do JAR confirmados em auditoria binária anterior. Code pin `Vonr/Ars-Controle@14c5f4770a9ec265491fb9a7ae1a60a2123dfbc0`; host Ars 5.13.1 / NeoForge 21.1.248 no pack. Corpo dos métodos, runtime e QA condicionados.

| Ficha | Classe | Fórmula / boundary específica | Bloqueio |
|---|---|---|---|
| [precise-delay](glyphs/precise-delay.md) | `EffectPreciseDelay` | EventQueue; n Extend Time → 2^n ticks, quando nested event duration+1, max n 20 | ⚠️ scheduler/budget, exactly-once Mastery; adapter RPG ⛔ |
| [filter-above](glyphs/filter-above.md) | `FilterYLevel.ABOVE` | Integer.compare(targetY, (int)(casterY-1))==+1 | ⚠️ singleton field y / negative-Y casting; adapter RPG ⛔ |
| [filter-below](glyphs/filter-below.md) | `FilterYLevel.BELOW` | Integer.compare(targetY, (int)(casterY-1))==-1 | ⚠️ singleton field y / negative-Y casting; adapter RPG ⛔ |
| [filter-level](glyphs/filter-level.md) | `FilterYLevel.LEVEL` | Integer.compare(targetY, (int)(casterY-1))==0 | ⚠️ caster wrapper vs player eye pos; adapter RPG ⛔ |
| [filter-not](glyphs/filter-not.md) | `FilterUnary.NOT` | 1 filtro child não-adaptativo; cursor pula augments; !shouldResolve | ⚠️ validation/NOT nested blocked; adapter RPG ⛔ |
| [filter-or](glyphs/filter-or.md) | `FilterBinary.OR` | 2 children; short-circuit boolean; cursor + skip | ⚠️ `FilterRandom` child2 recebe augments do índice inicial; adapter RPG ⛔ |
| [filter-xor](glyphs/filter-xor.md) | `FilterBinary.XOR` | 2 children; true se resultados distintos | ⚠️ parser e singleton field `res`; adapter RPG ⛔ |
| [filter-xnor](glyphs/filter-xnor.md) | `FilterBinary.XNOR` | 2 children; true se resultados iguais (ambos false também) | ⚠️ parser e singleton field `res`; adapter RPG ⛔ |
| [filter-random](glyphs/filter-random.md) | `FilterRandom.INSTANCE` | base 0.5; AMP>0: 1−0.5/2^AMP; AMP<0: 0.5/2^−AMP | ⚠️ singleton `chance`, RNG provider; sem double-roll; adapter RPG ⛔ |

## Alertas para perks

- `FilterUnary` e `FilterBinary` são partes adaptativas do parser Ars e seus validadores negam chaining. Alterar o contexto não cria segunda cast root; não aplicar dupla mana/cooldown/Mastery.
- `FilterBinary.getFilters()` prepara o segundo filho Random via augments retornados do índice `idx` (o mesmo usado no primeiro), apesar de segundo filho existir em `idx+skip`: possível indexação incorreta, **sem bug de runtime confirmado**.
- As instâncias registry mantêm campos mutáveis `res`, `chance` e `y`; isto exige QA de reentrância em casts concorrentes, mas sem evidência não representa falha comprovada.
- `Precise Delay` 2^20 ticks é teto do shift quando limite de ExtendTime realmente aplicado; não inferir que o host mantém events/chunks por esse tempo nem prometer suporte em Survival.
- O RPG Skill Tree não possui aqui adapter de validação de contexto. Black Arcana mantém casting/world policy próprio; Ars é authority no resolver e scheduler.

Estado: ✅ dossiês/source signatures; ⚠️ host/config/physical/scheduler; ⛔ mutações perks sem contrato/teste. Nenhum código Java, CI ou Survival alterado por esta matriz.

[README](README.md) · [JAR ID](EXACT-BINARY-GLYPHS-1.6.16.md) · [padrão](../../meta/PERK-READY-TECHNICAL-STANDARD.md).
