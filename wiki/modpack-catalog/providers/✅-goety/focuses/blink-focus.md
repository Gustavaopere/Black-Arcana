# Goety 3.1.4 — `blink_focus`

Status: **✅ CATALOGADO / COUNTED_EXACT** · identificador factual obtido da auditoria do **JAR 3.1.4 hash-matched** · **⚠️ funcionamento físico/números não validados nesta etapa**.

## Identidade canônica

- **Provider:** Goety (mod id `goety`).
- **JAR instalado e auditado:** `goety-3.1.4.jar` (NeoForge/Minecraft 1.21.1); SHA-1 `a0770e180e4e8b1b87d8fa9c8356e9dbf34d82a7`.
- **Identidade de Focus no artefato:** `blink_focus` — item/ação de Focus ativo do conjunto exato de 123. Não é o `empty_focus` proxy.
- **Posição no inventário exato:** 9/123. Número ordinal editorial, não identificador de registry ou ordem de carregamento.
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

## Auditoria de targeting e teleporte para perks — fonte adjacente Goety 3.1.1 (26/10/2026)

**Proveniência e escopo:** `blink_focus` tem **identidade e aquisição** no JAR instalado `goety-3.1.4.jar` SHA-1 `a0770e180e4e8b1b87d8fa9c8356e9dbf34d82a7`, conforme o inventário exato desta ficha. **A semântica a seguir é exclusivamente do código-fonte público Goety 3.1.1** em [Vivideru/Goety-3@6c41a04f2d712097c4461f969a6bb8ee277149ef](https://github.com/Vivideru/Goety-3/commit/6c41a04f2d712097c4461f969a6bb8ee277149ef). Não houve confronto de classfiles com o JAR 3.1.4; não há equivalência demonstrada de métodos, config, política de claims ou hooks. Grau: `SOURCE_ADJACENT_311 / mutating_hook=NOT_VERIFIED / physical_qa=NOT_TESTED`.

**Descrição funcional da versão de referência:** deslocamento do próprio caster. A aquisição de entidade à frente, a posição de colisão do bloco e o estado de agachamento selecionam caminhos diferentes de teleporte; o método de servidor que aceita um destino em bloco passa por `EntityTeleportEvent.EnderEntity`.

### Evidência localizável na fonte 3.1.1

- [`ModItems.BLINK_FOCUS` — linha 425](https://github.com/Vivideru/Goety-3/blob/6c41a04f2d712097c4461f969a6bb8ee277149ef/src/main/java/com/Polarice3/Goety/common/items/ModItems.java#L425): registro `new MagicFocus(new BlinkSpell())` para o ID, sem certificar a implementação binária 3.1.4.
- [`BlinkSpell.java`](https://github.com/Vivideru/Goety-3/blob/6c41a04f2d712097c4461f969a6bb8ee277149ef/src/main/java/com/Polarice3/Goety/common/magic/spells/void_spells/BlinkSpell.java): `defaultStats().setRange(32)`, `getSpellType()=VOID`, `acceptedEnchantments()=RANGE`, `SpellResult`, `findTeleportLocation`, `enderTeleportEvent`.
- [`SpellConfig.java` — linhas 1777–1784](https://github.com/Vivideru/Goety-3/blob/6c41a04f2d712097c4461f969a6bb8ee277149ef/src/main/java/com/Polarice3/Goety/config/SpellConfig.java#L1777-L1784): **defaults de 3.1.1** `blinkCost=8`, `blinkDuration=0` e `blinkCoolDown=20`. O corpo `BlinkSpell.defaultCastDuration()` **retorna literalmente 0**, independentemente da leitura do parâmetro `BlinkDuration` nesse método da fonte. Config efetiva da instalação desconhecida.
- [`ISpell.entityResult`](https://github.com/Vivideru/Goety-3/blob/6c41a04f2d712097c4461f969a6bb8ee277149ef/src/main/java/com/Polarice3/Goety/api/magic/ISpell.java) e [`MobUtil.teleportTowards/teleport`](https://github.com/Vivideru/Goety-3/blob/6c41a04f2d712097c4461f969a6bb8ee277149ef/src/main/java/com/Polarice3/Goety/utils/MobUtil.java#L1332-L1395) são consumidores de targeting, posições, eventos e bloqueios do teleporte; não é suficiente ler apenas o arquivo da spell.

### Parâmetros, caminhos e limites (apenas 3.1.1)

| Eixo | Contrato localizado | Limite técnico para perks |
|---|---|---|
| Range | Base `SpellStat.range=32` no override; níveis do Focus `RANGE` adicionam alcance; `rightStaff(staff)` dobra o valor. | É range de **aquisição inicial e um parâmetro de cálculo**, não garantia de deslocamento máximo da entidade. Não aplicar bônus externo em 3.1.4 sem consumer exato. |
| Aquisição de entidade | `entityResult(level,caster,range,3)` tenta entidade dentro de um ray de origem ocular e geometria expandida; `ISpell` exige entidade viva? **O predicado explícito é de `LivingEntity`, espectador excluído e entidade pickable** no método default; não confundir raio de colisão 3 com alvo AOE. | `entityResult` não certifica teleporte bem-sucedido nem permissões de proteção. Conferir fonte nativa no JAR real. |
| Se há entidade à frente | Até **64 tentativas** no loop de `MobUtil.teleportTowards(caster,entity)`, interrompendo na primeira que retorna true. O helper submete `EnderEntity` e só executa `randomTeleport` quando a validação permite. | 64 = limite de tentativas, **não 64 teletransportes**; o resultado pode ser falha e não está ligado a um evento Black Arcana. |
| Sem entidade, caster não agachado | `findTeleportLocation(world,caster,32 + range)` projeta linha até bloco usando `MobUtil.rayTrace`, probes de bloco/fluido e correção de ledge/LOS; em seguida `enderTeleportEvent` usa `BlockFinder.SummonPosition` e `EventHooks.onEnderTeleport` antes de `teleportTo`. | Distância da sondagem `32+range` é diferente do `range` da busca por entidade; não declarar cap único. Cancelamento do evento impede o `teleportTo` desse ramo. |
| Sem entidade, caster agachado | Até 64 tentativas de `MobUtil.teleport(caster,range)`, em localização aleatória condicionada pela checagem de terreno e `EnderEntity`. | Não transformar em dash determinístico ou teleporte confirmado sem resultado server-side. |
| Efeitos e mundo | `SpellResult` gera feedback de evento/som em um ramo; não contém `DamageSource` nem modificação direta de blocos nos corpos inspecionados. | Som, partículas e client prediction **não são evidência de teleporte consumado**; verificar claims/modpacks/event subscribers. |
| Custo/cooldown | `defaultSoulCost` e `defaultSpellCooldown` leem config; `defaultCastDuration=0`. | A transação de Soul Energy e a aplicação de cooldown ficam no caminho `IWand/DarkWand/SEHelper` do provider; **não estão resolvidas como hook seguro**. |

### Implicações de integração

- **Identidade:** um cast `blink_focus` pode realizar zero ou um teleporte efetivo; múltiplas tentativas não geram conjurações distintas. Mastery requer critério explícito: intenção aceita, evento de teleporte permitido ou destino consumado; esses três momentos não são equivalentes.
- **Targeting:** ampliar `range`, substituir alvo, atravessar proteção ou escolher destino por perk é **⛔ bloqueado** sem um adapter real para a versão 3.1.4. Um `EnderEntity` identificado em fonte adjacente **não prova que seja o ponto de mutação apropriado** do pack ou que todas as rotas terminem nele.
- **Segurança:** proteger teleporte contra atravessar barreiras, blocos não carregados, dimensão incorreta e áreas privadas exige validação no servidor. Black Arcana mantém `WorldEffectPolicy` apenas sobre efeitos próprios; não atribuir autorização retroativa ao Goety.

**Pendência 3.1.4:** conferir classfile/ABI do `BlinkSpell`, método e predicado de `entityResult`, `MobUtil`, eventos de teleporte, plugins de claims, Soul Energy/cooldown e dedicated-server/Survival. **Status: ⚠️ source-adjacent; sem sete evidências, sem alteração dos índices e sem aprovação de mutação.**
