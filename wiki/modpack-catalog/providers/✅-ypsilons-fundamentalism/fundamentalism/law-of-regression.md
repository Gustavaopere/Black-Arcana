# Law Of Regression

**✅ Revalidação SHA-exata 2026-10-13:** spell ID estático `ypfundamentals:law_of_regression` confirmado no JAR físico/publicador 1.1.7.1 (`a2855c253202a8fcc2925fcf5b1bf86d64fbe4da`), escola default Fundamentalism, [Java21 #38436717443](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38436717443) SUCCESS. `COUNTED_EXACT` somente registry e classe, +0 novas raízes. [Dossiê](../EXACT-BINARY-SPELLS-1.1.7.1.md). Progressão, mana/config, multiplayer e Survival ⚠️.


- ID: `ypfundamentals:law_of_regression`
- escola: `ypfundamentals:fundamentalism`
- rarity: Legendary
- níveis: 1–4
- cast: CONTINUOUS, castTime base 200 ticks / 10 s
- mana: 80 / 70 / 60 / 50 (`manaCostPerLevel=-10`)
- cooldown: 5 s
- heal por `onCast`: `spellLevel`
- loot: desabilitado
- crafting: desabilitado
- `requiresLearning=true`

## Efeito

Cada execução provider-native de `onCast` posta `SpellHealEvent`, cura o próprio caster em `spellLevel` e remove efeitos curáveis por `EffectCures.HONEY`. A frequência/total efetivo de cura ao longo de um continuous cast depende do pipeline Iron's 3.16.3 e requer runtime QA; não multiplicar manualmente por ticks.

## Aprendizado

Remedium >=5 aprende o spell. O SpellSelectionEvent oferece:
- Remedium 5–9 → lvl1
- 10–13 → lvl2
- 14–16,18–19 → lvl3
- 20 → lvl4

**QA:** o switch omite Remedium 17, portanto no source pin não adiciona option para 17. Registrar como quirk upstream, não corrigir silenciosamente.

## Dedup

Principles progression é authority do unlock e do nível exposto.