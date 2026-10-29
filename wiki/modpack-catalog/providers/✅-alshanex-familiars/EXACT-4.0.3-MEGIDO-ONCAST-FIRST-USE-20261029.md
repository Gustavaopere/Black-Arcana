# Alshanex Familiars 4.0.3 — primeiro uso após getters e chamadas de fórmula em Megido

Estado: `EXACT_JAR_ONCAST_DIRECT_CALLS_VERIFIED / IMMEDIATE_USE_PARTIAL / TARGETING_AND_EFFECT_NOT_VERIFIED / PERK_FAIL_CLOSED`.

## Proveniência e limite de observação

A versão física é `alshanex_familiars-1.21.1_v4.0.3.jar`, SHA-1 `e5051c2385a426d05bf203ba8081a23d891f6686`. O workflow [run 40941276448](https://github.com/Gustavaopere/Black-Arcana/actions/runs/40941276448) exigiu **SHA-1 idêntico antes da inspeção**; job `megido_first_use` **SUCCESS**, sete testes sintéticos **PASS**, artifact `12927531288` contendo somente categorias/contagens.

Script e regressões: `docs/qa/alshanex_403_megido_first_use.py`, `docs/qa/alshanex_403_megido_first_use_test.py`; workflow `.github/workflows/alshanex-403-megido-first-use.yml`. O `javap -p -s -c` inspecionou transitoriamente a classe `MegidoSpell`. Nenhuma instrução ou implementação do fornecedor foi gravada no repositório ou no artifact (clean-room, All Rights Reserved).

## Contratos verificados no método `MegidoSpell.onCast`

| Chamada alvo | Observação bytecode 4.0.3 | Teto de prova |
|---|---|---|
| `getRange(): float` | **1 chamada direta**; a primeira instrução posterior foi classificada como `NEXT_INSTRUCTION_NOT_PROVEN_CONSUMER` | O consumidor e a propagação de `15.0F` permanecem `NOT_VERIFIED` |
| `getRadius(): float` | **1 chamada direta**; imediatamente após o retorno ocorre conversão de `float` para outro tipo primitivo (`FLOAT_PRIMITIVE_CONVERSION`) | Não foi certificado qual tipo de destino nem o uso geométrico de `10.0F` |
| `getDamage(int, LivingEntity): float` | **1 chamada direta** à assinatura declarada na própria `MegidoSpell` | Fórmula, multiplicadores, aplicação e repetição de dano `NOT_VERIFIED` |
| `getMaxConnections(int, LivingEntity): int` | **1 chamada direta** à assinatura declarada na própria `MegidoSpell` | Valor, limites reais, conexões efetivas e alvos `NOT_VERIFIED` |

Valores já comprovados no mesmo SHA físico, em auditoria independente: `getRange() = 15.0F` e `getRadius() = 10.0F`. [Retornos literais](EXACT-4.0.3-MEGIDO-RANGE-RADIUS-LITERALS-20261029.md) e [contagem dos callsites da classe](EXACT-4.0.3-MEGIDO-GETTER-CALLSITES-20261029.md). O novo verificador lê somente a instrução **imediatamente seguinte** a cada invocação, sem inferir o fluxo posterior. Para `getRange`, até esse primeiro passo ficou inconclusivo.

O método `getUniqueInfo` já havia sido verificado como outro caller direto de `getRange/getRadius`; não foi reclassificado nem declarado runtime de combate. Uma chamada `getDamage` em `onCast` **não equivale** a um único impacto de dano, tampouco um único call de `getMaxConnections` a um número fixo de saltos: o controle pode usar loops, entidades, filtros e contratos de outros providers.

## Gates de interoperabilidade pendentes

1. Rastrear os consumidores finais dos retornos de `getRange/getRadius` por análise **simbólica bounded** e/ou API oficial exata. Não deduzir `target_range=15` nem `AOE_radius=10` apenas pelos nomes.
2. Auditar as fórmulas de `getDamage` e `getMaxConnections` e condições de `checkPreCastConditions` sem reproduzir implementação proprietária.
3. Identificar hook provider-native seguro, nível do cast, ordem do custo/cooldown, ownership e deduplicação, antes de habilitar perks de range, AOE, dano ou conexões.
4. Exigir testes reais de cliente/servidor modpack, alvos e proteções. **CI de auditoria de JAR não é QA física.**

**Sem promoção:** `mutating_hook=NOT_VERIFIED`, `COMPLETE_PERK_READY=0`, `physical_qa=NOT_TESTED`, `7 spells + 11 rituais = 18 identidades` inalterados. O runtime permanece propriedade do Alshanex/Iron's; Black Arcana não relança efeitos ou liquida custos em paralelo, RPG Skill Tree só fornece progressão através de contrato real.
