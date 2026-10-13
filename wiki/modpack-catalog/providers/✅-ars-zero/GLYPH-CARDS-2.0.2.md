# Ars Zero 2.0.2 — 12 fichas de capacidades de glifo

**Adendo binário 2026-10-13:** as 12 fichas públicas listadas abaixo são históricas. A [prova física](EXACT-BINARY-GLYPHS-2.0.2.md) confirmou os IDs destas 12 e mais **6 novos** (18 próprios únicos), além de 4 cópias opcionais. As fichas de Sustain/Discard/Hollow/Sphere/Cube/Flatten estão em `glyphs/`. Os mínimos atuais são **1.857 global / 1.855 no escopo**; os valores 1.851/1.849 abaixo pertencem ao checkpoint anterior. A prova não certifica gameplay/Survival.


Status: **✅ 12/12 capacidades públicas distintas documentadas** como `COUNTED_RELEASE_BOUNDED` · **⚠️ IDs de registry, internals exatos, aquisição e execução física continuam condicionados**.

## Evidência e limite de fechamento

- Instalação documentada no pack: `ars_zero-1.21.1-2.0.2.jar`, mod ID `ars_zero`, SHA-1 `ac9b6e6f7a2bd403ee7cdc16023509fde7c4e1d0`, NeoForge 1.21.1, CurseForge project/file `1377482 / 8703997`.
- As 12 entradas têm nomes de display e papéis semânticos da [matriz de evidências da release](GLYPH-CATALOG.md). Elas não representam doze `ResourceLocation` extraídos de um registry binário 2.0.2. A fonte pública upstream 1.21.1 é anterior ao release e não é tomada como pin de implementação.
- Já constam no ledger `COUNTED_RELEASE_BOUNDED` como **12 capacidades singulares**. Materializar 12 páginas cria **+0 novas identidades**, preservando os mínimos **1.851 global / 1.849 no escopo solicitado** e o denominador semântico final aberto.
- **Excluídos da contagem singular:** `AOE II`, `AOE III`, `Amplifier II`, `Amplifier III`, compatibilidade copiada desativada por padrão. Não extrapolar augments Cube/Sphere/Flatten/Hollow históricos à build exata 2.0.2.
- Arcane Shield tem prova de atividade via fix da release 2.0.2 e contexto editorial de release anterior, não prova do identificador exato de registry.
- Ars Zero/Ars Nouveau mantêm autoridade de phase casting, mana/Source e world effects; Black Arcana não duplica os mecanismos nem inventa integração. Nenhuma Stage do runtime foi promovida.

## Índice — 12/12

| # | Capacidade pública | Evidência | Ficha |
|---:|---|---|---|
| 1 | Temporal Context Form | official current project page | [Abrir](glyphs/temporal-context-form.md) |
| 2 | Near Form | official current project page | [Abrir](glyphs/near-form.md) |
| 3 | Push | official current project page | [Abrir](glyphs/push.md) |
| 4 | Select | official current project page | [Abrir](glyphs/select.md) |
| 5 | Conjure Voxel | official current project page + 2.0.2 voxel fixes | [Abrir](glyphs/conjure-voxel.md) |
| 6 | Anchor | official current project page + 2.0.2 live-context fix | [Abrir](glyphs/anchor.md) |
| 7 | Remove Gravity | official current project page | [Abrir](glyphs/remove-gravity.md) |
| 8 | Convergence | official current project page | [Abrir](glyphs/convergence.md) |
| 9 | Geometrize | official current project page + 2.0.2 packet security | [Abrir](glyphs/geometrize.md) |
| 10 | Conjure Blight | official current project page + exact 2.0.2 world-safety fixes | [Abrir](glyphs/conjure-blight.md) |
| 11 | Beam | official current project page + exact 2.0.2 lifetime change | [Abrir](glyphs/beam.md) |
| 12 | Conjure Arcane Shield | exact 2.0.2 fixes confirm the active mechanic; older official 2.0.x cross-version notes describe barrier semantics | [Abrir](glyphs/conjure-arcane-shield.md) |

## Validação pendente

**⚠️ JAR exato:** obter evidência factual dos registry IDs, glyph classes, receitas, config e gates individuais; nunca derivar IDs dos nomes exibidos. **⚠️ Survival/QA físico:** testar cada efeito e seus riscos, sem presumir PASS a partir do build do Black Arcana. **⛔ Integração:** sem hooks provider-native comprovados, qualquer adapter permanece fail-closed.

**Clean-room:** páginas refletem campos factuais do catálogo técnico próprio e delimitam explicitamente incertezas; nenhum corpo de código ou asset upstream incorporado.
