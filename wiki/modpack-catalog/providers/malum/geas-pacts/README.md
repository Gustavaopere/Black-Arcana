# Malum 1.8.2 — Geas / Pacts / Oaths / Authorities

## Estado

`INSTALLED-LINE EXISTENCE PROVEN / 13 PUBLISHER-NAMED ENTRIES CONFIRMED ACROSS 1.8 + 1.8.2 CHANGELOGS / COMPLETE 1.8.2 REGISTRY UNVERIFIED / ACQUISITION+INTERNALS FAIL-CLOSED`

Esta categoria registra somente Geas/Pacts/Oaths/Authorities que possuem evidência publisher-authored da linha instalada. Protótipos comentados em source, nomes observados apenas na branch posterior 1.9.x e contagens inferidas não contam como gameplay 1.8.2.

## Entradas nomeadas no changelog 1.8

O changelog publisher-authored da geração 1.8, ancorado ao commit exato da linha 1.8.2 identificado no catálogo pai, nomeia explicitamente:

1. `Pact of the Prospector`
2. `Pact of the Profane Glutton`
3. `Pact of the Berserker`
4. `Pact of Wyrd Reconstruction`
5. `Pact of the Cloudskipper`
6. `Oath of the Overkeen Eye`
7. `Oath of Unmakers Disdain`
8. `Oath of Unsighted Resistance`
9. `Authority of the Gleeful Target`

Esses nomes provam presença/alteração na geração 1.8, mas não fornecem por si só registry ID, recipe, acquisition, numerical effect ou runtime hook da build instalada.

## Entradas nomeadas especificamente no changelog 1.8.2

A atualização publisher-authored `1.8.2` nomeia adicionalmente:

10. `Pact of the Lone Druid`
11. `Pact of the High Priest`
12. `Pact of the Blastweaver`

Além disso, `Pact of the Prospector` volta a ser alterado na 1.8.2.

`Pact of the Blastweaver` é documentado como o novo nome de `Pact of the Pyromaniac`. Portanto `Pact of the Pyromaniac` é tratado como **nome anterior/renomeado**, não como uma 13ª entrada ativa adicional.

## Contagem segura

A evidência atual confirma **12 nomes ativos/distintos** mencionados pelos changelogs 1.8/1.8.2, mais um nome histórico renomeado (`Pact of the Pyromaniac`).

Isso **não** equivale a `12/12 COMPLETO`. A branch posterior contém uma superfície maior, mas ela não pode ser retroprojetada para o JAR `1.8.2` sem evidência exata.

## Campos ainda não verificados

Para cada entrada acima permanecem `NÃO VERIFICADO` quando não explicitados pelo changelog público:

- registry/content ID;
- tier/classificação interna;
- método de aquisição;
- custo/recurso;
- efeito quantitativo;
- duração/cooldown;
- condições de ativação/desativação;
- persistência;
- incompatibilidades/mutual exclusion;
- API/hook consumível por Black Arcana ou RPG Skill Tree.

## Deduplicação Black Arcana

A existência instalada de Pacts/Oaths/Authorities é suficiente para bloquear qualquer alegação de novidade baseada apenas em:

- “pacto permanente”;
- “oath”;
- “tradeoff persistente”;
- “authority” como nome temático.

Arcana Vincular só permanece semanticamente distinta se conservar sua arquitetura aprovada de **typed persistent relationships, external resource authority, transactional reserve/commit/refund, consent/ownership/protection, lifecycle e recursion prevention**.

Nenhuma integração futura deve gravar estado Malum diretamente ou duplicar o settlement de um Geas provider-owned.
