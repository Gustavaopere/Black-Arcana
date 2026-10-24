# Wind’s Spellbooks 1.0.5 — assinatura de recast e registry de efeitos

**Campanha:** continuação pós-PR #887 (24/10/2026) · **Estado:** ✅ metadados de ABI e registries inspecionados; ⚠️ dispatch e factory-binding permanecem pendentes.

## Autoridade física e clean-room

- Minecraft/NeoForge 1.21.1, Java 21. A modlist atual do sibling RPG Skill Tree registra Wind's `wind_spellbooks-1.0.5.jar` (posição 571), Iron's Spellbooks `irons_spellbooks-1.21.1-3.16.3.jar` (342) e IronSable X Wind's `ironsable-wind-1.0.0.jar` (345).
- O JAR Wind's 1.0.5 é verificado contra SHA-1 `8744886899bc245ae147a44baa2b183689cec7da` antes de qualquer `javap`.
- Não publicar JAR, métodos decompilados, instruções originais ou assets. Apenas metadados de assinaturas, hierarquia declarada e referências JVM estruturais; respeitar autoria do provider.

## Escopo do scanner de metadados

`docs/qa/winds_105_effect_registry_dispatch.py` consulta as declarações JVM (`javap -p -s`) e referências de bytecode (`javap -c -p`) em **cinco classes exatamente escolhidas**: `AeropicSpell`, `AeropicEffect`, `TailwindSpell`, `TailwindEffect`, `ModMobEffectRegistry`. A inspeção continua exigindo a população total já congelada em 64 classes e o inventário dos sete spells do JAR.

São dois eixos independentes:

1. **Compatibilidade de ABI:** `AeropicSpell.getRecastCount(int, LivingEntity)` declara o descritor JVM `(ILnet/minecraft/world/entity/LivingEntity;)I`. O `AeropicEffect` referencia simbolicamente `AbstractSpell.getRecastCount` com o mesmo descritor. Isso comprova **compatibilidade estática de assinatura**, não o receiver, a dispatch target ou a execução do override. O host Iron's Spellbooks 3.16.3 e seus contratos precisam de auditoria própria.
2. **Possíveis origens do efeito:** a classe `ModMobEffectRegistry` é inspecionada em busca de `String tailwind`/`acrobatics`/`aeropic`, instruções `new` das classes de efeito, `DeferredRegister.register`, referências de campo e `invokedynamic` por método. A co-presença de strings, factories e campos não prova a ligação entre `TAILWIND`/`ACROBATICS` e a instância concreta: sem rastreio de operandos, bootstraps e class init, registrar `NOT_PROVEN`.

## Critérios de aceitação

- Nove testes sintéticos para descriptor exato, ausência de override/base call, parser de declaração, candidates `new` e proibição de falsas alegações de binding.
- Executar no JAR exato em GitHub Actions, inspecionar `effect-registry-dispatch.json` e registrar apenas fatos positivos verificados nas fichas. Sem extrapolar nomes de classes para hooks.
- CI geral `verify` e `stage05_qa_companion_smoke`, workflow Wind e HEAD final verdes. Comparar main/branch/diff antes de merge.

**Não altera:** runtime Black Arcana, casting do Iron's/Wind's, perks do RPG Skill Tree, contadores de recast, `PlayerRecasts`, armazenamento, registries, config, risco/Survival ou Stage. Hooks mutadores ⛔ `SEM_HOOK_SEGURO`. Stage 06.05 🟡, QA físico do Stage 09 pendente.

**Denominadores invariantes:** 7/7 spells Wind's com fichas, 9/9 getters selecionados, 64/64 classes inventariadas, identidade binária geral 38/39 e mínimo global ≥1.856 (percentual —%).

## Resultado compilado verificado na execução do JAR — 24/10/2026

**Fonte de primeira ordem:** [Wind CI #40139355055](https://github.com/Gustavaopere/Black-Arcana/actions/runs/40139355055) `SUCCESS`; artefato `effect-registry-dispatch.json` baixado e inspecionado, resultado `PASS_SHA_EXACT_REGISTRY_AND_DISPATCH_SYMBOLS`, JAR Wind's 1.0.5 SHA-1 `8744886899bc245ae147a44baa2b183689cec7da`, população **64** classes.

**ABI e superclass:** `AeropicSpell` e `TailwindSpell` estendem diretamente `io.redspace.ironsspellbooks.api.spells.AbstractSpell`; `AeropicEffect` e `TailwindEffect` estendem `io.redspace.ironsspellbooks.effect.MagicMobEffect` e implementam `ISyncedMobEffect` no cabeçalho compilado. `AeropicSpell.getRecastCount(int, LivingEntity)` declara o descritor JVM `(ILnet/minecraft/world/entity/LivingEntity;)I`, exatamente o descritor que o `AeropicEffect` referencia no owner **`AbstractSpell`**. **Compatibilidade de assinatura comprovada; receiver, despacho dinâmico, resultado do método e contrato do host ainda `NOT_PROVEN`.**

**Registry compilado — evidência por região da classe `ModMobEffectRegistry`:**

| Região | Evidência positiva observada | Não provado |
|---|---|---|
| `static {}` | Strings `aeropic`, `tailwind`; referências `ACROBATICS`, `TAILWIND` (DeferredHolder); chamada a `DeferredRegister.register(String, Supplier)`; **2** instruções `invokedynamic` | Qual bootstrap/supplier corresponde a qual registro/campo |
| `lambda$static$0()` | Instrução `new AeropicEffect` e referência ao construtor `(MobEffectCategory, int)` | Ligação desse supplier com o registro/holder `ACROBATICS` |
| `lambda$static$1()` | Instrução `new TailwindEffect` e referência ao construtor `(MobEffectCategory, int)` | Ligação desse supplier com o registro/holder `TAILWIND` |
| `register(IEventBus)` | Chamada a `DeferredRegister.register(IEventBus)` | Momento de registro, execução física e instanciação runtime |

Os dois `invokedynamic` e a ordem dos operandos em `static {}` precisam de análise do `BootstrapMethods`/stack antes de `registration_field_to_instance_binding` poder deixar de ser `NOT_PROVEN`. A evidência **não** autoriza criar hooks próprios de movimento, recast ou armazenamento, nem promover QA físico.

**Regressão:** `docs/qa/winds_105_registry_dispatch_contract.py` valida os cinco cabeçalhos, as superclasses diretamente declaradas, ABI idêntica, 2 sites `invokedynamic`, strings, referências aos dois campos e duas factories candidatas; os 10 testes de mutação rejeitam alegações precoces de dispatch ou de binding.
