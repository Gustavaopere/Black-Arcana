# Wind's Spellbooks 1.0.5 — efeitos, movimentos e registries

**Estado ✅: símbolos compilados verificados no JAR exato; ⚠️ efeitos aplicados e hooks continuam não homologados.** Isto não é um novo mod, spell, adapter nem autorização de perk mutadora.

## Contexto físico e recorte

- Versão instalada da modlist sibling: `wind_spellbooks-1.0.5.jar`, mod ID `wind_spellbooks`, SHA-1 congelado `8744886899bc245ae147a44baa2b183689cec7da` (posição 571). Iron's Spellbooks host `irons_spellbooks-1.21.1-3.16.3.jar` e IronSable X Wind's `ironsable-wind-1.0.0.jar` são dependências/sibling providers distintos; não são automaticamente incluídos na inspeção.
- A auditoria anterior verificou 64 classes do JAR oficial, nove getters escalares selecionados e 16 `invoke*` diretos aos getters (zero a partir de outra classe no mesmo JAR). A ausência de chamada direta não explica o comportamento dos efeitos.
- O novo scanner `docs/qa/winds_105_effect_boundaries.py` percorre todas as `.class` do namespace físico Wind's, aproveitando a verificação ZIP/SHA exata já homologada.

## Perguntas semânticas e limites

1. Quais classes no JAR têm nomes associados a `Tailwind`, `Acrobatics` ou `Effect`? **Nome é apenas indicador de candidato**: não prova registration, listener, efeito ativo, hook nem atributo efetivo.
2. Quais métodos possuem referências diretas aos campos `TAILWIND` ou `ACROBATICS` do registry observado? Qual o método de origem e se ele é `onCast`, `tick`, `applyEffectTick` ou um helper?
3. Em candidatos de efeito, quais assinaturas e símbolos JVM sugerem possíveis operações de velocidade, salto, queda, atributo, impulso, dano, tick e remoção? Relatar métodos, campos, chamadas e famílias de operadores, sem copiar implementação nem atribuir argumentos.

## Prova admissível

- `onCast` de `TailwindSpell` lê o campo `TAILWIND` e o de `AeropicSpell` lê `ACROBATICS`: isso é **prova de referência JVM ao registry**, não de qual instância `MobEffect`/classe é retornada ou de como seu modificador funciona.
- `javap -c -p` é usado apenas para obter metadados simbólicos de método/campo/opcode, publicando **somente JSON de inventário**. Sem source/copiar asset/disassembly ou JAR proprietário.
- O scanner usa `CANDIDATE_AND_OR_REGISTRY_REFERENCE_ONLY`; `runtime_effect_settlement` é sempre `NOT_PROVEN` sem host/provider execution. Nenhum ponteiro de API de perks decorre de nomes.
- Falha de SHA, classe/roster, referência onCast esperada, duplicidade, erro do scanner ou método fora do limite de output deve falhar fechado.

## Gates de integração

- Rodar os testes sintéticos de proveniência, a varredura no JAR exato e inspecionar o artefato JSON. Só depois registrar fatos nas fichas `tailwind.md` e `aeropic.md`, distinguindo `name-candidate`, `direct-field-ref` e o que permanece `NOT_PROVEN`.
- `Black Arcana CI` (`verify` e `stage05_qa_companion_smoke`) e `Wind's exact-JAR` no HEAD final devem ser `SUCCESS`; reconciliar o PR com a `main` atual antes do merge.
- Nenhum Stage promovido: `06.05` 🟡 para aceitação física, `09` pendente; runtime Black Arcana próprio, RPG Skill Tree apenas provider progressão/gates; nenhum hook mutador da Wind implementado.
- Denominadores independentes e preservados: catálogo Wind's **7/7 magias**; getters previamente selecionados **9/9**; campanha binária **38/39**; global **—%**, ≥1.856 objetos.

## Evidência binária confirmada — JAR 1.0.5

