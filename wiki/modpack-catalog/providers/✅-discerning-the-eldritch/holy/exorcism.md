# Exorcism

**Registro binário físico (2026-10-13):** ✅ `COUNTED_EXACT` — `discerning_the_eldritch:exorcism`, classe `net.acetheeldritchking.discerning_the_eldritch.spells.holy.ExorcismSpell`, escola padrão `SchoolRegistry.HOLY_RESOURCE` ([Java 21 #38455449207](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38455449207), [dossiê](../EXACT-BINARY-SPELLS-1.4.4-1.21.md)). Insanity default off: presença no registry não garante uso em jogo. Custos/efeitos e Survival ⚠️; +0.

- **ID:** `discerning_the_eldritch:exorcism`
- **School:** Holy
- **Level:** 1
- **Rarity:** Epic
- **Cast:** Long, 10 ticks
- **Mana:** 75
- **Cooldown:** 25 s
- **Role:** cleanse/reset DTE Insanity

## Config gate

DTE Insanity system upstream default = **disabled**.

`allowCrafting()` and `allowLooting()` return true only when `DTEServerConfig.enableInsanitySystem` is true. `canBeCastedBy` also fails when the system is disabled and fails when the player has no insanity to remove under the attachment state checked by the provider.

## Settlement

On a valid cast with Insanity attachment value >0:

- `INSANITY_METER = 0`;
- `IS_INSANE = false`.

It does **not** implement a general harmful-effect cleanse. The name Exorcism must not be generalized into “remove all debuffs”.

## Dedup / authority

This is the canonical DTE Insanity purge. Any Divine/Holy bridge should manipulate the DTE attachments only through an explicit integration contract; do not infer insanity from Darkness or titles.

## Presentation

Iron's `CLEANSE_CAST` sound and kneeling-prayer animation.

## Source

`ExorcismSpell.java`, `DTEServerConfig`, DTE 1.4.4 branch.
