# Capability Matrix Delta — Ars Polymorphia 1.0.3

Status: `EXACT SOURCE-PINNED / ZERO-SEMANTIC BRIDGE`

| Capability | Exact evidence | Black Arcana consequence |
|---|---|---|
| Ars Storage/Crafting Lectern recipe-conflict enumeration | exact 1.0.3 source injects into Ars crafting-matrix change and enumerates server-side matching crafting recipes for the player's lectern matrix | Ars + Polymorph-compatible provider retain recipe-selection authority; Black Arcana must not create another resolver |
| Player-scoped selection state | source resolves lectern inventory and Polymorph selection by player UUID/player data | do not globalize or duplicate provider selection state in Black Arcana |
| Client conflict selector | exact source has one client mixin for Ars crafting-terminal presentation | client selector state is presentation/intent, never Black Arcana gameplay authority |
| Server-side settlement | provider unit payload requires Ars crafting-terminal/lectern context and re-resolves the current recipe through Polymorph before updating Ars state | Black Arcana should observe any final craft result, not replay reset/selection traffic |
| Provider networking | protocol version `1`; one provider-owned play-to-server payload `ars_polymorphia:reset_crafting_result` | no second packet protocol or settlement path is justified in Black Arcana |
| Direct host bindings | 4 common + 1 client required mixin/accessor bindings | current Ars-version compatibility remains runtime QA, not an inferred contract |
| Spell/glyph/ritual/resource/action content | no independent magical action registry is established by the exact source tree | semantic magic delta `+0`; no Stage 07 spell-domain gap is consumed |

## Host compatibility disposition

Physical host set is Ars Nouveau `5.13.1` plus `polymorph_plus` `1.3.1+1.21.1`. Exact source requires mod id `polymorph`, targets Ars build host `5.4.2.938`, and contains a Minecraft range declaration `[1.21,1.21.1)` despite an explicit `minecraft_version=1.21.1` property.

These are compatibility questions, not permission to fabricate an alias or second authority. Runtime integration remains fail-closed until direct current-host evidence exists.
