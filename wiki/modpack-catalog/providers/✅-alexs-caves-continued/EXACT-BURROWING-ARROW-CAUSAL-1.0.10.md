# Burrowing Arrow — fluxo causal SHA-exato, 1.0.10

**Estado:** ⚠️ `PARTIAL_STATIC_CAUSAL`; não é ficha individual com contrato integral certificado. `NO_MUTATION`, `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `provider_universe_closed=false`. Nenhuma raiz de magia adicional foi certificada.

## Identidade da evidência

- Provider `alexscaves` — Alex's Caves Continued `1.0.10`, Minecraft `1.21.1`, NeoForge, Java 21. Arquivo: `alexscaves-1.0.10-neoforge+1.21.1.jar`, 75.279.314 bytes, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`; SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`.
- `BurrowingArrowItem.class`: `com/github/alexmodguy/alexscaves/server/item/`, SHA-256 `be5e566fc89b01c311d70d8d2a0fbbe7387601c9b07e70417135bd668b51fded`.
- `BurrowingArrowEntity.class`: `com/github/alexmodguy/alexscaves/server/entity/item/`, SHA-256 `2fc54e3d320e716e2ccd39bca598c1d4be6a1a1fc3bfbe3e01a6b5bd6690b975`.
- `ACItemRegistry$6.class`: `com/github/alexmodguy/alexscaves/server/item/`, SHA-256 `721d302ffe9969fd15510f63035c2d338be5a962a91f88519c0b527efe8b53a6`.
- Prova reproduzível: [auditor read-only](../../../../docs/qa/alexscaves_1010_burrowing_entity_probe.py), [assertivas de bytecode SHA-exato](../../../../docs/qa/alexscaves_1010_burrowing_entity_static_checks.py), [workflow](../../../../.github/workflows/alexscaves-1010-burrowing-entity-probe.yml), [manifesto das transcrições](EXACT-BURROWING-ARROW-ENTITY-DISCOVERY-1.0.10.json), [descoberta original](EXACT-BURROWING-CAVE-MAP-DISCOVERY-1.0.10.md). Run `44830850816`, job `136615116371` passou. As três transcrições integrais ficam no artefato `14675699386`, retido até 04/12/2026. Não inferir aprovação de runtime real a partir desse job.

## Entrada, autoria e munição

`ACItemRegistry.BURROWING_ARROW` solicita registro do item `alexscaves:burrowing_arrow` pela factory `lambda$static$129`. O método `BurrowingArrowItem.createArrow(Level, ItemStack, LivingEntity, ItemStack)` instancia `BurrowingArrowEntity(Level, LivingEntity)`; as duas `ItemStack` não são lidas nesse **corpo local**. Seu consumo em arco/besta ou engine herdado permanece `NÃO VERIFICADO`.

A entidade tem três construtores. `(EntityType,Level)` e `(Level,LivingEntity)` executam `setBaseDamage(3.5)` e aumentam o nível de piercing em 1 via `AbstractArrowAccessor.ac$setPierceLevel` (`@28–44` e `@58–74`). `(Level, double x, double y, double z)` usa `setBaseDamage(3.5)` (`@55–59`), mas **não** contém a chamada de piercing extra. Ambas as factories concretas criam uma `ItemStack` nova de `ACItemRegistry.BURROWING_ARROW`, passam arma `null` ao construtor de `AbstractArrow` e não recuperam a stack original nesse ponto. `3.5` é atributo de dano-base **solicitado**, não dano final confirmado nem tipo de dano.

O callback `ACItemRegistry$6.getProjectile` constrói o caminho posicional `(Level, x, y, z)` e atribui `pickup=ALLOWED`. Sua classe não liquida munição nem prova aceitação de spawn. Não contar separadamente como novo cast.

## Gate de escavação — `canMine(BlockPos)`

O bytecode do método particular `@0–76` retorna falso se:
- `getOwner()` é não nulo e **não** é `Player` (`@5–17`); owner nulo é permitido neste gate (importante para dispenser).
- `BlockState.is(ACTagRegistry.UNMOVEABLE)` (`@27–34`).
- `BlockState.getFluidState().isEmpty()` é falso (`@37–44`).
- `BlockState.getDestroySpeed(level,pos) == -1.0F` (`@47–60`).
- `getDugBlockCount() >= 5` (`@63–68`).

Com essas condições satisfeitas, devolve true (`@71–76`). O valor **5 limita solicitações contabilizadas**, não demonstra cinco blocos destruídos com sucesso. Há filtro explícito de tag/fluido/hardness e owner, porém nenhum check local de claim, `WorldEffectPolicy`, permissões do jogador ou gamerule. Isso não prova que checks externos sejam inexistentes.

## Estado, geometria e tempo — `tick()`

Primeiro chama `AbstractArrow.tick()` (`@0–1`) e atualiza progresso visual de escavação: quando o flag `DIGGING` está ativo, soma 1 até 5; quando inativo, reduz 1 até 0 (`@4–64`).

Somente segue a escavação quando `inGround` está true, `hitPos != null` e `canMine(hitPos)` retorna true (`@65–89`); então atualiza o estado sincronizado `DIGGING` (`@90–92`).

Para dureza de bloco retornada `d`, o corpo calcula o limiar inteiro em ticks:

`H = int(max(d, 0.2F) * 15.0F)` (`@107–128`, conversão JVM `f2i`).

O progresso de fissura é `int((float)miningTime / H * 10.0F)` (`@129–141`); somente envia `Level.destroyBlockProgress(entityId,hitPos,stage)` quando stage varia (`@142–168`). O som de impacto é solicitado quando `miningTime % 8 == 0` (`@171–189`).

O método usa **pós-incremento de `miningTime`** e compara o valor anterior a `H` (`@208–220`). Desde `miningTime=0`, o primeiro pedido de remoção ocorre no **(H+2)-ésimo tick elegível consecutivo**, se o bloco/permissões/estado não forem alterados. Isso é duração do fluxo local, não cooldown global.

Quando o valor anterior supera `H`, `tick` chama `Level.destroyBlock(hitPos, true)` (`@223–232`) e **descarta o Boolean de retorno** (`@235 pop`). Depois incrementa `DUG_BLOCK_COUNT` incondicionalmente (`@236–243`), reinicia o contador/visual e solicita `setDeltaMovement(normalize(center(hitPos)-position)*0.30000001192092896)` (`@246–268`). Caso contrário, solicita `setDeltaMovement((center(hitPos)-position)*0.20000000298023224)` (`@274–283`), sem normalização local. Movimento final e colisão dependem do engine.

Ao perder a condição de escavação, limpa `destroyBlockProgress(entityId,hitPos,-1)`, zera `hitPos` e desativa `DIGGING` (`@289–319`). Com o flag ativo, controla o som `CORRODENT_TEETH` com `soundTime` decrementado e recarga local de 38 ticks (`@322–361`). Não há chamada explícita `isClientSide` ou `getGameRules` no corpo `tick` — **não** concluir execução duplicada/êxito de destruição sem runtime real.

## Colisão, sincronização, persistência e descarte

- `onHitBlock` delega primeiro a `AbstractArrow.onHitBlock` e depois registra a posição atingida em `hitPos` (`@0–13`).
- `tickDespawn` não chama `AbstractArrow.tickDespawn` enquanto `isDigging()` for true (`@0–11`), podendo afetar retenção durante escavação; lifespan global não verificado.
- `startFalling` atribui `inGround=false` (`@0–5`).
- `remove` limpa a animação de quebra de bloco com estágio -1 se houver `hitPos`, zera `hitPos` e delega ao `AbstractArrow.remove` (`@0–33`).
- `getDefaultPickupItem` devolve nova stack `BURROWING_ARROW` (`@0–18`), sem garantir pickup real nem preservar stack original.
- `DUG_BLOCK_COUNT` e `DIGGING` usam `SynchedEntityData` (serializers `INT` e `BOOLEAN`), inicializados com 0 e false. `miningTime`, `hitPos`, progresso visual e sons são campos próprios sem equivalência provada com NBT. A classe **não declara** `addAdditionalSaveData` ou `readAdditionalSaveData`; a persistência herdada e após reload está `NÃO VERIFICADO`.
- A interpolação de apresentação `getDiggingAmount(partialTicks) = 0.2F*(prev+(current-prev)*partialTicks)` não define tamanho de hitbox ou dano.

## Consequências para perks e world safety

**Observação comprovada no corpo nativo:** `destroyBlock` é solicitado sem observar seu sucesso, e o limite de cinco consumido após a tentativa. Isso pode fazer a contagem divergir das destruições efetivas; confirmar em ambiente real a reação a proteção de claims, eventos de cancelamento e servidor dedicado. A chamada de destruição não inclui um argumento `Player`, mas os outros sistemas podem aplicar verificações fora desse corpo.

**Candidatos de design, não hooks autorizados:** dano-base, piercing, contador de escavação, dureza/tempo de mineração e vetores de deslocamento seriam parâmetros de interesse para atributos/Mastery/perks; não há nesta inspeção um boundary seguro e confirmado que permita modificá-los. Não injetar mutação em campo, reexecutar efeito, recompensar XP por tentativa nem contornar autoridade de mundo. `Black Arcana` manterá world safety e casting próprios; `RPG Skill Tree` permanece provider de progressão.

**Pendências de certificação:** (1) engine exato `AbstractArrow` e callbacks de arco/besta/dispenser; (2) targeting, dano final/tipo, hit de entidade, custo e aquisição/receita; (3) todos os consumidores transitivos de `BurrowingArrowEntity`; (4) transformações mixin e runtime integrado; (5) persistência e replay; (6) bloco protegido/claims/GameRules e QA físico. Mantém-se `NO_MUTATION` e **não** promove `PERK-READY-CERTIFICATIONS.json` nem os índices.
