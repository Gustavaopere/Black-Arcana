# Escola Empty — Dreamless Spells

## Identidade

- school id: `dreamless_spells:empty`
- power: `dreamless_spells:empty_spell_power`
- resist: `dreamless_spells:empty_magic_resist`
- damage type: `dreamless_spells:empty_magic`
- focus tag: `dreamless_spells:empty_focus`
- focus atual: `dreamless_spells:empty_gem`
- default cast sound: Iron's Evocation Cast
- `requiresLearning`: false por default do `SchoolType`
- `allowLooting`: true por default do `SchoolType`

## Spells ativas

| Spell | ID | Mana | Cooldown | Cast | Níveis |
|---|---|---:|---:|---|---:|
| Drained | `dreamless_spells:drained` | 0 | 180 s | LONG, 30 ticks | 1–3 |
| Dullard | `dreamless_spells:dullard` | 0 | 180 s | LONG, 30 ticks | 1–3 |
| Mute / Doorway Effect | `dreamless_spells:doorway_effect` | 0 | 10 s | LONG, 60 ticks | 1–5 |

Todas são Legendary e todas exigem o efeito `dreamless_spells:emptied` no caster antes de iniciar o cast.

## Emptied

O efeito é aplicado por qualquer set completo Empty Priest/Brawler/Hunter por 200 ticks, amplifier 3.

Modifiers declarados pelo efeito:

- Spell Resist: +0.25 ADD_MULTIPLIED_BASE por nível de amplifier;
- Empty Spell Power: +0.05 ADD_MULTIPLIED_BASE por nível de amplifier;
- Max Mana: -0.25 ADD_MULTIPLIED_BASE por nível de amplifier.

Com amplifier 3, o scaling padrão de MobEffect multiplica por 4. A intenção sistêmica observável é trocar mana tradicional por resistência e poder Empty; o resultado efetivo com todos os modifiers do pack requer runtime QA.

## Aquisição

Os `DefaultConfig` das três spells não desabilitam crafting. A escola é lootável por default e seu Empty Gem é focus válido. Isso as torna elegíveis aos pipelines genéricos do Iron's quando esses pipelines aceitam addon schools.

Fonte de scroll Empty garantida pelo próprio Dreamless: **NÃO VERIFICADO**.

Mais importante: ter o scroll não basta. O caster precisa de `Emptied`, e a progressão das armaduras usa `empty_rune`, cuja rota survival não foi localizada no source 1.1.9.

Ver `PROGRESSION.md`.

## Integração

Black Arcana não cria mana alternativa nem ignora o gate de Emptied. Perks podem reconhecer casts Empty concluídos pelo provider, mas não devem:

- aplicar Emptied diretamente sem contrato explícito;
- zerar mana por fora;
- repetir Drained/Dullard/Mute;
- criar uma segunda escola `empty`.