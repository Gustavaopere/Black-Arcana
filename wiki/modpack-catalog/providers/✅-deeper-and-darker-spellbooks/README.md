# Deeper and Darker: Spellbooks — catálogo canônico

**Prova física 2026-10-12:** [quatro registros estáticos exatos da Version B 1.3.3](EXACT-BINARY-SUMMONS-1.3.3-VER-B.md) ([auditoria #38329132941](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38329132941)), SHA-1 publicador/físico `783123ae86c91c01527c10f338679caaef42eb42`. **✅ 4/4 `COUNTED_EXACT` só no registro**, campanha **8/39 / 31/39**, +0; mínimos 1851/1849. O registrador migrou do pacote `item` no source 1.3.0 para `registeries` no binário 1.3.3. ⚠️ Runtime, crash fix, config, aquisição e Survival não certificados.

## Estado

- Mod ID: `darkermagic`
- JAR instalado: `darkermagic-1.3.3-1.21.1-ver.b.jar`
- Runtime metadata: `1.3.3-1.21.1`
- Loader/game: NeoForge 1.21.1
- Provider base: Iron's Spells 'n Spellbooks + Deeper and Darker
- Release exata instalada: CurseForge file ID `7897469`; Modrinth version ID `oBllvIgO`
- Variante instalada: **Version B** — Warden Mage Armor com 10% Eldritch Spell Power (Version A = 5%)
- Inventário público da release: **4 summon spells**
- Catálogo de inventário: **4/4**
- Source público disponível: `RevTheSprout/Deeper-and-Darker-Spellbooks@df242888d16e580a8f76e0d937fe50d66bbed8ed`, porém declara `mod_version=1.3.0`; serve somente como baseline estrutural, não como bytecode 1.3.3.

## Quatro spells do inventário

O projeto oficial descreve a linha atual como contendo quatro summon spells. O registry do source 1.3.0 possui exatamente estes quatro nomes/IDs, e os changelogs públicos 1.3.1 e 1.3.2 tratam apenas de enchantability de armor; 1.3.3 trata do crash dos summon spells em servidor, sem anunciar adição/remoção de spell.

1. [Summoned Warden](eldritch/summoned-warden.md)
2. [Summoned Shattered](eldritch/summoned-shattered.md)
3. [Summoned Sculk Centipede](eldritch/summoned-sculk-centipede.md)
4. [Summoned Sculk Snapper](eldritch/summoned-sculk-snapper.md)

## Regra de evidência

As fichas distinguem explicitamente:

- **RELEASE 1.3.3 VER B CONFIRMADA** — identidade instalada, número de spells, variante B e changelog;
- **SOURCE 1.3.0 BASELINE** — IDs, configs, fórmulas e lifecycle observados no último source público;
- **BYTECODE EXATO 1.3.3** — quatro identidades/classes de spell, registrador e bootstrap confirmados estaticamente;
- **NÃO VERIFICADO FUNCIONALMENTE EM 1.3.3** — hotfix de servidor, fórmulas, lifecycle, configs, aquisição, multiplayer, Survival e release.

Não promover o source 1.3.0 a authority 1.3.3.

## Provenance

- CurseForge: project `deeper-and-darker-spellbooks`, file ID `7897469`, `darkermagic-1.3.3-1.21.1-ver.b.jar`, release 2026-04-09.
- Modrinth: project `bY4q13Xr`, version `oBllvIgO`, Version B 1.3.3-1.21.1.
- Source baseline: commit `df242888d16e580a8f76e0d937fe50d66bbed8ed`, branch NeoForge 1.21.1, `mod_version=1.3.0`, Iron's dependency 3.15.0.

Ver [TECHNICAL-AUDIT.md](TECHNICAL-AUDIT.md).