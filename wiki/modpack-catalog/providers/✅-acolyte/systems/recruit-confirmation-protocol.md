# Recruit confirmation protocol and menu

Status: `BINARY_VERIFIED` for exact publisher Acolyte 1.0.3; installed-JAR equality and assembled-pack behavior are `NOT_VERIFIED`, physical QA is `NOT_TESTED`. These menu/network classes implement companion actions and add **0 Acolyte-owned spells**. See [release evidence](../BINARY-CONTRACTS-1.0.3.md) and the [artifact manifest](../ARTIFACT-CATALOG-MANIFEST-1.0.3.json).

The menu is registered as `acolyte:recruit_menu`. `HumanEntity#openRecruitScreen(ServerPlayer)` captures current server values, creates a `RecruitMenu` through `HumanEntity$1`, and writes the same values to its client constructor. The client screen sends `acolyte:confirm_recruit`; the server validates and executes the action. Ownership, payment and deadline behavior are detailed in the [recruitment contract](recruitment-contract.md).

## Menu data and client display

The menu's data fields are final opening-time snapshots. The ordered opening-buffer fields are:

| Sequence | Value | Wire type |
|---|---|---|
| 1 | Entity runtime ID | `int` |
| 2–5 | Health, max health, attack damage, armor | Four `float`s |
| 6 | Recruited **and owned by this recipient** | `boolean` |
| 7 | Contract remaining fraction, or 0 for an unowned recipient | `float` |
| 8 | Display name text | UTF string |
| 9 | Spell-list length | `int` |
| 10 | Each host spell identity | Resource-location entries |
| 11 | Current recruit cost | `int` |
| 12–13 | Remaining contract ticks, current total duration ticks | Two `long`s |
| 14 | Selected profile tier, or 1 for a null profile | `int` |

`HumanEntity#getAllProfileSpells()` collects attack, defense, mobility and utility lists in that order, then barrage and single-use spells; null list members are omitted, duplicates removed, and the result limited to eight. The menu transmits **spell identities**, without spell levels, quality values or cooldown state. This list is a display aid; it does not prove every icon has an executable goal in that role.

The 200×217 screen uses atlas identity `acolyte:textures/gui/recruit_screen.png` (200×335). It displays the captured health, armor and duration and draws a live client entity portrait when the ID resolves as a living entity. The transmitted max health, attack damage and contract-progress values are not rendered as separate stats by `renderStats`. The tier frame clamps its visual tier to 1–4. At most eight host spell icons are drawn in two columns; host null/`none` resolutions are skipped.

Owned duration displays the opening snapshot as minutes:seconds after integer division by 20. Unowned duration displays integer in-game days (`ticks/24000`) when at least one day, otherwise integer minutes (`ticks/1200`). These screen/menu classes contain no live countdown refresh. The emerald cost is rendered from the snapshot price; affordability is checked later by the server.

`RecruitMenu` exposes the player's 27 inventory slots and nine hotbar slots. Its `quickMoveStack` returns empty, and `stillValid(Player)` always returns true; these methods do not add entity-distance validity or a shift-transfer route.

## Client actions and packet shape

`RecruitScreen#init` branches only on the recipient-facing recruited flag. False shows Hire. True shows Follow, Stay and Unrecruit. It does not disable Hire based on affordability or disable either order based on a selected/current-order state. `TexturedButton` supplies ordinary/hover texture rendering and the label, with no additional permission policy.

Each click sends its packet and immediately closes the screen. Follow requests `orderStay=false`; Stay requests true. Successful hiring reopens the menu from the server after payment and assignment. Release/order branches do not reopen it in this handler.

`PacketConfirmRecruit` is a record `(int entityId, boolean unrecruitOnly, boolean hasOrder, boolean orderStay)` implementing `CustomPacketPayload`. Its type ID is **`acolyte:confirm_recruit`**. `NetworkHandler` registers it play-to-server under protocol version string **`"1"`**; `handle` enqueues the operation through the payload context.

| Factory | `unrecruitOnly` | `hasOrder` | `orderStay` |
|---|---|---|---|
| `recruit(entityId)` | false | false | false |
| `unrecruit(entityId)` | true | false | false |
| `order(entityId,stay)` | false | true | requested value |

