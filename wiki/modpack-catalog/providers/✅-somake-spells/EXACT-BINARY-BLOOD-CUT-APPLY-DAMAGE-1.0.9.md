# Somake Spells 1.0.9 — Blood Cut: argumentos da chamada secundária applyDamage

**Certificação:** ✅ `SHA_EXACT_TYPED_APPLY_HANDOFF` e ✅ despacho virtual host → override → setter `0.15f` (PR #863); ⚠️ resultado de dano/cura efetiva; ⛔ perks mutadoras sem hook real.

## Artefato físico e método

- Registry: `somakespells:blood_cut`.
- `somakespells-1.0.9-1.21.1.jar`, CurseForge File `8867079`, SHA-1 físico e publisher `171841ac9f802be9309ecc166c1d972ac6d404c0`.
- Método de evento auditado: `BloodCutEffect.onLivingDamage(LivingDamageEvent.Post)`, **103 instruções JVM**, cinco desvios normais, uma única chamada compilada a `DamageSources.applyDamage`.
- [GitHub Actions Java 21 #39604864087](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39604864087) **SUCCESS**, **86 testes sintéticos** no conjunto (7+9+5+10+10+10+22+13), bytecode da versão exata protegido por SHA, sem exportação de JAR, classfile, código-fonte ou método bruto.
- Verificador clean-room [`somake_109_blood_cut_apply.py`](../../../../docs/qa/somake_109_blood_cut_apply.py), [testes](../../../../docs/qa/somake_109_blood_cut_apply_test.py) e [workflow](../../../../.github/workflows/somake-109-blood-cut-refs.yml).

## Assinatura e pilha JVM

O callsite (índice de instrução **100**) é o método estático tipado:

`io.redspace.ironsspellbooks.damage.DamageSources.applyDamage(Entity, float, DamageSource):boolean`

A inspeção dos **onze últimos opcodes**, com descritores de método e tipos JVM, confirmou a pilha antes da chamada:

| Índices | Produtor | Papel na chamada |
|---|---|---|
| 92–93 | `aload_0` e `LivingDamageEvent.Post.getEntity():LivingEntity` | Primeiro argumento: **entidade atingida no evento**, `event.getEntity()` |
| 94 | `fload_3` | Segundo argumento: valor `float` armazenado em `local_3` no índice 28 |
| 95–97 | `ModSpells.BLOOD_CUT`, `DeferredHolder.get()`, cast para `BloodCutSpell` | Receiver do método que constrói a fonte do dano |
| 98–99 | `aload_1` e `BloodCutSpell.getDamageSource(Entity):SpellDamageSource` | Terceiro argumento: fonte derivada da entidade que originou o dano original |
| 100 | `DamageSources.applyDamage(Entity,float,DamageSource):boolean` | Um único ponto de aplicação **possível** no grafo normal |
| 101–102 | `pop`, `return` | O retorno booleano não é usado pelo próprio handler |

O dossiê [causal anterior](EXACT-BINARY-BLOOD-CUT-CAUSAL-EVENT-1.0.9.md) demonstrou a origem de `local_1`: `event.getSource().getEntity()`, validada como `LivingEntity`. Também demonstrou a origem de `local_3`:

```text
sourceEntity = event.getSource().getEntity()
effect = sourceEntity.getEffect(BLOOD_CUT)
amplifier = effect.getAmplifier()
local3 = event.getNewDamage()
       * (((float)(amplifier + 1) * getEntityPowerMultiplier(sourceEntity)) * 0.1f)

request = DamageSources.applyDamage(
    event.getEntity(),
    local3,
    BloodCutSpell.getDamageSource(sourceEntity)
)
```

Esta é **uma reconstrução semântica de argumentos e expressão compilados**, não código reutilizado do provider nem pseudocódigo que deva ser copiado como implementação. A expressão é válida somente quando as guardas anteriores permitem chegar ao callsite e a aritmética mantém a ordem JVM `float`.

O grafo anterior mostrou **dois caminhos sintáticos** que alcançam essa chamada e **três caminhos que não alcançam**. Saltos diretos ao `return` são saídas legítimas; o verificador rejeita jumps para o meio da preparação dos operandos. A quantidade de caminhos não equivale a probabilidades de proc ou eventos contados.

## Discrepância relevante: duas sobrecargas de getDamageSource

A chamada neste handler é **`BloodCutSpell.getDamageSource(Entity)` (um argumento)**.

O [dossiê de lifesteal anterior](EXACT-BINARY-BLOOD-CUT-LIFESTEAL-1.0.9.md) comprovou o literal `0.15f` passado a `SpellDamageSource.setLifestealPercent(float)` **na sobrecarga `getDamageSource(Entity,Entity)` (dois argumentos)**.

**A ligação foi demonstrada posteriormente, no PR #863.** A [auditoria física do Iron's 3.16.3 #39613550972](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39613550972) prova que o método herdado de um argumento chama a sobrecarga de dois argumentos via `invokevirtual`, repassando a mesma entidade duas vezes; o `BloodCutSpell` a sobrescreve e passa `0.15f` ao setter. Isto **certifica o parâmetro nominal da fonte do hit secundário**, mas não uma cura aplicada de 15%.

O fato seguro atualizado é: **o dano secundário usa a sobrecarga herdada de um argumento, que despacha virtualmente para a override do Somake com dois argumentos e `setLifestealPercent(0.15f)`**. A cura real e a taxa efetiva continuam desconhecidas. [Dossiê de despacho virtual](EXACT-BINARY-BLOOD-CUT-IRONS-VIRTUAL-LIFESTEAL-1.0.9.md).

## Implicações para perks de RPG Skill Tree

- **Alvo:** o candidato ao dano secundário é `event.getEntity()`, não a entidade de origem do dano. Não inferir alcance, área, hitbox ou projétil desse handler.
- **Escalonamento:** o dano solicitado usa `getNewDamage()`, nível do efeito e `getEntityPowerMultiplier(sourceEntity)`; os limites internos do multiplicador, mitigação e valores efetivos permanecem condicionados.
- **Fonte:** a origem de `SpellDamageSource` recebe `sourceEntity` como argumento; isso não prova a identidade do caster original, a propriedade de Mastery ou a cadeia de cura.
- **Retorno:** `applyDamage` devolve um booleano, mas o método `onLivingDamage` descarta o resultado. Não atribuir automaticamente hit confirmado ou Mastery por essa chamada.
- **Proteção contra recursão:** o handler retorna quando o evento original tem `SpellDamageSource`, mas não há prova de proteção contra todas as fontes não mágicas/terceiros.
- **Integração:** sem contrato real de mutação por caster, não alterar dano por interceptação, não reaplicar dano para simular perk, não cobrar custo/cooldown extra e não duplicar eventos de Mastery. **⛔ FAIL_CLOSED**.

**Testes ainda necessários:** inspecionar o processamento de lifesteal e o settlement efetivo no host; executar dedicated server e modpack com ambos os providers, medir dano/vida/restauração, validar PvP, invulnerabilidade e acerto secundário. CI sintético e GameTests do Black Arcana não equivalem a esses testes reais.

**Estado:** Somake ✅ **83/83 IDs**, 🟡 análise estática em andamento (**8/83** neste recorte), ⚠️ comportamento host/real condicionado e ⛔ hook per-player bloqueado. Catálogo global —% (denominador aberto, piso documental ≥1.856). Nenhuma magia/adapter novos; Stage 06.05 🟡, Stage 09 físico PENDING.
