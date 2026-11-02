# Raygun 1.0.10 — recorte SHA-exato de targeting e X_RAY

## Escopo

Continuidade do catálogo de **Alex's Caves Continued 1.0.10**, após PR #1014, sem promover prematuramente os dois itens pendentes (Raygun e Tremorzilla Beam). A modlist física do sibling identifica `alexscaves-1.0.10-neoforge+1.21.1.jar` com SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`. A ficha `raygun.md` já possui extensa evidência de charge, danos, rede e codecs, mas não tem a reconstrução fechada do targeting.

A [sonda read-only](alexscaves_1010_raygun_xray_target_probe.py) trabalha sobre a classe `RaygunItem.class` SHA-256 `3fc60cb7ff8be2744becf8ac9e524799349996972708845a124f02650bfb344c` e o método `onUseTick(Level,LivingEntity,ItemStack,int):void`, cujo digest selecionado `b037276094928625e501d13fddd11829e3fe5540d585f7d8213f37b098c39bc5` foi observado anteriormente na PR #985. Registra apenas seis janelas limitadas de opcode/JVM e referências para X_RAY, ray traces e requests de dano, sem distribuir a implementação inteira.

O [workflow](../../.github/workflows/alexscaves-1010-raygun-xray-target.yml) baixa o publisher JAR exato, executa regressões negativas e registra a descoberta. A primeira execução sem `EXACT-RAYGUN-XRAY-TARGET-1.0.10.json` é `UNSEALED DISCOVERY`; o manifesto só deve ser criado com bytes e referências realmente observados. A HEAD final exige execução `--seal` e toda CI verde antes de qualquer merge.

## Critérios de interpretação

- **X_RAY:** registrar onde a leitura do encantamento aparece e quais branches estão ao redor. Não declarar que o encantamento perfura todas as paredes, altera o raio ou ignora claims apenas pela presença do símbolo.
- **Geometria:** separar `ProjectileUtil.getHitResultOnViewVector`, `ProjectileUtil.getEntityHitResult` e `Level.getEntities`. Constantes numéricas, AABB de seleção e distância de ray trace não são automaticamente equivalentes ao alcance final de cada modo.
- **Dano:** `causeRaygunDamage` e `ACCompat.hurt` documentam requests nativos, não dano aceito, número de acertos, owner final ou procs de RPG Skill Tree.
- **Segurança:** `WorldEffectPolicy`, guards de PvP, origem do pacote C2S, integridade de `ChargeUsed`/`UseTime`, QA de cliente/servidor e listeners externos continuam como evidências separadas.

Esta sonda só fecha um **recorte observável** de targeting; não reconstrói todas as arestas do CFG ou fluxo de exceções. `NOT_CERTIFIED`, `NO_MUTATION`, `mutating_hook=NOT_VERIFIED` e `physical_qa=NOT_TESTED` permanecem. Não alterar contadores de fichas/contratos, não abrir novo runtime e não promover Stage 06.
