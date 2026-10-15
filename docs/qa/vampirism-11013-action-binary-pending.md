# Vampirism 1.10.13 — exact publisher player-action registry audit

**🟡 Audit in progress; no `COUNTED_EXACT` claim and no catalog promotion.**

Physical sibling `neoforge-rpg-skilltree@9e6436edb0049a8dcc4e47165db0f6850e5efa68` modlist position **#558**: `Vampirism-1.21-1.10.13.jar`, mod ID `vampirism`, SHA-1 `349b6e4ea893c98a580775b1725399903e222228`; NeoForge Minecraft 1.21.1. Official CurseForge project **233029**, file **8814121**, release 1.10.13. Exact upstream source pin `TeamLapen/Vampirism@e1ed095713cef5e9eb151d0ee58908fa830d6bb7`.

Source catalog already counts **19** strictly provider-native player actions. Exact pinned `VampireActions` constructs/registers **14** actions, `HunterActions` **3**, `LordActions` **2** using NeoForge DeferredRegister and `LambdaMetafactory` constructor suppliers. This audit targets only the compiled declaration/namespace/class/holder registration identity and the event-bus submission method. It is not proof of the bus being executed in the assembled modpack, user ability unlocks or actual provider action behavior.

The read-only Java 21 script will hash-match the publisher file, find the three compiled action registry classes, compare each literal ID, constructor handle and holder field against source-pinned manifest, reject any extra/missing/duplicate/foreign registration, and emit narrow JSON only. Test fixture uses entirely independent synthetic Java 21 registry code; publisher JAR remains excluded from the repository.

**Fail-closed boundaries:** Vampirism is authoritative for blood/feeding, factions, Lord progression, player skills, `ActionHandler` permissions, cooldown/duration and state. Do not duplicate blood/casting/resource, mutate unlock progression or infer success from `ActionActivatedEvent` alone. Runtime config, event-bus initialization, client ActionWheel, dedicated multiplayer/Survival/relog/death, interop with Bloodlines, Werewolves, Vampiric Ageing and Vampire Spells Addon all remain unverified. RPG Skill Tree is sibling progress/perks only under inspected real contracts. Black Arcana Stage 06.05 remains 🟡; D035 carries exact physical acceptance under Stage09.

Current campaign before proof: **30/39 exact / 9/39 conditional**, strict reconstructed minima **1,856 global / 1,854 in scope**. All 19 actions are already counted as source-pinned, so successful exact proof would add **+0** new semantic actions.
