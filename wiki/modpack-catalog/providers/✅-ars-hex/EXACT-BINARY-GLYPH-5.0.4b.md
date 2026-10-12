# Ars Hex 5.0.4b — Soul Shatter com registry binário exato

**✅ 1/1 glifo `COUNTED_EXACT` no registro estático, condicionado à presença de `malum` · ⚠️ runtime completo/configuração/Survival não aprovados.** Segunda promoção entre os **39 providers da campanha original**: **2/39** promovidos, **37/39** permanecem condicionados. **+0** novos objetos, pois Soul Shatter já integrava a contagem.

## Âncora da prova física

- **Artefato físico:** `ars_hex-1.21.1-5.0.4b.jar`, mod ID `ars_hex`, NeoForge Minecraft 1.21.1, posição física **#045**. SHA-1 exigido pela modlist: `2354710ea312e2a6e0fbc3eb2dbafb8e06f10cf4`.
- **Release publicador:** [Ars Hex Unity 5.0.4b, CurseForge arquivo 7404679](https://www.curseforge.com/minecraft/mc-mods/ars-hex-unity/files/7404679), projeto **1357380**, 01/01/2026. O download da publicação teve exatamente o SHA-1 do pack e tamanho **273389 bytes**.
- **Prova binária NON-MERGE:** [workflow #38291974275](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38291974275), branch `audit/ars-hex-504b-physical-soul-shatter-20261012@94a9614d498996b9bd50f0bb548d39de1ba68598`, **SUCCESS**, Java 21 `javap` + enumeração somente de nomes das classes na cópia verificada do JAR. Nenhum JAR, bytecode, receita ou corpo de classe foi integrado.
- **Pré-condição de conteúdo do pack:** Malum está instalado (mod ID `malum`; `malum-1.21.1-1.8.2.jar`) na modlist sibling certificada. Esse fato torna o gate `ModList.isLoaded("malum")` **elegível para registro**, mas não prova que o conjunto completo de mods carregou corretamente em servidor.

## Identidade e gate auditados

| # | Owner | Classe literal no JAR | Registry ID final | Gate de registro | Evidência |
|---:|---|---|---|---|---|
| 1 | `ars_hex` | `EffectSoulShatter` | `ars_hex:glyph_soul_shatter` | `ModList.isLoaded(malum)` | `EXACT_BINARY_STATIC` |

A classe de entrada `ArsHex` referencia exatamente **uma** chamada de `ArsNouveauRegistry.init`. Esta chama `registerCompatGlyphs`, cujo caminho condicionado a `malum` chama `registerMalumGlyphs`. Esse método usa **uma** referência a `EffectSoulShatter.INSTANCE` e **uma** chamada ao helper do addon; o helper contém **uma** chamada a `GlyphRegistry.registerSpell`. O construtor de `EffectSoulShatter` passa a string literal `glyph_soul_shatter` a `ArsHex.prefix`, que constrói namespace `ars_hex` por `ResourceLocation.fromNamespaceAndPath`. A árvore do JAR contém **uma** classe glyph top-level própria, `EffectSoulShatter.class`. Total: **1/1 identidade direta**, sem segundo glifo.

O mesmo registro possui **três** chamadas `PerkRegistry.registerPerk` no ramo Malum: `SoulWardPerk`, `MagicProficencyPerk`, `SpiritSpoilsPerk`. **As perks não são glifos nem três feitiços adicionais**. Partículas Iron's, equipamento `EnchanterScythe`, módulos Hexerei e recursos Hexcasting não são adicionados à contagem de spell roots. Hexerei/Hexcasting não constam no snapshot físico do pack.

## Reconciliação semântica e limites

A identidade `ars_hex:glyph_soul_shatter` constava como `COUNTED_SOURCE_PINNED` (uma identidade) e passa a **`COUNTED_EXACT` apenas na dimensão de ID/registro estático do JAR atual**. **1 objeto continua sendo 1 objeto. +0 novas identidades.** Campanha dos 39: **2/39** proofs exatas (Ars Additions cinco + Ars Hex uma), **37/39** sem fecho; mínimo global **1851** e solicitado **1849** inalterados, denominador de cobertura aberto.

**⚠️ Fora do escopo da prova:** retorno em runtime de `ModList.isLoaded`, carregamento real de todas as dependências (Ars Nouveau 5.13.1 / Malum 1.8.2 / Ars Elemental 0.7.10.1 / Iron's 3.16.3 / Lodestone 1.8.2), recipe manager, desbloqueio do glifo, configuração, custos de mana, dano/espíritos efetivos, ausência de duplicação de Soul Shatter, multiplayer, persistência e Survival. A documentação source-pinned de Tier II, mana, VOODOO, recipe e augments não foi revalidada por esta inspeção do registry binário.

**Authority e clean-room:** Ars Nouveau controla casting/Source; Malum controla dano Voodoo/spirits; Ars Hex controla seu glifo de integração; Black Arcana não clona nenhuma implementação ou duplica dano, resources ou rewards. Stage 06.05 permanece 🟡, sem promoção de aceitação física.

[README](README.md) · [ficha Soul Shatter](glyphs/soul-shatter.md) · [matriz dos 39](../../meta/REVALIDACAO-BINARIA-39-PROVIDERS-2026-10-08.md).
