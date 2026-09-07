# Goety Iron 3.1 — auditoria técnica e provenance

## Identidade física

A modlist corrente fixa:

- `GoetyIron-1.21.1-NeoForge-3.1.jar`
- mod ID `goetyiron`
- runtime `3.1`
- mixin config visível na modlist: `goetyiron.mixins.json`
- SHA-1 `c8529867e798661ed01fb2948abda23735888fc6`
- CurseForge fingerprint `482454312`

A publicação oficial fixa:

- CurseForge project `1367643`;
- file `8662179`;
- NeoForge;
- Minecraft 1.21.1;
- upload em 2026-08-16;
- tamanho público de aproximadamente 495.7 KB;
- licença MIT;
- client + server.

## Source status

Durante esta auditoria não foi localizado um repositório-fonte público oficial que pudesse ser associado com segurança ao File ID `8662179`/runtime `3.1`.

A licença MIT declarada na página da publicação **não autoriza inventar um source pin ausente**. Portanto o estado é:

`EXACT RELEASE + PUBLIC DESCRIPTION/CHANGELOG VERIFIED / SOURCE REVISION UNLOCATED / INTERNALS FAIL-CLOSED`.

Nenhum repositório de terceiro com nome semelhante é substituído como authority.

## Superfície exata derivada do material oficial

### Página do projeto

Confirma:

- bridge de mobs Iron's → Goety servants;
- oito servants nomeados publicamente;
- obtenção de servants por Focus summoning ou ritual transform/summon em alto nível;
- Spellcaster Servants podem aprender spells adicionais;
- servants podem ser fortalecidos por upgrade orbs.

### Changelog do File ID 8662179

Confirma especificamente para 3.1:

1. fix de config options sem efeito;
2. Improved Ominous Fire Orbs não devem ser destruídos por allied mobs;
3. fixes de compatibilidade não especificados;
4. spell attribute config options por servant;
5. Tincture of Forgetfulness pode resetar Goety Void Vault;
6. summoned Polar Bears podem ser substituídos por Polar Bear Servants, configurável;
7. summoned Vexes podem ser substituídos por Vex Servants, configurável.

## Internals não verificados

Sem source/API exatos, não afirmar:

- package/class names além do que a própria modlist expõe como mixin config;
- registry IDs de entities/items/focuses;
- eventos NeoForge usados;
- mixin targets;
- exact dependency version ranges;
- entity ownership fields;
- summon replacement signatures;
- spell-learning storage;
- upgrade-orb algorithm;
- spell attribute config schema/defaults;
- Void Vault mutation call;
- projectile ownership/damage settlement do Ominous Fire Orb;
- API pública para integração.

## Runtime QA ainda necessário

Mesmo a superfície pública precisa de validação real no pack para promover compatibilidade operacional:

- load dedicado com Goety 3.1.4 + Iron's 3.16.3;
- summon/ritual path dos servants usados no modpack;
- learning adicional de spells;
- upgrade orb behavior;
- config de spell attributes;
- Polar Bear/Vex replacement on/off;
- friendly handling do Improved Ominous Fire Orb;
- Tincture → Void Vault reset;
- save/reload e ownership;
- interação com Epic Fight/world scaling quando pertinente.

Até lá, runtime status permanece `QA PENDING`.
