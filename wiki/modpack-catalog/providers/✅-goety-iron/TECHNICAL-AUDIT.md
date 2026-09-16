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

- CurseForge project `1367643`, file `8662179`, NeoForge 1.21.1, upload em 2026-08-16;
- Modrinth project `tZpynDu5`, version `YZXNIxvk`;
- arquivo Modrinth `GoetyIron-1.21.1-NeoForge-3.1.jar`, `507646` bytes;
- SHA-1 Modrinth `c8529867e798661ed01fb2948abda23735888fc6`;
- publicação Modrinth em `2026-08-16T12:40:42.435094Z`;
- client + server.

O SHA-1 publicado no Modrinth é idêntico ao SHA-1 da modlist física. Isso fecha a identidade do artefato 3.1 instalado contra uma segunda superfície publisher-controlled.

## License/provenance

Os metadados públicos divergem:

- CurseForge declara `MIT License`;
- Modrinth declara `LicenseRef-All-Rights-Reserved` / All Rights Reserved.

Essa divergência impede generalizar a declaração MIT para o projeto inteiro sem uma licença de source ou esclarecimento upstream. Para Black Arcana, a postura canônica é a mais restritiva: inspeção factual para interoperabilidade/provenance pode registrar identificadores, hashes e comportamento observado, mas código, texto, assets, modelos ou sons não são copiados/reutilizados com base na declaração CurseForge isolada.

## Source status

O metadata exato do projeto Modrinth publica:

- `source_url=null`;
- `issues_url=null`;
- `wiki_url=null`.

Busca de repositórios não localizou um source oficial Goety Iron associado com segurança ao publisher/projeto. `Rinko1231/GoetyIronLink` é outro mod e não é usado como authority.

Portanto o estado é:

`EXACT 3.1 ARTIFACT HASH MATCH / CROSS-LOADER RELEASE LINE AUDITED / SOURCE REVISION UNLOCATED / INTERNALS FAIL-CLOSED`.

## Cross-loader release evidence

A linha 1.21.1 possui uma ponte pública relevante para a linha 1.20.1, documentada em [RELEASE-SYNC-EVIDENCE.md](RELEASE-SYNC-EVIDENCE.md).

### 3.0.0 NeoForge / 2.1.0 Forge

- NeoForge 1.21.1 `3.0.0`: Modrinth `GYDNpLkn`;
- Forge 1.20.1 `2.1.0`: Modrinth `QvSYOnxH`.

Os dois changelogs do publisher declaram explicitamente que a branch NeoForge 1.21.1 havia sido portada e estava **identical in content** à branch Forge 1.20.1 naquele checkpoint. Esse é um contrato editorial de equivalência de conteúdo para o par de releases, não equivalência binária.

### 3.1 NeoForge / 2.2 Forge

- NeoForge 1.21.1 `3.1`: `YZXNIxvk`, publicado `2026-08-16T12:40:42.435094Z`;
- Forge 1.20.1 `2.2`: `kYqXKiOc`, publicado `2026-08-16T12:41:17.102981Z`.

Os changelogs inglês/chinês desses dois releases são idênticos, incluindo os mesmos sete fixes/features. Isso prova sincronização do delta publicado, mas não autoriza assumir que toda classe/resource/registry é idêntica entre loaders.

## Superfície exata derivada do material oficial

### Página do projeto

Confirma:

- bridge de mobs Iron's → Goety servants;
- obtenção de servants por Focus summoning ou ritual transform/summon em alto nível;
- Spellcaster Servants podem aprender spells adicionais;
- servants podem ser fortalecidos por upgrade orbs.

A descrição Modrinth atual nomeia nove servants, incluindo `First Flamebearer Servant`; a descrição CurseForge atual enumera oito e o omite. O changelog 3.0.0/2.1.0 também cita First Flamebearer Servant, então o conjunto público diretamente sustentado é **pelo menos nove nomes**, sem alegação de completude de registry.

### Changelog do File ID 8662179 / Modrinth YZXNIxvk

Confirma especificamente para 3.1:

1. fix de config options sem efeito;
2. Improved Ominous Fire Orbs não devem ser destruídos por allied mobs;
3. fixes de compatibilidade não especificados;
4. spell attribute config options por servant;
5. Tincture of Forgetfulness pode resetar Goety Void Vault;
6. summoned Polar Bears podem ser substituídos por Polar Bear Servants, configurável;
7. summoned Vexes podem ser substituídos por Vex Servants, configurável.

O release Forge 2.2 publica o mesmo delta textual.

## Tentativa de artifact inspection

O Modrinth publica o URL CDN direto do exato arquivo `YZXNIxvk`, mas as ferramentas desta sessão recusaram materializar o conteúdo `application/java-archive` para inspeção factual local. Nenhum caminho alternativo de decompilação/reconstrução foi usado para contornar essa limitação.

Consequentemente, o catálogo não afirma dump de registries/resources do 3.1.

## Internals não verificados

Sem source/API exatos ou inventário factual do JAR, não afirmar:

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
- API pública para integração;
- equivalência estrutural 2.2 Forge ↔ 3.1 NeoForge além do delta publisher-controlled já provado.

## Semantic denominator

A nova evidência fecha melhor identidade do artefato e provenance cross-loader, mas não individualiza Focuses, rituals ou outras ações mágicas próprias da build 3.1. Goety Iron continua **+0** no strict semantic minimum neste checkpoint; o mínimo global permanece **797** e o provider-component metric não muda.

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
