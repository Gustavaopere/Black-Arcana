# Goety 3.1.4 — `telekinesis_focus`

Status: **✅ CATALOGADO / COUNTED_EXACT** · identificador factual obtido da auditoria do **JAR 3.1.4 hash-matched** · **⚠️ funcionamento físico/números não validados nesta etapa**.

## Identidade canônica

- **Provider:** Goety (mod id `goety`).
- **JAR instalado e auditado:** `goety-3.1.4.jar` (NeoForge/Minecraft 1.21.1); SHA-1 `a0770e180e4e8b1b87d8fa9c8356e9dbf34d82a7`.
- **Identidade de Focus no artefato:** `telekinesis_focus` — item/ação de Focus ativo do conjunto exato de 123. Não é o `empty_focus` proxy.
- **Posição no inventário exato:** 104/123. Número ordinal editorial, não identificador de registry ou ordem de carregamento.
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

## Auditoria de controle de alvo e lifecycle para perks — fonte adjacente Goety 3.1.1 (26/10/2026)

**Fonte de identidade:** `telekinesis_focus` está documentado no JAR físico Goety **3.1.4**, SHA-1 `a0770e180e4e8b1b87d8fa9c8356e9dbf34d82a7`, sem contrato comportamental do JAR auditado nesta ficha. **Fonte dos métodos abaixo:** somente o commit público **3.1.1** [Vivideru/Goety-3@6c41a04f2d712097c4461f969a6bb8ee277149ef](https://github.com/Vivideru/Goety-3/commit/6c41a04f2d712097c4461f969a6bb8ee277149ef). Nenhum bug, campo, assinatura, cálculo ou permissão é atribuído ao JAR **3.1.4** sem reconciliação exata. `SOURCE_ADJACENT_311 / mutating_hook=NOT_VERIFIED / physical_qa=NOT_TESTED`.

**Descrição funcional da implementação de referência:** canalização contínua que tenta adquirir uma entidade e ajustar seu deslocamento conforme direção visual do caster; impactos laterais e um anel de equipamento podem acrescentar dano. Sem vínculo comprovado com dano ou transformação Black Arcana.

### Código e classe causal (3.1.1)

- [`ModItems.TELEKINESIS_FOCUS` — linha 314](https://github.com/Vivideru/Goety-3/blob/6c41a04f2d712097c4461f969a6bb8ee277149ef/src/main/java/com/Polarice3/Goety/common/items/ModItems.java#L314) registra `MagicFocus(new TelekinesisSpell())`; [`MagicFocus`](https://github.com/Vivideru/Goety-3/blob/6c41a04f2d712097c4461f969a6bb8ee277149ef/src/main/java/com/Polarice3/Goety/common/items/magic/MagicFocus.java) armazena um campo `ISpell spell` e retorna esse objeto via `getSpell()`.
- [`TelekinesisSpell.java`](https://github.com/Vivideru/Goety-3/blob/6c41a04f2d712097c4461f969a6bb8ee277149ef/src/main/java/com/Polarice3/Goety/common/magic/spells/TelekinesisSpell.java) estende [`EverChargeSpell`](https://github.com/Vivideru/Goety-3/blob/6c41a04f2d712097c4461f969a6bb8ee277149ef/src/main/java/com/Polarice3/Goety/common/magic/EverChargeSpell.java) → [`ChargingSpell`](https://github.com/Vivideru/Goety-3/blob/6c41a04f2d712097c4461f969a6bb8ee277149ef/src/main/java/com/Polarice3/Goety/common/magic/ChargingSpell.java). Métodos relevantes: `startSpell`, `findVictim`, `conditionsMet`, `SpellResult`, `stopSpell`.
- [`MobUtil.getSingleTarget`](https://github.com/Vivideru/Goety-3/blob/6c41a04f2d712097c4461f969a6bb8ee277149ef/src/main/java/com/Polarice3/Goety/utils/MobUtil.java#L597-L633): raycast com LOS e geometria AABB de seleção; [`DarkWand.MagicResults`](https://github.com/Vivideru/Goety-3/blob/6c41a04f2d712097c4461f969a6bb8ee277149ef/src/main/java/com/Polarice3/Goety/common/items/magic/DarkWand.java#L769-L834) e [`ISpell`](https://github.com/Vivideru/Goety-3/blob/6c41a04f2d712097c4461f969a6bb8ee277149ef/src/main/java/com/Polarice3/Goety/api/magic/ISpell.java) são partes da rotina de custo e ciclo — **não** uma interface de modificação já liberada.
- [`SpellConfig.java` — linhas 1933–1945](https://github.com/Vivideru/Goety-3/blob/6c41a04f2d712097c4461f969a6bb8ee277149ef/src/main/java/com/Polarice3/Goety/config/SpellConfig.java#L1933-L1945): defaults somente de 3.1.1 `telekinesisCost=4`, `telekinesisChargeUp=0` ticks, `telekinesisMaxHealth=100`, lista configurável `telekinesisBlackList`. Não interpretar como config instalada.

### Matriz de parâmetros e riscos da fonte adjacente

| Eixo | Código observado no 3.1.1 | Avaliação/limite para 3.1.4 |
|---|---|---|
| Casting/custo | `EverChargeSpell` define `everCharge=true` e `Cooldown()=0`; `ChargingSpell` tem `defaultCastDuration=72000` e `defaultSpellCooldown=0`. No `TelekinesisSpell.stopSpell` existe cooldown explícito `secondsToTicks(5)` quando caster é `Player`. | **Custo ao longo do canal, frequência e ordem de débito** precisam rastrear `DarkWand/SEHelper` e QA; não inferir “cast grátis” pelo cooldown base 0. |
| Aquisição de alvo | `startSpell` zera `victim` e tenta `findVictim`; `MobUtil.getSingleTarget(level,caster,range,3,NO_CREATIVE_OR_SPECTATOR)` usa predicado explícito e LOS; caster `Mob` substitui o alvo por `mob.getTarget()`. | **O predicado usado não é o overload padrão que exclui aliados automaticamente**; filtros efetivos para cada entidade precisam QA. `range`, raio de seleção 3 e LOS são eixos distintos. |
| Potency/range | `defaultStats().setPotency(1)`; seleção utiliza `SpellStat.range`, `potency` e bônus de `POTENCY/2.0` e `RANGE`. O corpo de `SpellResult` multiplica a força calculada pela potência. | Potência não equivale linearmente a dano; `getRangeLevel` não equivale a limite de movimento ou mutabilidade via perk. |
| Critério de tamanho/HP | `findVictim` compara volumes de bounding boxes; depois há bloco que testa `this.victim instanceof LivingEntity` antes de aplicar limites de `maxHealth`, `BANISH_IMMUNE` e blacklist. **Em uma aquisição iniciada com `this.victim=null`, esse teste interno não avalia o `target` recém-encontrado.** | Risco de lógica da **fonte 3.1.1**: a restrição de HP/blacklist pode não executar durante a aquisição inicial. Não anunciar bypass confirmado no JAR 3.1.4; requer teste específico e correlação classfile. |
| Estado de alvo e concorrência | `TelekinesisSpell` mantém `public Entity victim` no **objeto Spell**; `MagicFocus` recebe `new TelekinesisSpell()` durante registro, mantém e retorna essa referência. Início e parada zeram o campo; processamento contínuo o atualiza. | **Risco de compartilhamento de estado entre conjuradores** na fonte 3.1.1 se instância de item/spell for reutilizada; ainda não há prova física de interferência nem de identidade/instâncias no 3.1.4. Projetar testes com dois casters e dois itens simultâneos. |
| Deslocamento/colisão | `SpellResult` calcula vetor derivado da mirada, distância, posição e velocidade atual; ajusta delta, aplica `MobUtil.push` e reseta queda em certas forças positivas; em colisão horizontal pode aplicar `flyIntoWall` condicionado por velocidade. | `force` não representa blocos/tick finais sem `MobUtil.push`/physics; velocidade, dano e wall collision podem mudar com addons/lag. |
| Dano extra | `RING_OF_FORCE` pode reduzir ar e causar `ModDamageSource.choke` em condição; choque na parede usa `flyIntoWall` condicional. | Dano direto de telekinesis **não é garantido por cada tick**; duração e immunities ainda não validadas em 3.1.4. |
| Interrupção | `conditionsMet` rejeita `caster.hurtTime>0`; se `victim` não nula e fora de alcance, a zera e rejeita. `stopSpell` a zera e tenta aplicar cooldown para jogador. | Cancelamento por damage, logout, troca de staff, dimension change e cast concorrente exigem testes de cleanup — não presumir isolamento por jogador. |

### Contratos para perks e integração

**Design elegível só após prova:** `range` de aquisição, limite de massa/volume, velocidade de controle, resistência do alvo, recarga, custo de canal, colisão e interrupções. **Nenhum deles é um hook verificado para mutação per-player** no Goety 3.1.4. Um adapter deve usar a autoria causal Goety, não um segundo sistema de arrasto/teleporte Black Arcana que compita por velocidade da mesma entidade.

**Risco prioritário:** validar separadamente (1) filtro de maxHealth/blacklist na aquisição e (2) se `victim` é efetivamente compartilhado entre dois jogadores, utilizando contexto servidor dedicado, sem explorar bypass em runtime; qualquer integração de alvo/força fica **⛔ FAIL-CLOSED** até esse resultado. Atividades em cada tick são efeitos da mesma canalização, não novas conjurações para Mastery.

**Gate de certificado:** classfiles 3.1.4 e fluxo de `MagicFocus`/`DarkWand`/`IChargingSpell`, isolamento de estado, testes PVP/proteção, valores de config carregada e testes reais. **Estado: ⚠️ apenas análise de source adjacente; não promover manifesto, índices, Stages ou mutating hooks.**

## Adendo de ABI exata do JAR 3.1.4 — 26/10/2026

**Nova evidência, distinta do estudo da fonte 3.1.1 acima:** no JAR `goety-3.1.4.jar` com SHA-1 `a0770e180e4e8b1b87d8fa9c8356e9dbf34d82a7`, o [probe de assinaturas e relações de chamadas](../EXACT-3.1.4-ABI-AND-SYMBOLIC-CALL-AUDIT-20261026.md) confirmou os símbolos abaixo (`GitHub Actions run 40344481668`, `success`; artifact `12659699310`).

`TelekinesisSpell` declara o campo `public Entity victim`. `findVictim` referencia `MobUtil.getSingleTarget`, `Mob.getTarget` e `SpellStat.getRange`; `stopSpell` referencia `SEHelper.addCooldown`. **Isto não demonstra compartilhamento indevido do estado `victim` nem a lógica de filtro de HP/blacklist.**

**Interpretação estrita:** `EXACT_ABI_CALL_REFERENCES_VERIFIED` cobre apenas classe/método/field e referências estáticas apontadas; **não** confirma ramos executados, fórmulas, balanceamento, configs, eventos efetivos, hooks seguros ou testes físicos. A análise `SOURCE_ADJACENT_311` permanece uma fonte separada; `mutating_hook=NOT_VERIFIED` e `physical_qa=NOT_TESTED` continuam válidos. Goety mantém autoridade, sem homologação de perks e sem incremento dos contadores globais.
