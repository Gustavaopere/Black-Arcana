# Hazen N Stuff 1.4.0.14 — auditoria binária do registry de 38 magias

**Checkpoint inicial:** 2026-10-14 · Minecraft 1.21.1 / NeoForge / Java 21. **🟡 Auditoria automatizada proposta; ⚠️ nenhum PASS binário afirmado antes de observar a CI do JAR real.**

## Identidade instalada e fonte

- Mod ID: `hazennstuff`; arquivo físico `hazennstuff-1.4.0.14.jar`; SHA-1 esperado da modlist atual `Gustavaopere/neoforge-rpg-skilltree/main@9e6436edb0049a8dcc4e47165db0f6850e5efa68`: `3be20bacb44c1923348ab6f61b685eec6aacfdcd` (item físico #312).
- Arquivo oficial [CurseForge 8277644](https://www.curseforge.com/minecraft/mc-mods/hazen-n-stuff/files/8277644/additional-files), NeoForge 1.21.1, versão `1.4.0.14`, publicação 2026-06-19. O download CDN é candidato até passar o hash físico.
- Fonte release-pinned `Hazentouvel/Hazen_N_Stuff@5fcaf39cf399609f6c1c87d14f8d4807098c9cce`; `Spells/HnSSpellRegistries.java` declara 38 inicializações ativas `registerSpell(new XSpell())` e uma 39ª linha **comentada**, `REIGN_OF_TYROS`, que não deve ser contada. O catálogo canônico [38/38](../../wiki/modpack-catalog/providers/✅-hazen-n-stuff/SOURCE-1.4.0.14-SPELL-INVENTORY.md) é referência factual, sem redistribuir implementação do provider.

## Escopo preciso do gate novo

O workflow `.github/workflows/hazen-14014-binary-audit.yml` executa um teste sintético Java 21 com stubs antes de adquirir o JAR; exige SHA-1 da modlist e `modId=hazennstuff` do `META-INF/neoforge.mods.toml`, e examina `javap -c -p` de `HnSSpellRegistries` e das 38 classes concretas encontradas no archive.

O auditor `docs/qa/hazen_14014_binary_audit.py` exige que cada registro compilado seja rastreável pelo padrão `new classe → dup → invokespecial construtor → invokestatic registerSpell → putstatic campo`. Os pares `classe/campo` precisam coincidir exatamente com as 38 fichas (incluindo a ausência de `reign_of_tyros`). Também confronta o `ResourceLocation.fromNamespaceAndPath("hazennstuff", "spell_id")` inicializado em cada classe com o valor consultado por `getSpellResource()`.

O resultado `PASS` (se observado) comprova **apenas esses 38 registros compilados e os IDs encontrados nos 38 construtores do JAR exato**, sem executar Minecraft, sem inspecionar todas as branches de efeitos e sem certificar a equivalência total entre source e binário. Um desvio retorna `UNPROVEN_OR_MISMATCH`; arquivo diferente, hash incorreto, metadados inválidos, classes ausentes e falha de ferramenta retornam `FAIL_CLOSED`. O workflow publica somente JSON de evidência, não o JAR de terceiros.

## Validação pendente e clean-room

- ⚠️ **PENDING:** identificação dos 38 spells dentro de um registry Iron's **carregado**, testes em servidor dedicado/Survival, disponibilidade em livros/loot/crafting, três gates de inventário Golden Shower/Night's Edge/Scorching Slash, mod configs, GeckoLib/animation, bônus de equipamento, PvP/claims e gestão de mana.
- ⛔ RPG Skill Tree Mastery/perks sem contrato real homologado; Black Arcana não duplica o casting, mana nem efeitos provider-owned. Stage 06.05 segue sem promoção; Stage 09 conserva a aceitação física D035.
- **Campanha global na abertura:** ✅ 27/39 `COUNTED_EXACT` e ⚠️ 12/39 condicionados; nenhum dos 38 objetos é identidade semântica nova nesta PR. Não promover a 28/39 sem CI binária exata e reconciliação dos testes/ledgers globais.

**Registro de conclusão:** anotar HEAD, run, hash SHA-256 e contagens **somente após verificá-los**. Qualquer diferença entre o bytecode e a expectativa source-pinned é dado para triagem, não autorização para modificar o provider.
