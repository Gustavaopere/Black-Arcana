# Somake Spells 1.0.9 — Funeral Bloom: prova de fluxo float e limite de ramificações

**Estado:** ✅ expressão JVM float de `getImpactDamage` demonstrada; ⚠️ `getRadius` conserva prova limitada a clamp e contagem de branches; ⛔ nenhuma mutação por perk homologada.

## Artefato exato e metodologia

- Modlist sibling `neoforge-rpg-skilltree/main@ed5b65b890767b406ce41127bcb793775263c7bd`: `somakespells-1.0.9-1.21.1.jar`, CurseForge File 8867079, mod ID `somakespells`, SHA-1 `171841ac9f802be9309ecc166c1d972ac6d404c0`.
- [Execução Java 21 #39243467444](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39243467444) **SUCCESS**, 10 testes (incluindo fixture Java compilada); dois métodos de `com.somake.somakespells.spells.blood.FuneralBloomSpell` avaliados com identidade e assinaturas JVM exatas. Uma versão posterior da PR adicionou snapshots negativos para exigir a permanência da evidência; considerar apenas CI da HEAD final como gate de merge.
- [Scanner](../../../../docs/qa/somake_109_float_dataflow.py), [testes](../../../../docs/qa/somake_109_float_dataflow_test.py) e [workflow](../../../../.github/workflows/somake-109-float-dataflow.yml). Interpreta a pilha abstrata e os tipos de todas as instruções de um método linear, aceitando somente uma invocação externa comprovada a `getSpellPower` com descriptor e argumentos válidos. Qualquer opcode, ramificação, campo ou invocação não admitida bloqueia o resultado; jamais exportar código do provider, bytecode, assets ou JAR.

## `getImpactDamage(int,LivingEntity):float`

**Resultado técnico comprovado por análise integral de pilha:**

```text
return_float32 = 1.5f + (getSpellPower(level_input, caster) * 0.75f)
```

A ordem da expressão acompanha as instruções JVM observadas: primeiro a multiplicação float por `0.75`, depois a adição float de `1.5`. O método é linear (0 branches), usa dois literais float e contém **uma referência a `getSpellPower`** com o `level_input` e o `caster` recebidos. Não reordenar a expressão como se as operações de ponto flutuante fossem associativas sob todas as condições de arredondamento IEEE-754.

**O que esta prova não significa:** `getSpellPower` ainda precisa ser resolvido sob o host exato Iron's e sob configuração/atributos efetivos. A fórmula não garante que cada cast use esse retorno; não demonstra `DamageSources.applyDamage`, redução do alvo, dano final, evento cancelável, crítico, PvP, claims ou ganho de Mastery. O callsite de efeito mecânico está no `FuneralBloomBudEntity.impact`, já auditado separadamente.

## `getRadius(int,LivingEntity):float`

| Evidência | Resultado exato | Limite |
|---|---|---|
| Método e assinatura | `(ILnet/minecraft/world/entity/LivingEntity;)F` | Identidade física do mesmo JAR |
| Branches | 2 instruções de desvio no método | O avaliador linear devolve `NOT_PROVED / branch_or_throw`; nenhum caminho é inferido |
| `Mth.clamp(FFF)F` | Segundo e terceiro operandos literais imediatamente anteriores: `10.0f` e `15.0f` | Não comprova o resultado bruto do primeiro operando nem sua origem em todas as branches |
| Contexto do método | Literais adicionais `0.65`, `0.82`, `9.5`, `1` e referência a `SchoolType.getPowerFor` do probe numérico anterior | Fórmula integral do alcance e contribution de escola continuam desconhecidas |

Os argumentos do clamp constituem evidência de limites **daquela chamada JVM**, não da área efetiva, hitbox da entidade ou raio final para toda condição possível. O método exige auditoria de CFG, do branch predicate e do consumo de seus retornos antes de propor perk de alcance.

## Engenharia de perks e ownership

- ✅ O retorno algébrico do getter de dano pode alimentar uma ficha documental e futura simulação *somente* com SpellPower grounded, nunca substituir o efeito nativo.
- ⚠️ `FuneralBloomBudEntity.impact` referencia `DamageSources.applyDamage`, Wither e `SpellHealEvent`; esses canais não são equivalentes, podem ser condicionais, e dependem de verificação de evento/consumidores/owner.
- ⛔ **FAIL_CLOSED** para adaptação de dano por jogador, raio, targeting e escala até contratos públicos/eventos exatos, sem novo cast, dupla mana/cooldown ou Mastery por cada bud.
- ⚠️ Testes Java21 estáticos não substituem cliente, multiplayer, Survival, datapack/config, world-safety, reload ou modpack real sob D035.

Somake continua owner da execução da magia; Iron's é authority de host e recursos; RPG Skill Tree fornece progressão/Mastery/perks apenas por boundaries reais; Black Arcana mantém somente seu próprio runtime. Sem nova identidade de magia, Stage 06.05 continua 🟡.

**Continuidade:** analisar CFG e caminho de `SchoolType.getPowerFor` para `getRadius`; confirmar descriptor/implementação admissível de `getSpellPower` no Iron's 3.16.3, configuração do pack e a aplicação downstream de dano. Relacionados: [dossiê numérico](EXACT-BINARY-FUNERAL-BLOOM-NUMERIC-1.0.9.md), [bud](EXACT-BINARY-FUNERAL-BLOOM-BUD-1.0.9.md), [ficha](registry-1.0.9/funeral-bloom.md).
