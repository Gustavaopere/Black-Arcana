# Goety 3.1.4 — `poison_dart_focus`

Status: **✅ CATALOGADO / COUNTED_EXACT** · identificador factual obtido da auditoria do **JAR 3.1.4 hash-matched** · **⚠️ funcionamento físico/números não validados nesta etapa**.

## Identidade canônica

- **Provider:** Goety (mod id `goety`).
- **JAR instalado e auditado:** `goety-3.1.4.jar` (NeoForge/Minecraft 1.21.1); SHA-1 `a0770e180e4e8b1b87d8fa9c8356e9dbf34d82a7`.
- **Identidade de Focus no artefato:** `poison_dart_focus` — item/ação de Focus ativo do conjunto exato de 123. Não é o `empty_focus` proxy.
- **Posição no inventário exato:** 73/123. Número ordinal editorial, não identificador de registry ou ordem de carregamento.
- **Aquisição documental:** o JAR exato contém receita base de aquisição homônima para este Focus e sem condition de mod carregado; o conjunto tem 80 recipes de tipo `goety:ritual` e 43 shaped. **O tipo específico desta receita não é deduzido apenas pela lista agregada.** A execução real com recursos/progressão do modpack não foi comprovada nesta etapa.
- **Conta semântica:** `COUNTED_EXACT`, já incluída nos 123 Focuses Goety do ledger; materializar a ficha **não acrescenta uma nova identidade**. Receitas alternativas de obtenção não criam outros spells.
- **Escola/categoria exata, classe e método runtime, cast-time, Soul Energy, cooldown, alcance, dano, efeitos, targeting, PVP/proteção, progressão/research e numeric balance:** **NÃO VERIFICADO nesta ficha**. A identificação factual do item não estabelece automaticamente contrato de API/efeito.

## Authority e deduplicação

Goety é a autoridade de Soul Energy, Focus/Staff casting, custos, recipe execution, servants, cleanup e estado persistente. Black Arcana não cria outro Soul ledger, uma segunda conjuração, um débito adicional, novo summon ou uma segunda world mutation; quaisquer bridges futuras exigem boundary server-safe comprovada e comportamento fail-closed.

## Evidência

- [Inventário semântico exato 3.1.4](../EXACT-3.1.4-SEMANTIC-INVENTORY.md): lista de **123** nomes `_focus` ativos, com `empty_focus` excluído e aquisição agregada 80/43.
- [Auditoria do artefato](../EXACT-3.1.4-ARTIFACT-AUDIT.md): hash físico verificado e exclusões.
- [Fronteira de integração](../INTEGRATION-RULES.md) e [catálogo anterior](../FOCUS-CATALOG.md).

**Clean-room:** a ficha contém dados factuais de identidade e proveniência, não código, assets, tradução de tooltip ou implementação upstream.

## Dossiê técnico — projétil, perfuração e efeitos de veneno (fonte 3.1.1, 26/10/2026)

