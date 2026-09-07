# Goety Iron 3.1 — catálogo público release-bounded

## Estado

- JAR instalado: `GoetyIron-1.21.1-NeoForge-3.1.jar`
- Mod ID runtime: `goetyiron`
- Versão runtime: `3.1`
- Minecraft: `1.21.1`
- Loader: NeoForge
- CurseForge Project ID: `1367643`
- CurseForge File ID: `8662179`
- SHA-1 do artefato instalado: `c8529867e798661ed01fb2948abda23735888fc6`
- CurseForge package fingerprint da instância: `482454312`
- Publicação exata: **confirmada** — release NeoForge 1.21.1 de 2026-08-16
- Licença declarada: `MIT License`
- Repositório-fonte público exato: **NÃO LOCALIZADO**
- Estado: `EXACT-ARTIFACT-PINNED / PUBLIC SERVANT SURFACE AUDITED / SOURCE INTERNALS UNVERIFIED / FAIL-CLOSED`

## Função do provider

Goety Iron integra **Iron's Spells 'n Spellbooks** ao sistema de **servants do Goety**. Sua página oficial descreve criaturas do Iron's convertidas/adaptadas para servants comandáveis e confirma dois caminhos de obtenção em alto nível:

- summon por Focus;
- transformação/summon por ritual.

Também confirma que Spellcaster Servants podem aprender spells adicionais e ser fortalecidos com upgrade orbs.

A bridge não constitui uma terceira plataforma de magia: Goety continua autoridade de servant ownership/lifecycle e Iron's continua autoridade da identidade de spellcasting/atributos que o addon reutiliza.

## Servants explicitamente nomeados pela página oficial

O texto público atual nomeia oito servants:

1. Pyromancer Servant
2. Cryomancer Servant
3. Cleric Servant
4. Archevoker Servant
5. Necromancer Servant
6. Ancient Knight Servant
7. Dead King Servant
8. Alchemist Servant

Ver [SERVANT-CATALOG.md](SERVANT-CATALOG.md).

Esse conjunto é uma **lista pública nominal**, não prova de que o registry da build contém exatamente oito entidades. A release 3.1 também documenta replacements de Polar Bears e Vexes por versões servant, o que demonstra superfícies adicionais sem autorizar uma contagem total de registries.

## Delta público exato da release 3.1

O changelog oficial do File ID `8662179` registra:

- correção de configurações que não produziam efeito;
- correção para Improved Ominous Fire Orbs destruídos por aliados;
- correções de compatibilidade com alguns mods;
- configuração de atributos de spell para cada servant;
- Tincture of Forgetfulness capaz de resetar o Void Vault do Goety;
- summoned Polar Bears podem ser substituídos por Polar Bear Servants, configurável;
- summoned Vexes podem ser substituídos por Vex Servants, configurável.

Esses itens são tratados como **surface behavior público**, não como prova de classes, hooks ou signatures internas.

## Limites do catálogo

Sem source/API exatos publicamente localizados, permanecem não verificados:

- registry IDs;
- nomes e quantidade de Focuses próprios;
- ritual recipes e conditions;
- lista completa de servants/entities;
- spell-learning storage e mutation API;
- upgrade-orb internals;
- atributos exatos/config schema;
- replacement hook de Polar Bear/Vex;
- causalidade e settlement dos spells executados pelos servants;
- interoperability real com a versão instalada de Iron's e Goety além da presença/load.

## Authority / deduplicação

- Goety é authority de servant ownership, lifecycle, Focus/ritual framework e Soul Energy.
- Iron's Spells é authority de seus spells/escolas/atributos e casting semantics nativos.
- Goety Iron é authority apenas da camada que transforma/conecta essas entidades e atributos.
- Black Arcana não cria segunda Soul Energy, segundo servant state, segundo mana ledger ou segundo spellcast settlement.

## Documentos

- [Catálogo público de servants e mechanics](SERVANT-CATALOG.md)
- [Auditoria técnica/provenance](TECHNICAL-AUDIT.md)
- [Regras de integração](INTEGRATION-RULES.md)

## Fontes públicas

- CurseForge project: `https://www.curseforge.com/minecraft/mc-mods/goety-iron`
- CurseForge exact file: `https://www.curseforge.com/minecraft/mc-mods/goety-iron/files/8662179`
