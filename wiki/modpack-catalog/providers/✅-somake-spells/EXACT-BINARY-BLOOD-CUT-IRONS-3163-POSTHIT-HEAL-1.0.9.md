# Blood Cut 1.0.9 × Iron's 3.16.3 — fonte de cura, cálculo nominal e limites

**Situação:** ✅ argumento de setter do Blood Cut, despacho virtual e pilha de cura host certificados estaticamente; ⚠️ dispatch real do evento e cura efetiva ainda não validados; ⛔ nenhuma perk mutadora habilitada.

## Proveniência física

| Artefato | Origem e identidade | Verificação |
|---|---|---|
| Somake Spells | `somakespells-1.0.9-1.21.1.jar`, CurseForge file `8867079` | SHA-1 `171841ac9f802be9309ecc166c1d972ac6d404c0` |
| Iron's addon-facing API | `irons_spellbooks-1.21.1-3.16.3-api.jar` | SHA-256 `69e81104a9fd31a402d9c89ab09c2a6b2fd6d2ab98db5a37bb159517363ee9ad` |
| Iron's runtime completo | `irons_spellbooks-1.21.1-3.16.3.jar`, [CurseForge File 8680204](https://www.curseforge.com/minecraft/mc-mods/irons-spells-n-spellbooks/files/8680204) | SHA-256 `13d644474ddba4f8478b4ce68294687fd509c994b3f344a224142b102dbe6f73` |

A auditoria inicial sobre o **JAR de API** não encontrou marcador de lifesteal nas classes acessíveis e falhou de forma controlada, pois a API não é uma prova suficiente do processamento de eventos. O **JAR runtime oficial**, inspecionado e fixado por hash, revelou `SpellDamageSource` e `DamageSources.postHitEffects`. Não se deve inferir que o código de gameplay está ausente apenas porque uma API destinada a addons não o expõe.

