# Goety 3.1.4 — `fire_breath_focus`

Status: **✅ CATALOGADO / COUNTED_EXACT** · identificador factual obtido da auditoria do **JAR 3.1.4 hash-matched** · **⚠️ funcionamento físico/números não validados nesta etapa**.

## Identidade canônica

- **Provider:** Goety (mod id `goety`).
- **JAR instalado e auditado:** `goety-3.1.4.jar` (NeoForge/Minecraft 1.21.1); SHA-1 `a0770e180e4e8b1b87d8fa9c8356e9dbf34d82a7`.
- **Identidade de Focus no artefato:** `fire_breath_focus` — item/ação de Focus ativo do conjunto exato de 123. Não é o `empty_focus` proxy.
- **Posição no inventário exato:** 35/123. Número ordinal editorial, não identificador de registry ou ordem de carregamento.
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

## Dossiê técnico — canalização, dano de fogo e mutação do mundo (27/10/2026)

**Proveniência obrigatória:** `COUNTED_EXACT` e identidade do item pertencem ao **JAR Goety 3.1.4 SHA-1 `a0770e180e4e8b1b87d8fa9c8356e9dbf34d82a7`**; somente os **símbolos e call-sites** listados na [auditoria exata](../EXACT-3.1.4-FIRE-BREATH-FROST-NOVA-ELECTRO-ORB-ABI-20261027.md) são afirmações binárias desta versão (run [`40498956210`](https://github.com/Gustavaopere/Black-Arcana/actions/runs/40498956210), artifact `12731937460`). Todas as fórmulas, estatísticas, defaults, casos condicionais e etapas de execução abaixo são **da fonte adjacente 3.1.1** em [`Vivideru/Goety-3@6c41a04f2d712097c4461f969a6bb8ee277149ef`](https://github.com/Vivideru/Goety-3/commit/6c41a04f2d712097c4461f969a6bb8ee277149ef), **não verificados como iguais no 3.1.4**. `SOURCE_ADJACENT_311` · `mutating_hook=NOT_VERIFIED` · `physical_qa=NOT_TESTED`.

### Vinculação, classes e fonte

- [`ModItems.FIRE_BREATH_FOCUS`](https://github.com/Vivideru/Goety-3/blob/6c41a04f2d712097c4461f969a6bb8ee277149ef/src/main/java/com/Polarice3/Goety/common/items/ModItems.java#L300): `new MagicFocus(new FireBreathSpell())` na fonte 3.1.1. A identidade `fire_breath_focus` foi provada separadamente no artefato físico 3.1.4.
- [`FireBreathSpell.java`](https://github.com/Vivideru/Goety-3/blob/6c41a04f2d712097c4461f969a6bb8ee277149ef/src/main/java/com/Polarice3/Goety/common/magic/spells/FireBreathSpell.java) herda [`BreathingSpell.java`](https://github.com/Vivideru/Goety-3/blob/6c41a04f2d712097c4461f969a6bb8ee277149ef/src/main/java/com/Polarice3/Goety/common/magic/BreathingSpell.java), que estende `EverChargeSpell` e implementa [`IBreathingSpell.java`](https://github.com/Vivideru/Goety-3/blob/6c41a04f2d712097c4461f969a6bb8ee277149ef/src/main/java/com/Polarice3/Goety/api/magic/IBreathingSpell.java). O caminho `IBreathingSpell.getBreathTarget` usa `MobUtil.getTargets`.
- [`SpellConfig.java`](https://github.com/Vivideru/Goety-3/blob/6c41a04f2d712097c4461f969a6bb8ee277149ef/src/main/java/com/Polarice3/Goety/config/SpellConfig.java#L1106-L1119): defaults **exclusivos da referência 3.1.1** `fireBreathCost=2` (descrito como custo por segundo), `fireBreathChargeUp=0`, `fireBreathTime=100` (limite de canalização; config 0 admite duração indefinida), `fireBreathCoolDown=100`, `fireBreathDamage=2.0`, `dragonFireGriefing=true`. Não converter números em saldo/cooldown efetivo do modpack sem 3.1.4 + config.
- [`WandUtil.getStats`](https://github.com/Vivideru/Goety-3/blob/6c41a04f2d712097c4461f969a6bb8ee277149ef/src/main/java/com/Polarice3/Goety/utils/WandUtil.java#L169-L176) acumula atributos de `SpellStat` nessa referência; o perfil base da spell é `range=8` e `burning=1`.

### Contrato de parâmetros na fonte 3.1.1

| Eixo | Comportamento da fonte | Perk design e risco |
|---|---|---|
| Canalização | `BreathingSpell` é `EverChargeSpell`; `FireBreathSpell.shotsNumber` consulta `FireBreathDuration` e `defaultCastUp` consulta `FireBreathChargeUp`. O custo é configurado como **por segundo**, mas a liquidação efetiva depende de `DarkWand/SEHelper`. | Não tratar cada tick ou hit como cast independente. Cap de shots, cancelamento e saldo não podem ser substituídos por custo do Black Arcana. |
| Targeting | `getBreathTarget(caster, range)` → `MobUtil.getTargets(...,range,3.0D)`. Para um caster do tipo `Mob` com alvo, `conditionsMet` exige LOS e distância até `range+4`. | Range numérico não é cone/LOS garantido para jogadores; filtros reais devem ser auditados. |
| Dano | `baseDamage()` usa configuração × `WandUtil.damageMultiply`; `SpellResult` soma potency, podendo duplicar dano com Ring of Dragon. Seleciona `ModDamageSource.fireBreath` ou `magicFireBreath` se usa Nether Robe. | Tipo de dano **pode mudar por equipamento**. Não aplicar multiplicadores duas vezes nem inferir hit crítico/perfil de resistência a partir do nome Fire. |
| Queimadura | `burning` inicial 1, encantamento BURNING incrementa. Quando `target.hurt` retorna true, `target.igniteForSeconds(5 × burning)`. | Uma tentativa sem dano aceito não garante fogo. O estado ignite não é uma segunda conjuração. |
| Alteração do mundo | Com `RING_OF_THE_DRAGON` e `DragonFireGriefing` na fonte, realiza até três sondas de `world.clip` e pode chamar `setBlockAndUpdate` com `BaseFireBlock.getState` para local elegível. | **Potencial mudança persistente do mundo**: claims, anti-griefing, compatibilidade de blocos, número de sondas e orçamento devem ser conferidos. Black Arcana `WorldEffectPolicy` não governa automaticamente efeitos externos. |
| Visual e física | `showWandBreath` emite partículas com efeito condicionado a Ring of Dragon e a `range`; no ramo encantado da fonte, `range` visual é atribuído ao `WandUtil.getRangeLevel`, não necessariamente somado. | Não confundir distância visual com targeting/dano. Diferenças são do código 3.1.1, não bug confirmado 3.1.4. |

### Prova exata limitada à ABI do JAR 3.1.4

`FireBreathSpell.SpellResult` possui call-sites para `SpellStat.getRange`, `getBreathTarget`, `Entity.hurt`, `igniteForSeconds`, `ModDamageSource.fireBreath`, `magicFireBreath`, `BaseFireBlock.getState` e **`ServerLevel.setBlockAndUpdate`**; as interfaces e `showWandBreath` existem. **Não** se verificaram as condições dos ramos, limites de recurso, valor do dano ou o mundo efetivamente alterado. A referência `setBlockAndUpdate` justifica um **gate de world safety**, não um parecer de violação.

**QA pendente:** dedicated-server Survival com e sem Ring of Dragon, config `dragonFireGriefing`, claim protegido, chuva/água, aliados/PVP, cancelamento, equip swap, chunks, start/use/stop e débito de Soul Energy; medir hits/segundo e partículas. **⛔ Sem hook de mutação de blocks, range ou burning aprovado.** Nenhuma certificação estrita foi acrescentada.
