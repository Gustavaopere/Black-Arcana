# Ars Controle 1.6.16 — nove spell parts binários exatos

**Estado de registry:** ✅ `COUNTED_EXACT` **9/9**, um efeito e oito filtros; **+0 novas identidades**, mínimo **1851 global / 1849 escopo**, campanha **12/39 exatos / 27/39 pendentes**.

## JAR exato e metodologia

- JAR físico do sibling #041: `ars_controle-1.21.1-1.6.16.jar`, SHA-1 `795567371450debec83fe634fd0114c295f7da5a`.
- JAR do publicador Modrinth `r7YxZN9m`, **313828 bytes**, SHA-1 `795567371450debec83fe634fd0114c295f7da5a`. Integridade, ZIP e bytecode Java 21 confirmados em [Actions #38339934100](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38339934100) (SUCCESS); HEAD de auditoria `f4cb6998687771c35f1a42f7b5b3736916de1dc8`.
- A execução inicial [#38339462230](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38339462230) falhou por exigir IDs literais completos; no binário real, `ACNames` monta o path por `GlyphLib.prependGlyph`. A segunda auditoria verificou os nove sufixos, os nove calls do host, o registro e o bootstrap.
- Source do release: `Vonr/Ars-Controle@14c5f4770a9ec265491fb9a7ae1a60a2123dfbc0` (checagem de código-fonte anterior). A prova atual é baseada diretamente nos bytes do JAR físico/pub.

## Cadeia e identidades

`ArsControle` → `ACRegistry.register(IEventBus)` → `ACRegistry.Glyphs.registerAll()` → nove chamadas incondicionais `register(AbstractSpellPart)` → `GlyphRegistry.registerSpell` do Ars. O comportamento de `GlyphLib.prependGlyph` do host Ars Nouveau 5.13.1 tem [prova binária independente](../✅-ars-additions/HOST-GLYPH-IDS-EXACT-5.13.1.md), [run #38266741543](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38266741543).

| Tipo | Identidade |
|---|---|
| Efeito | `ars_controle:glyph_precise_delay` |
| Filtro | `ars_controle:glyph_filter_above` |
| Filtro | `ars_controle:glyph_filter_below` |
| Filtro | `ars_controle:glyph_filter_level` |
| Filtro | `ars_controle:glyph_filter_or` |
| Filtro | `ars_controle:glyph_filter_xor` |
| Filtro | `ars_controle:glyph_filter_xnor` |
| Filtro | `ars_controle:glyph_filter_not` |
| Filtro | `ars_controle:glyph_filter_random` |

Outros blocks, items, attachments, data components e block entities já inventariados não são glyphs adicionais.

## Limites do resultado

**⚠️ NÃO PROVADO:** entrada real no registry da instância, execução e custo de Source/mana, atraso, Warping Spell Prism, ticket de chunks, cross-dimension, persistência, configs implantadas, multiplayer, deduplicação e aquisição/Survival. Stage 06.05 permanece 🟡; nenhum PASS físico presumido.

Ars Nouveau detém mana/Source/gramática; Ars Controle detém seus filtros/relays. Black Arcana conserva casting, hazards, custos e WorldEffectPolicy, sem duplicar casts ou introduzir bridge não comprovada. Registro factual clean-room sem copiar código/artefatos do provider.
