# Wind's Spellbooks 1.0.5 — auditoria técnica

## Proveniência

- Pack: `wind_spellbooks-1.0.5.jar` / `wind_spellbooks` / 1.0.5.
- CurseForge: project `1519158`, file `8485822`, NeoForge 1.21.1, publicado em 2026-07-22.
- Notion e modlist atuais convergem no mesmo JAR/versão.
- Source GitHub público da build 1.0.5: **não localizado**.
- O inventário foi fechado inicialmente pela publicação oficial (sete spells upgradáveis) e pelos sete IDs/classes observados no runtime; a [auditoria exata](EXACT-BINARY-SPELLS-1.0.5.md) agora também comprova hash JAR físico/publicador, sete chamadas binárias e entrypoint.

## Registry observado

- `wind_spellbooks:wind_jump` → `net.raptorzizi.wind_spellbooks.spells.wind.WindJumpSpell`
- `wind_spellbooks:tornado` → `...TornadoSpell`
- `wind_spellbooks:iron_slash` → `...IronSlashSpell`
- `wind_spellbooks:aeropic` → `...AeropicSpell`
- `wind_spellbooks:almighty_push` → `...AlmightyPushSpell`
- `wind_spellbooks:wind_blade` → `...WindBladeSpell`
- `wind_spellbooks:tailwind` → `...TailwindSpell`

A classe/package `spells.wind` e a descrição oficial da escola sustentam a classificação Wind dos sete.

## Fingerprints ASM observados

O mod Ypsilon's Fundamentalism/FundamentalPrinciples analisou o bytecode carregado no runtime e registrou:

- Wind Jump: `createsEntity`, `usesImpulseCastData`, `createsProjectile`, `usesAddEffect`;
- Tornado: `createsEntity`, `createsProjectile`, `usesRaycast`;
- Iron Slash: `usesPotentiation`, `createsEntity`, `usesImpulseCastData`, `usesTeleport`, `usesAddEffect`;
- Aeropic: `hasRecasts`, `usesImpulseCastData`, `usesAddEffect`;
- Almighty Push: `createsEntity`, `usesAddEffect`;
- Wind Blade: `usesShoot`, `createsEntity`, `createsProjectile`;
- Tailwind: `usesAddEffect`.

Esses flags são evidência estrutural de bytecode, não uma decompilação. Eles não autorizam inventar signatures ou fórmulas.

## Changelogs úteis

- 1.0.1: Aeromancer loot table, Wind affinity ring texture, Book of Tempests advancement, Wind staff recipe e correção de Tailwind fall damage.
- 1.0.3: correção de crash de Tornado em servidor.
- 1.0.5: release exata instalada; changelog público curto (`Add lang`).

Isso prova continuidade dos spells Tornado/Tailwind na linha e que a 1.0.5 incorpora fixes anteriores, mas não substitui bytecode exato para balanceamento.

## Campos deliberadamente não preenchidos

Mesmo após inspecionar o JAR exato para o registry estático, seguem `NÃO VERIFICADO` por spell, por ausência de auditoria numérica/funcional:

- min/max level individual;
- rarity;
- cast type/time;
- mana;
- cooldown;
- spell power/damage/heal;
- range/radius/duration;
- target/friendly-fire/PvP/boss/summon rules;
- recast count/window de Aeropic;
- exact projectile/entity/effect types e lifecycle;
- acquisition weights/recipes por scroll;
- server/client authority fina e API signatures.

## Deduplicação e authority

Fingerprint é suficiente para impedir que o design do Black Arcana trate estes espaços como vazios. Porém não é suficiente para implementar um bridge numérico. O provider continua authority de cast, effects, projectiles, impulse, teleport e recasts.

## Integração com IronSable

O pack possui IronSable 1.2.0. A release do IronSable declara que `maelstrom`, `tempests_grasp` e `downburst` usam Wind school quando Wind's Spellbooks está presente. Ownership continua IronSable; não duplicar estes três dentro deste provider.

## Estado

`COUNTED_EXACT` para registry binário estático 7/7 / catálogo semântico 7/7; source não localizado, parâmetros numéricos, config, gameplay e Survival ⚠️. [Prova #38312284152](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38312284152).
