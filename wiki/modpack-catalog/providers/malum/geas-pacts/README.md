# Malum 1.8.2 — Geas / Pacts / Oaths / Authorities

## Estado

`37 ACTIVE GEAS EFFECT-TYPE IDENTITIES RELEASE-BOUNDED / PACT+OATH+AUTHORITY+CREED SURFACE CLOSED / ACQUISITION+NUMERICAL EFFECTS+RUNTIME/API QA PENDING`

A linha instalada 1.8.2 possui um inventário release-bounded de **37 registros ativos de `GeasEffectType`**: 28 Pacts, 6 Oaths, 2 Authorities e 1 Creed. Esse fechamento é factual para identidade/deduplicação; ele não transforma o registry de Geas em spell/action registry nem autoriza usar internals do provider como contrato de implementação.

## Evidência de intervalo completo 1.8.2

A linha oficial `SammySemicolon/Malum-Mod` para Minecraft 1.21.1 é delimitada por:

- `f56691e56e591a6d8d1859ff119e749375e14d61`, primeiro checkpoint observado com `mod_version=1.8.2`; o pai ainda declara `1.8.1`;
- `03b743a37f3eeb0cc7f4364f0730e1f135f78408`, último checkpoint observado antes de o filho avançar para `1.8.3`.

`MalumGeasEffectTypes.java` possui blob SHA `2aef164fcedae891b2c6805f2edbd8ee48cffbfe` nos dois extremos. A consulta ao histórico Git do próprio caminho durante toda a janela mostra somente o commit inicial `f56691e...`, que já estabelece a versão 1.8.2, e **nenhuma alteração posterior** antes da transição para 1.8.3. Assim, não existe alteração intermediária/reversão desse registry dentro da linha auditada.

## Inventário ativo release-bounded

### 28 Pacts

- `malum:pact_of_defiance`
- `malum:pact_of_the_parasite`
- `malum:pact_of_the_lifeweaver`
- `malum:pact_of_the_warlock`
- `malum:pact_of_the_reaper`
- `malum:pact_of_the_berserker`
- `malum:pact_of_the_fortress`
- `malum:pact_of_the_shield`
- `malum:pact_of_reciprocation`
- `malum:pact_of_the_shattering_addict`
- `malum:pact_of_the_arcanaphage`
- `malum:pact_of_rune_exploitation`
- `malum:pact_of_self_care`
- `malum:pact_of_the_high_priest`
- `malum:pact_of_tidal_affinity`
- `malum:pact_of_patience_repaid`
- `malum:pact_of_the_windswept`
- `malum:pact_of_the_continuing_shot`
- `malum:pact_of_the_cloudskipper`
- `malum:pact_of_the_skybreaker`
- `malum:pact_of_contentedness`
- `malum:pact_of_the_lone_druid`
- `malum:pact_of_the_profane_ascetic`
- `malum:pact_of_the_profane_glutton`
- `malum:pact_of_combustion`
- `malum:pact_of_the_prospector`
- `malum:pact_of_the_blastweaver`
- `malum:pact_of_wyrd_reconstruction`

### 6 Oaths

- `malum:oath_of_the_overkeen_eye`
- `malum:oath_of_the_overburdened_mind`
- `malum:oath_of_the_overeager_fist`
- `malum:oath_of_unmakers_disdain`
- `malum:oath_of_unsighted_resistance`
- `malum:oath_of_the_undiscerned_maw`

### 2 Authorities

- `malum:authority_of_the_inverted_heart`
- `malum:authority_of_the_gleeful_target`

### 1 Creed

- `malum:creed_of_the_blight_eater`

Os protótipos `bond_of_beloved_chains`, `bond_of_deaths_seekers` e `authority_of_crushing_melancholy` aparecem comentados e não são registros ativos; portanto ficam excluídos.

## Relação com os changelogs 1.8 / 1.8.2

Os changelogs publisher-authored já confirmavam nominalmente parte dessa superfície, incluindo Prospector, Profane Glutton, Berserker, Wyrd Reconstruction, Cloudskipper, Overkeen Eye, Unmakers Disdain, Unsighted Resistance e Gleeful Target. O changelog 1.8.2 também altera Lone Druid, High Priest, Prospector e registra a mudança de nome de Pyromaniac para Blastweaver.

`Pact of the Pyromaniac` é, portanto, nome histórico/renomeado e não uma 38ª identidade ativa adicional.

## Contagem semântica

Os **37 registros estão fechados para inventário factual**, mas contribuem **0** ao ledger atual de objetos mágicos semânticos. Esse ledger exclui effects/statuses e conta spell/glyph/rite ou ação sobrenatural discreta equivalente; o registry aqui auditado é explicitamente `GeasEffectType`, isto é, uma superfície de efeito/progressão persistente, não um registry de casts independente.

A contagem é relevante para colisão temática e deduplicação de design, especialmente para Arcana Vincular, mas não deve ser somada como 37 spells/actions.

## Campos ainda não verificados

O inventário ativo e os IDs acima estão fechados release-bounded. Permanecem `NÃO VERIFICADO` quando não sustentados por documentação pública/runtime QA:

- método de aquisição por entrada;
- recipe/ritual ou pré-requisitos de obtenção;
- custos/recursos;
- efeitos quantitativos;
- duração/cooldown;
- condições exatas de ativação/desativação;
- persistência e migração;
- incompatibilidades/mutual exclusion;
- safe public API/hook consumível por Black Arcana ou RPG Skill Tree;
- equivalência byte-a-byte entre source e JAR físico.

## Deduplicação Black Arcana

A superfície instalada de Pacts/Oaths/Authorities/Creed bloqueia qualquer alegação de novidade baseada apenas em:

- “pacto permanente”;
- “oath”;
- “tradeoff persistente”;
- “authority” como nome temático.

Arcana Vincular só permanece semanticamente distinta se conservar sua arquitetura aprovada de **typed persistent relationships, external resource authority, transactional reserve/commit/refund, consent/ownership/protection, lifecycle e recursion prevention**.

Nenhuma integração futura deve gravar estado Malum diretamente ou duplicar o settlement de um Geas provider-owned.