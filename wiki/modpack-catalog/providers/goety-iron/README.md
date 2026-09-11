# Goety Iron 3.1 — catálogo público release-bounded

## Estado

- JAR instalado: `GoetyIron-1.21.1-NeoForge-3.1.jar`
- Mod ID runtime: `goetyiron`
- Versão runtime: `3.1`
- Minecraft: `1.21.1`
- Loader: NeoForge
- CurseForge Project ID: `1367643`
- CurseForge File ID: `8662179`
- Modrinth Project ID: `tZpynDu5`
- Modrinth Version ID: `YZXNIxvk`
- SHA-1 do artefato instalado: `c8529867e798661ed01fb2948abda23735888fc6`
- SHA-1 do arquivo 3.1 publicado no Modrinth: `c8529867e798661ed01fb2948abda23735888fc6`
- CurseForge package fingerprint da instância: `482454312`
- Publicação exata: **confirmada** — release NeoForge 1.21.1 de 2026-08-16
- Licença publicada: **DIVERGENTE** — CurseForge declara `MIT License`; Modrinth declara `All Rights Reserved`
- Repositório-fonte público exato: **NÃO LOCALIZADO**; Modrinth publica `source_url=null`
- Estado: `EXACT-ARTIFACT-HASH-MATCH / CROSS-LOADER RELEASE LINE AUDITED / PUBLIC SERVANT SURFACE AUDITED / SOURCE INTERNALS UNVERIFIED / FAIL-CLOSED`

O hash Modrinth da release 3.1 é idêntico ao hash da modlist física. Portanto a identidade do artefato publicado e instalado está fechada em nível SHA-1. Isso não equivale a source pin nem a inventário interno.

Enquanto a divergência de licença entre plataformas não for reconciliada por uma superfície upstream mais autoritativa, Black Arcana aplica a postura clean-room mais restritiva e não presume que o projeto inteiro é reutilizável sob MIT.

## Função do provider

Goety Iron integra **Iron's Spells 'n Spellbooks** ao sistema de **servants do Goety**. Sua página oficial descreve criaturas do Iron's convertidas/adaptadas para servants comandáveis e confirma dois caminhos de obtenção em alto nível:

- summon por Focus;
- transformação/summon por ritual.

Também confirma que Spellcaster Servants podem aprender spells adicionais e ser fortalecidos com upgrade orbs.

A bridge não constitui uma terceira plataforma de magia: Goety continua autoridade de servant ownership/lifecycle e Iron's continua autoridade da identidade de spellcasting/atributos que o addon reutiliza.

## Servants explicitamente nomeados por superfícies atuais do publisher

As superfícies atuais divergem na redação:

- CurseForge nomeia oito servants na descrição do projeto;
- Modrinth nomeia os mesmos oito **mais First Flamebearer Servant**;
- o changelog publisher-controlled de 3.0.0/2.1.0 também cita explicitamente **First Flamebearer Servant**, confirmando que esse nome pertence à linha 1.21.1 atual e não é apenas texto isolado da página Modrinth.

O conjunto nominal público diretamente sustentado é, portanto, **pelo menos nove servants**:

1. First Flamebearer Servant
2. Pyromancer Servant
3. Cryomancer Servant
4. Cleric Servant
5. Archevoker Servant
6. Necromancer Servant
7. Ancient Knight Servant
8. Dead King Servant
9. Alchemist Servant

Ver [SERVANT-CATALOG.md](SERVANT-CATALOG.md).

Esse conjunto é uma **lista pública nominal**, não prova de que o registry da build contém exatamente nove entidades. A release 3.1 também documenta replacements de Polar Bears e Vexes por versões servant, o que demonstra superfícies adicionais sem autorizar uma contagem total de registries.

## Release synchronization — Forge 1.20.1 ↔ NeoForge 1.21.1

A linha pública possui uma ponte de provenance relevante, detalhada em [RELEASE-SYNC-EVIDENCE.md](RELEASE-SYNC-EVIDENCE.md):

- `3.0.0` NeoForge 1.21.1 e `2.1.0` Forge 1.20.1 têm changelogs do publisher que declaram explicitamente que o conteúdo das duas branches era idêntico naquele checkpoint;
- `3.1` NeoForge e `2.2` Forge foram publicados em 2026-08-16 com changelogs bilíngues idênticos e o mesmo delta funcional;
- isso prova uma linha de releases sincronizada, mas **não** autoriza promover source/internals 1.20.1 para autoridade exata 3.1 sem reconciliação por objeto.

## Delta público exato da release 3.1

Os changelogs oficiais de `3.1` e `2.2` registram o mesmo conjunto de mudanças:

- correção de configurações que não produziam efeito;
- correção para Improved Ominous Fire Orbs destruídos por aliados;
- correções de compatibilidade com alguns mods;
- configuração de atributos de spell para cada servant;
- Tincture of Forgetfulness capaz de resetar o Void Vault do Goety;
- summoned Polar Bears podem ser substituídos por Polar Bear Servants, configurável;
- summoned Vexes podem ser substituídos por Vex Servants, configurável.

Esses itens são tratados como **surface behavior público**, não como prova de classes, hooks ou signatures internas.

## Limites do catálogo

Sem source/API exatos publicamente localizados ou inventário factual do JAR 3.1, permanecem não verificados:

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

O Modrinth publica o URL CDN e o hash exatos do arquivo 3.1, mas a ferramenta de download desta auditoria não conseguiu materializar o binário para inspeção factual. Esse limite operacional não é preenchido por extrapolação.

## Authority / deduplicação

- Goety é authority de servant ownership, lifecycle, Focus/ritual framework e Soul Energy.
- Iron's Spells é authority de seus spells/escolas/atributos e casting semantics nativos.
- Goety Iron é authority apenas da camada que transforma/conecta essas entidades e atributos.
- Black Arcana não cria segunda Soul Energy, segundo servant state, segundo mana ledger ou segundo spellcast settlement.

## Estado semântico

O novo evidence checkpoint fecha melhor identidade, provenance e sincronização de releases, mas não individualiza as ações mágicas da build 3.1. Portanto Goety Iron permanece **+0** no strict semantic minimum neste checkpoint; o mínimo global permanece **797**.

## Documentos

- [Catálogo público de servants e mechanics](SERVANT-CATALOG.md)
- [Auditoria técnica/provenance](TECHNICAL-AUDIT.md)
- [Evidência de sincronização das releases](RELEASE-SYNC-EVIDENCE.md)
- [Regras de integração](INTEGRATION-RULES.md)

## Fontes públicas

- CurseForge project: `https://www.curseforge.com/minecraft/mc-mods/goety-iron`
- CurseForge 3.1 file: `https://www.curseforge.com/minecraft/mc-mods/goety-iron/files/8662179`
- CurseForge 2.2 file: `https://www.curseforge.com/minecraft/mc-mods/goety-iron/files/8662199`
- Modrinth project: `https://modrinth.com/mod/goetyiron`
- Modrinth project API: `https://api.modrinth.com/v2/project/tZpynDu5`
- Modrinth versions API: `https://api.modrinth.com/v2/project/tZpynDu5/version`
