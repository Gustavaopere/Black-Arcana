# Somake Spells 1.0.9 — Blood Cut: causalidade compilada do evento Post

**Estado:** ✅ proveniência estática da entidade, efeito, amplificador, expressão float intermediária e filtro `SpellDamageSource`; ⚠️ dano efetivamente entregue e comportamento do host não observados; ⛔ nenhuma mutação de perks por jogador homologada.

## Fonte exata e teste

- Registry: `somakespells:blood_cut`; JAR `somakespells-1.0.9-1.21.1.jar`; CurseForge File `8867079`; SHA-1 físico `171841ac9f802be9309ecc166c1d972ac6d404c0`.
- Método: `com.somake.somakespells.effect.blood.BloodCutEffect.onLivingDamage(LivingDamageEvent.Post):void`.
- [Java 21 #39599959888](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39599959888): **SUCCESS**, SHA-1 conferido e **73 testes sintéticos** na bateria conjunta (7 + 9 + 5 + 10 + 10 + 10 + 22). Registros RED/GREEN dos gates de proveniência: #39596479022, #39597115056, #39597543277 e #39597988594 (falhas esperadas antes dos implementos), com execuções GREEN subsequentes.
- Verificador [`somake_109_blood_cut_event_args.py`](../../../../docs/qa/somake_109_blood_cut_event_args.py), [testes](../../../../docs/qa/somake_109_blood_cut_event_args_test.py) e [workflow Java 21](../../../../.github/workflows/somake-109-blood-cut-refs.yml). **Nenhum JAR, classfile ou corpo de método foi versionado.** Saída apenas de identidades, índices e relações JVM derivadas.

## Cadeia de proveniência comprovada

| Localização compilada | Prova causal estrita | Interpretação permitida |
|---|---|---|
| Índices 0–9 | `event.getSource().getEntity()` → `astore_2` → `instanceof LivingEntity` → `ifeq` de saída → `checkcast LivingEntity` → `astore_1` | O argumento de entidade utilizado adiante é um `LivingEntity` proveniente da **entidade da fonte do dano**, não necessariamente o caster original |
| Índices 10–14 | `event.getSource()` → `instanceof io.redspace.ironsspellbooks.damage.SpellDamageSource` → `ifeq` prossegue; condição verdadeira executa `return` | Evento cuja fonte **é** `SpellDamageSource` é excluído antes de novo dano no handler |
| Índices 15–20 | `LivingEntity(local_1).getEffect(BLOOD_CUT)` → `astore_2` → `ifnull` de saída | Proc condicionado à presença do efeito `BLOOD_CUT` na entidade que originou o dano |
| Índices 21–28 | `event.getNewDamage()` → `MobEffectInstance(local_2).getAmplifier()` → `aload_1` → `getDamageModifier(int,LivingEntity)` → `fmul` → `fstore_3` | O resultado intermediário do handler é o **dano do evento × retorno do modificador**, preservando multiplicação JVM `float` |
| Índice 100 | Uma referência a `DamageSources.applyDamage` | Ponto de chamada possível no fluxo normal; argumentos concretos finais, regras de execução e resultado ainda dependem de auditoria própria |

O gate de CFG independente [#39553030589](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39553030589) preserva **103 instruções**, **cinco desvios** e **dois caminhos sintáticos para o callsite de dano / três sem esse callsite**. Caminhos sintáticos **não** são cinco eventos de gameplay nem probabilidades.

## Relação com a fórmula do modificador

A [prova de retorno JVM](EXACT-BINARY-BLOOD-CUT-CFG-MODIFIER-1.0.9.md) determinou, com operações `float` na ordem compilada:

```text
a = MobEffectInstance.getAmplifier() da entidade fonte do dano
e = LivingEntity retornado por event.getSource().getEntity()

F(e) = BloodCutSpell.getEntityPowerMultiplier(e)
M(a,e) = ((float)(a + 1) * F(e)) * 0.1f
D_intermediario = event.getNewDamage() * M(a,e)
```

No handler Post a entidade foi previamente aprovada por `instanceof LivingEntity`, portanto o ramo `e != null` do getter é o correspondente a esse callsite. O fallback `1.0f` para `e == null` existe no getter, mas **não** é selecionado pela cadeia normal aqui auditada.

**Importante:** `D_intermediario` é a expressão compilada anterior à chamada `DamageSources.applyDamage`; não é uma medição do dano entregue. Não reorganizar as duas multiplicações float do getter como `double` ou assumir arredondamento/mitigação do host.

## Filtro de fonte e risco de recursão

A condição `event.getSource() instanceof SpellDamageSource` retorna imediatamente quando verdadeira. Portanto, este handler **não processa como novo proc** eventos com fonte do tipo `SpellDamageSource`.

Essa condição ajuda a limitar proc-chains de dano mágico do Iron's, mas **não é uma garantia universal contra recursão**: uma segunda fonte que não seja `SpellDamageSource`, hooks de terceiros ou conversões downstream podem seguir outra rota. A prova não inclui a implementação interna do `DamageSources.applyDamage`, o despacho real do event bus, nested events, PvP ou outros mods.

## Considerações para perks e integração

- **Escalonamento:** o parâmetro `a` é o amplificador de `BLOOD_CUT` na **entidade de origem do dano**; há dependência adicional de `getEntityPowerMultiplier(e)`. A fórmula interna desse multiplicador e caps permanecem não avaliados.
- **Alvo:** `e` representa a entidade que originou o dano; o receptor do `DamageSources.applyDamage` ainda não foi certificado. Não equiparar o dado a alcance, área, hitbox ou tipo de alvo da magia.
- **Lifesteal:** o [dossiê SHA-exato](EXACT-BINARY-BLOOD-CUT-LIFESTEAL-1.0.9.md) demonstra `0.15f` entregue ao setter de `SpellDamageSource`; não comprova percentual de cura efetivamente recebido.
- **Mastery e proc:** não atribuir Mastery por cada dano secundário nem aplicar segunda cobrança/cooldown. O RPG Skill Tree só pode influenciar o provider mediante boundary real e comprovado.
- **Hook externo:** ⛔ `FAIL_CLOSED`. Nenhuma API por caster para modificar as fórmulas, origem, alvo ou cura foi homologada.

**Próxima evidência:** rastrear a pilha e os argumentos de `DamageSources.applyDamage`, filtros dos demais ramos, destino do evento secundário no Iron's 3.16.3 e QA exato em cliente/modpack/servidor. Somake é autoridade sobre o efeito; Iron's sobre o host de spell/damage; Black Arcana preserva o runtime próprio; RPG Skill Tree fornece progressão mediante contratos reais.

## Cobertura

Sem incremento de raízes semânticas ou novos adapters. Somake permanece **83/83 IDs registrados**, **8/83 fichas no recorte de método estático** e **5/83 no recorte downstream anterior** (métricas independentes). Global técnico **—%** por denominador aberto, piso **≥1.856**. Stage 06.05 🟡, Stage 09 físico pendente.

## Suplemento de argumentos do dano secundário — PR #862

A [auditoria Java 21 #39604864087](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39604864087) certificou os três argumentos do callsite: `event.getEntity()`, `local_3` e `BloodCutSpell.getDamageSource(local_1)`. O descritor de source usado aqui é **`getDamageSource(Entity)`**, ao passo que o literal `0.15f` documentado anteriormente apareceu em **`getDamageSource(Entity,Entity)`**. O vínculo entre sobrecargas e healing permanece ⚠️ não provado. Ver [dossiê específico](EXACT-BINARY-BLOOD-CUT-APPLY-DAMAGE-1.0.9.md). O `boolean` devolvido por `applyDamage` é descartado e não é teste de hit confirmado.
