# Alshanex Familiars 4.0.3 — limite de conexões e dependências do dano de Megido

Estado: `EXACT_INT_LITERAL_VERIFIED / DAMAGE_INVOCATION_VERIFIED / DAMAGE_FORMULA_NOT_VERIFIED / MUTATOR_FAIL_CLOSED`.

## Autoridade exata e execução auditável

- Modlist física `neoforge-rpg-skilltree`, entrada `alshanex_familiars-1.21.1_v4.0.3.jar`, `modid=alshanex_familiars`, SHA-1 **`e5051c2385a426d05bf203ba8081a23d891f6686`**.
- CI read-only [run 40949235333](https://github.com/Gustavaopere/Black-Arcana/actions/runs/40949235333), job `megido_numeric_footprint` **SUCCESS**. O auditor exigiu paridade SHA-1 **antes** de ler o binário. **11 regressões sintéticas** passaram no último run. Run inicial de estrutura: `40948995027`.
- Ferramenta: `docs/qa/alshanex_403_megido_numeric_footprint.py` e regressões `docs/qa/alshanex_403_megido_numeric_footprint_test.py`, workflow `.github/workflows/alshanex-403-megido-numeric-footprint.yml`.
- Apenas metadados de ABI, agregações de operações e limites literais foram produzidos. Nenhum corpo de método, disassembly, JSON proprietário ou asset foi copiado para o repositório (clean-room, All Rights Reserved).

## Contratos efetivamente verificados por método

| Método exato compilado | Observação demonstrada | O que **não** está demonstrado |
|---|---|---|
| `MegidoSpell.getMaxConnections(int, LivingEntity): int` | Retorna **diretamente `2147483647` (`Integer.MAX_VALUE`)** em duas instruções (uma constante `int` e `ireturn`), sem leituras locais de rank/caster e sem aritmética/ramificações detectadas | Quantos alvos são atingidos, se há outro cap, se há limite de cadeia/loops, custo e consequência de uma perk |
| `MegidoSpell.getDamage(int, LivingEntity): float` | Corpo com **cinco instruções**, uma invocação não qualificada referida como `getSpellPower`, uma leitura local do argumento de nível e outra de caster; **zero** operações aritméticas `float`/`int`, conversões, leituras de campo ou branches locais | Igualdade com `getSpellPower`, fórmula de dano, multiplicadores, efeito aplicado por alvo, qualificativo da classe proprietária da chamada ou intensidade por nível |

A tentativa de reconhecer `getDamage` como um retorno direto, sem transformações, de `getSpellPower` recebeu resultado **`NOT_VERIFIED`** sob o padrão exato exigido pelo auditor. Portanto a documentação registra uma **referência de chamada**, não `getDamage = getSpellPower`.

### Consequência de `Integer.MAX_VALUE`

`2.147.483.647` é o **valor do método** que representa um teto inteiro virtualmente aberto, **não** número de saltos reais ou tamanho demonstrado de busca. O próprio `onCast` chama `getMaxConnections`, como demonstrado na [auditoria de primeiro uso](EXACT-4.0.3-MEGIDO-ONCAST-FIRST-USE-20261029.md), mas o consumidor completo ainda não foi inspecionado. Restrições físicas, orçamento, target filtering, descarte de entidades e limites de processamento podem existir **fora** do getter. Nenhuma dessas hipóteses foi homologada.

Assim, uma perk que some ou multiplique `getMaxConnections` é potencialmente redundante e pode provocar overflow se tratar esse valor como inteiro aritmético. **Não executar mutação, clamp, adaptação de custo, segunda seleção ou segundo cast por suposição.** Investigar a causalidade real, budgets/caps do provider e a seam server-native antes de propor qualquer efeito.

### Pendências para próxima auditoria

1. Investigar estaticamente o fluxo que consome `getMaxConnections`, filtros de alvos, comportamento de overflow e possíveis caps de chains, sem publicar código de terceiro.
2. Investigar a chamada `getSpellPower`: owner/descriptor e condições de retorno com evidência do JAR exato, sem inferir desde já uma fórmula de dano.
3. Confirmar lado servidor, proteção de mundo, custos, cooldown, respeitar APIs/hook reais e QA física multiplayer no modpack.
4. Nenhuma certificação de perk/implementação pode ser promovida antes desses gates.

Estado inalterado: `7 spells + 11 rituais = 18` identidades semânticas; `COMPLETE_PERK_READY=0`, `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`. Alshanex e Iron's mantêm ownership de seus efeitos, custos e casting. O Black Arcana não duplica execução; RPG Skill Tree só entrega progressão mediante contrato.

## Descoberta posterior: entidades/targeting cross-provider (29/10/2026)

O [relatório de ABI do `onCast`](EXACT-4.0.3-MEGIDO-ONCAST-TARGET-ENTITY-ABI-20261029.md) demonstrou referências a `MegidoEntity` (Alshanex) e `BallLightning` (Iron's) com chamadas `setDamage(float)` e dois `Level.addFreshEntity`. Não comprova dois spawns efetivos, consumidores finais de `getMaxConnections` ou dano real. O ownership de cada entidade pertence a seu provider.
