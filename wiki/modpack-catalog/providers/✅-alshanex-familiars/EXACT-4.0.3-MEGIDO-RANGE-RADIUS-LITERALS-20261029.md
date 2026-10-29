# Alshanex Familiars 4.0.3 — Megido: constantes literais dos dois getters

Estado: `EXACT_BINARY_DIRECT_LITERAL_RETURN / RUNTIME_CONSUMERS_NOT_VERIFIED / MUTATOR_FAIL_CLOSED`.

## Prova de identidade e método

O workflow [run 40935905518](https://github.com/Gustavaopere/Black-Arcana/actions/runs/40935905518), job `megido_literal_audit` (SUCCESS), baixou `alshanex_familiars-1.21.1_v4.0.3.jar` do publisher File ID `8675568` e exigiu SHA-1 `e5051c2385a426d05bf203ba8081a23d891f6686`, igual à autoridade física do modpack, **antes de inspecionar bytecode**.

O parser `docs/qa/alshanex_403_megido_literal.py` verificou unicamente a classe `net.alshanex.alshanex_familiars.spells.MegidoSpell`, descritores de retorno `()F` e retornos `float` de exatamente duas instruções. Qualquer acesso a campo, branch, invocação ou aritmética é rejeitado como `DYNAMIC_NOT_VERIFIED`.

| Contrato do provider | Valor literal retornado no JAR 4.0.3 | Status |
|---|---:|---|
| `MegidoSpell.getRange(): float` | **15.0F** | `EXACT_DIRECT_FLOAT_LITERAL` |
| `MegidoSpell.getRadius(): float` | **10.0F** | `EXACT_DIRECT_FLOAT_LITERAL` |

O job passou **seis** testes sintéticos de parsing/fail-closed e gravou somente `evidence.json` como artifact `12925410592` (14 dias de retenção). O desassemblador `javap` foi invocado apenas transitoriamente; sua saída, métodos e código do fornecedor não são versionados nem redistribuídos.

## Limites explícitos

Estes são valores **da implementação literal dos getters**, não comprovação de alcance real de um cast no modpack, raio exato de dano em cada fase, escala por nível, número de conexões, prioridade de alvos, tamanho de projétil ou custo/cooldown. O uso de `getRange` ou `getRadius` pelos consumidores `onCast` e pela entidade de efeito, assim como os níveis de configuração do pack, **não** foi verificado nesta tranche. Nem todas essas relações precisam existir.

As assinaturas de `getDamage(int, LivingEntity)`, `getMaxConnections(int, LivingEntity)` e `checkPreCastConditions(...)` estavam verificadas na [auditoria de ABI anterior](EXACT-4.0.3-RITUAL-SCHEMA-SPELL-ABI-20261029.md), mas nenhuma fórmula, chamada ou pré-condição foi inferida nesta inspeção. Não equiparar `getRadius` a uma *perk* de AOE pronta.

### Boundary Black Arcana / Skill Tree

- O Alshanex continua owner do spell e da integração Iron's; Black Arcana não substitui o cast, altera getters privados por suposição, duplica dano ou cobra mana/cooldown novamente.
- RPG Skill Tree pode propor perks de alcance/área/conexões por contrato real, mas mutações continuam **⛔ fail-closed** enquanto não houver um hook provider-native comprovado e teste de causalidade no servidor.
- `COMPLETE_PERK_READY` **não** é promovido; QA física do modpack segue `NOT_TESTED`. Total de identidades: **7 spells + 11 rituais**, inalterado.

**Reprodução:** script `docs/qa/alshanex_403_megido_literal.py`, testes `docs/qa/alshanex_403_megido_literal_test.py`, workflow `.github/workflows/alshanex-403-megido-literals.yml`; artifact textual `12925410592`, run `40935905518`.

## Evidência complementar posterior: consumidores na própria classe (29/10/2026)

O [relatório de callsites do JAR 4.0.3](EXACT-4.0.3-MEGIDO-GETTER-CALLSITES-20261029.md) verificou duas referências diretas de invocação a cada getter na classe `MegidoSpell`: uma em `onCast` e outra em `getUniqueInfo` (run `40938851308`). Essa verificação **posterior** resolve somente a lacuna anterior de existência dos callsites nessa classe; não demonstra a propagação do valor retornado para targeting, dano ou área efetiva. Nenhum hook/QA física foi certificado.