- [Auditoria física Java 21 #39620296495](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39620296495) **SUCCESS**, SHA oficial da API e do runtime, 107 testes sintéticos no conjunto de Blood Cut (7+9+5+10+10+10+22+13+11+10). O HEAD documental subsequente exige nova execução final.
- Auditor read-only: [`somake_109_irons_lifesteal_host.py`](../../../../docs/qa/somake_109_irons_lifesteal_host.py), [testes](../../../../docs/qa/somake_109_irons_lifesteal_host_test.py), [GitHub Actions](../../../../.github/workflows/somake-109-blood-cut-refs.yml).
- Sem versão de arquivos de fornecedor, assets, JARs, classfiles, método disassemblado bruto ou implementação reproduzida.

## Cadeia causal estática do host

O runtime declara `io.redspace.ironsspellbooks.damage.SpellDamageSource` com campo `lifesteal:F`, setter `setLifestealPercent(float)`, getter `getLifestealPercent():float` e predicado `hasPostHitEffects():boolean`.

A classe `io.redspace.ironsspellbooks.damage.DamageSources` contém `postHitEffects(LivingDamageEvent.Post):void`, com **65 instruções JVM**. A auditoria de operandos, descritores e posições de carga/armazenamento prova:

| Índice de instrução | Operação e proveniência | Consequência certificada |
|---|---|---|
| 10–11 | `SpellDamageSource.hasPostHitEffects()`, guarda de retorno | Handler prossegue apenas se o source declara efeitos pós-hit |
| 13–14 | `event.getNewDamage():float` → `fstore_3` | `local_3` contém dano novo do evento |
| 16–17 | `event.getEntity()` → `astore 4` | Vítima do evento separada do futuro receptor de cura |
| 19–27 | `event.getSource().getEntity()` → `local_5`; `instanceof LivingEntity`, `checkcast LivingEntity` e `astore 6` | O candidato a **beneficiário da cura** é a entidade associada à origem do dano, se for LivingEntity |
| 29–32 | `getLifestealPercent()` → comparação com `0.0f` e `ifle` | Cura ignorada quando o percentual não é estritamente positivo |
| 33–38 | `aload 6`, `getLifestealPercent()`, `fload_3`, `fmul`, `LivingEntity.heal(float)` | **Recebedor da chamada `heal` é a entidade da origem do dano**, com argumento `lifestealPercent × event.getNewDamage()` |

Em notação semântica de dados compilados, condicionada às guardas:

```text
sourceEntity = event.getSource().getEntity()      // precisa ser LivingEntity
victim       = event.getEntity()                   // não é o receptor do heal
rate         = SpellDamageSource.getLifestealPercent() // precisa ser > 0.0f
healRequested(sourceEntity) = rate * event.getNewDamage()
```

Não é uma transcrição de implementação proprietária, nem um resultado de Survival. O método faz o produto em **float JVM**. Não se deve trocar essa expressão por uma medição pós-armadura, um percentual de saúde máxima ou um valor `double` sem nova prova.

## Ligação com Blood Cut

O [dossiê de despacho virtual](EXACT-BINARY-BLOOD-CUT-IRONS-VIRTUAL-LIFESTEAL-1.0.9.md) comprovou que o callsite secundário `BloodCutSpell.getDamageSource(sourceEntity)` entra no método `AbstractSpell.getDamageSource(Entity)`, encaminha **a mesma entidade para ambos os argumentos** de `getDamageSource(Entity,Entity)`, despacha virtualmente para o override Somake e entrega **`0.15f`** ao setter de `SpellDamageSource`.

Consequentemente, quando uma fonte de Blood Cut assim construída alcançar `postHitEffects` e suas condições forem satisfeitas, a fórmula solicitada ao método de cura é:

```text
healRequested = 0.15f * event.getNewDamage()
healReceiver  = event.getSource().getEntity() as LivingEntity
```

**Isto é uma prova da rota compilada e da quantidade solicitada**, não uma garantia de 15% de HP recuperado em qualquer acerto. A execução do evento, alterações por outros mods, saúde já máxima, cancelamentos, invulnerabilidade e a lógica final de `LivingEntity.heal` não foram medidos.

## Limites de interoperabilidade

- O método `postHitEffects` e a cadeia de chamadas são físicos; o registro/dispatch do método no event bus **ainda não está certificado nesta auditoria**.
- `DamageSources.applyDamage` no handler Somake recebe a vítima do `LivingDamageEvent.Post`, um float intermediário e a fonte com parâmetro nominal. O retorno booleano dessa chamada é descartado pelo Somake. Não concluir que todos os pedidos causam um evento Post nem que todos os pedidos de cura acrescentam HP.
- O `sourceEntity` é a entidade de `DamageSource.getEntity` e **não deve ser presumido como player, caster original ou owner de Mastery** sem contrato comprovado.
- O predicado de percentual positivo e a validação de `LivingEntity` são guardas físicas; demais regras de elegibilidade, PvP, efeitos concorrentes e caps permanecem ⚠️.
- Black Arcana é autoridade sobre seu próprio runtime; Iron's conserva autoridade de source, dano, hit effects e cura; Somake conserva a magia Blood Cut; RPG Skill Tree só fornece atributos/Mastery/perks por contratos reais. **Não duplicar o pipeline nem aplicar uma segunda cura.**

**Perks de lifesteal por caster: ⛔ FAIL_CLOSED.** Não foi identificada uma API segura para trocar o percentual individual sem mutação do estado de source alheio. A expressão observada pode orientar especificação de balanceamento e testes, mas não autoriza implementação.

## Próxima validação

Confirmar assinatura/anotação/registro de `postHitEffects` no NeoForge event bus da versão exata; demonstrar o despacho após dano realmente bem-sucedido; executar provider-loaded QA no modpack real com vida reduzida e máxima, escudos, PvP, invulnerabilidade, interação com outros efeitos e restart. Medir vida antes/depois. CI e GameTests próprios não substituem esse trabalho.

**Cobertura permanece:** Somake 83/83 IDs ✅, 8/83 no recorte de profundidade estática 🟡, 5/83 no recorte downstream aprofundado anterior ⚠️; global —% com denominador aberto e piso documental ≥1.856. +0 IDs, +0 adapters, +0 hooks. Stage 06.05 🟡, Stage 09 físico PENDING.
