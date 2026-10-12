# Ars Hex 5.0.4b — ficha única Soul Shatter

Status: **✅ 1/1 glyph provider-owned `COUNTED_EXACT` em registro binário**, **⚠️ configuração/runtime real/Survival condicionados**.

## Pin e escopo

- JAR físico `ars_hex-1.21.1-5.0.4b.jar`, mod ID `ars_hex`, SHA-1 `2354710ea312e2a6e0fbc3eb2dbafb8e06f10cf4`.
- Source retarget para release `Alexthw46/Ars-Unity@b25528adf8c0135585cd6d654582efa147e0a227`; **não** é prova de paridade byte-a-byte com o JAR.
- [GLYPHS.md](GLYPHS.md) e [REGISTRIES.md](REGISTRIES.md) comprovam **uma** identidade de glyph quando `malum` está carregado; Malum é fisicamente presente e o ramo é elegível. Hexerei/Hexcasting são ausentes no pack e seus recursos dormant/orphans **não entram** na contagem.
- A identidade `ars_hex:glyph_soul_shatter` teve [registro binário físico confirmado](EXACT-BINARY-GLYPH-5.0.4b.md) em [#38291974275](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38291974275); o ledger passa a `COUNTED_EXACT` com **+0 novas identidades**, mantendo **1.851 global / 1.849 no escopo solicitado**.
- A semântica de Soul Shatter é dano Voodoo com fórmula de fonte e augments conhecidos; **nenhum RNG/amount de recompensa espiritual está demonstrado na classe**.
- Não ocorre promoção de Stage do Black Arcana. Cost, school compatibility, host version interoperability e teste físico do glyph ficam ⚠️ condicionados.

| # | Registry ID source-pinned | Display | Ficha |
|---:|---|---|---|
| 1 | `ars_hex:glyph_soul_shatter` | Soul Shatter | [Abrir](glyphs/soul-shatter.md) |

**Prova atual:** ✅ `ArsHex.prefix("glyph_soul_shatter")` no JAR SHA-matched, com registro Malum-condicionado e 1 classe de glyph. Isso não aprova execução física. [Matriz exata](EXACT-BINARY-GLYPH-5.0.4b.md).

## Autoridade e limites

Ars Nouveau é autoridade do cast/mana; Malum da liquidação espiritual/damage type; Ars Hex do bridge; Black Arcana não duplica evento, dano, ganho de souls ou casts. Adapter permanece ⛔ fail-closed sem hook exato seguro.

**Clean-room:** dados factuais e limites derivados do dossiê técnico existente; sem copiar assets ou implementação upstream.
