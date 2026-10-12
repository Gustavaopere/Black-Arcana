# Ars Additions 21.3.0 — prova estrutural do registro mágico binário

Estado: **✅ 1/39 providers com prova estrutural do JAR físico / ⚠️ 0/39 promoções completas `COUNTED_EXACT`**. O ledger Ars Additions permanece **`COUNTED_SOURCE_PINNED`**, com **5** raízes já contabilizadas e **+0 novas identidades**.

## Proveniência física e auditável

- Arquivo instalado: `ars_additions-1.21.1-21.3.0.jar`, mod ID `ars_additions`, físico #040 do snapshot certificado de 587 posições; publisher CurseForge projeto/arquivo `974408 / 7646325`.
- SHA-1 físico do sibling e JAR oficial baixado: **`ce2440b606acb20b79a42bf7c6c24d163c93241f`**; verificado em runner GitHub Actions antes da inspeção. Comprimento verificado: **1458261 bytes**.
- Auditorias isoladas **NON-MERGE**, com Java 21 e inspeção local de referências estruturais `javap` (sem copiar bytecode, bodies, JSON ou JAR): [#38261401056](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38261401056), [#38261976223](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38261976223), ambas **SUCCESS**; branch audit `audit/ars-additions-2130-exact-five-magic-register-20261012@dddc142aa8a463f218df6ddb0e6821dc2da9fcab`.
- Source de comparação do provider, somente para semântica/nomes: `Jarva/Ars-Additions@91f102a90dc058cf40e4eac5a67a881e48b856b4`. O SHA-1 do release oficial = SHA-1 físico **não comprova que o source foi usado byte a byte para gerar esse JAR**.

## Matriz exata de chamadas de registro

| # | Tipo | Classe simbólica referenciada | Construção de identidade no JAR | Branch no helper |
|---:|---|---|---|---|
| 1 | `GLYPH` | `MethodRetaliate` | `ars_additions:GlyphLib.prependGlyph(retaliate)` | `NO_BRANCH` |
| 2 | `GLYPH` | `EffectMark` | `ars_additions:GlyphLib.prependGlyph(mark)` | `NO_BRANCH` |
| 3 | `GLYPH` | `MethodRecall` | `ars_additions:GlyphLib.prependGlyph(recall)` | `NO_BRANCH` |
| 4 | `RITUAL` | `RitualChunkLoading` | `ars_additions:ritual_chunk_loading` | `NO_BRANCH` |
| 5 | `RITUAL` | `RitualLocateStructure` | `ars_additions:ritual_locate_structure` | `NO_BRANCH` |

A classe principal `ArsAdditions` referencia `ArsNouveauRegistry.init` uma vez. `init` chama `registerGlyphs`, `registerRituals` e `registerPerks` uma vez cada. Os helpers contêm **3 chamadas de registro de glyph**, **2 de ritual**, **1 de perk**; não há branch nos quatro métodos examinados. O perk `ReachPerk` **não é um sexto objeto mágico**. As duas classes de ritual retornam um ID construído pelo `RESOURCE_LOCATION` provider-owned; `RitualChunkLoading` é a implementação nominal de Arcane Permanence. Os três glyphs usam um método **do Ars host**, `GlyphLib.prependGlyph`, cujo valor resolvido no Ars 5.13.1 instalado não foi executado/confirmado nesta auditoria.

Os IDs de glyph `ars_additions:glyph_retaliate`, `ars_additions:glyph_mark` e `ars_additions:glyph_recall` continuam **source/guide-pinned**, não resultado binário final extraído da função do host. As duas construções rituais `ars_additions:ritual_chunk_loading` e `ars_additions:ritual_locate_structure` foram verificadas diretamente.

## Limites e contabilidade

**1/39 auditorias estruturais com SHA-matched JAR; 38/39 ainda sem auditoria estrutural; 0/39 promoções de ledger a `COUNTED_EXACT`.** Ainda faltam a resolução externa de `GlyphLib.prependGlyph` no host físico, possíveis config/gates de pós-registro, comportamento do host Ars 5.13.1 contra a baseline source Ars 5.11.2, integração da instância e obtenção real em Survival. `NO_BRANCH` nos helpers não equivale a magias habilitadas. O ritual de chunkloading **não autoriza force-loading** pelo Black Arcana.

Sem novas identidades: **5 `COUNTED_SOURCE_PINNED`**, mínimos **1851 global / 1849 escopo** inalterados. Runtime mágico permanece na autoridade de Ars Nouveau/Ars Additions; Black Arcana aplica fail-closed a bridges sem API validada. Conteúdo documentado é apenas evidência factual clean-room, não redistribuição de implementação do provider.

[README](README.md) · [registry source-pinned](REGISTRIES.md) · [matriz das 39 pendências](../../meta/REVALIDACAO-BINARIA-39-PROVIDERS-2026-10-08.md).
