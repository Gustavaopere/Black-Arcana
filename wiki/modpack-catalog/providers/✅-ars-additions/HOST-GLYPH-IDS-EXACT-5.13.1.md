# Ars Additions 21.3.0 + Ars Nouveau 5.13.1 — cinco IDs mágicos binários exatos

**✅ 5/5 `COUNTED_EXACT` (registro estático).** A linha Ars Additions é a **primeira das 39 source/release-bounded originalmente pendentes promovida por prova exata de registry**: **1/39 encerrada para identidade binária**, **38/39 ainda sem prova completa**. Não equivale a aprovação física de disponibilidade em Survival, execução, custos nem compatibilidade funcional.

## JARs e autoridade física

| Papel | JAR exato | SHA-1 da modlist física, reproduzido no publicador | Bytes comprovados | Posição modlist |
|---|---|---|---:|---:|
| Host de glyph/ritual | `ars_nouveau-1.21.1-5.13.1.jar` | `02782d071ee5fab3b5c4b8ced67b7e1748277dfd` | 20107711 | #047 |
| Addon dos cinco roots | `ars_additions-1.21.1-21.3.0.jar` | `ce2440b606acb20b79a42bf7c6c24d163c93241f` | 1458261 | #040 |

Minecraft 1.21.1, NeoForge runtime físico da modlist **21.1.250**; sibling `neoforge-rpg-skilltree/main@06ec1d1d586d4fc3cf957223cfc9ac30077f2875`. CurseForge official project/file **Ars Nouveau 401955/8721482** e **Ars Additions 974408/7646325**; nenhuma versão mais nova do host foi substituída automaticamente.

**Provas reprodutíveis, isoladas NON-MERGE:**
- [#38261401056](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38261401056): addon hash-matched, entrypoint `ArsNouveauRegistry.init`, helpers com **3 glyph + 2 ritual calls**, 1 perk separado, nenhum desvio condicional detectado nos quatro helpers.
- [#38261976223](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38261976223): addon hash-matched, constructor dos três glifos consome `AddonGlyphNames` via `ArsAdditions.prefix`, os dois rituais constroem seus próprios `RESOURCE_LOCATION`.
- [#38266741543](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38266741543) **SUCCESS** no audit commit `dd76bb42242791da7e7a9a8d3b7ee7d0de9b055b`: SHA-1 **ambos** publisher JARs conferido antes da inspeção local com `javap`/Java 21. O `GlyphLib.prependGlyph(String)` do host físico implementa concatenação fixa `glyph_` + argumento, **sem branch** no método; as strings exatas `retaliate`, `mark`, `recall` entram nesse método no addon. O `ArsAdditions.prefix` do addon usa namespace `ars_additions`. Nenhum outro prefixo/namespace é inferido.

## 5/5 raízes mágicas exatas do addon

| # | Tipo | Classe de registro | ID de registro completo | Prova do ID |
|---:|---|---|---|---|
| 1 | `GLYPH` | `MethodRetaliate` | `ars_additions:glyph_retaliate` | `host_prefix_verified` |
| 2 | `GLYPH` | `EffectMark` | `ars_additions:glyph_mark` | `host_prefix_verified` |
| 3 | `GLYPH` | `MethodRecall` | `ars_additions:glyph_recall` | `host_prefix_verified` |
| 4 | `RITUAL` | `RitualChunkLoading` | `ars_additions:ritual_chunk_loading` | `direct_resource_location` |
| 5 | `RITUAL` | `RitualLocateStructure` | `ars_additions:ritual_locate_structure` | `direct_resource_location` |

O registro `ReachPerk` está separado e **não é uma sexta identidade mágica**. Charms, MobEffects, receitas de fabricação, itens, Storage, turrets e compostos de feitiço são superfícies do addon, mas não roots adicionais por mera presença. Todos os cinco owners/IDs são exclusivos ao namespace `ars_additions`, sem deduplicar erradamente glifos do host `ars_nouveau`.

## Gate de promoção e limites

**Estado semântico novo:** na tabela de 39, **Ars Additions 21.3.0** passa de `COUNTED_SOURCE_PINNED` a **`COUNTED_EXACT` para o conjunto mágico 5/5**, porque há igualdade criptográfica com **ambos** JARs físicos, cinco entradas/calls sem desvio de registro nos helpers examinados, resolução do host prefix e exclusão da perk. Não se está promovendo automaticamente os registries de 35 blocos, 61 itens, mob effect, charms, perks ou serializers: a auditoria exata abrange apenas as **cinco raízes mágicas**.

**Sem delta de conteúdo:** cinco identidades *já incluídas* no mínimo, **+0** novas. Preservar **1851 mínimo global / 1849 mínimo no escopo**, denominador final ainda aberto.

**⚠️ QA independente não realizada:** carregamento efetivo de addons/host no modpack completo, configs, habilitação, desbloqueios, receitas/Source/mana/ritual costs, scroll/glyph learning, obtenção em Survival, efeitos reais, multiplayer, persistência, compatibilidade com Ars 5.13.1 e comportamento em servidor dedicado com a instância real. `NO_BRANCH` é observação estática de helper, não um teste completo de inicialização ou compatibilidade. O ritual `ritual_chunk_loading` permanece provider-owned e não dá ao Black Arcana autoridade de force-loading.

**Clean-room:** inspecionadas somente estruturas simbólicas e recursos textuais de identidade; não copiar nem commitar bytecode, corpos de método, assets, JAR ou receitas do publicador. Black Arcana mantém casting e rituais próprios; Ars Nouveau é authority de mana/Source/glyph execution e Ars Additions de seus efeitos.

[Auditoria dos registration helpers](BINARY-REGISTRATION-21.3.0.md) · [inventário do provider](REGISTRIES.md) · [README](README.md) · [rastreamento das 39](../../meta/REVALIDACAO-BINARIA-39-PROVIDERS-2026-10-08.md).
