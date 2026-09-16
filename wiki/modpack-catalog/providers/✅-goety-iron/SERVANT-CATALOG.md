# Goety Iron 3.1 — catálogo público de servants

## Escopo

Este arquivo registra somente entidades e mechanics afirmadas por superfícies publisher-controlled. Ele **não** representa dump de registry nem catálogo técnico completo do JAR.

## Servants nomeados publicamente

As descrições atuais não são idênticas: CurseForge enumera oito servants, enquanto Modrinth enumera esses mesmos oito mais **First Flamebearer Servant**. O changelog oficial pareado de `3.0.0` NeoForge / `2.1.0` Forge também cita First Flamebearer Servant, confirmando sua presença nominal na linha 1.21.1 atual.

Assim, o conjunto público diretamente sustentado é de **pelo menos nove nomes**, sem alegação de completude de registry:

| Nome público | Origem temática | Papel confirmado publicamente | Registry ID | Aquisição exata | Spell set / atributos |
|---|---|---|---|---|---|
| First Flamebearer Servant | Iron's Spells | servant; forma Ominous Trial e armor-swapping citados em 3.0.0/2.1.0 | NÃO VERIFICADO | mecanismo específico não fechado | NÃO VERIFICADO |
| Pyromancer Servant | Iron's Spells | servant comandável | NÃO VERIFICADO | Focus ou ritual em alto nível; mapping específico não verificado | NÃO VERIFICADO |
| Cryomancer Servant | Iron's Spells | servant comandável | NÃO VERIFICADO | idem | NÃO VERIFICADO |
| Cleric Servant | Iron's Spells | servant comandável | NÃO VERIFICADO | idem | NÃO VERIFICADO |
| Archevoker Servant | Iron's Spells | servant comandável | NÃO VERIFICADO | idem | NÃO VERIFICADO |
| Necromancer Servant | Iron's Spells | servant comandável | NÃO VERIFICADO | idem | NÃO VERIFICADO |
| Ancient Knight Servant | Iron's Spells | servant comandável | NÃO VERIFICADO | idem | NÃO VERIFICADO |
| Dead King Servant | Iron's Spells | servant comandável; forma Ominous Trial citada em 3.0.0/2.1.0 | NÃO VERIFICADO | idem | NÃO VERIFICADO |
| Alchemist Servant | Iron's Spells | servant comandável | NÃO VERIFICADO | idem | NÃO VERIFICADO |

As páginas usam linguagem não exaustiva (`currently added include`) e a própria divergência entre CurseForge e Modrinth demonstra que a lista não deve ser promovida a `9/9 registry complete`.

Histórico adicional: o changelog 2.0.0 da linha Forge também cita servant versions de Cultists e Icy Spider. Isso é evidência histórica de release, mas não é promovido silenciosamente a inventário atual 3.1 porque as superfícies atuais auditadas não os reconfirmam.

## Mechanics públicas adicionais

### Focus / ritual acquisition

A página oficial diz que os servants são obtidos por **focus summoning** ou por **transformação e summon via rituals**. Não há evidência pública suficiente para mapear cada servant a um Focus/ritual específico da build 3.1.

### Spell learning

Spellcaster Servants podem aprender spells adicionais. A publicação não expõe o storage, validação, limites, schools aceitas, custo, ownership ou mutation boundary.

### Upgrade orbs

Servants podem ser fortalecidos com upgrade orbs. Tiering, caps, recipes e atributos afetados não são enumerados no material público auditado.

### Spell attributes por servant — release 3.1

O changelog exato da 3.1 adiciona **spell attribute configuration options for each servant**. Isso prova configurabilidade de atributos de spell por servant, mas não o schema nem os defaults.

### Polar Bear replacement — release 3.1

A 3.1 documenta que Polar Bears invocados podem ser substituídos por **Polar Bear Servants**; o replacement pode ser desabilitado em config.

### Vex replacement — release 3.1

A 3.1 documenta que Vexes invocados podem ser substituídos por **Vex Servants**; o replacement pode ser desabilitado em config.

Esses dois mechanics não são usados para declarar automaticamente novos registry entries: o changelog prova o replacement behavior, não a estrutura interna que o implementa.

### Improved Ominous Fire Orbs

A 3.1 corrige Improved Ominous Fire Orbs que podiam ser destruídos por allied mobs. A existência nominal desse mechanic é pública, mas ownership, projectile type, damage e causal provenance permanecem não verificados.

### Tincture of Forgetfulness / Void Vault

A 3.1 adiciona capacidade de a **Tincture of Forgetfulness** resetar o **Void Vault** do Goety. Trata-se de uma mutação explícita de estado Goety mediada pelo addon; Black Arcana não deve duplicar esse state reset.

## Regras de uso no catálogo Black Arcana

- Não converter os nove nomes públicos em registry IDs inventados.
- Não tratar nove nomes como inventário completo da build.
- Não atribuir mana/Soul Energy cost sem evidência exata.
- Não classificar servants como summons Black Arcana.
- Não conceder Mastery por mera presença/tick do servant.
- Qualquer progressão futura exige autoria causal e evento discreto deduplicável.
- Qualquer integração de spell damage deve preservar Iron's/Goety settlement e evitar double-processing.
