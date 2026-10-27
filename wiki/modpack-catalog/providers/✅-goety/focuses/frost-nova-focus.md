# Goety 3.1.4 — `frost_nova_focus`

Status: **✅ CATALOGADO / COUNTED_EXACT** · identificador factual obtido da auditoria do **JAR 3.1.4 hash-matched** · **⚠️ funcionamento físico/números não validados nesta etapa**.

## Identidade canônica

- **Provider:** Goety (mod id `goety`).
- **JAR instalado e auditado:** `goety-3.1.4.jar` (NeoForge/Minecraft 1.21.1); SHA-1 `a0770e180e4e8b1b87d8fa9c8356e9dbf34d82a7`.
- **Identidade de Focus no artefato:** `frost_nova_focus` — item/ação de Focus ativo do conjunto exato de 123. Não é o `empty_focus` proxy.
- **Posição no inventário exato:** 40/123. Número ordinal editorial, não identificador de registry ou ordem de carregamento.
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

## Dossiê técnico — explosão fria, alvo alternativo e cooldown próprio (27/10/2026)

**Proveniência obrigatória:** `COUNTED_EXACT` e identidade do item pertencem ao **JAR Goety 3.1.4 SHA-1 `a0770e180e4e8b1b87d8fa9c8356e9dbf34d82a7`**; somente os **símbolos e call-sites** listados na [auditoria exata](../EXACT-3.1.4-FIRE-BREATH-FROST-NOVA-ELECTRO-ORB-ABI-20261027.md) são afirmações binárias desta versão (run [`40498956210`](https://github.com/Gustavaopere/Black-Arcana/actions/runs/40498956210), artifact `12731937460`). Todas as fórmulas, estatísticas, defaults, casos condicionais e etapas de execução abaixo são **da fonte adjacente 3.1.1** em [`Vivideru/Goety-3@6c41a04f2d712097c4461f969a6bb8ee277149ef`](https://github.com/Vivideru/Goety-3/commit/6c41a04f2d712097c4461f969a6bb8ee277149ef), **não verificados como iguais no 3.1.4**. `SOURCE_ADJACENT_311` · `mutating_hook=NOT_VERIFIED` · `physical_qa=NOT_TESTED`.

### Arquitetura e fontes

- [`ModItems.FROST_NOVA_FOCUS`](https://github.com/Vivideru/Goety-3/blob/6c41a04f2d712097c4461f969a6bb8ee277149ef/src/main/java/com/Polarice3/Goety/common/items/ModItems.java#L354) → [`FrostNovaSpell.java`](https://github.com/Vivideru/Goety-3/blob/6c41a04f2d712097c4461f969a6bb8ee277149ef/src/main/java/com/Polarice3/Goety/common/magic/spells/frost/FrostNovaSpell.java) na árvore pública **3.1.1**, sem declarar equivalência do registro construtor 3.1.4.
- [`SpellStat.java`](https://github.com/Vivideru/Goety-3/blob/6c41a04f2d712097c4461f969a6bb8ee277149ef/src/main/java/com/Polarice3/Goety/common/magic/SpellStat.java): na fonte 3.1.1, ordem de construtor (`potency,duration,range,radius,burning,velocity`). `FrostNovaSpell.defaultStats` corresponde a `potency=0`, `duration=1`, `range=16`, `radius=3.5`, `burning=0`, `velocity=0`.
- [`SpellConfig.java`](https://github.com/Vivideru/Goety-3/blob/6c41a04f2d712097c4461f969a6bb8ee277149ef/src/main/java/com/Polarice3/Goety/config/SpellConfig.java#L1222-L1234): **defaults somente 3.1.1** `frostNovaCost=40`, `frostNovaTime=0`, `frostNovaCoolDown=100`, `frostNovaTargetCoolDown=160`, dano mínimo `5.0` e máximo `10.0`.
- [`SpellExplosion.java`](https://github.com/Vivideru/Goety-3/blob/6c41a04f2d712097c4461f969a6bb8ee277149ef/src/main/java/com/Polarice3/Goety/utils/SpellExplosion.java) e [`GoetyEffects`](https://github.com/Vivideru/Goety-3/blob/6c41a04f2d712097c4461f969a6bb8ee277149ef/src/main/java/com/Polarice3/Goety/common/effects/GoetyEffects.java): consumers indiretos de área, congelamento e dano a comparar com classfile 3.1.4.

### Dimensões da magia na fonte 3.1.1

| Dimensão | Semântica da fonte adjacente | Implicação de perk |
|---|---|---|
| Centro do efeito | `spellTarget` começa no caster; `isShifting(caster) && getTarget(caster)!=null` substitui pelo target. | **Modo shift** não equivale apenas a aumentar range. Validar autoria do alvo, distância real, consentimento e proteção PVP. |
| Cooldown custom | `hasCustomCooldown` retorna true. `SpellResult` escolhe `defaultSpellCooldown` ou `FrostNovaTargetCoolDown` para shift-target; depois chama `SEHelper.addCooldown` para jogador. | Há dois perfis de cooldown na fonte; não duplicar no RPG/Black Arcana, não assumir redução genérica aplicada antes/depois. |
| Dano e raio | `radius=3.5` inicial, `RADIUS` incrementa, `rightStaff` adiciona 0.5. Dano `max/min` configuráveis + potência/2 com Focus encantado; `SpellExplosion` produz knockback/dano sob filtro de aliados e outros predicados. | AOE e dano têm consumers separados. A geometria e dano podem ser afetados pelo `SpellExplosionDouble` da fonte, não só pela animação. |
| Freeze | `GoetyEffects.FREEZING` aplicado nos alvos elegíveis do callback `explodeHurt`; duração `5 segundos × SpellStat.duration` e amp 0, +1 com rightStaff. | Duração de status ≠ cast duration; alvo que não recebe dano ou é aliado não pode ser inferido como congelado sem teste. |
| Amplificadores | `POTENCY`, `RADIUS` e `DURATION` são encantamentos aceitos na fonte; `POTENCY` adiciona metade do nível à potência de dano. | Aumento por perk deve respeitar limites e distinguir `damage`, `radius`, `duration` e `cooldown`. |
| Partículas | `createParticleBall` percorre grade até os limites de raio inteiro com saltos de loop em algumas células; onda visual `ShockwaveParticleOption` é independente do conjunto de vítimas. | Limitar orçamento de partículas/raio, sem contar partículas como hits ou créditos de Mastery. |
| Casting | `frostNovaTime=0` é **tempo de lançamento**, não duração do `FREEZING`; `getSpellType()=FROST` na referência. | Escola e tempo efetivo 3.1.4 dependem de prova de registry/código/config física. |

### ABI exata Goety 3.1.4 confirmada

`FrostNovaSpell` está presente e declara `SpellResult`, `hasCustomCooldown` e `createParticleBall`. `SpellResult` referencia `SpellStat.getRadius`, `getDuration`, `getTarget`, `ModAttributes.getCooldownDiscount` e **`SEHelper.addCooldown`**. Os símbolos provam uma superfície de cooldown **provider-native**, mas **não** a fórmula, o valor ou se foi registrado em todos os caminhos. A chamada ao `SpellExplosion` anônimo não foi interpretada semanticamente pelo probe.

**QA obrigatória:** caster versus target shift, varinhas/staff, limites de raio/potência, imunidade congelamento, allies, cooldown duplicado, custo antes/depois, cancelamento e listeners, dedicated server e teste de performance. **⛔ Alteração de cooldown, AOE ou FREEZING segue bloqueada para perks**; sem homologação física ou por sete evidências.
