# Goety 3.1.4 — `weakening_focus`

Status: **✅ CATALOGADO / COUNTED_EXACT** · identificador factual obtido da auditoria do **JAR 3.1.4 hash-matched** · **⚠️ funcionamento físico/números não validados nesta etapa**.

## Identidade canônica

- **Provider:** Goety (mod id `goety`).
- **JAR instalado e auditado:** `goety-3.1.4.jar` (NeoForge/Minecraft 1.21.1); SHA-1 `a0770e180e4e8b1b87d8fa9c8356e9dbf34d82a7`.
- **Identidade de Focus no artefato:** `weakening_focus` — item/ação de Focus ativo do conjunto exato de 123. Não é o `empty_focus` proxy.
- **Posição no inventário exato:** 119/123. Número ordinal editorial, não identificador de registry ou ordem de carregamento.
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

## Dossiê técnico — área, debuffs e duração (fonte 3.1.1, 26/10/2026)

**Escopo e autoridade:** identidade do Focus e receita base são fatos da auditoria do JAR instalado **Goety 3.1.4** `goety-3.1.4.jar` (SHA-1 `a0770e180e4e8b1b87d8fa9c8356e9dbf34d82a7`); **toda descrição de semântica, classe e número abaixo pertence somente à fonte pública Goety 3.1.1**, commit [`Vivideru/Goety-3@6c41a04f2d712097c4461f969a6bb8ee277149ef`](https://github.com/Vivideru/Goety-3/commit/6c41a04f2d712097c4461f969a6bb8ee277149ef). O bytecode **3.1.4 não foi confrontado** com estas classes; nenhuma compatibilidade, falha, assinatura ou hook de 3.1.4 é afirmada. **Classificação:** `SOURCE_ADJACENT_311` · `mutating_hook=NOT_VERIFIED` · `physical_qa=NOT_TESTED`.

**Resumo funcional (apenas 3.1.1):** aplicação instantânea de `GoetyEffects.SAPPED` e `MobEffects.WEAKNESS` em entidades vivas encontradas ao redor do conjurador, excluindo aliados segundo `MobUtil.areAllies`. Não é projétil; os efeitos são aplicados dentro do loop de entidades, com feedback visual independente.

### Localizadores técnicos pinados

- [`ModItems.WEAKENING_FOCUS`](https://github.com/Vivideru/Goety-3/blob/6c41a04f2d712097c4461f969a6bb8ee277149ef/src/main/java/com/Polarice3/Goety/common/items/ModItems.java#L312) liga o item a `new MagicFocus(new WeakeningSpell())` na árvore pública 3.1.1.
- [`WeakeningSpell.java`](https://github.com/Vivideru/Goety-3/blob/6c41a04f2d712097c4461f969a6bb8ee277149ef/src/main/java/com/Polarice3/Goety/common/magic/spells/WeakeningSpell.java): `defaultStats().setDuration(5).setRadius(7.0D)`; encantamentos `POTENCY`, `RADIUS`, `DURATION`; `SpellResult`.
- [`GoetyEffects.java`](https://github.com/Vivideru/Goety-3/blob/6c41a04f2d712097c4461f969a6bb8ee277149ef/src/main/java/com/Polarice3/Goety/common/effects/GoetyEffects.java#L36) registra `SAPPED`; a interpretação de atributos internos desse efeito exige inspecionar sua implementação exata.
- [`SpellConfig.java`](https://github.com/Vivideru/Goety-3/blob/6c41a04f2d712097c4461f969a6bb8ee277149ef/src/main/java/com/Polarice3/Goety/config/SpellConfig.java#L1925-L1932): defaults de 3.1.1 `weakeningCost=100`, `weakeningDuration=0` (*tempo de lançamento*, não duração dos efeitos) e `weakeningCoolDown=400`. Config do pack 3.1.4 não foi conferida.
- [`MobUtil.areAllies`](https://github.com/Vivideru/Goety-3/blob/6c41a04f2d712097c4461f969a6bb8ee277149ef/src/main/java/com/Polarice3/Goety/utils/MobUtil.java) e [`MathHelper.secondsToTicks`](https://github.com/Vivideru/Goety-3/blob/6c41a04f2d712097c4461f969a6bb8ee277149ef/src/main/java/com/Polarice3/Goety/utils/MathHelper.java) determinam filtro de alvo e conversão de unidades no uso observado.

### Eixos editáveis em design, não API certificada

| Eixo | Contrato demonstrado somente no 3.1.1 | Consequência |
|---|---|---|
| Área | `SpellStat.radius=7.0` é truncado para `int`, somando níveis de `RADIUS` quando aplicáveis. `getEntitiesOfClass(LivingEntity.class, caster.getBoundingBox().inflate(radius))` retorna entidades dentro de **AABB** expandida. | Não interpretar como círculo/esfera real apenas pela animação de onda. Um aumento de raio eleva o volume pesquisado e potencial de multitarget. |
| Validação de alvos | Dentro do loop, exclui `MobUtil.areAllies(caster,livingEntity)`. O caster pode estar na AABB, mas depende do filtro de aliados; nenhum predicado explícito de LOS é aplicado no corpo do `SpellResult`. | Não garantir exclusão do caster apenas pela geometria, e não declarar atravessamento de paredes em 3.1.4 sem QA. |
| Intensidade | Cada alvo elegível recebe `SAPPED` com amplificador `potency + 4` e `WEAKNESS` com amplificador `potency`; `POTENCY` encantada incrementa o valor-base. | **Amplificador do efeito** não equivale a redução percentual linear; não inventar multiplicadores de atributos, stacking ou bônus de dano. |
| Duração do status | `SpellStat.duration=5`, somando níveis `DURATION`; passa `secondsToTicks(duration)` aos dois `MobEffectInstance`. | Duração de **5 segundos na fonte** e `castDuration=0` são conceitos separados; valores do 3.1.4 dependem de classfile/config real. |
| Dano/tipo | O corpo inspecionado usa `addEffect` e som, **não** `hurt`. | Não atribuir dano direto, crítico ou elemento ofensivo sem semântica concreta do efeito; `SAPPED` pode ter consumidores próprios a auditar. |
| Partículas e orçamento | Dois loops percorrem `i,k ∈ [-radius,radius)`, até `4 × radius²` posições para radius positivo, cada qual com chance de emitir partículas; pacote visual de onda separado. | Perks de aumento de AOE requerem orçamento de iteração + entidades; partículas não comprovam aplicação de status. |
| Custos e resfriamento | `WeakeningCost=100`, `WeakeningCoolDown=400` e cast `0` apenas como defaults da referência 3.1.1. | O provider mantém débito/cooldown no pipeline de varinha e Soul Energy, sem hook 3.1.4 liberado. |

### Contrato de causalidade e pending QA

Uma conjuração produz **uma tentativa provider-native**, potencialmente vários `addEffect`; Mastery não pode contar uma ativação por entidade, por debuff ou por partícula. Não duplicar `WEAKNESS` por um segundo pipeline Black Arcana. Não atribuir `Arcane Danger` ou `Corruption` apenas pela temática de maldição.

**Plano de prova obrigatório:** revisar classfile `WeakeningSpell` do Goety 3.1.4; instâncias de `SAPPED` e sua semântica; entidade aliada/owner/PVP/caster, barreira entre caster e alvo, radius muito alto, valores negativos/limites em config, stacking/refresh de potion effects; cancelar cast/débito em dedicated server e registrar efeito sem proc duplicado.

**Estado:** ⚠️ documentação da fonte adjacente; perks de aumento de área, potência, duração, categorias de dano e redução de custo **⛔ não mutáveis** até contrato de integração real. Não alterar certificados/índices.