Fonte: [Wind CI #40136512061](https://github.com/Gustavaopere/Black-Arcana/actions/runs/40136512061) `SUCCESS`, artefato `effect-boundaries.json` inspecionado, SHA-1 `8744886899bc245ae147a44baa2b183689cec7da`. Scanner visitou **64** classes do namespace e classificou **9** classes como candidatas por nome ou referência de campo. Não são nove magias ou nove efeitos registrados.

### `net.raptorzizi.wind_spellbooks.effect.TailwindEffect` — métodos do efeito candidato

| Método compilado | Símbolos observados no corpo | Limite de interpretação |
|---|---|---|
| `applyEffectTick(LivingEntity, int)` | `LivingEntity.getDeltaMovement`, `onGround`, `setDeltaMovement(DDD)`; escrita em `LivingEntity.fallDistance`; leitura `Player.xxa`, `Player.zza` | Há uma superfície explícita de movimento/queda; não se conhece magnitude, beneficiário ou path runtime efetivo. |
| `onEffectStarted(LivingEntity, int)` | `Attributes.JUMP_STRENGTH`, `AttributeModifier.Operation.ADD_MULTIPLIED_TOTAL`, `AttributeInstance.addTransientModifier` e `removeModifier`; aritmética float | Há uma superfície de atributo de salto e operação multiplicativa dentro do método; valor, condições, alvo e ciclo efetivo não foram resolvidos. |
| `onEffectRemoved(LivingEntity, int)` | `Attributes.JUMP_STRENGTH`, `MOVEMENT_SPEED`, `AttributeInstance.removeModifier`; ramos `ifnull` | Remove modificadores por referência simbólica; não deduzir que velocidade seja criada nesse mesmo método, nem tempo/stacking. |

**Correção da lacuna anterior:** percentuais de `TailwindSpell.getPercentAirSpeed` e `getPercentJump` não são invocados diretamente de outra classe Wind's, mas o próprio `TailwindEffect` contém operações de movimento e atributos. Não são legitimamente classificáveis como `UI_ONLY` nem podem ser usados como argumento do modifier sem fluxo JVM comprovado. O registry `TAILWIND` é lido por `TailwindSpell.onCast`; a ligação exata do factory/registro do efeito ao objeto ainda não foi provada neste relatório.

### `net.raptorzizi.wind_spellbooks.effect.AeropicEffect` — recasts e combate

| Método compilado | Símbolos observados no corpo | Limite de interpretação |
|---|---|---|
| `applyEffectTick(LivingEntity, int)` | `AbstractSpell.getRecastCount(ILivingEntity)I`, `PlayerRecasts.addRecast`, `PlayerRecasts.hasRecastForSpell`, `RecastInstance.<init>`, `DamageSources.applyDamage`; escrita em `LivingEntity.fallDistance`, `Entity.invulnerableTime` | Prova dependências de recast, dano e queda no método, mas não dano, quantidade, alvo, taxa/condições nem execução. |
| `onEffectAdded(LivingEntity, int)` | `AbstractSpell.getRecastCount`, `ServerPlayer.getPersistentData`, `CompoundTag.putInt/remove` | Recast/persistência estão presentes simbolicamente; não há prova de valor nem de estado salvo exato. |
| `onEffectRemoved(LivingEntity, int)` | `PlayerRecasts.decrementRecastCount`, `hasRecastForSpell`, `CompoundTag.remove`, `LivingEntityAccessor.setLivingEntityFlagInvoker` | Há caminho de limpeza de recast/flags, sem provar ordem de cleanup ou políticas anti-duplicação. |

**Caveat de despacho virtual:** o efeito referencia o método **da classe-base** `AbstractSpell.getRecastCount`, não uma chamada direta à classe `AeropicSpell.getRecastCount` — isso explica o zero cross-class do PR #886 sem demonstrar qual override é executado. O host Iron's 3.16.3, receiver concreto e runtime devem ser auditados antes de qualificar a relação causal.

## Gate para regressões

`docs/qa/winds_105_effect_contract.py` fixa SHA-1, 64 classes, população 9 de candidatos, referências de `onCast` aos campos `ACROBATICS` e `TAILWIND`, e os símbolos compilados observados nos dois efeitos (incluindo jump attribute, movimento, fallDistance, recast e dano). O contrato exige `NOT_PROVEN` para settlement do efeito. Os testes sintéticos rejeitam falso hook, classe ausente, mudança em campo e alteração na semântica dos metadados.

**Resultado técnico:** duas classes de efeito com superfícies compiladas identificadas, sem novos spells (`7/7`), sem novo getter (`9/9` selecionados), sem CI de cliente/Survival, sem proof de magnitude, unit/argument binding ou hook mutador. `Stage 06.05` 🟡, Stage 09 pendente, progresso global —%.
