# Wind's Spellbooks 1.0.5 — ampliação de getters puros de mobilidade

## Escopo e autoridade

- Base: catálogo e quatro ASTs escalares homologadas documentalmente no PR #882, sem mudança de `7/7` spells ou registro mágico ≥1.856.
- JAR provider: `wind_spellbooks-1.0.5.jar`, SHA-1 `8744886899bc245ae147a44baa2b183689cec7da` (verificação obrigatória **antes** do `javap`).
- Fonte de presença e versão: modlist física do sibling RPG Skill Tree, posição 571; não tratar versão do publisher diferente como instalada.
- Novos candidatos, todos retorno JVM `freturn`: `AlmightyPushSpell.getRange(int, LivingEntity)`, `IronSlashSpell.getDistance(int, LivingEntity)`, `TailwindSpell.getPercentAirSpeed(int)`, `TailwindSpell.getPercentJump(int)` e `WindJumpSpell.getJumpStrength(int, LivingEntity)`.

## Critério de prova

`docs/qa/winds_105_mobility_getters.py` reutiliza o parser de pilha e a verificação integral do JAR do PR #882. Não introduz interpretador alternativo. **Somente** instruções aritméticas permitidas, sem escrita em campos, chamadas desconhecidas, condicionais ou saltos, podem formar uma AST compilada. Se qualquer um dos cinco métodos apresentar opcode desconhecido, assinatura ambígua, ausência ou pilha inconsistente, o processo termina com `FAIL_CLOSED` e o CI reprova. Não publicar fórmula suposta a partir de chamadas soltas.

Inicialmente todos os cinco candidatos são **🟡 EM AUDITORIA** até a execução do workflow no HEAD exato. O inventário das fichas anteriores não deve ser substituído por valores de um novo scanner sem cruzar a saída com o JAR SHA-exato. Depois da evidência do CI, escrever fórmulas nos `.md` individuais apenas quando o resultado for `EXACT_STRAIGHT_LINE_EXPRESSION`. Não registrar `PASS` por inspeção sintética.

## Limites explícitos

Um retorno denominado `range`, `distance`, `strength` ou `percent` **não comprova** alcance efetivo em blocos, potência, raio de colisão, tipo de alvo, política de PvP, aplicação em entidades, dano, unidades, scaling configurável nem possibilidade de mutação por perk. Host Iron's preserva mana/cooldown/casting, Wind's preserva o efeito, RPG Skill Tree fornece progressão somente por contrato e Black Arcana controla apenas seu runtime.

Continuam **⛔ SEM_HOOK_SEGURO** as perks mutadoras que ainda não têm API/surface comprovada e QA provider-native. Manter `Stage 06.05` 🟡, `Stage 09` físico pendente, cobertura global —% e 38/39 identidade binária sem promoção.

## Qualidade

- Regressões sintéticas com ausência de método, corpo com branch/chamada desconhecida, pilha inconsistente e arquivo/classe extra.
- CI exato do JAR da versão 1.0.5, seguido de revisão do artefato JSON, sem redistribuição do JAR, bytecode ou código do provider.
- Reconciliar a branch com a última `main` antes de merge, reexecutar CI do HEAD final, verificar os jobs do workflow específico e CI geral; distinguir premerge de postmerge.
