# Megido 4.0.3 — fronteiras de targeting, entidades e spawn no onCast

Estado: `EXACT_JAR_SYMBOLIC_ABI_VERIFIED / ENTITY_EFFECTS_AND_TARGET_FILTERS_NOT_VERIFIED / NO_MUTATOR / NO_PHYSICAL_QA`.

## Autoridade e clean-room

O artefato instalado `alshanex_familiars-1.21.1_v4.0.3.jar` tem SHA-1 `e5051c2385a426d05bf203ba8081a23d891f6686`. [Run 40952180943](https://github.com/Gustavaopere/Black-Arcana/actions/runs/40952180943), job `megido_oncast_symbol_references` (SUCCESS), **8 regressões sintéticas** e artifact textual `12931243625`, verificou o mesmo SHA antes de inspecionar `net.alshanex.alshanex_familiars.spells.MegidoSpell`. Auditor: `docs/qa/alshanex_403_megido_oncast_targets.py`. O output contém somente nomes simbólicos/descritores de métodos e contagens agregadas; nenhum corpo de método, bytecode, sequência de instruções ou asset de terceiro foi copiado (All Rights Reserved).

## Referências exatas dentro do onCast

| Símbolo do binário 4.0.3 | Callsites diretos | Limite da conclusão |
|---|---:|---|
| `TargetEntityCastData.getTarget(ServerLevel):LivingEntity` (Iron's) | 1 | Busca/consulta de alvo, não validação de targeting final |
| `MegidoEntity(Level, Entity, Entity)` (Alshanex) | 1 | Construtor referenciado; o papel dos dois parâmetros `Entity` ainda não foi auditado |
| `MegidoEntity.setDamage(float)` (Alshanex) | 1 | Configuração de dano, não quantidade de impactos |
| `BallLightning(Level, LivingEntity)` (Iron's) | 1 | Construtor de entidade do Iron's, não criação incondicional |
| `BallLightning.setDamage(float)` (Iron's) | 1 | Configuração de dano, fórmula e hit count pendentes |
| `BallLightning.setPos(Vec3)` (Iron's) | 1 | Posicionamento, não geometria final |
| `Level.addFreshEntity(Entity):boolean` | **2** | Dois pontos de chamada; **não** equivalem a dois spawns garantidos |
| `getRange():float` e `getRadius():float` (referências não qualificadas) | 1 cada | Getters de retornos literais 15.0F e 10.0F; efeitos geométricos finais pendentes |
| `getDamage(int, LivingEntity):float`, `getMaxConnections(int, LivingEntity):int` (não qualificadas) | 1 cada | `getMaxConnections` retorna `Integer.MAX_VALUE`; alvos/conexões reais não certificados |

Outras referências incluem `MagicData.getAdditionalCastData`, `AbstractSpell.onCast`, `Math.random` (3), `Math.sin` e `cos`, `LivingEntity.getBbWidth/getBbHeight` (2 cada) e coordenadas `getX/Y/Z`. São símbolos de invocação — não reprodução do algoritmo.

O método `onCast` compilado contém **149 instruções**, **4 operações de branch**, **1 `goto`** e **3 operações de alocação**. Sem fluxo de controle e lifecycle efetivos não se pode afirmar número de entidades instanciadas, efeitos por alvo, caps de loop, filtros ou cargas de CPU.

## Fronteiras e pendências de integração

Megido apresenta **fronteira entre dois providers**: Alshanex detém `MegidoSpell`/`MegidoEntity`; Iron's detém `BallLightning`, dados de alvo e parte do casting. O Black Arcana não deve criar dano/entidades/custos em um segundo pipeline; RPG Skill Tree só informa progressão através de contrato real. A implementação física do Iron's **não foi auditada nesta tranche**: seus símbolos foram observados dentro do JAR exato Alshanex 4.0.3.

Permanecem `NOT_VERIFIED`: comportamento de `MegidoEntity` e `BallLightning`, consumidores finais de `Integer.MAX_VALUE`, limites de target/iterations, deduplicação, cooldown, cost, API de mutação, server authority e proteção de mundo. Próximo exame deve usar JAR físico **das entidades e do Iron's instalado**, não extrapolar de calls simbólicos.

`COMPLETE_PERK_READY=0`, `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`. Identidades Alshanex: **7 spells + 11 rituais = 18**, sem mudança de denominador, stage ou índice alfabético.

## Complemento posterior — entidades dos dois JARs físicos (29/10/2026)

O [relatório de lifecycle cruzado](EXACT-4.0.3-MEGIDO-DUAL-ENTITY-LIFECYCLE-20261029.md) corrigiu a lacuna de **ausência de inspeção do JAR Iron's**: o Iron's **3.16.3** SHA-1 `017fd8140c477f9ae602cf95594f1c23bef1d6e3` agora foi diretamente auditado junto com o Alshanex 4.0.3. São provadas ABIs e referências simbólicas de `BallLightning` e `MegidoEntity`, **não** a execução de um cast físico nem a cardinalidade de alvos. Permanecem gates de mutação e multiplayer fail-closed.
