# Provedores source/release-bounded — roteiro de verificação binária

**Quarta prova física independente, 2026-10-12:** Dreamless Spells 1.1.9, [run #38302406303](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38302406303), comprovou o SHA-1 físico versus JAR oficial e quatro classes/registrations de spells; [dossiê](../providers/✅-dreamless-spells/EXACT-BINARY-SPELLS-1.1.9.md). Campanha **4/39 exatos, 35/39 pendentes**, +0 novos; versões anteriores deste documento são checkpoints históricos.

**Terceira prova independente (2026-10-12):** Crystal Chronicles 0.1.3-alpha, registro `crystal_chronicles:prismatic_portal` físico e publicado com SHA-1 idêntico. [Run #38298343874](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38298343874). Campanha 3/39 exatos e 36/39 condicionados. Nenhuma nova magia.

**Estado atualizado 2026-10-12:** roster original congelado de **39** providers source/release-bounded. **✅ 4/39 `COUNTED_EXACT` para roots mágicas** (Ars Additions 5/5, Ars Hex 1/1 sob gate Malum, Crystal Chronicles 1/1, Dreamless Spells 4/4); **⚠️ 35/39** ainda carecem de prova binária exata. Runtime real, configuração, aquisição e Survival seguem gates independentes; **+0** novos objetos.

Snapshot: `Black-Arcana/main@9141a8ed1c345db4e995e5f2aa849df2c24769b9` / sibling modlist `de80b186357cad20ba5b81892a8682777e96e35a`.

Uma correspondência entre **nome/versão do arquivo JAR** e o ledger já foi comprovada para 69 providers presentes pelo [crosswalk](PHYSICAL-LEDGER-VERSION-RECONCILIATION-2026-10-08.md); essa operação não lê registry nem garante os mesmos bytes de release pública.

| Provider | Linha/version ledger | Quantidade já identificada | Evidência semântica atual | Evidência para promover registry |
|---|---|---:|---|---|
| [Ars Nouveau](../providers/✅-ars-nouveau/README.md) | 5.13.1 | 109 | COUNTED_SOURCE_PINNED | ⚠️ Exato JAR SHA + enumeração exaustiva das identidades + condições de registro + deduplicação; **não executado neste lote** |
| [Ars Additions](../providers/✅-ars-additions/README.md) | 21.3.0 | 5 | COUNTED_EXACT | ✅ [cinco IDs binários finais (host Ars 5.13.1 + addon 21.3.0)](../providers/✅-ars-additions/HOST-GLYPH-IDS-EXACT-5.13.1.md), ambos JARs SHA físico/pub verificados [#38266741543](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38266741543); 3 glifos + 2 rituais, 1 perk não contada; +0. ⚠️ config/Survival/runtime não aceitos |
| [Ars Controle](../providers/✅-ars-controle/README.md) | 1.6.16 | 9 | COUNTED_SOURCE_PINNED | ⚠️ Exato JAR SHA + enumeração exaustiva das identidades + condições de registro + deduplicação; **não executado neste lote** |
| [Ars Technica](../providers/✅-ars-technica/README.md) | 2.7.6 | 11 | COUNTED_SOURCE_PINNED | ⚠️ Exato JAR SHA + enumeração exaustiva das identidades + condições de registro + deduplicação; **não executado neste lote** |
| [Ars Hex](../providers/✅-ars-hex/README.md) | 5.0.4b | 1 | COUNTED_EXACT | ✅ [1/1 glifo `ars_hex:glyph_soul_shatter` de registry físico exato](../providers/✅-ars-hex/EXACT-BINARY-GLYPH-5.0.4b.md); [run #38291974275](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38291974275), SHA-1 `2354710ea312e2a6e0fbc3eb2dbafb8e06f10cf4`; condicionado a `ModList.isLoaded(malum)`, Malum instalado; 3 perks excluídas, +0; ⚠️ runtime/Survival não testados |
| [Ars Zero](../providers/✅-ars-zero/README.md) | 2.0.2 | 12 | COUNTED_RELEASE_BOUNDED | ⚠️ Exato JAR SHA + enumeração exaustiva das identidades + condições de registro + deduplicação; **não executado neste lote** |
| [Ars Elemental](../providers/✅-ars-elemental/README.md) | 0.7.10.1 | 47 | COUNTED_SOURCE_PINNED | ⚠️ Exato JAR SHA + enumeração exaustiva das identidades + condições de registro + deduplicação; **não executado neste lote** |
| [Ars 'n' Spells](../providers/✅-ars-n-spells/README.md) | 3.3.4 | 5 | COUNTED_RELEASE_BOUNDED | ⚠️ Exato JAR SHA + enumeração exaustiva das identidades + condições de registro + deduplicação; **não executado neste lote** |
| [Apprentice's Codex](../providers/✅-apprentice-codex/README.md) | 0.9.7.1 | 83 | COUNTED_SOURCE_PINNED | ⚠️ Exato JAR SHA + enumeração exaustiva das identidades + condições de registro + deduplicação; **não executado neste lote** |
| [Backported Spellbooks](../providers/✅-backported-spellbooks/README.md) | physical 0.1.2 / embedded 0.1.0 | 6 | COUNTED_RELEASE_BOUNDED | ⚠️ Exato JAR SHA + enumeração exaustiva das identidades + condições de registro + deduplicação; **não executado neste lote** |
| [Deeper & Darker Spellbooks](../providers/✅-deeper-and-darker-spellbooks/README.md) | 1.3.3 Version B | 4 | COUNTED_RELEASE_BOUNDED | ⚠️ Exato JAR SHA + enumeração exaustiva das identidades + condições de registro + deduplicação; **não executado neste lote** |
| [Discerning The Eldritch](../providers/✅-discerning-the-eldritch/README.md) | 1.4.4 | 22 | COUNTED_SOURCE_PINNED | ⚠️ Exato JAR SHA + enumeração exaustiva das identidades + condições de registro + deduplicação; **não executado neste lote** |
| [Dreamless Spells](../providers/✅-dreamless-spells/README.md) | 1.1.9 | 4 | COUNTED_EXACT | ✅ [4/4 spell IDs binários estáticos](../providers/✅-dreamless-spells/EXACT-BINARY-SPELLS-1.1.9.md), file 7905334, SHA-1 `d51960bfb8af1aafa5d716ef9a48c3135f36b956`, [run #38302406303](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38302406303); +0 novos; ⚠️ config/Emptied/Counterspell/Survival |
| [GTBC's Geomancy Plus](../providers/✅-gtbcs-geomancy-plus/README.md) | 1.1.0-1.21.1 | 12 | COUNTED_RELEASE_BOUNDED | ⚠️ Exato JAR SHA + enumeração exaustiva das identidades + condições de registro + deduplicação; **não executado neste lote** |
| [Farmer's Spell 'n Spellbooks](../providers/✅-farmers-spell/README.md) | 1.0.5.1-1.21.1 | 6 | COUNTED_SOURCE_PINNED | ⚠️ Exato JAR SHA + enumeração exaustiva das identidades + condições de registro + deduplicação; **não executado neste lote** |
| [SnackPirate's Aeromancy Additions](../providers/✅-aeromancy-additions/README.md) | 1.2.8 | 10 | COUNTED_SOURCE_PINNED | ⚠️ Exato JAR SHA + enumeração exaustiva das identidades + condições de registro + deduplicação; **não executado neste lote** |
| [Hazen N Stuff](../providers/✅-hazen-n-stuff/README.md) | 1.4.0.14 | 38 | COUNTED_SOURCE_PINNED | ⚠️ Exato JAR SHA + enumeração exaustiva das identidades + condições de registro + deduplicação; **não executado neste lote** |
| [Ender's Spells and Stuff: Requiem](../providers/✅-enders-spells-and-stuff-requiem/README.md) | 0.1.7 | 53 | COUNTED_SOURCE_PINNED | ⚠️ Exato JAR SHA + enumeração exaustiva das identidades + condições de registro + deduplicação; **não executado neste lote** |
| [Fire's Ender Expansion](../providers/✅-fires-ender-expansion/README.md) | 2.4.1 | 11 | COUNTED_SOURCE_PINNED | ⚠️ Exato JAR SHA + enumeração exaustiva das identidades + condições de registro + deduplicação; **não executado neste lote** |
| [IronSable](../providers/✅-ironsable/README.md) | 1.2.0 | 7 | COUNTED_RELEASE_BOUNDED | ⚠️ Exato JAR SHA + enumeração exaustiva das identidades + condições de registro + deduplicação; **não executado neste lote** |
| [ISS: Magic From The East](../providers/✅-iss-magic-from-the-east/README.md) | 1.1.5 | 22 | COUNTED_SOURCE_PINNED | ⚠️ Exato JAR SHA + enumeração exaustiva das identidades + condições de registro + deduplicação; **não executado neste lote** |
| [Legendary Spellbooks](../providers/✅-legendary-spellbooks/README.md) | 0.3.2 | 30 | COUNTED_SOURCE_PINNED | ⚠️ Exato JAR SHA + enumeração exaustiva das identidades + condições de registro + deduplicação; **não executado neste lote** |
| [Monsters & Spellbooks](../providers/✅-monsters-spellbooks/README.md) | 0.0.16.3 | 98 | COUNTED_RELEASE_BOUNDED | ⚠️ Exato JAR SHA + enumeração exaustiva das identidades + condições de registro + deduplicação; **não executado neste lote** |
| [Paladin Spells](../providers/✅-paladin-spells/README.md) | 1.1.1 | 5 | COUNTED_SOURCE_PINNED | ⚠️ Exato JAR SHA + enumeração exaustiva das identidades + condições de registro + deduplicação; **não executado neste lote** |
| [Wind's Spellbooks](../providers/✅-winds-spellbooks/README.md) | 1.0.5 | 7 | COUNTED_RELEASE_BOUNDED | ⚠️ Exato JAR SHA + enumeração exaustiva das identidades + condições de registro + deduplicação; **não executado neste lote** |
| [Ypsilon's Fundamentalism](../providers/✅-ypsilons-fundamentalism/README.md) | 1.1.7.1 | 15 | COUNTED_SOURCE_PINNED | ⚠️ Exato JAR SHA + enumeração exaustiva das identidades + condições de registro + deduplicação; **não executado neste lote** |
| [Tunes n' Tomes](../providers/✅-tunes-n-tomes/README.md) | 1.1.0-HOTFIX | 16 | COUNTED_RELEASE_BOUNDED | ⚠️ Exato JAR SHA + enumeração exaustiva das identidades + condições de registro + deduplicação; **não executado neste lote** |
| [Companions!](../providers/✅-companions/README.md) | 1.3.4 | 9 | COUNTED_SOURCE_PINNED | ⚠️ Exato JAR SHA + enumeração exaustiva das identidades + condições de registro + deduplicação; **não executado neste lote** |
| [Crystal Chronicles](../providers/✅-crystal-chronicles/README.md) | 0.1.3-alpha | 1 | COUNTED_EXACT | ✅ [prova binária estática 1/1](../providers/✅-crystal-chronicles/EXACT-BINARY-SPELL-0.1.3-alpha.md), file 8346590, SHA-1 `afdc32ab27661cd52160280dc4273d70a2d4a3d2`, [run #38298343874](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38298343874); +0 novos, ⚠️ Survival/config/portal pendentes |
| [Reliquified Ars Nouveau](../providers/✅-reliquified-ars-nouveau/README.md) | 0.8.1 | 19 | COUNTED_SOURCE_PINNED | ⚠️ Exato JAR SHA + enumeração exaustiva das identidades + condições de registro + deduplicação; **não executado neste lote** |
| [Reliquified Artifacts](../providers/✅-reliquified-artifacts/README.md) | 1.0.8 | 52 | COUNTED_SOURCE_PINNED | ⚠️ Exato JAR SHA + enumeração exaustiva das identidades + condições de registro + deduplicação; **não executado neste lote** |
| [Reliquified Iron's Spells 'n Spellbooks](../providers/✅-reliquified-irons-spells-n-spellbooks/README.md) | 0.2.7 | 25 | COUNTED_SOURCE_PINNED | ⚠️ Exato JAR SHA + enumeração exaustiva das identidades + condições de registro + deduplicação; **não executado neste lote** |
| [Waystones](../providers/✅-waystones/README.md) | 21.1.45 | 3 | COUNTED_SOURCE_PINNED | ⚠️ Exato JAR SHA + enumeração exaustiva das identidades + condições de registro + deduplicação; **não executado neste lote** |
| [Eidolon: Repraised](../providers/✅-eidolon-repraised/README.md) | 0.5.0.2 | 42 | COUNTED_SOURCE_PINNED | ⚠️ Exato JAR SHA + enumeração exaustiva das identidades + condições de registro + deduplicação; **não executado neste lote** |
| [Vampirism](../providers/✅-vampirism/README.md) | 1.10.13 | 19 | COUNTED_SOURCE_PINNED | ⚠️ Exato JAR SHA + enumeração exaustiva das identidades + condições de registro + deduplicação; **não executado neste lote** |
| [Bloodlines](../providers/✅-bloodlines/README.md) | 3.0.9 | 28 | COUNTED_SOURCE_PINNED | ⚠️ Exato JAR SHA + enumeração exaustiva das identidades + condições de registro + deduplicação; **não executado neste lote** |
| [Werewolves](../providers/✅-werewolves/README.md) | 2.0.3.3 | 8 | COUNTED_SOURCE_PINNED | ⚠️ Exato JAR SHA + enumeração exaustiva das identidades + condições de registro + deduplicação; **não executado neste lote** |
| [Hexalia](../providers/✅-hexalia/README.md) | 1.3.7 | 29 | COUNTED_SOURCE_PINNED | ⚠️ Exato JAR SHA + enumeração exaustiva das identidades + condições de registro + deduplicação; **não executado neste lote** |
| [Malum](../providers/✅-malum/README.md) | 1.8.2 | 26 | COUNTED_RELEASE_BOUNDED | ⚠️ Exato JAR SHA + enumeração exaustiva das identidades + condições de registro + deduplicação; **não executado neste lote** |

## Fechamento condicional do Ars Hex — segundo provider binário, 2026-10-12

[Run #38291974275](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38291974275) extraiu só contagens/ID/path do JAR exato Ars Hex 5.0.4b após comparação criptográfica com a modlist; comprovados **1 glyph**, `malum` gate, registro Ars `GlyphRegistry.registerSpell`, três perks fora da contagem. [Dossiê exato](../providers/✅-ars-hex/EXACT-BINARY-GLYPH-5.0.4b.md). Campanha original agora **2/39 `COUNTED_EXACT` / 37/39** pendentes. Isso não prova carregamento integral de Malum/Ars nem aquisições/Survival e não acrescenta identidade mágica.

## Fechamento do host binário — Ars Additions 21.3.0, 2026-10-12

A [matriz exata 5/5](../providers/✅-ars-additions/HOST-GLYPH-IDS-EXACT-5.13.1.md) demonstra `GlyphLib.prependGlyph` na versão física **Ars Nouveau 5.13.1** (SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd`) e as construções de identidade no **Ars Additions 21.3.0** (SHA-1 `ce2440b606acb20b79a42bf7c6c24d163c93241f`). A auditoria [#38266741543](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38266741543) verificou os dois binários antes de emitir IDs. **1/39 promoção completa em registro mágico**, **38/39 pendentes**; **+0 magias**, 1851/1849 mínimos mantidos. Não há PASS de compatibilidade funcional, config ou Survival.

## Checkpoint pós-snapshot — Ars Additions 21.3.0, 2026-10-12

A evidência [#38261401056](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38261401056) e [#38261976223](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38261976223) prova **1/39** registros estruturais binários no mesmo artefato SHA-matched ao físico, incluindo 3 glyphs + 2 rituais e 1 perk excluído. O host `GlyphLib.prependGlyph` não foi resolvido: **0/39 promoções completas**; preservar todos os 39 itens originais no quadro e os 5 objetos previamente contados.

## Coleta física reproduzível — integridade dos 69 fingerprints (2026-10-10)

O coletor read-only `docs/qa/physical_provider_fingerprint_collector.py` lê os JARs correspondentes às **69 linhas** do crosswalk físico. Executar, a partir da raiz do Black Arcana, somente quando houver acesso autorizado à cópia real da instância:

```bash
python3 docs/qa/physical_provider_fingerprint_collector.py --instance "/caminho/da/instancia" > providers-69-fingerprint.json
```

**Garantia técnica do coletor:** a validação de ZIP e os hashes SHA-1/SHA-256 usam **um único descritor aberto por arquivo**, com `O_NOFOLLOW` quando disponível e comparação de identidade/tamanho/`mtime`/`ctime` antes e depois. O status `CHANGED_DURING_SCAN` recusa uma substituição ou gravação detectada durante a leitura **sem emitir hashes**. Outros casos fail-closed incluem `MISSING`, `UNSAFE`, `UNREADABLE`, `OVERSIZED` e `INVALID_JAR`. O procedimento é somente leitura; não carrega mods, não extrai classes nem aplica datapacks. Testes usam artefatos ZIP sintéticos, não JARs físicos de providers.

**Fronteira semântica:** mesmo um resultado `FINGERPRINTED` de **69/69** demonstraria somente integridade de arquivo ZIP e fingerprint daquela coleta; não identifica os 39 registries de spells, não prova correspondência a publicação oficial, não certifica config/Survival nem autoriza promover `COUNTED_SOURCE_PINNED`/`COUNTED_RELEASE_BOUNDED` para `COUNTED_EXACT`. Conferir JAR real, provenance, IDs de registry, gates e deduplicação **por provider** antes de mudar qualquer linha. **Nenhuma execução nos JARs reais nem promoção de contagem foi realizada nesta revisão.**

## Requisitos mínimos para encerrar cada linha

- Capturar **bytes do JAR da instância efetiva** ou uma fonte oficialmente reproduzível com igualdade criptográfica verificável, usando a modlist física atual como identidade do artefato.
- Inventariar apenas spell/ritual/glyph/discrete player-owned magical roots; documentar também registries excluídos e optional-provider gates para não criar falsos positivos.
- Comparar lista de IDs/nome/owner/namespace/condições e cardinalidade com o dossiê atual; sem correspondência binária não atualizar `COUNTED_SOURCE_PINNED`/`COUNTED_RELEASE_BOUNDED`.
- Revisar consumo, aquisição e configurações como **gate independente**: registry exato não equivale a magia habilitada nem obtenível em Survival.
- Não copiar classes, assets nem código proprietário de providers (clean-room). Reproduzir apenas observações e contratos de interoperabilidade publicados.
