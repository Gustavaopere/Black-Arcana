# Malum 1.8.2 — Spirits

## Estado

`TYPED SPIRIT RESOURCE SYSTEM PROVEN / DEFERRED-REGISTRY MODEL PROVEN / EARTHEN ID EVIDENCE PRESENT / COMPLETE 1.8.2 SPIRIT TYPE REGISTRY UNVERIFIED`

Tipos de Spirit e suas regras de aquisição/consumo ficam separados de rites, Geas e demais systems. Cada recurso espiritual só recebe documentação individual quando sua presença e identidade puderem ser ligadas com segurança à build instalada.

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

## Registry model da linha 1.8

O changelog publisher-authored da geração 1.8 confirma que **Spirit Types** migraram para um Deferred Registry e que os nomes passaram a carregar identificador de mod + nome, com impacto explícito em compatibilidade de terceiros.

Isso é prova arquitetural da linha instalada, não uma lista completa dos tipos 1.8.2.

## Identidade exata publicamente observada

O catálogo pai registra evidência datapack/issue da build 1.8.2 para:

- `malum:earthen`

Este ID pode ser tratado como identidade exata observada na linha instalada. Ele **não** autoriza extrapolar os demais tipos a partir da branch 1.9.x.

## O que continua bloqueado

- contagem total de Spirit Types 1.8.2;
- IDs restantes;
- recipes e drop/reaping tables por tipo;
- geração exata por entidade;
- quantidade produzida por Spirit Reaping;
- query/consume/refund API pública estável;
- causal hook seguro para converter uma morte em tipos/quantidades reais de spirit;
- compatibilidade runtime exata com Gaze/Ars Hex e outros consumers.

## Black Arcana 07.02

A postura canônica permanece fail-closed:

- não sintetizar `death -> Malum spirit` a partir de um evento genérico;
- não adivinhar tipo/count por mob, elemento ou tema;
- não criar um segundo wallet/storage de spirits;
- não consumir/refundar sem boundary provider-native verificado;
- não conceder progressão por mera observação periódica de um saldo.

O catálogo só poderá promover a lista completa quando houver evidência exata da build que não dependa de retroprojeção da branch posterior nem de decompilação.