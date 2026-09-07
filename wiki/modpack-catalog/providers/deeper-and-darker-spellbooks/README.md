# Deeper and Darker: Spellbooks — catálogo canônico

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
- **NÃO VERIFICADO EM BYTECODE 1.3.3** — todo detalhe que a release não prova e que pode ter sido alterado pelo hotfix de summons.

Não promover o source 1.3.0 a authority 1.3.3.

## Provenance

- CurseForge: project `deeper-and-darker-spellbooks`, file ID `7897469`, `darkermagic-1.3.3-1.21.1-ver.b.jar`, release 2026-04-09.
- Modrinth: project `bY4q13Xr`, version `oBllvIgO`, Version B 1.3.3-1.21.1.
- Source baseline: commit `df242888d16e580a8f76e0d937fe50d66bbed8ed`, branch NeoForge 1.21.1, `mod_version=1.3.0`, Iron's dependency 3.15.0.

Ver [TECHNICAL-AUDIT.md](TECHNICAL-AUDIT.md).