**Escopo e autoridade:** identidade do Focus e receita base são fatos da auditoria do JAR instalado **Goety 3.1.4** `goety-3.1.4.jar` (SHA-1 `a0770e180e4e8b1b87d8fa9c8356e9dbf34d82a7`); **toda descrição de semântica, classe e número abaixo pertence somente à fonte pública Goety 3.1.1**, commit [`Vivideru/Goety-3@6c41a04f2d712097c4461f969a6bb8ee277149ef`](https://github.com/Vivideru/Goety-3/commit/6c41a04f2d712097c4461f969a6bb8ee277149ef). O bytecode **3.1.4 não foi confrontado** com estas classes; nenhuma compatibilidade, falha, assinatura ou hook de 3.1.4 é afirmada. **Classificação:** `SOURCE_ADJACENT_311` · `mutating_hook=NOT_VERIFIED` · `physical_qa=NOT_TESTED`.

**Resumo funcional (apenas 3.1.1):** cria um `PoisonQuill` server-side, com trajetória de flecha, velocidade configurada pelo `SpellStat`, dono do projétil e possível modo perfurante condicionado ao staff; no impacto aplica dano de projétil e um status que depende do equipamento do dono.

### Cadeia de classes e proveniência

- [`ModItems.POISON_DART_FOCUS`](https://github.com/Vivideru/Goety-3/blob/6c41a04f2d712097c4461f969a6bb8ee277149ef/src/main/java/com/Polarice3/Goety/common/items/ModItems.java#L359) → [`PoisonDartSpell.java`](https://github.com/Vivideru/Goety-3/blob/6c41a04f2d712097c4461f969a6bb8ee277149ef/src/main/java/com/Polarice3/Goety/common/magic/spells/wild/PoisonDartSpell.java) → [`PoisonQuill.java`](https://github.com/Vivideru/Goety-3/blob/6c41a04f2d712097c4461f969a6bb8ee277149ef/src/main/java/com/Polarice3/Goety/common/entities/projectiles/PoisonQuill.java). O cadastro semântico no JAR 3.1.4 é distinto desta reconstrução de código **3.1.1**.
- [`SpellConfig.java`](https://github.com/Vivideru/Goety-3/blob/6c41a04f2d712097c4461f969a6bb8ee277149ef/src/main/java/com/Polarice3/Goety/config/SpellConfig.java#L1436-L1445) defaults fonte 3.1.1: `poisonDartCost=8`, `poisonDartTime=0`, `poisonDartCoolDown=20` e `poisonDartDamage=2.5`.
- [`GoetyEffects.ACID_VENOM`](https://github.com/Vivideru/Goety-3/blob/6c41a04f2d712097c4461f969a6bb8ee277149ef/src/main/java/com/Polarice3/Goety/common/effects/GoetyEffects.java#L99), [`MobUtil.areAllies`](https://github.com/Vivideru/Goety-3/blob/6c41a04f2d712097c4461f969a6bb8ee277149ef/src/main/java/com/Polarice3/Goety/utils/MobUtil.java) e os tipos `IOwned`/`ISpellEntity` participam da seleção e da atribuição de efeito na referência.

### Campos e comportamento causal observados

| Eixo | Fonte 3.1.1 | Implicação de perk |
|---|---|---|
| Identidade/escola | `PoisonDartSpell.getSpellType()=WILD`; `SpellResult` cria um único `PoisonQuill` com `setOwner(caster)` e `world.addFreshEntity`. | Spawn não é uma nova conjuração adicional; identificar pelo Focus e autoria original. |
| Velocidade e precisão | `defaultStats().setVelocity(1.6F)`; encantamento `VELOCITY` adiciona níveis/3, `shootFromRotation(..., velocity, 1.0F)` define inaccuracy do lançamento. | Velocidade inicial ≠ alcance garantido; gravidade/colisão/água ficam no entity tick e engine física. |
| Potência, duração | `setExtraDamage(potency)` e `setDuration(duration)`; `DURATION` e `POTENCY` no Focus ajustam esses valores; `setSpear(rightStaff(staff), potency+1)` governa perfuração. | Potência pode alterar **dano e nível de perfuração**, não somente dano; tempo não é lifetime, mas duração adicional do status. |
| Dano | `PoisonQuill.onHitEntity` seleciona `SpellConfig.PoisonDartDamage` para dono não-Mob, ou `Attributes.ATTACK_DAMAGE` para owner `Mob`, adiciona `extraDamage`, e usa `damageSources().arrow(quill,owner)`. | Cálculo do dano é do **projétil**, não necessariamente dano mágico; não reclassificar como escola mágica/elemental no dano sem API. |
| Perfuração | `getSpearLevel()>0` habilita conjunto de IDs atingidos e limite baseado em `pierceLevel + 1`; projétil em modo não perfurante descarta após hit elegível. `canHitEntity` evita dono e geralmente aliados, com exceção de alvo explícito de um Mob; há proteção adicional contra owners alinhados. | Não transformar `pierce level` em “número de danos garantidos”: cancelamentos de `hurt`, alvos mortos, imunidades e reentradas são condicionais. |
| Estado de veneno | Só após `hurt` retornar true e a vítima estar viva, não-Enderman e `LivingEntity`: aplica `POISON`, ou `ACID_VENOM` se o owner/owner mestre possui Wild Robe, com `secondsToTicks(2 + duration)`. | Efeito condicional, com identidade de dano/status distintas; duração-base de 2 segundos **não é cast time**. Status pode ser negado mesmo após impacto. |
| Água e física | Se caster submerso no instante do lançamento, `setAqua(true)`; no projétil `getWaterInertia()` retorna `0.99F` nesse modo, diferente do retorno herdado. | Perk de velocidade subaquática exige consumidor da entidade, não somente `SpellStat.velocity`. |
| Persistência | `PoisonQuill` serializa `Aqua`, `Spear`, `SpearLevel`, `Duration`, `ExtraDamage` em NBT; posição, dono e dinâmica vêm da base `Arrow`. | Consultar lifecycle após save/reload e dono offline. Não inferir persistência perfeita sem teste binário 3.1.4. |
| Lifetime/removal | Descarta se chunk do projétil não carregado, `tickCount >= 100` ou alojado no chão; colisão de bloco provoca discard; colisão com entidade depende da perfuração/condições. | **100 ticks é teto observado do source**, não duração do debuff; não “aumentar duração” para estender lifetime. |

### Segurança, budgets e plano de compatibilidade

A versão 3.1.1 encaminha o hit via `DamageSource.arrow` e a decisão de status para `PoisonQuill.onHitEntity`. Portanto, perk de `projectile size`, multi-shot, perfuração, status de veneno, dano e duração tem **consumers diferentes**; alterar apenas o `SpellStat` não certifica o resultado e não autoriza spawn adicional. Qualquer expansão de hitbox ou perfuração exige boundary de friendly-fire/owner, idempotência de alvo e limite de entidades processadas.

**Testes obrigatórios para 3.1.4:** classfile `PoisonDartSpell/PoisonQuill`; uma e múltiplas entidades alinhadas; friendly-fire, Mob vs jogador, Wild Robe e underwater; persistência reload, chunk unload, interceptação de damage events, `ENDERMAN`, owner offline, PvP/claims, velocidade/hitbox e custo/cooldown por cast.

**Status:** ⚠️ enriquecimento source-adjacent; nenhum hook de alteração de projétil no JAR instalado foi verificado. **⛔ Fail-closed** para mutações, sem incrementar certificados ou alterar o índice 100%.

## Adendo de ABI exata do JAR 3.1.4 — 26/10/2026

**Nova evidência, distinta do estudo da fonte 3.1.1 acima:** no JAR `goety-3.1.4.jar` com SHA-1 `a0770e180e4e8b1b87d8fa9c8356e9dbf34d82a7`, o [probe de assinaturas e relações de chamadas](../EXACT-3.1.4-ABI-AND-SYMBOLIC-CALL-AUDIT-20261026.md) confirmou os símbolos abaixo (`GitHub Actions run 40344481668`, `success`; artifact `12659699310`).

`PoisonDartSpell.SpellResult` referencia `PoisonQuill.setOwner`, `setDuration` e `setExtraDamage`. `PoisonQuill.onHitEntity(EntityHitResult)` e `onHitBlock(BlockHitResult)` estão presentes. Tipos de dano, status, pierce, flags, números e persistência continuam sem equivalência binária demonstrada.

**Interpretação estrita:** `EXACT_ABI_CALL_REFERENCES_VERIFIED` cobre apenas classe/método/field e referências estáticas apontadas; **não** confirma ramos executados, fórmulas, balanceamento, configs, eventos efetivos, hooks seguros ou testes físicos. A análise `SOURCE_ADJACENT_311` permanece uma fonte separada; `mutating_hook=NOT_VERIFIED` e `physical_qa=NOT_TESTED` continuam válidos. Goety mantém autoridade, sem homologação de perks e sem incremento dos contadores globais.
