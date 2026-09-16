# Goety Iron 3.1 — exact-artifact semantic closure

## Estado canônico do catálogo

- JAR físico: `GoetyIron-1.21.1-NeoForge-3.1.jar`
- Mod ID: `goetyiron`
- versão: `3.1`
- Minecraft: `1.21.1`
- loader: NeoForge
- CurseForge project/file: `1367643 / 8662179`
- SHA-1 físico e auditado: `c8529867e798661ed01fb2948abda23735888fc6`
- licença publicada: **DIVERGENTE** — CurseForge declara MIT; Modrinth declara All Rights Reserved; Black Arcana mantém a postura clean-room mais restritiva
- classificação: `BRIDGE_COMPAT + SPELL/RITUAL CONTENT`
- estado semântico: `COUNTED_EXACT`
- contribuição semântica: **14**
- componente técnico: **#59** após Phase 2BL

A Phase 2BL substitui o antigo limite publisher-only por evidência do JAR exato hash-matched. O artefato não é redistribuído; os artifacts de evidência preservam somente hashes, metadata, signatures/registry identities, resource paths, conditions e resumos de outcome.

## Inventário semântico exato

O provider registra exatamente **2 Focuses próprios**:

- `FIERY_FOCUS`
- `TARNISHED_FOCUS`

Ambos são superfícies `MagicFocus` do Goety ligadas a spells de summon próprios do addon. Nenhuma dessas identidades está entre os 123 Focuses ativos já contados no Goety 3.1.4 base.

O JAR empacota **14 recipes `goety:ritual`**. Dois são apenas caminhos de aquisição dos dois Focuses e não são recontados. Os **12 rituais não-Focus** restantes têm outcomes distintos e nenhuma condition de mod carregado. O conjunto inclui conversões/summons de servants e três outcomes de item/estado (`goetyiron:hemolytic_ring`, `irons_spellbooks:rotten_spell_book` e conversão para `goety:heretic_servant`), sem duplicar os 238 outcomes distintos do inventário Goety-base canônico.

Portanto: **2 Focus + 12 rituais não-Focus = 14 objetos mágicos semânticos `COUNTED_EXACT`.**

## Gate de registration/config

O passe estrutural do initializer prova:

- Focus holders: `2`;
- branches no static initializer do registry: `0`;
- chamadas `DeferredRegister.register` observadas no initializer: `22`;
- referências a config no initializer: `0`;
- campos config enable/disable-like: `0`.

Logo os dois Focuses não dependem de um gate provider-specific de registration/config. Configs de atributos, balance e replacement behavior continuam runtime/balance QA, não identidade semântica.

## Authority e deduplicação

- Goety continua authority de Soul Energy, Focus framework e servant ownership/lifecycle.
- Iron's continua authority de seus spells, entidades e atributos-base.
- Goety Iron é authority apenas das adaptações, Focuses, rituais e servants que ele próprio registra.
- Black Arcana não cria segundo Soul ledger, segundo servant state, segundo cast pipeline nem double-processing.

## Evidência

- NON-MERGE PR #205, HEAD `1feb07a7b9c721a0851e374ebe27c8dc748191fc`;
- structural run `34704435612`, artifact `10301537361`, digest `sha256:c39d4aff68878e34aa3a88e5bd07bf12b6b6616030b5ba20789bdff1e4fd7445`;
- targeted semantic run `34704813857`, artifact `10301716793`, digest `sha256:ec1e35546743ccd9e39763e664fd236336d84278ef74036b0c70b50eba73b7ff`;
- registration/config run `34705555893`, artifact `10301284496`, digest `sha256:28ce5ae85692e82c23b3bae8bc5a7ef29c90006ac220cd86067c55fe9b854973`.

Runtime servant lifecycle, spell settlement, cross-addon compatibility, generated config behavior e qualquer adapter Black Arcana permanecem fail-closed até QA/contrato provider-native específico.
