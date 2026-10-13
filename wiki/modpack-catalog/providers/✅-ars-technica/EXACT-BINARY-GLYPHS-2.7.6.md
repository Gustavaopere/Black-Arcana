# Ars Technica 2.7.6 — 11 identidades mágicas exatas no JAR físico

**Estado:** ✅ `COUNTED_EXACT` para **11/11 registros estáticos de glyphs**. Dez `Effect*` e um `AugmentSuperheat` foram encontrados, sem branch em `GlyphRegistry.registerGlyphs()`. Este pacote já havia sido catalogado por source: **+0** novas identidades, mínimos **1851 global / 1849 escopo** inalterados. Campanha de 39: **13/39 exatos / 26/39 pendentes**.

## Artefato oficial e validação Java 21

- Sibling modlist física #050: `ars_technica-1.21.1-2.7.6.jar` e SHA-1 `adb2641d538375f6eff6a22f0196bb330ab0b171`.
- Publicador [CurseForge file 7642730](https://www.curseforge.com/minecraft/mc-mods/ars-technica/files/7642730): `ars_technica-1.21.1-2.7.6.jar`, **3691171 bytes**, SHA-1 `adb2641d538375f6eff6a22f0196bb330ab0b171` exatamente igual ao fingerprint físico.
- [Auditoria binária isolada #38342392322](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38342392322) **SUCCESS**, branch `audit/ars-technica-276-static-20261013`, HEAD `7b46b220e92c830c376e23fb1763c71dcae5ca41`.
- Fonte provider usada como contexto anterior: `zeroregard/Ars-Technica@bf34b58ff8908837e5894dee773d3afbd98aa3e3`. O fecho físico **não** se apoia somente na fonte; o SHA e o bytecode do JAR instalado/publicado são verificados.

## Registry e classes comprovadas

A inspeção dos binários `com.zeroregard.ars_technica.ArsTechnica` e `com.zeroregard.ars_technica.registry.GlyphRegistry` confirma a ligação entre entrypoint e `registerGlyphs()`. Onze `register(AbstractSpellPart)` encaminham os objetos à API `com.hollingsworth.arsnouveau.api.registry.GlyphRegistry.registerSpell`, sem instruções de desvio condicional no método. As 11 classes físicas declaradas abaixo existem, inicializam os IDs literais pelo helper `ArsTechnica.prefix` e usam o mod ID `ars_technica`.

| ID | Classe concreta | Tipo |
|---|---|---|
| `ars_technica:glyph_carve` | `EffectCarve` | efeito |
| `ars_technica:glyph_pack` | `EffectPack` | efeito |
| `ars_technica:glyph_polish` | `EffectPolish` | efeito |
| `ars_technica:glyph_obliterate` | `EffectObliterate` | efeito |
| `ars_technica:glyph_press` | `EffectPress` | efeito |
| `ars_technica:glyph_superheat` | `AugmentSuperheat` | augment |
| `ars_technica:glyph_fuse` | `EffectFuse` | efeito |
| `ars_technica:glyph_whirl` | `EffectWhirl` | efeito |
| `ars_technica:glyph_insert` | `EffectInsert` | efeito |
| `ars_technica:glyph_telefeast` | `EffectTelefeast` | efeito |
| `ars_technica:glyph_apply` | `EffectApply` | efeito |

Não adicionar ao denominador blocos/máquinas de Create, armaduras, data components, perk `thread_pressure`, entidades filhas nem recipes de aquisição.

## Condições não aprovadas

**⚠️ Runtime/provider-native:** Ars Technica 2.7.6 foi desenvolvido contra Ars Nouveau 5.11.0.1267 e Create 6.0.8; o modpack físico documenta Ars Nouveau 5.13.1 e Create 6.0.10. Bytecode estático não confirma execução de hooks/mixins nesse conjunto. Permanecem pendentes configuração instalada, aquisição de glyphs no Survival, mana/Source settlement, Source Motor, Transmutation Turret, inventários e fluidos de processamento, world effects, networking e multiplayer, performance e dedicados cliente/servidor. Stage 06.05 segue 🟡.

**Authority:** Ars Nouveau conserva mana, Source, spell context e glyph grammar; Create conserva processamento e cinética; Ars Technica possui apenas a ponte concreta dessas interfaces e seus efeitos; Black Arcana mantém seu próprio cast, hazards e WorldEffectPolicy. Fallback não verificado e duplo debit/proc ficam fail-closed.

**Clean-room:** provas baseadas em hashes, classe/ID e rotas de registro observáveis; não houve importação de código, bytecode ou assets de terceiros.
