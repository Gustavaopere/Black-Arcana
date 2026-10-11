# Goety Iron 3.1 — `FIERY_FOCUS`

Estado: **✅ CATALOGADO / `COUNTED_EXACT`** para identidade factual de Focus no JAR hash-matched; **⚠️ runtime, spell internals, costs e Survival não verificados**.

## Identidade e proveniência

- **Provider:** Goety Iron, mod ID `goetyiron`; conteúdo próprio do addon, não do Goety base ou de Iron's Spells 'n Spellbooks.
- **Focus holder auditado:** `FIERY_FOCUS`. O holder é um campo/identidade factual de registry evidenciado, **não** uma `ResourceLocation` de spell cujo path foi provado.
- **Ordinal editorial:** 1/2; não é registry index ou ordem de ativação.
- **Artefato exato:** `GoetyIron-1.21.1-NeoForge-3.1.jar`, SHA-1 físico e publisher `c8529867e798661ed01fb2948abda23735888fc6`, CurseForge project/file `1367643 / 8662179` (Modrinth version `YZXNIxvk`).
- **Tipo:** uma superfície `MagicFocus` do Goety vinculada a identidade de magia de summon própria do addon, conforme auditoria factual. O **alvo exato do summon e a classe concreta não estão comprovados por Focus** nesta ficha.
- **Aquisição:** um dos dois rituais `goety:ritual` de aquisição de Focus empacotados. Cada Focus tem uma via de aquisição no pacote; **ingredients, cost, research, prerequisites e sucesso real em Survival: NÃO VERIFICADO**.
- **Inclusão:** Focus incondicional na inspeção restrita do initializer (zero branches de registration, zero config references e zero flags enable/disable-like), mas isso **não** prova que todos os gates de gameplay estejam desabilitados.
- **Contagem:** identidade já incluída nas **2 `COUNTED_EXACT`** do addon; ficha = **+0 identidades semânticas**. Sua recipe de aquisição não vira um ritual adicional.

## Fronteira técnica e de gameplay

- **Runtime registry ID, classe/método, tipo de servo individual, damage, cast time, Soul Energy, cooldown, range, targeting, skills, level, config de atributos, hooks/eventos públicos, lifecycle, entity ownership e world safety:** **NÃO VERIFICADO** na documentação factual do JAR 3.1; não inferir pelo nome do holder.
- Goety é autoridade de Focus/Staff, Soul Energy e servant lifecycle. Iron's é autoridade de suas spell/attribute surfaces; o addon é dono das adaptações e dos registros próprios. Black Arcana não realiza um segundo summon, Soul Energy debit, conjuração, replacement ou progress event sem causalidade provider-native verificável.
- O pack real, as condições de servidor dedicado/cliente e os gates de Survival exigem prova física; os testes de CI do Black Arcana **não** validam conjuração individual do addon.
- A auditoria conta separadamente **12 rituais não-Focus com outcomes distintos**: suas identidades individuais de resource/recipe/signature não estão preservadas nos documentos atuais e **não são inventadas** nesta ficha.

## Evidência e clean-room

[Lista canônica de Focuses e limites dos rituais](../README.md) · [auditoria do artefato](../EXACT-3.1-ARTIFACT-AUDIT.md) · [regras de integração](../INTEGRATION-RULES.md).

Licença declarada é divergente (CurseForge MIT; Modrinth All Rights Reserved). Ficha apenas factual; não contém bytecode, código, recipe JSON, modelos, assets, tooltips ou textos criativos.
