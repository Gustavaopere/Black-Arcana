# Cloudshaping

Status: `SOURCE-PINNED 5.13.1 / GLOBAL-WEATHER RITUAL`

- Registry id: `ars_nouveau:ritual_cloudshaping`
- Class: `RitualCloudshaper`
- Exact release checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`

## Provider-native behavior

Cloudshaping operates on the server Overworld because Ars Nouveau treats weather as global. Once per 20 game ticks it advances ritual progress; at progress `18` it applies one weather outcome and finishes.

Optional item state is mutually exclusive because `canConsumeItem` accepts only one item while the consumed-item list is empty:

- no modifier: clear weather using a random clear delay sampled from `12000..180000` ticks;
- Gunpowder: rain for a random duration sampled from `12000..24000` ticks;
- Lapis Block: rain + thunder for a random duration sampled from `3600..15600` ticks.

The modifier item is provider-owned ritual input state, not a Black Arcana cost channel.

## Authority / Black Arcana boundary

Weather selection, random duration and global settlement remain Ars Nouveau authority. Black Arcana must not reapply weather, double-consume the modifier or convert this ritual into a generic weather cast.

Future Black Arcana weather/domain mechanics require a semantic gap and independent safety/budget contracts.

## QA

Exact source behavior is pinned to 5.13.1. Interaction with other weather-control providers in the 612-mod runtime remains a separate QA item.