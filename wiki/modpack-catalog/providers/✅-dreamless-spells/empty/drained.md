# Drained

**Status do registro:** ✅ `COUNTED_EXACT` para ID estático no JAR físico — [evidência](../EXACT-BINARY-SPELLS-1.1.9.md) ([run #38302406303](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38302406303)). As fórmulas, efeitos, gate, custos e duração abaixo continuam source-pinned, sem QA física de execução/Survival.

- ID: `dreamless_spells:drained`
- escola: Empty (`dreamless_spells:empty`)
- rarity: Legendary
- níveis: 1–3
- cast: LONG
- cast time base: 30 ticks = 1.5 s
- mana: 0 em todos os níveis
- cooldown: 180 s
- target range: 32
- target-area visual: raio 3
- settlement radius no source atual: **2**
- neutral spell power: 5 / 10 / 15
- duração neutra: 200 / 400 / 600 ticks = 10 / 20 / 30 s

## Gate

Só pode ser iniciada se o caster tiver `dreamless_spells:emptied`. Sem o efeito, o pre-cast retorna false.

## Descrição provider

`Reduces the target's mana by 10% per level`.

## Efeito

Depois de mirar um LivingEntity, Drained procura LivingEntity em torno do alvo e aplica `dreamless_spells:drained` aos elegíveis que:

- não sejam o caster;
- estejam dentro do radius efetivo;
- não sejam friendly-fire em relação ao caster.

O effect modifica `irons_spellbooks:max_mana` com `-0.1 ADD_MULTIPLIED_TOTAL` e recebe amplifier `spellLevel - 1`.

Nominalmente:

- nível 1: -10% Max Mana total;
- nível 2: -20%;
- nível 3: -30%.

Duração = `spellPower × 40` ticks.

## Divergências 1.1.9

### Cap de vítimas

A classe declara `MAX_TARGETS = 5`, mas o `AtomicInteger targets` nunca é incrementado. Portanto o código auditado não impõe o limite de cinco durante a iteração.

### Radius

O pre-cast desenha radius 3. No settlement, `radius` resolve para o import estático de `FireflySwarmProjectile.radius`; no Iron's 3.16.3 esse valor é `2f`. Declarações locais de radius 3 não alimentam a busca final.

Documentação canônica: **intenção visual 3 / settlement estático 2 / runtime QA obrigatório**.

## Obtenção

A spell mantém crafting habilitado por default e a escola Empty é lootável por default. Empty Gem é o school focus válido.

Entretanto, o uso em survival depende de `Emptied`, cuja rota normal passa pelos full sets Empty e pela `empty_rune`; a aquisição survival dessa rune não foi localizada no provider 1.1.9.

## Authority / dedup

Authority = aplicação única de `DSSEffects.DRAINED_EFFECT` pelo `onCast`. Black Arcana não deve reaplicar redução de mana, refazer a busca em área ou impor silenciosamente o cap 5.

## QA

- 6+ alvos hostis dentro da área para confirmar ausência/presença do cap;
- alvos entre 2 e 3 blocos para confirmar divergência de radius;
- friendly-fire/party filtering;
- duração e Max Mana nos três níveis;
- cast após perder `Emptied` durante os 30 ticks de cast.

## Atualização de ABI exata 1.1.9 — 27/10/2026

A [auditoria do JAR físico dreamless_spells-1.1.9.jar](../EXACT-1.1.9-SPELL-CAST-AND-COUNTERSPELL-ABI-20261027.md) (SHA-1 `d51960bfb8af1aafa5d716ef9a48c3135f36b956`, run [#40499150605](https://github.com/Gustavaopere/Black-Arcana/actions/runs/40499150605)) confirmou estas relações de código **sem importar corpos de método**:

O classfile `DrainedSpell` confirma `checkPreCastConditions` e `onCast` com referência a `DSSEffects.EMPTIED_EFFECT`. O `onCast` usa `TargetedTargetAreaCastData.getTarget`; o método compilado `lambda$onCast$0` referencia `DSSEffects.DRAINED_EFFECT` e `LivingEntity.addEffect`. O binário não certifica neste probe o raio final, o limite de cinco vítimas ou a duração descritos na fonte 1.1.9.

**Status:** `EXACT_BINARY_METHOD_REFERENCES` (estático) · `SOURCE_ALIGNED_NUMBERS_NOT_BINARY_PROVEN` · `physical_qa=NOT_TESTED` · `mutating_hook=NOT_VERIFIED`. Nenhum registro novo, certificação de perk, custo adicional ou segundo pipeline Black Arcana. O provider permanece autoridade do efeito, e Iron's da transação de casting.