The codec writes a fixed-width integer followed by the three booleans in that order: **7 payload-field bytes**, excluding NeoForge/Minecraft packet framing. There is no price, owner UUID, duration, spell level or menu ID in this payload; those are server-owned state or absent from the operation.

## Server validation and causality

The enqueued handler executes these branches in order:

1. Require the context player to be a `ServerPlayer`; resolve the entity ID in that player's **current `ServerLevel`**; require `HumanEntity`. Otherwise return.
2. If `unrecruitOnly`, require stored ownership by this player, invoke `onUnRecruit`, and return. This takes precedence if both action flags are true.
3. Otherwise, if `hasOrder`, require stored ownership, set the requested stay boolean, and return.
4. Otherwise, if already recruited, return. A different owner receives `gui.acolyte.recruit.already_hired`; the current owner receives no renewal or new charge.
5. Obtain the entity's current recruit cost and count exact emerald stacks. If insufficient, send `gui.acolyte.recruit.not_enough_emeralds(cost)` and return.
6. Remove the price, invoke `recruit(player,currentLevel)`, then reopen the recruit screen.

The count helper examines `Inventory.items`; the removal helper iterates the inventory's container indices, shrinking exact emerald stacks by the smaller of remaining price and stack count until the price is satisfied. The demonstrated payment precedes ownership mutation and menu reopening. There is no refund or rollback branch in this handler.

The handler has no explicit distance, line-of-sight, alive-state, current-menu/entity binding, creative exemption or protection-system check. Same-level entity lookup, Human type checks and the branch-specific ownership/payment checks are the demonstrated boundaries. This is a description of the audited checks, not a claim of a verified protection bypass or observed multiplayer failure. Runtime consequences and external hooks remain `NOT_TESTED`.

## Technical boundaries

| Quantity | Value / authority |
|---|---|
| Target | One current-level runtime entity ID; only Human families accepted by the handler. |
| Range / radius | No numeric packet-range gate. Client menu opening comes from normal Human interaction. |
| Cost / duration | Server recomputes price from the selected profile; [recruitment](recruitment-contract.md) owns tier and game-time values. |
| Action time / cooldown | Enqueued server work; no local cast time or action cooldown. Exact latency is not specified. |
| Mana / damage / knockback | No local debit or damage/knockback action. |
| Spell level / school / projectile | N/A for the protocol; UI spell IDs are host identities only. |
| Stay behavior | [Stay-order goal](../goals/stay-order.md); setting the flag does not itself run that goal. |

## Binary evidence

All names below begin `net.raptorzizi.acolyte.`; PC ranges refer to the exact publisher class methods, not copied bodies.

- `registries.ModMenuRegistry#<clinit>` PCs 0–27 and `lambda$static$0` PCs 0–8 establish the menu identity/factory.
- `entity.mobs.wizards.human.HumanEntity#openRecruitScreen(ServerPlayer)` PCs 0–225; its serialization lambda PCs 0–147; `#getAllProfileSpells` PCs 0–139 and `#addSpellArray` PCs 0–48. `HumanEntity$1#createMenu` PCs 0–61 captures the server menu.
- `gui.RecruitMenu` buffer constructor PCs 0–164; `#addPlayerInventory` PCs 0–102; `#stillValid` PCs 0–1; `#quickMoveStack` PCs 0–3.
- `gui.RecruitScreen#init` PCs 0–273; `#renderStats` PCs 0–290; duration formatters PCs 0–41 / 0–45; `#renderSpellIcons` PCs 0–128; `#renderTierFrame` PCs 0–76; `#onRecruitClicked` PCs 0–20, `#onOrderClicked` PCs 0–21, `#onUnrecruitClicked` PCs 0–20. `RecruitScreen$TexturedButton#renderWidget` PCs 0–151.
- `network.NetworkHandler#onRegisterPayloads` PCs 0–35. `PacketConfirmRecruit#<clinit>` PCs 0–33; its factories PCs 0–11; codec lambdas PCs 0–36 / 0–23; `#handle` PCs 0–14; enqueued `lambda$handle$2` PCs 0–209; emerald helpers PCs 0–63 / 0–72.

Client presentation, packet arrival, multiple-player ordering, stale menus, entity removal, protection integration, restart/dimension transitions and installed-host compatibility were not exercised in a running pack.
