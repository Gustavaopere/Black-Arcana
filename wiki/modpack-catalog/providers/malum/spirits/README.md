# Malum 1.8.2 — Spirits

## Estado

`9 SPIRIT TYPE IDENTITIES RELEASE-BOUNDED / TYPED SPIRIT RESOURCE SYSTEM PROVEN / DEFERRED-REGISTRY MODEL PROVEN / REAPING+QUERY/CONSUME/REFUND RUNTIME CONTRACTS PENDING`

Tipos de Spirit e suas regras de aquisição/consumo ficam separados de rites, Geas e demais systems. A linha 1.8.2 agora possui inventário nominal release-bounded dos **9 `SpiritArcanaType` base**, mas isso não fecha geração por entidade, quantidades, recipes nem uma API segura de query/consume/refund.

## Authority do recurso

Malum Spirits são recursos tipados provider-owned usados por Spirit Arcana. Eles não são uma barra genérica de mana e não são intercambiáveis automaticamente com:

- Goety Soul Energy;
- Eidolon Soul/Soul Shards;
- Gravebound Souls;
- Iron's mana;
- Vampirism blood;
- Black Arcana Blood Reservoir mB;
- Black Arcana Infernal Lava mB;
- XP/health genéricos.

Qualquer bridge precisa preservar **tipo real + quantidade real + owner causal + settlement exactly-once**.

## Evidência de intervalo completo 1.8.2

A linha oficial `SammySemicolon/Malum-Mod` para Minecraft 1.21.1 é delimitada por:

- `f56691e56e591a6d8d1859ff119e749375e14d61`, primeiro checkpoint observado com `mod_version=1.8.2`; o pai ainda declara `1.8.1`;
- `03b743a37f3eeb0cc7f4364f0730e1f135f78408`, último checkpoint observado antes de o filho avançar para `1.8.3`.

`MalumSpiritTypes.java` tem blob SHA `fa772479f0f73131dabf33d9342299c7e20405e1` nos dois extremos. A consulta ao histórico Git do próprio caminho ao longo de toda a janela retorna **nenhum commit intermediário**, eliminando a hipótese de uma mudança temporária/revertida nesse registry dentro da linha auditada.

## Registry model da linha 1.8

O changelog publisher-authored da geração 1.8 confirma que **Spirit Types** migraram para um Deferred Registry e que os nomes passaram a carregar identificador de mod + nome, com impacto explícito em compatibilidade de terceiros.

Isso é prova arquitetural da linha instalada; a lista nominal abaixo vem da inspeção factual release-bounded do registry, sem promover implementação interna como contrato.

## Inventário base release-bounded — 9 tipos

- `malum:sacred`
- `malum:wicked`
- `malum:arcane`
- `malum:eldritch`
- `malum:aerial`
- `malum:aqueous`
- `malum:earthen`
- `malum:infernal`
- `malum:umbral`

Esses nove registros são identidades de **recurso/tipo**, portanto contribuem **0** ao ledger atual de objetos mágicos semânticos. A contagem não cria uma segunda economia de spirits nem autoriza Black Arcana a gerar, substituir, consumir ou refundar esses recursos.

## O que continua bloqueado

O total e os IDs base de Spirit Types 1.8.2 estão fechados release-bounded. Continuam pendentes:

- recipes e drop/reaping tables por tipo;
- geração exata por entidade;
- quantidade produzida por Spirit Reaping;
- query/consume/refund API pública estável;
- causal hook seguro para converter uma morte em tipos/quantidades reais de spirit;
- compatibilidade runtime exata com Gaze/Ars Hex e outros consumers;
- equivalência byte-a-byte entre source e JAR físico.

## Black Arcana 07.02

A postura canônica permanece fail-closed:

- não sintetizar `death -> Malum spirit` a partir de um evento genérico;
- não adivinhar tipo/count por mob, elemento ou tema;
- não criar um segundo wallet/storage de spirits;
- não consumir/refundar sem boundary provider-native verificado;
- não conceder progressão por mera observação periódica de um saldo.

O fechamento nominal dos nove tipos melhora deduplicação e validação de identidade, mas não altera authority, causalidade ou settlement do runtime Malum.