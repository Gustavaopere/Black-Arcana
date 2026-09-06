# Arquitetura candidata — Reservatório Hemático

## Estado

`CONCEITO / PESQUISA — NÃO IMPLEMENTADO`

## Componentes propostos

### 1. Hematic Source Classifier
Server-authoritative. Decide se uma entidade/provider possui sangue utilizável e qual subtype.

### 2. Blood Reservoir Multiblock
Estrutura física que expõe `capacity_mB`, `stored_mB`, identidade persistente e operações transacionais bounded.

### 3. Hematic Link Registry
Mantém vínculos `caster ↔ source`, com ownership/consent, dimensão, distância, tipo e lifecycle.

### 4. Blood Cost Provider
Provider de custo específico da Blood school. Não consulta mana normal. Produz quote/reservation/commit/refund exclusivamente sobre fontes hemáticas permitidas.

### 5. Blood Producer Pipeline
Única fronteira para inserir mB no sistema por extração/coleta legitimamente confirmada. Evita que múltiplos hooks creditem o mesmo evento.

### 6. HUD Snapshot
Snapshot server-authored de capacidade/disponibilidade/reservas e estado dos vínculos.

## Fluxo

`spell request → blood quote → source resolution → reservation → target/gate validation → spell commit → blood commit`

Falha antes do commit libera a reserva. Falha/remoção de source entre quote e settlement faz fail-closed/requote segundo policy explícita.

## Invariantes

- zero mana normal;
- zero regen passiva do reservatório;
- sangue não é vida abstrata;
- uma unidade de mB tem identidade contábil única;
- sem double-credit por dano/kill;
- sem cross-dimension implícito;
- sem consumo client-authoritative;
- sem chunk force-load só para manter vínculo;
- compat providers continuam donos de seus recursos nativos.
