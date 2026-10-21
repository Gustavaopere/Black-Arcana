# Epic Fight 21.17.3.1 — precedência de AttackPhase e processamento independente do tridente de retorno

**Atualização de prova temporal posterior:** ✅ [JAR exato Java21 #39103337112](EXACT-TRIDENT-RETURN-KINEMATICS-21.17.3.1.md) verificou a sequência contígua de opcodes da **cinemática de retorno** em `ThrownTridentPatch.tickEnd`: `t=max(tickCount-returnTick-10,0)`, `min(t²×0.0005+abs(t×0.05),min(10,d))` e `setPos`. A afirmação histórica abaixo de que velocidade/tempo eram apenas `SOURCE_ADJACENT` passou a ser superada **para esses operandos e essa fórmula**, sem homologar duração, raio, colisões ou velocidade efetiva em jogador real.


**18/10/2026 · ✅ `EXACT_PUBLISHER_METHOD_ORDERED_REFERENCES_AND_OPERANDS` · ⚠️ valor de fase carregada e dano de mundo não observados · ⛔ adapters de perks/Mastery ainda bloqueados.**

## Artefato e verificação

- Mod ID `epicfight`; versão do snapshot físico oficial `21.17.3.1`; CurseForge projeto 405076, arquivo 8175609. Verificação do publicador no runner: SHA-1 `fb199b7bbea2fc402da28ab586e73f47e32f8fc0`, SHA-256 `8b882554cf10086398340fbdc741819ee72a801a3adce516c7f4768326a39526`. O runner baixou o JAR oficial; não houve novo dump local.
- [Workflow Java21 #39102096383](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39102096383), job `exact_skill_parameters`: **SUCCESS**, novo verificador **9/9 autotestes** e `PASS_BOUNDED_TRIDENT_PHASE_PRECEDENCE_AND_RETURN_PATH`, `deviations=[]`. Artefato JSON **#12127086820**, sem redistribuição do JAR de terceiros.
- [Verificador read-only e fail-closed](../../../../docs/qa/epicfight_211731_trident_return_phase_flow.py) e [workflow](../../../../.github/workflows/epicfight-211731-perk-binary.yml). Pré-requisitos incluem prova anterior de JSONs/identidades, SHA exato e associações dos três `AttackPhaseProperty` builders.
- Duas tentativas intermediárias da nova inspeção falharam **no verificador**, antes deste PASS: sintaxe do probe corrigida; janela de leitura do segundo mapa corrigida; acesso à variável local de fase tornado explícito. Não representam falhas de gameplay. O run acima é a evidência positiva selecionada.

## Wrathful Lightning — mapas de propriedades não representam automaticamente fases distintas

| Evidência exata | O que o método realmente demonstra |
|---|---|
| `EpicFightSkills.lambda$static$40`, registro `epicfight:wrathful_lighting` | constrói **dois grupos**: grupo 0 `MAX_STRIKES_MODIFIER.setter(1)`; grupo 1 `MAX_STRIKES_MODIFIER.setter(3)`, `DAMAGE_MODIFIER.setter(8)`, `ARMOR_NEGATION_MODIFIER.adder(100)`, `STUN_TYPE=KNOCKDOWN` e tag `WEAPON_INNATE` |
| `WrathfulLightingSkill.registerPropertiesToAnimation` | o **mesmo objeto Phase**, numa iteração sobre `AttackAnimation.phases`, recebe `properties.get(0).entrySet()` em `Phase.addProperties`, depois `properties.get(1).entrySet()` no mesmo loop |
| `AttackAnimation$Phase.addProperties` | itera entradas e escreve em `this.properties` usando `java/util/Map.put(key,value)`; entradas posteriores com a mesma chave **sobrescrevem** valores anteriores |

**Consequência delimitada:** nesse caminho de registro, quando executado, `MAX_STRIKES_MODIFIER.setter(3)` do grupo 1 substitui `setter(1)` do grupo 0 em cada `Phase` alcançada. Portanto **não** catalogar “fase 1 = 1 alvo; fase 2 = 3 alvos” apenas porque há dois `newProperty`. Um `MAX_STRIKES` da fase não equivale ao número de vítimas/strikes efetivamente realizados no servidor. Este gate não lê um objeto `AttackAnimation` já carregado nem testa outras alterações posteriores do mesmo mapa.

## Everlasting Allegiance — fonte de dano do retorno versus builder de skill

| Caminho | Evidência exata do JAR | Implicação para perks |
|---|---|---|
| `EverlastingAllegiance.registerPropertiesToAnimation` | corpo compilado `aload_0; areturn`, **sem mutação de phase properties nesse método** | os valores existentes no builder da skill não podem ser tratados como propriedades automaticamente injetadas numa `AttackAnimation` por esse método |
| `EverlastingAllegiance.executeOnServer` | caminho de `recalledBySkill` já documentado em auditoria anterior | ativa um ciclo provider-native associado ao tridente rastreado, não autoriza novo cast Black Arcana |
| `ThrownTridentPatch.recalledBySkill` | escreve `dealtDamage` e `innateActivated` e guarda `returnTick` no patch | há um estado de retorno próprio do projétil; não é a mesma coisa que uma fase de ataque convencional |
| `ThrownTridentPatch.tickEnd` — área | três `dconst_1` antes de `AABB.inflate(DDD)`, seguidas de `Level.getEntities` | **expansão de 1 bloco por eixo da bounding box do tridente**, não “raio circular de 1 bloco”, nem limite fixo de alvos |
| `tickEnd` — fonte | `EpicFightDamageSources.trident`, `StunType.HOLD`, `WEAPON_INNATE`, `setBaseArmorNegation(30.0F)`, `ValueModifier.multiplier(1.4F)` + `attachDamageModifier` | o retorno constrói um `DamageSource` com **base de armor negation = 30** e multiplicador de dano **1,4**, independentemente do método vazio de registro de animações; isso **não é equivalente por definição** a aplicar `ARMOR_NEGATION_MODIFIER.adder(30)` sobre qualquer base |
| `tickEnd` — dano | constante `8.0F` na região do loop, seguida de `EnchantmentHelper.modifyDamage` e `Entity.hurt` | **8.0F é entrada pré-modificações de encantamento e mitigação**, não perda final de HP |
| `tickEnd` — movimento | `Math.pow`, dois `Math.min`, atualização `ThrownTrident.setPos` | retorno tem cálculo de deslocamento dinâmico; o verificador não calcula velocidade efetiva em bloco/tick, nem distância máxima de recall |

**Fonte pública adjacente 21.17.3 (sem promoção automática do conjunto inteiro para 21.17.3.1):** [`ThrownTridentPatch.java`](https://github.com/Antikythera-Studios/epicfight/blob/a78aa24b72e90a9d09f5fd61925e4369d117abaf/src/main/java/yesman/epicfight/world/capabilities/projectile/ThrownTridentPatch.java), [`WrathfulLightingSkill.java`](https://github.com/Antikythera-Studios/epicfight/blob/a78aa24b72e90a9d09f5fd61925e4369d117abaf/src/main/java/yesman/epicfight/skill/weaponinnate/WrathfulLightingSkill.java), [`AttackAnimation.java`](https://github.com/Antikythera-Studios/epicfight/blob/a78aa24b72e90a9d09f5fd61925e4369d117abaf/src/main/java/yesman/epicfight/api/animation/types/AttackAnimation.java#L503-L517) e [`EverlastingAllegiance.java`](https://github.com/Antikythera-Studios/epicfight/blob/a78aa24b72e90a9d09f5fd61925e4369d117abaf/src/main/java/yesman/epicfight/skill/weaponinnate/EverlastingAllegiance.java#L90-L94).

O source adjacente indica ainda uma fórmula acelerada de retorno dependente de `tickCount - returnTick` com teto de movimento de 10 unidades por tick e passagem pelo loop de dano enquanto `innateActivated`. Os operandos e a sequência contínua da fórmula agora têm prova **EXACT_PUBLISHER_ORDERED_CONTIGUOUS_COMPILED_OPERANDS** no [novo gate](EXACT-TRIDENT-RETURN-KINEMATICS-21.17.3.1.md); a validação completa de todos os fluxos de controle e efeitos físicos permanece pendente. Nenhum limitador explícito de quantidade total de vítimas foi comprovado por esta auditoria.

## Correções de modelagem de perks

- **Wrathful:** não atribuir `MAX_STRIKES.setter(1)` a “primeira fase” e `setter(3)` a “segunda”; a semântica do código compilado é **sobreposição de mapas da mesma Phase**. Uma perk para “+alvos” depende de reconhecer o estado final e de hook legítimo, não de editar números de builder lidos isoladamente.
- **Everlasting:** distinguir `AttackPhaseProperty` declarado no supplier de skill e **`EpicFightDamageSource` construído no tick do projétil**. Mudança de dano, tipo e `armorNegation` requer avaliar o source efetivamente usado no retorno. `AABB.inflate(1,1,1)` é um parâmetro espacial do código de varredura; não um contrato de área circular alterável externamente.
- **Mastery, proc e deduplicação:** o loop de retorno pode iterar entidades em vários ticks, sob regras do provider; não contabilizar uma nova ativação de magia para cada `Entity.hurt` ou cada etapa de movimento. Sem chave causal provider-owned e prova de settlement, bridge fica **⛔**.
- **Target, cooldown, duração, resultado final e charge:** continuam desconhecidos ou não medidos em player real; o presente verificador não testa alterações de atributos persistentes, `ServerPlayerPatch`, `LivingDamageEvent.Post` nem replay.

**Autoridades:** Epic Fight owns skill/animação/projétil/estados e source de dano; RPG Skill Tree somente progressão/perks/gates por contratos; Black Arcana mantém seu próprio runtime mágico. **Contagem inalterada:** 43/43 IDs core, 3/3 raízes sobrenaturais, 40 habilidades não mágicas relevantes a perks. **+0** magias, **+0** adapters. Global 1.857 objetos semânticos mínimos / 1.855 estritos, denominador total —%. Stage 06.05 🟡 e Stage 09 físico PENDING, PR #825 draft sem merge.
