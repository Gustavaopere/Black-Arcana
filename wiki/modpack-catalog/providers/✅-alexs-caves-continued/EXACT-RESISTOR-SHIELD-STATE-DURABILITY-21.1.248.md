# Resistor Shield — state transport, continuation and durability (1.0.10 / NeoForge 21.1.248)

## Reproduction and authority

Publisher artifact SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c32e9f2e95bffae0e7c`, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, 75,279,314 bytes; Minecraft 1.21.1, Java 21. Official NeoForge server installer SHA-256 `68eeab77059ba53df1812f1afa5bf530ab2566a3cdcd5f924aa6e71be42e410c`; server overlay `1808fab692dc44b2d474295d1cdd9f1fe8a7dceab4f594210873646fafdf1359`, SRG `26ca9c40d7e1681190b428583c38816852218e78df3f8bdb60a59a78503aec71`, universal `90a56f70425711b4e1a4b94ff0c2904ae9f6d74ca6478b3b2152ac794a07b8e5`. Distributed classes, not a transformed running modpack.

[Discovery run 45461121524](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45461121524), job 138683640420, artifact 14953056580: **629,148 bytes**, SHA-256 `942f310f74d356bfa527dbf77bff3d007bf23cd05e1b0f2714ce57fa69bbc5d4`, 17 owners, five scope checks. [Probe](../../../../docs/qa/alexscaves_1010_resistor_shield_state_durability_probe.py), [workflow](../../../../.github/workflows/alexscaves-1010-resistor-shield-state-durability.yml). Final-head replay required. Extends [native causal evidence](EXACT-RESISTOR-SHIELD-NATIVE-CAUSAL-1.0.10.md) and [defense engine](EXACT-RESISTOR-SHIELD-ENGINE-21.1.248.md).

## State and ownership

ResistorShieldItem class SHA `ffd3fddd74f8d44049886e9013de2e3d67cbd2a721015369175e8442c5044741`. setUseTime Code `f13930a82a8ca44ec18547920ae856863a7055e55764ae7cb3d96a42071fdb0f`; setSwitchTime `c2d73884540a35e88a5ef36717e7a2030738110d7624cbec6b7945ffc0b0b1eb`: obtain/create tag @1, previous value @10 and store @13, new value @21, setTag @26. setPolarity `60037278e6b7f36403083e9953cbc6e6e84091d8c009b872bcfeba85a95664dc`: tag @1, putBoolean @10, setTag @15. isScarlet `d2eb53b10791e1cd0b592890221e220c3c3d54473aa52cc9aa9a9cfc77691ccc` reads tag or false. ACCompat retrieves/writes copies; null setter removes CUSTOM_DATA. CompoundTag stores IntTag or ByteTag; numeric type 99 permits numeric conversions, getByte/getInt return zero on missing or incompatible type. getBoolean tests nonzero converted byte, not textual Boolean parsing. State is stack-local, not a player-owned account/perk or authorization.

PatchedDataComponentMap class SHA `8e2e4f6d466ccefada14f1d8bbce7ff158cd2cdbd0f3ea17fa4bbe442aa5b76f`:

| Method / Code SHA-256 | Proven boundary |
|---|---|
| get / `1513e5c2069b39db26e7054c6ffd30bea2d804cbcd7260d9898a9c539007b798` | patch lookup, null entry falls back to prototype; Optional.empty resolves null |
| set / `ba654f328e64afba4de2f94acfddb2617877dc85fdd7c04a497876f590d8ee44` | CommonHooks.validateComponent @1; ensureMapOwnership @5; equality with prototype @21 removes override @32, otherwise Optional.ofNullable @51 and put @54 |
| remove / `6183e2b07bb2b963066014bbb2bf79d29ca4e836082a8659deab1041422e9e8f` | non-null prototype produces Optional.empty @24/27, otherwise removes patch @44 |
| copy / `c6aff92c085eb3659e28d9b2e890e0c63ed77c558a67a9fe615c714801d4ead0` | shares map/prototype with copy-on-write flags; ensureMapOwnership copies map before mutation, not universal deep-copy proof |
| asPatch / `74d1b20871a3c9c9541bb5cb8a8b70883b2847d0d819a305b2df361a3cd8dd95` | empty patch constant or wrapped map with copy-on-write |

DataComponents initializer binds literal custom_data @13 through lambda @16 and register @21 to CUSTOM_DATA @24. DataComponentPatch initializer constructs CODEC through dispatchedMap/xmap and STREAM_CODEC via nested $1. ItemStack initializer constructs CODEC lazily, OPTIONAL_STREAM_CODEC through $1, STREAM_CODEC through $2. This is codec entry-point evidence, not a complete nested codec implementation audit or runtime persistence proof.

## Menu and packet boundaries

AbstractContainerMenu.broadcastChanges Code `744798ea426eb96fbd05e1cbfc97073e97524f6c1219859e337422d5f2986a6a`: slot item, memoized copy supplier, listener @47, remote synchronization @54. synchronizeSlotToRemote `bbf5c8d1b96e3039a7efb77d00198e3dc921644a3e5fb8ec797cf97865c40e11` checks suppression and ItemStack.matches @23; changed slot copy @47 and non-null synchronizer.sendSlotChange @66. matches compares count and isSameItemSameComponents, latter compares item and components. Component map equals compares prototype and patch. Container slot packet class `cd25247856bee2afb5712214ac336431268befe013bdbc4429f39aaa3d77350d` copies stack in constructor, uses byte/varint/short header then OPTIONAL_STREAM_CODEC. Content packet class `c4a1e0f1efdd0607946ad52fb73579c9a6ca04227e53242e5c1bc9e8f48442c2` copies items/carried stack and uses OPTIONAL_LIST_STREAM_CODEC plus OPTIONAL_STREAM_CODEC. No proof that a shield tick actually sends a packet, remote client applies it or saves/reloads preserve state.

## Continued use and durability

IItemExtension.canContinueUsing Code `b090a35bc4502b419baf64d40f65fab1e32b87959dfd776ade84794e58121385`: same reference passes; otherwise both nonempty and ItemStack.isSameItem @23. No explicit polarity/component equality in this default. IItemStackExtension.canPerformAction `1c2b3684ce2a867edbfdd8899cd7f13b21b3eae5ad6e1276787db28382c152fd` delegates to Item.canPerformAction with stack and ability. Actual hook overrides not presumed.

ItemStack.isDamageableItem Code `f6812b5e020b2876522b0314870f1c65331ac0e5d2f27a12cc20e95d55f9d13f` requires MAX_DAMAGE and DAMAGE, rejects UNBREAKABLE. get/setDamageValue and getMaxDamage delegate to Item. Raw getEnchantments reads ENCHANTMENTS or EMPTY; ACCompat.enchantLevel reads that raw map. EnchantmentHelper.processDurabilityChange `89a14566218ef8a9b87dd342bc5e6c6fc148253f4fcfb2a95c2ba2fd7ff275b9` converts amount to float, MutableFloat @6, runIterationOnItem @19, intValue @23; lambda `a169532c6ca9127aa164463941239eee0d8304f8d781b8e9300568ecde0768c9` calls Enchantment.modifyDurabilityChange @14. runIterationOnItem `6b686fb46d4be3e95586bb5c6bb1e36bee35163ee19054efbff9a2ccc86cc30e` starts from raw map, resolves registry lookup @17; when available uses getAllEnchantments @27, iterates and invokes visitor @82. modifyDurabilityChange `875341b3fcf8e245e748255c106de30a32d98f5df71f9e6d462d06966af34f06` dispatches ITEM_DAMAGE and modifyItemFilteredCount. Raw Heavy Slam level is therefore not proof of the effective enchantment pipeline for durability. No guaranteed one-point settlement.

ItemCooldowns.addCooldown `151898aae82df55a22568833165d235a16a3a730c55b91edf7bc43e61d55ffb8` keys by Item, sets start tick and end tick+duration. getCooldownPercent `d1528c992773798e6273589cd18f962cc3c24b7512b54d435f35756b5d03638e` clamps (end-(tick+partial))/(end-start) to 0..1. Do not treat SwitchTime as cooldown.

## Boundaries and remaining work

Nested codec bodies, actual effective enchantment filters/overrides, client application, live side/order, reload, replacement of stack during use and physical PvP/claim checks remain open. Static individual certification remains partial; no new roots, no index changes, no executable hook. `NO_MUTATION`, `physical_qa=NOT_TESTED`, provider OPEN.
