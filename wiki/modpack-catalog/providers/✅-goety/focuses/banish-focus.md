# Goety 3.1.4 — `banish_focus`

Status: **✅ CATALOGADO / COUNTED_EXACT** · identificador factual obtido da auditoria do **JAR 3.1.4 hash-matched** · **⚠️ funcionamento físico/números não validados nesta etapa**.

## Identidade canônica

- **Provider:** Goety (mod id `goety`).
- **JAR instalado e auditado:** `goety-3.1.4.jar` (NeoForge/Minecraft 1.21.1); SHA-1 `a0770e180e4e8b1b87d8fa9c8356e9dbf34d82a7`.
- **Identidade de Focus no artefato:** `banish_focus` — item/ação de Focus ativo do conjunto exato de 123. Não é o `empty_focus` proxy.
- **Posição no inventário exato:** 2/123. Número ordinal editorial, não identificador de registry ou ordem de carregamento.
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

## Dossiê técnico — banimento por toque e validação de destino (fonte 3.1.1, 26/10/2026)

**Escopo e autoridade:** identidade do Focus e receita base são fatos da auditoria do JAR instalado **Goety 3.1.4** `goety-3.1.4.jar` (SHA-1 `a0770e180e4e8b1b87d8fa9c8356e9dbf34d82a7`); **toda descrição de semântica, classe e número abaixo pertence somente à fonte pública Goety 3.1.1**, commit [`Vivideru/Goety-3@6c41a04f2d712097c4461f969a6bb8ee277149ef`](https://github.com/Vivideru/Goety-3/commit/6c41a04f2d712097c4461f969a6bb8ee277149ef). O bytecode **3.1.4 não foi confrontado** com estas classes; nenhuma compatibilidade, falha, assinatura ou hook de 3.1.4 é afirmada. **Classificação:** `SOURCE_ADJACENT_311` · `mutating_hook=NOT_VERIFIED` · `physical_qa=NOT_TESTED`.

**Resumo funcional (apenas 3.1.1):** Focus de Void que tenta deslocar aleatoriamente uma entidade tocada, sob limites de vida máxima, imunidades e blacklist avaliados em `conditionsMet`. O caminho de validação do alvo **não é idêntico**, em identidade, ao objeto recebido em `touchResult`; não é seguro projetar perks de teleporte ou alvo assumindo equivalência.

### Localizadores causais da fonte adjacente

- [`ModItems.BANISH_FOCUS`](https://github.com/Vivideru/Goety-3/blob/6c41a04f2d712097c4461f969a6bb8ee277149ef/src/main/java/com/Polarice3/Goety/common/items/ModItems.java#L426) registra `banish_focus` como `MagicFocus(new BanishSpell())` nessa revisão, sem certificar o método no JAR 3.1.4.
- [`BanishSpell.java`](https://github.com/Vivideru/Goety-3/blob/6c41a04f2d712097c4461f969a6bb8ee277149ef/src/main/java/com/Polarice3/Goety/common/magic/spells/void_spells/BanishSpell.java): herda `TouchSpell`; `defaultStats().setRange(64)`; `getSpellType()=VOID`; encantamento `RANGE`; `conditionsMet` e `touchResult`.
- [`TouchSpell.java`](https://github.com/Vivideru/Goety-3/blob/6c41a04f2d712097c4461f969a6bb8ee277149ef/src/main/java/com/Polarice3/Goety/common/magic/TouchSpell.java), [`ITouchSpell.java`](https://github.com/Vivideru/Goety-3/blob/6c41a04f2d712097c4461f969a6bb8ee277149ef/src/main/java/com/Polarice3/Goety/api/magic/ITouchSpell.java) e [`DarkWand.interactLivingEntity/canCastTouch`](https://github.com/Vivideru/Goety-3/blob/6c41a04f2d712097c4461f969a6bb8ee277149ef/src/main/java/com/Polarice3/Goety/common/items/magic/DarkWand.java#L320-L330) / [`canCastTouch`](https://github.com/Vivideru/Goety-3/blob/6c41a04f2d712097c4461f969a6bb8ee277149ef/src/main/java/com/Polarice3/Goety/common/items/magic/DarkWand.java#L732-L762): o clique direto produz um `target`, a admissão consulta `conditionsMet` pelo caminho `IWand.cannotCast`, e o `ITouchSpell.targetConditions` padrão retorna `true`. A versão de fonte inspecionada de `BanishSpell` **não sobrescreve** `targetConditions`.
- [`SpellConfig.java`](https://github.com/Vivideru/Goety-3/blob/6c41a04f2d712097c4461f969a6bb8ee277149ef/src/main/java/com/Polarice3/Goety/config/SpellConfig.java#L1764-L1775): *defaults só do 3.1.1* `banishCost=16`, `banishCoolDown=400`, `banishMaxHealth=100`, `banishBlackList=[]`. Como `TouchSpell` retorna cast duration 0, não atribuir parâmetro de cast-time inexistente a `BanishSpell`.
- [`MobUtil`](https://github.com/Vivideru/Goety-3/blob/6c41a04f2d712097c4461f969a6bb8ee277149ef/src/main/java/com/Polarice3/Goety/utils/MobUtil.java), [`RandomUtil.nextInt`](https://github.com/Vivideru/Goety-3/blob/6c41a04f2d712097c4461f969a6bb8ee277149ef/src/main/java/com/Polarice3/Goety/utils/RandomUtil.java) e [`ISpell.entityResult`](https://github.com/Vivideru/Goety-3/blob/6c41a04f2d712097c4461f969a6bb8ee277149ef/src/main/java/com/Polarice3/Goety/api/magic/ISpell.java) completam os contratos de targeting e sorteio.

### Contrato de parâmetros e efeitos, estritamente 3.1.1

| Parâmetro | Semântica observada | Implicações de perk |
|---|---|---|
| Target de **admissão** | `conditionsMet` usa `entityResult(world,caster,3,3.0F)`, isto é, raycast curto com 3 de alcance e 3 de expansão. Se interceptar `LivingEntity`, examina `getMaxHealth() > BanishMaxHealth`, tag `BANISH_IMMUNE` e `BanishBlackList`. | A verificação **não recebe** o mesmo parâmetro `target` de `touchResult`; quando raycast não encontra entidade, essa checagem específica é ignorada. Pode existir divergência entre alvo olhado e clicado. |
| Evento na admissão | `conditionsMet` chama `EventHooks.onEnderTeleport(living, caster X/Y/Z)` para a entidade atingida pelo raycast e rejeita se o evento for cancelado. | **Coordenadas propostas nesse evento não são as do destino aleatório real**. Não tratar evento prévio como autorização final de destino ou prova universal de proteção de claims. |
| Target efetivo | `DarkWand.interactLivingEntity` encaminha o `target` real da interação para `BanishSpell.touchResult` após `canCastTouch`. `ITouchSpell.targetConditions` padrão é permissivo. | **Risco de validação com entidade diferente** — a versão 3.1.4 precisa ser auditada exatamente antes de modificar filtros, alcance ou teleporte. |
| Distância do efeito | `SpellStat.range=64` na referência. `RANGE` no Focus soma níveis; `rightStaff(staff)` dobra. A quantidade máxima de tentativas de posição = `range` (inteiro), com sorteio horizontal/vertical proporcional ao range. | **Alcance 3** na seleção prévia ≠ **range 64** do sorteio. Multiplicar range aumenta não só distância potencial, mas o limite de iterações e carga. |
| Bloqueios do destino | Sorteio usa `randomTeleport(d3,d4,d5,true)`, posição Y com `Mth.clamp` dentro da altura lógica; remove montaria antes de tentar e emite `GameEvent.TELEPORT`/sons se teleporte retorna true. | O caminho `touchResult` não invoca explicitamente `EventHooks.onEnderTeleport` para cada destino aleatório no corpo inspecionado; **não inferir** ausência de validação nos internals de `randomTeleport` sem classfile/runtime. |
| Condição geométrica | Calcula `caster.distanceToSqr(candidate) > range/4.0` antes da tentativa. Uma distância **ao quadrado** é comparada a um termo **linear**. | Este é o teste literal da fonte, não um limite em blocos simples; o significado final de distanciamento exige teste. |
| Dano e cooldown | `touchResult` não causa dano direto no corpo analisado; custo e cooldown vêm do caminho `DarkWand/SEHelper` e config `Banish`. | Não há evento garantido de “banimento bem-sucedido” para conceder Mastery; deduplicar tentativa, admissibilidade e resultado físico. |

### Observações de segurança e certificação

**Hipótese crítica de 3.1.1, NÃO alegação do JAR 3.1.4:** a admissão pode verificar um alvo adquirido por raycast de curta distância, enquanto a operação trabalha sobre a entidade tocada, e a consulta `EnderEntity` ocorre antes da seleção aleatória do destino. É obrigatório testar: (a) entidade tocada dentro/fora do raycast, (b) imunidade e blacklist de ambas, (c) claims protegidos, (d) cancelamento do evento prévio, (e) falha nas tentativas, (f) passageiro/desmontagem, (g) staff encantado/caster multiplayer.

**Integração:** perímetro/validação de destino, imobilidade de boss, tier de banish, range e cooldown são **candidatos conceituais**, não pontos de alteração liberados. Qualquer bridge que repita a operação, force `randomTeleport` ou ignore cancelamentos é **⛔ FAIL-CLOSED**. Black Arcana não assume autoridade sobre o teleporte Goety; RPG Skill Tree não pode contabilizar tentativa como sucesso garantido.

**Pendências:** classfiles, overloads de target, rota EnderTeleport, provider hooks e permissões da instalação física 3.1.4, config efetiva e dedicated-server/survival QA. A identidade está `COUNTED_EXACT`; a certificação técnica permanece ⚠️. Nenhuma entrada no manifesto das sete evidências ou nos índices é alterada.

## Adendo de ABI exata do JAR 3.1.4 — 26/10/2026

**Nova evidência, distinta do estudo da fonte 3.1.1 acima:** no JAR `goety-3.1.4.jar` com SHA-1 `a0770e180e4e8b1b87d8fa9c8356e9dbf34d82a7`, o [probe de assinaturas e relações de chamadas](../EXACT-3.1.4-ABI-AND-SYMBOLIC-CALL-AUDIT-20261026.md) confirmou os símbolos abaixo (`GitHub Actions run 40344481668`, `success`; artifact `12659699310`).

`BanishSpell.conditionsMet` referencia `EventHooks.onEnderTeleport`, enquanto `BanishSpell.touchResult` referencia `LivingEntity.randomTeleport`, `stopRiding` e `SpellStat.getRange`. **A divergência entre o alvo pré-validado e o alvo realmente tocado permanece hipótese da fonte 3.1.1, não um bug demonstrado do 3.1.4.**

**Interpretação estrita:** `EXACT_ABI_CALL_REFERENCES_VERIFIED` cobre apenas classe/método/field e referências estáticas apontadas; **não** confirma ramos executados, fórmulas, balanceamento, configs, eventos efetivos, hooks seguros ou testes físicos. A análise `SOURCE_ADJACENT_311` permanece uma fonte separada; `mutating_hook=NOT_VERIFIED` e `physical_qa=NOT_TESTED` continuam válidos. Goety mantém autoridade, sem homologação de perks e sem incremento dos contadores globais.

## Adendo da auditoria estrutural exata 3.1.4 — 26/10/2026

A [auditoria método-a-método do JAR com SHA verificado](../EXACT-3.1.4-TARGET-SOUL-STRUCTURAL-AUDIT-20261026.md) (run `40362689828`, PASS) confirmou que `BanishSpell.conditionsMet` referencia `entityResult` e `EventHooks.onEnderTeleport`, enquanto `BanishSpell.touchResult` referencia `LivingEntity.randomTeleport` e `stopRiding` **sem invocar diretamente `onEnderTeleport`** no mesmo método. O binário `DarkWand.interactLivingEntity` referencia `canCastTouch` e `ITouchSpell.touchResult`; `canCastTouch` referencia `ITouchSpell.targetConditions`.

**A distinção é estrutural, não prova bug, exploit, falta de permissão ou alvo trocado em 3.1.4.** `randomTeleport` e outros componentes podem impor verificações próprias. Testar adversários diferentes em raycast/toque, imunidades, claims e cancelamentos antes de qualquer perk mutadora. `mutating_hook=NOT_VERIFIED` · `physical_qa=NOT_TESTED` · **⛔ fail-closed**.
