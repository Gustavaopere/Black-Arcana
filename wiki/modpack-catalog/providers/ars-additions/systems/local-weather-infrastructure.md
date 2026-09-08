# Local weather infrastructure

Status: `SOURCE-PINNED 21.3.0 / DORMANT-IN-PRODUCTION PATH / NOT CATALOGED AS ACTIVE MAGIC`

Exact source pin: `Jarva/Ars-Additions@91f102a90dc058cf40e4eac5a67a881e48b856b4`.

Ars Additions registers a serializable chunk attachment `ars_additions:local_weather_status` with enum states NONE, CLEAR, RAIN, SNOW and THUNDER. It also has a network payload capable of synchronizing that attachment to watched chunks.

However, the exact 21.3.0 production path does **not** establish an active local-weather magic system:

- `WeatherStatus.setWeatherStatus` explicitly assigns `NONE` when `FMLEnvironment.production` is true;
- the experimental `mixin/weather/WeatherMixins.java` implementation is entirely commented out;
- no weather mixin appears in the exact `ars_additions.mixins.json` manifest.

Therefore the registered attachment/network plumbing is cataloged as dormant/incomplete infrastructure, not as proof that Ars Additions currently overrides rain, snow, thunder, biome precipitation or weather gameplay per chunk in the shipped production path.

## Black Arcana boundary

Black Arcana must not treat the presence of `local_weather_status` as an existing weather-control provider contract. If this infrastructure becomes active in a future provider version, the exact-version audit must be reopened before integrating weather or environmental magic.
