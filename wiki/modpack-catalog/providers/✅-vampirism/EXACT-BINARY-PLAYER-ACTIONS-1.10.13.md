# Vampirism 1.10.13 — exact physical player-action registry proof

**✅ `COUNTED_EXACT` for the 19 player-action static registry identities only. ⚠️ Not a gameplay, action success, configuration or Survival PASS.**

## Publisher and physical installation identity

- Physical sibling `neoforge-rpg-skilltree@9e6436edb0049a8dcc4e47165db0f6850e5efa68`, modlist position **#558**, `Vampirism-1.21-1.10.13.jar` / mod ID `vampirism` / NeoForge 1.21.1.
- Official CurseForge project **233029**, file **8814121**, release **Vampirism 1.10.13** (not 1.10.14 or the unrelated Minecraft 1.20.1 build).
- Exact publisher size **12,478,474 bytes**; SHA-1 `349b6e4ea893c98a580775b1725399903e222228` equals the physical sibling modlist identity; SHA-256 `e12dafe76bf5df1ab3ed2c94d67bc121eedd8399a88460248edf530180382f97`.
- [Independent Java 21 Action #38664546643](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38664546643): 7 synthetic fail-closed tests passed, download SHA-1 equality confirmed, publisher bytecode audited **PASS**.
- Exact source-version cross-check `TeamLapen/Vampirism@e1ed095713cef5e9eb151d0ee58908fa830d6bb7`; publisher bytes, not future source branches, define the proven runtime artifact.

## Static action identities (source cross-checked, physical JAR verified)

| Exact compiled `DeferredRegister<IAction>` holder | Registry IDs verified | Count |
|---|---|---:|
| `VampireActions` | `bat`, `dark_blood_projectile`, `disguise_vampire`, `freeze`, `half_invulnerable`, `regen`, `sunscreen`, `summon_bat`, `teleport`, `vampire_invisibility`, `vampire_rage`, `hissing`, `infect`, `jump_boost` | **14/14** |
| `HunterActions` | `awareness_hunter`, `disguise_hunter`, `potion_resistance_hunter` | **3/3** |
| `LordActions` | `lord_speed`, `lord_attack_speed` | **2/2** |
| **Total** | 19 unique `vampirism:*` player-action identities | **19/19** |

For each group the independent verifier checks:
1. compiled `VampirismRegistries.Keys.ACTION` and namespace `vampirism` in the deferred-register initialization;
2. individual `ACTIONS → literal ID → invokedynamic` supplier → `DeferredRegister.register` → holder field identity;
3. each LambdaMetafactory `REF_newInvokeSpecial` constructor handle against the exact source-version action class/field;
4. the public bus-registration bridge forwarding `ACTIONS.register(IEventBus)`, without claiming that the bus ran;
5. exhaustive cardinality, missing/extra/duplicate ID rejection and no class/holder alias substitution.

The 19 existing [action catalog entries](ACTION-CATALOG.md) describe provider native mechanics. NPC Entity Actions (10), Minion Tasks (7), skills (31 Vampire + 32 Hunter + 3 Lord), refinements (47), ordinary items/loot, cooldown ticks and action downstream effects are **not additional spell identities**.

## Provider boundaries and Stage gates

The compiled `DeferredRegister` is not direct evidence that the assembled current modpack initialized and applied the registry. Real permission/unlock, `ActionHandler` activation success, faction/Lord skill tree reachability, blood transaction/exhaustion/saturation, cooldown and duration behavior depend on live provider execution.

Vampirism 1.10.13 exclusively owns blood units/bar, Vampire/Hunter and Lord progression, action timers and persistence, minions/villages and skill unlock. Black Arcana must not duplicate these runtime state machines or apply a second blood charge. In particular, Bat can add exhaustion without immediate direct blood debit, and Half Invulnerable pays only on a qualifying blocked hit; `ActionActivatedEvent` fires before `onActivated` success.

Client ActionWheel, current config, real survival acquisition, dedicated multiplayer, relog/death/restart, Werewolves 2.0.3.3 / Bloodlines 3.0.9 / Vampiric Ageing 1.4.21 / Vampire Spells Addon 0.0.9 integrations all remain ⚠️ PENDING in Stage09. Black Arcana Stage 06.05 remains 🟡; sibling RPG Skill Tree may provide progression gates only through inspected safe contracts, not new authority over Vampirism actions.

Clean-room: inspected publisher artifact read-only in independent GitHub Actions; this repository does not contain the third-party JAR or copied game implementation. Generated narrow JSON evidence only.

## Reconstructible catalog accounting

**19 existing source-counted player-action identities → `COUNTED_EXACT` static physical identities**. **+0 newly discovered semantic actions**; strict reconstructible minima stay **1,856 global / 1,854 in scope**. The 39-provider proof campaign advances from **30/39 to 31/39 exact**, with **8/39** conditional. Runtime QA is not a catalog identity promotion criterion and remains separately outstanding.
