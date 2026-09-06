# Wiki Status

`FASE 2 ATIVA — CATÁLOGO / DEDUPLICAÇÃO EM PROGRESSO`

A arquitetura documental da Wiki já está canônica. A implementação das novas escolas continua bloqueada até a Fase 2 provar, provider por provider, quais capacidades já existem no modpack e quais lacunas possuem delta mecânico real.

## Checkpoints canônicos

### Fase 1 — Wiki estrutural

- PR #61 — `docs: build canonical spell wiki catalog`
- merge canônico: `edcc9f8cf1d582681d4b7d2aa1facbcb39b99ae9`
- resultado: estrutura `wiki/`, planos de escolas/sistemas, política provider-native/dedup, proveniência e arquitetura de recursos/bridges tornaram-se canônicos.

### Fase 2 — baseline do catálogo

- PR #62 — `docs: catalog all modpack magic providers`
- merge canônico: `17f87619bc8ed71023bc80d0adb752c13dc8c6c4`
- post-merge CI exata: run `34056029588` / Black Arcana CI #1477 — `SUCCESS`
- resultado: baseline de **101 componentes magic-relevant** reconciliados contra a modlist atual de **607 entradas top-level**, primeiras páginas granulares e matriz inicial `capability → provider → overlap → gap`.

**PR #62 não fechou a Fase 2.** Vários providers continuam com inventário, números, IDs, aquisição ou semantics exatas explicitamente pendentes.

## Passe atual — ecossistema Ars, segunda normalização

O catálogo agora materializa páginas específicas para:

- Ars Additions 21.3.0;
- Ars Zero 2.0.2;
- Ars Technica 2.7.6;
- Ars Creo 5.4.0;
- Ars Elemancy 1.18.3;
- Not Enough Glyphs 4.6.1;
- Ars 'n' Spells 3.2.4;
- Ars Polymorphia 1.0.3.

Também foi criada uma correção canônica de classificação para quatro linhas do baseline #62:

- Ars Creo → `BRIDGE / COMPAT / PROGRESSION`, não glyph provider;
- Ars Elemancy → `GEAR / ENCHANT / SUPPORT CONTENT`, não glyph provider;
- Ars 'n' Spells → bridge Ars Nouveau ↔ Iron's com capacidades/rituais discretos;
- Ars Polymorphia → compat de Storage Lectern/Polymorph, não spell/glyph provider.

A matriz de cobertura foi ampliada para registrar evidência de:

- contingencies / condition-triggered casting;
- stored-reference targeting via Mark/Recall;
- spell containers e cross-engine spellbook casting;
- mana/progression bridge Ars↔Iron's;
- Create-integrated magic/contraption casting;
- geometry, gravity, blight e randomization já presentes no ecossistema Ars.

## Restrições de design já comprovadas pela Fase 2

- **Caos:** generic randomness/probability não é lacuna por si só.
- **Ordem:** boolean logic, runes, geometry, walls, counters e constraints não são lacuna por si só.
- **Arcana Vincular:** simple damage/healing link não é lacuna; o possível delta continua sendo relationship/resource routing tipado e persistente, com lifecycle e transação correta.
- **Cross-engine magic:** generic Ars↔Iron's mana/spellbook unification já possui provider instalado; Black Arcana não deve duplicá-lo.
- **Automação mágica no Create:** Ars Creo/Technica já cobrem partes relevantes; apresentação sombria não cria delta mecânico.
- **Contingency casting:** trigger condicional genérico já é coberto no ecossistema Ars.

## O que ainda bloqueia a Fase 3

Ainda precisam de fechamento/reconciliação suficiente, conforme aplicável:

- Apprentice's Codex;
- Cataclysm: Spellbooks e addons correlatos;
- Dreamless, Leyline, Somake e demais spell addons com tabela pública incompleta;
- Goety 3.1.4 + Goety Cataclysm/Goety Iron onde pertinentes;
- Malum 1.8.2 + Vestis;
- Eidolon:Repraised 0.5.0.2;
- Hexalia 1.3.5 runtime / JAR 1.3.6;
- Toxony 0.10.7;
- Vampirism/Bloodlines/Werewolves e bridges;
- Mobstein 5.4.4;
- Soul Fire'd / Ignis Soulfires e bridges;
- demais providers Ars/Iron's e magical support components ainda sem primitive-level reconciliation;
- aquisição, IDs, custos, cooldowns, fórmulas e authority onde continuam `UNVERIFIED`.

## Fase 3 — continua BLOQUEADA

Não implementar ainda Caos, Ordem, Hemática/Vincular, Infernal, Divina/Celestial ou Bruxaria Integrada apenas a partir dos catálogos candidatos da Fase 1.

A transição só ocorre quando a matriz puder classificar cada candidato relevante como:

- duplicação;
- overlap parcial;
- delta mecânico real;
- ou comportamento não verificável que deve permanecer fail-closed.

## Pendências canônicas independentes

- Familiars & Divination continua seguindo o fluxo próprio do Stage 07.07;
- Stage 08 continua dono do balanceamento final onde os números ainda são TBD;
- QA visual/manual no cliente real não é inferido a partir de CI;
- bugs/discrepâncias de providers externos são registrados como evidência/pendência, não silenciosamente corrigidos pelo Black Arcana.
