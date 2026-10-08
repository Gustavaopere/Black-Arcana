# T.O Magic n' Extras 4.4.0.1 — fichas canônicas de spells

Este índice materializa em fichas individuais as **33 identidades de spell** já fechadas pela auditoria clean-room do publisher artifact exato CurseForge `6342780` para a versão física `4.4.0.1-1.21.1`.

O provider permanece **⚠️ parcial/condicionado**: o JAR físico atual está fingerprintado como `OTHER_VERIFIED` no SHA-1 `7b74816e89cc15dd0b5a31d9ea1e456024e8fae4`, mas seus bytes/proveniência e o delta exato do registry atual continuam não materializados; `traveloptics:blackout` segue sem rota survival objeto-a-objeto fechada e o runtime atual ainda não fecha todos os gates do provider.

## Contexto semântico público condicionado

As 33 fichas agora têm uma camada complementar de contexto comportamental em [`PUBLISHER-SEMANTIC-CONTEXT.md`](PUBLISHER-SEMANTIC-CONTEXT.md). Ela correlaciona **somente as 33 identidades exatas registradas** com descrições curtas, parafraseadas da página oficial atual do publisher.

Essa camada é deliberadamente **não-estrita e version-conditioned**: a página do projeto é viva e não é um snapshot versionado do alpha `4.4.0.1-1.21.1`. Ela não altera registry, reachability, números mecânicos, `blackout`, status do provider nem `+0 strict`. A autoridade exata continua sendo a auditoria do File `6342780` e, para o pack atual, a evidência física/runtimes registrada no `README.md`.

## Inventário por escola

### Blood — 1

- [`traveloptics:blood_howl`](blood/blood-howl.md)

### Eldritch — 5

- [`traveloptics:abyssal_blast`](eldritch/abyssal-blast.md)
- [`traveloptics:blackout`](eldritch/blackout.md)
- [`traveloptics:psychic_bolt`](eldritch/psychic-bolt.md)
- [`traveloptics:reversal`](eldritch/reversal.md)
- [`traveloptics:spectral_blink`](eldritch/spectral-blink.md)

### Ender — 6

- [`traveloptics:eternal_sentinel`](ender/eternal-sentinel.md)
- [`traveloptics:orbital_void`](ender/orbital-void.md)
- [`traveloptics:cursed_minefield`](ender/cursed-minefield.md)
- [`traveloptics:void_eruption`](ender/void-eruption.md)
- [`traveloptics:vortex_punch`](ender/vortex-punch.md)
- [`traveloptics:astral_sense`](ender/astral-sense.md)

### Evocation — 2

- [`traveloptics:ashen_breath`](evocation/ashen-breath.md)
- [`traveloptics:lingering_strain`](evocation/lingering-strain.md)

### Fire — 5

- [`traveloptics:ignited_onslaught`](fire/ignited-onslaught.md)
- [`traveloptics:burning_judgment`](fire/burning-judgment.md)
- [`traveloptics:meteor_storm`](fire/meteor-storm.md)
- [`traveloptics:lava_bomb`](fire/lava-bomb.md)
- [`traveloptics:gyro_slash`](fire/gyro-slash.md)

### Holy — 3

- [`traveloptics:nullflare`](holy/nullflare.md)
- [`traveloptics:summon_desert_dwellers`](holy/summon-desert-dwellers.md)
- [`traveloptics:sword_of_the_ancients`](holy/sword-of-the-ancients.md)

### Ice — 5

- [`traveloptics:axe_of_the_doomed`](ice/axe-of-the-doomed.md)
- [`traveloptics:cursed_revenants`](ice/cursed-revenants.md)
- [`traveloptics:despair`](ice/despair.md)
- [`traveloptics:halberd_horizon`](ice/halberd-horizon.md)
- [`traveloptics:cursed_blast`](ice/cursed-blast.md)

### Lightning — 4

- [`traveloptics:mechanized_predator`](lightning/mechanized-predator.md)
- [`traveloptics:rapid_laser`](lightning/rapid-laser.md)
- [`traveloptics:death_laser`](lightning/death-laser.md)
- [`traveloptics:em_pulse`](lightning/em-pulse.md)

### Nature — 2

- [`traveloptics:aerial_collapse`](nature/aerial-collapse.md)
- [`traveloptics:stele_cascade`](nature/stele-cascade.md)

## Contagem

