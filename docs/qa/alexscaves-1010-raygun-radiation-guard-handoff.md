# Raygun 1.0.10 — barreiras estáticas de resistência e aplicação de Irradiated

## Proveniência e contrato delimitado

Continuação da [PR #1018](https://github.com/Gustavaopere/Black-Arcana/pull/1018), integrada em `Black-Arcana/main@7227673be83a650099973b2f9473a4a07739dc69`. A versão física documentada permanece `alexscaves-1.0.10-neoforge+1.21.1.jar`, JAR SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`. O método de interesse é `RaygunItem.onUseTick(Level,LivingEntity,ItemStack,int):void`, digest do parse `b037276094928625e501d13fddd11829e3fe5540d585f7d8213f37b098c39bc5`.

A [sonda read-only](alexscaves_1010_raygun_radiation_guard_probe.py) examina exclusivamente metadados de classfile de regiões pontuais do método: `ACCompat.hurt @1041`, retorno e `ifeq @1044`, consulta da `ACTagRegistry.RESISTS_RADIATION`/predicado `Holder$Reference.is`, `ifne @1088 → 1157`, referência a `ACEffectRegistry.IRRADIATED`, `MobEffectInstance(..., 800, amplifier)`, `LivingEntity.addEffect @1119` com `ifeq @1122 → 1157`, e mensagem visual `sendMSGToAll @1154`. Não se reconstrói o CFG completo nem se assumem condições fora desses trechos.

O probe verifica ainda a declaração **publisher-default** da tag em `data/alexscaves/tags/entity_type/resists_radiation.json` do mesmo JAR, com SHA-256 e valores. A tag pode ser alterada ou ampliada pelo conjunto de datapacks em runtime; a listagem do JAR **não** é a registry efetiva do mundo nem imunidade global de todos os produtores de irradiação.

## Evidência e critérios

A [CI exata](../../.github/workflows/alexscaves-1010-raygun-radiation-guard.yml) executa **15 regressões sintéticas fail-closed**, verifica JAR, classe e método, extrai **somente** símbolos JVM, janelas curtas, saltos diretos e o inventário de tag. A primeira execução é `UNSEALED DISCOVERY` e **não** é homologação. Somente o resultado realmente observado deverá ser registrado no manifesto `EXACT-RAYGUN-RADIATION-GUARDS-1.0.10.json`, seguido de execução `--seal` na HEAD final, inspeção do diff e CI completa.

## Barreira de autoridade

Não derivar um callback de perk dos desvios ou do tag. Sem documentação e testes reais de provider/servidor, não é permitido alterar a aceitação de `Irradiated`, duração, amplifier, resistência, dano ou envio visual. `LivingEntity.addEffect` retorna um booleano; o desvio subsequente constitui apenas evidência estática do uso do retorno e não demonstra entrega final ao cliente ou eventual override de status.

O status `irradiated` possui consumidores próprios (tick, exaustão, Hazmat, heal event), que **não** recebem automaticamente as condições do produtor Raygun; consulte a [ficha do efeito](../../wiki/modpack-catalog/providers/✅-alexs-caves-continued/effects/irradiated.md). As regras do Black Arcana preservam `WorldEffectPolicy`, autoridade de servidor, claims/PvP, custos/cooldowns e não duplicação do pipeline do provider.

**Estado obrigatório:** ⚠️ parcial/condicionado; `NO_MUTATION`, `NOT_CERTIFIED`, `physical_qa=NOT_TESTED`; Raygun e Tremorzilla Beam ainda pendentes (Alex's Caves 28/30). Stage 06.05 não avança por auditoria de catálogo.
