# Wind's Spellbooks — catálogo canônico

## Estado

- Mod ID: `wind_spellbooks`
- JAR instalado: `wind_spellbooks-1.0.5.jar`
- Versão instalada: `1.0.5`
- Runtime alvo: NeoForge 1.21.1
- Provider base: Iron's Spells 'n Spellbooks
- Escola própria: Wind
- Release exata: CurseForge file `8485822`, publicada em 2026-07-22
- Catálogo: **7/7 spells ativos documentados**
- Estado de evidência: `RELEASE-PINNED 1.0.5 / RUNTIME-REGISTRY OBSERVED / SOURCE PÚBLICO NÃO LOCALIZADO / BYTECODE NUMÉRICO PENDENTE`

A página oficial da release 1.0.5 descreve o addon como uma escola completa de Wind com **sete spells upgradáveis**, armor de mago, staff, spellbook, Windmill e Aeromancer. Os logs reais do pack confirmam exatamente sete registrations `wind_spellbooks:*` e expõem as classes carregadas pelo runtime.

## Inventário 7/7

1. [Wind Jump](wind/wind-jump.md) — `wind_spellbooks:wind_jump`
2. [Tornado](wind/tornado.md) — `wind_spellbooks:tornado`
3. [Iron Slash](wind/iron-slash.md) — `wind_spellbooks:iron_slash`
4. [Aeropic](wind/aeropic.md) — `wind_spellbooks:aeropic`
5. [Almighty Push](wind/almighty-push.md) — `wind_spellbooks:almighty_push`
6. [Wind Blade](wind/wind-blade.md) — `wind_spellbooks:wind_blade`
7. [Tailwind](wind/tailwind.md) — `wind_spellbooks:tailwind`

## Evidência runtime do pack

O analisador ASM carregado no próprio modpack observou as classes e fingerprints abaixo:

| Spell | Classe runtime | Fingerprint observado |
|---|---|---|
| Wind Jump | `WindJumpSpell` | entity + `ImpulseCastData` + projectile + effect |
| Tornado | `TornadoSpell` | entity + projectile + raycast |
| Iron Slash | `IronSlashSpell` | potentiation + entity + impulse + teleport + effect |
| Aeropic | `AeropicSpell` | recasts + impulse + effect |
| Almighty Push | `AlmightyPushSpell` | entity + effect |
| Wind Blade | `WindBladeSpell` | shoot + entity + projectile |
| Tailwind | `TailwindSpell` | effect |

Esse fingerprint prova o uso estrutural desses mechanisms, mas **não prova sozinho valores, hit rules, duração, alcance ou fórmulas**. Esses campos permanecem `NÃO VERIFICADO` até extração do JAR/source exato.

## Progressão / obtenção

A release oficial confirma o ecossistema próprio de Wind, incluindo Windmill, Aeromancer, staff e spellbook. O changelog histórico 1.0.1 registra Aeromancer loot table, Wind staff recipe, Book of Tempests advancement e correção de fall damage de Tailwind.

A rota exata de obtenção de cada um dos sete scrolls, pesos de loot, crafting, níveis máximos e raridades não foi provada pelo artefato/source nesta auditoria e fica `NÃO VERIFICADO`.

## Deduplicação

Os sete contracts ocupam, no mínimo, estes espaços mecânicos comprovados:

- mobilidade por impulso com projectile/effect (`Wind Jump`);
- tornado targetado/raycast com entity/projectile (`Tornado`);
- ataque/mobilidade com potentiation + teleport/impulse (`Iron Slash`);
- mobilidade recast-based (`Aeropic`);
- push-themed spell com entity/effect (`Almighty Push` — settlement exato pendente);
- projectile Wind disparado (`Wind Blade`);
- buff/effect Wind com interação histórica com fall damage (`Tailwind`).

IronSable registra seus próprios `maelstrom`, `tempests_grasp` e `downburst` e apenas os classifica como Wind quando este addon está instalado. Esses três **não pertencem** ao inventário 7/7 de Wind's Spellbooks.

## Regra de fail-closed

Sem source/JAR bytecode exato, Black Arcana não deve inventar mana, cooldown, dano, range, recast count, friendly-fire, PvP ou APIs para estes spells. Integrações futuras devem usar IDs/runtime hooks comprovados e manter o provider como authority do efeito.

Ver [TECHNICAL-AUDIT.md](TECHNICAL-AUDIT.md).