- 33 fichas individuais materializadas;
- 33/33 correspondem a registros reais do exact publisher artifact;
- 33/33 registram explicitamente `Registry field` + `Concrete class` do mapping exato field -> class -> ID;
- 33/33 incluem contexto semântico público condicionado, sem promovê-lo a comportamento versionado do alpha/current physical;
- 33/33 include an exact File-`6342780` mechanics baseline for base/per-level mana, base/per-level spell-power inputs, cast type/time, max level, minimum rarity and default cooldown; these values are not projected to current physical SHA-1 `7b74816e...`;
- 24/33 carry **37 exact File-only resolved bounded accessor outputs** from File `6342780`: 29 no-`LivingEntity` outputs plus 8 LivingEntity-signature outputs proven entity-unused; the other 7 entity-unused effective-cast methods are exact direct delegates and resolve only through the pinned current Iron's 3.16.3 host contract, bringing numeric accessor/bridge coverage to **28/33** spell identities; **all 34/34 entity-reading numeric accessors are now dependency-classified** (24 host-spell-power only, 9 additionally using Iron's `SUMMON_DAMAGE`, 1 adding `Math.min`), so identity-level accessor/bridge/dependency coverage stays **33/33** while those 34 entity-reading methods remain numerically entity/config conditional;
- 30/33 individual spell cards now materialize their exact `ENTITY_SLOT_READ` dependency contracts from audit #658; the three cards with no entity-reading accessor remain `blackout`, `cursed_minefield` and `cursed_blast`. This adds dependency documentation only and assigns no new numeric return value;
- 7/33 carry explicit publisher-only quantitative/conditional notes where the living official page states a concrete threshold, timing, partition count, trajectory angle or equipment-evolution gate; these remain non-strict and non-version-pinned;
- 21/33 are now classified `HOST/PUBLISHER-DEFAULT CRAFTABLE + ENABLED / EFFECTIVE ELIGIBILITY CONDITIONAL`: exact File `6342780` has no direct craftability or enabled-default mutator in those concrete classes and no `isEnabled()` / `canBeCraftedBy(Player)` override, while current Iron's 3.16.3 defaults both `allowCrafting` and `enabled` to `true`; effective Scroll Forge eligibility still depends on active config, focus/school compatibility and player-learning gates;
- 2/33 retain provider Weapon `allowCrafting=true`; 10/33 retain provider Unique `allowCrafting=false`; 9 have exact structured loot anchors, while `blackout` additionally has `allowLooting=false` and its File-6342780 provider-owned direct + generic loot routes are excluded, though current-pack acquisition remains unresolved;
- 32 localization-only IDs residuais continuam excluídos;
- nenhum número de mana/cooldown/dano/nível foi inferido;
- status global do provider permanece ⚠️.

## Autoridade

`EXACT-4.4.0.1-ARTIFACT-AUDIT.md` continua sendo a evidência técnica primária. O baseline mecânico exato está em [`EXACT-4.4.0.1-MECHANICS-BASELINE.md`](EXACT-4.4.0.1-MECHANICS-BASELINE.md), os 37 resultados escalares File-only estão em [`EXACT-4.4.0.1-SCALAR-ACCESSORS.md`](EXACT-4.4.0.1-SCALAR-ACCESSORS.md), a classificação da superfície com `LivingEntity` está em [`EXACT-4.4.0.1-LIVINGENTITY-ACCESSORS.md`](EXACT-4.4.0.1-LIVINGENTITY-ACCESSORS.md), o bridge de effective cast time está em [`EXACT-4.4.0.1-CURRENT-HOST-EFFECTIVE-CAST-BRIDGE.md`](EXACT-4.4.0.1-CURRENT-HOST-EFFECTIVE-CAST-BRIDGE.md), o mapa completo de dependência dos 34 accessors entity-reading está em [`EXACT-4.4.0.1-ALL-ENTITY-DEPENDENCY-MAP.md`](EXACT-4.4.0.1-ALL-ENTITY-DEPENDENCY-MAP.md), o refinamento de craftability herdada está em [`HOST-CRAFTABILITY-3.16.3-CHECKPOINT.md`](HOST-CRAFTABILITY-3.16.3-CHECKPOINT.md), o default enabled está em [`HOST-ENABLED-3.16.3-CHECKPOINT.md`](HOST-ENABLED-3.16.3-CHECKPOINT.md), e a exclusão da rota provider-owned de loot para Blackout está em [`BLACKOUT-GENERIC-LOOT-EXCLUSION.md`](BLACKOUT-GENERIC-LOOT-EXCLUSION.md). Estas fichas são a projeção editorial objeto-a-objeto para o catálogo canônico.
