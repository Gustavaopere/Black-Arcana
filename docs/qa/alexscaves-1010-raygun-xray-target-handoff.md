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


## Resultado da descoberta compilada — GitHub Actions #41502820559

A [execução exploratória](https://github.com/Gustavaopere/Black-Arcana/actions/runs/41502820559) concluiu com sucesso **11 regressões sintéticas** e o probe SHA-exato no JAR original de **75.279.314 bytes**. A classe `RaygunItem.class` possui 26 métodos declarados no recorte e `onUseTick` foi verificado pelo digest de método `b037276094928625e501d13fddd11829e3fe5540d585f7d8213f37b098c39bc5`, com **523 instruções reconhecidas pelo parser**. O [manifesto de seis janelas JVM](../../wiki/modpack-catalog/providers/✅-alexs-caves-continued/EXACT-RAYGUN-XRAY-TARGET-1.0.10.json) fixa offsets, referências e desvios selecionados; a CI final deverá rerodar com `--seal`.

| Região nativa | Observação exata | Interpretação limitada |
|---|---|---|
| `onUseTick @35–58` | `ldc_w float 25.0f @35`, `fload 7 @38`, `fmul @40` e `fstore 8 @41`; `X_RAY @44` → `ACCompat.enchantLevel @47` → `ifle @50` → `istore 9 @58` | Há distância calculada `25.0f × float local 7` e um booleano local derivado do nível do encantamento. **Não** estabelecer 25 como alcance universal ou supor efeito de X_RAY sobre a distância sem rastrear os consumidores desses locais |
| `@60–83` | `ProjectileUtil.getHitResultOnViewVector @69` recebe `fload 8` convertido a double; `LivingEntity.pick @80` também recebe `fload 8` como distância | Duas buscas/colisões iniciais usam a distância calculada; a ordem de seleção efetiva e a extensão por X_RAY requerem continuação do CFG |
| `@627–660` | `ProjectileUtil.getEntityHitResult @640`; guarda `ifnull @647`, fallback para outro ramo em `@657` | Uma consulta adicional a entidades não é equivalente a cone permanente, LOS livre, raio, nem dano garantido |
| `@934–960` | `Level.getEntities @943` → iterator e `hasNext @955` → `ifeq @960` | Há enumeração server-side no trecho observado; não certifica quantidade máxima de alvos |
| `@987–1008` | Consultas `Entity.isAlliedTo @987`, `LivingEntity.isAlliedTo @996`, `isPassengerOfSameVehicle @1005`; desvio `ifne @1008` | Evidência local de exclusão de candidatos; sem prova de política PvP e ownership externos |
| `@1013–1056` | `instanceof TremorzillaEntity @1013`, desvio `ifne @1016`, `causeRaygunDamage @1026`, `ACCompat.hurt @1041`, branch de resultado `ifeq @1044` e `ifeq @1056`; `iload 18 @1029` escolhe operandos `2.0f` ou `1.5f` | O dano é **solicitado** em ramo condicionado, não dano final aceito. Sem origem completa de `local 18`, não vincular 2.0f a X_RAY, GAMMA_RAY, distância ou um tipo específico de alvo |

Nenhuma conclusão deste recorte autoriza alterar a variável local de distância, a ordem das rotas de ray trace, a lista de entidades ou `DamageSource`; não há hook estável documentado para uma perk alterar esses valores preservando exclusões, autoridade de servidor e limites de budget.

**Critério de fecho:** reconstruir o restante do CFG com as dependências de `local 7`, `local 9`, `local 18`, controles de `X_RAY`, limites de raycasts em blocos, caixa da enumeração e teste físico com alvos aliados/claims. Só depois avaliar viabilidade de hooks. A ficha continua ⚠️ `NOT_CERTIFIED` / `NO_MUTATION`, sem promover 28/30.
