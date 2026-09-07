# Goety Cataclysm 1.21.1-1.8.2 — catálogo público release-bounded

## Estado

- JAR instalado: `goety_cataclysm-1.21.1-1.8.2.jar`
- Mod ID runtime: `goety_cataclysm`
- Versão runtime: `1.21.1-1.8.2`
- Minecraft: `1.21.1`
- Loader: NeoForge
- CurseForge Project ID: `1224214`
- CurseForge File ID: `8518940`
- SHA-1 do artefato instalado: `4e3052a082200371b36e1a88fdce05e294d82757`
- CurseForge package fingerprint da instância: `588833616`
- Publicação exata: **confirmada** — release NeoForge 1.21.1 de 2026-07-27
- Changelog exato público: `First 1.21.1 release!`
- Licença declarada do projeto: `All Rights Reserved`
- Repositório público do autor: `Polarice3/Goety_Cataclysm`
- Source público exato da build 1.21.1-1.8.2: **NÃO LOCALIZADO**
- Inventário completo de focuses/spells/servants/rituais: **NÃO VERIFICADO**
- Estado: `EXACT-ARTIFACT-PINNED / PUBLIC SEMANTIC SURFACE AUDITED / GRANULAR INVENTORY UNVERIFIED / FAIL-CLOSED`

## O que a publicação oficial prova

Goety Cataclysm se apresenta como uma compatibilidade entre **Goety** e **L_Ender's Cataclysm** que permite ao jogador acessar spells e abilities derivados tematicamente de criaturas poderosas do Cataclysm.

O guia consolidado do modpack acrescenta apenas o enquadramento sistêmico seguro: o addon faz esse conteúdo participar da linguagem nativa do Goety — Soul Energy, Focus casting, summons/servants e progressão necromântica — em vez de criar uma terceira plataforma mágica independente.

Essas afirmações são suficientes para classificar domínio e sobreposição, mas **não** para fechar um catálogo nominal ou técnico de registries.

## Limite do source público

O repositório público atualmente disponível contém apenas a branch `master`; no checkpoint auditado ela aponta para Minecraft `1.20.1` e `mod_version=1.20-1.9.1`. A API pública do GitHub não retorna commits do repositório entre 2026-07-20 e 2026-08-01, embora o artefato NeoForge 1.21.1 tenha sido publicado em 2026-07-27.

Portanto:

- a `master` atual **não** é usada como source authority da build instalada;
- source histórico 1.20.x não é promovido a contrato 1.21.1;
- nenhum fork de terceiros substitui a revisão oficial ausente;
- nenhum bytecode é decompilado para reconstruir implementação protegida;
- nenhuma classe, registry ID, assinatura de método, custo, cooldown ou fórmula é inferida.

## Provider authority

- **Goety** permanece autoridade de Soul Energy, Focus/Staff casting, servant ownership/lifecycle, rituals, Research e Lichdom.
- **L_Ender's Cataclysm** permanece autoridade de suas criaturas, bosses e gameplay nativo.
- **Goety Cataclysm** é autoridade somente do conteúdo/bridge que ele próprio acrescenta entre esses providers.
- **Black Arcana** não cria uma segunda Soul Energy, segundo servant ledger, segundo ritual settlement nem segundo cast pipeline para representar este addon.

## Catálogo granular

Não há evidência pública suficiente da build exata para afirmar quantidade total ou nomes completos de:

- Focuses;
- spells/abilities;
- servant variants;
- ritual recipes/types;
- items de aquisição/progressão;
- registry IDs;
- custos de Soul Energy;
- cooldown/cast time/potency/duration;
- targeting, caps ou ownership hooks.

Qualquer ficha individual baseada nesses campos permanece bloqueada até evidência exata e licenciada da build 1.21.1-1.8.2 ou documentação pública oficial equivalente.

## Documentos

- [Auditoria técnica e provenance](TECHNICAL-AUDIT.md)
- [Regras de integração com Black Arcana](INTEGRATION-RULES.md)

## Fontes públicas

- CurseForge project: `https://www.curseforge.com/minecraft/mc-mods/goety-cataclysm`
- CurseForge exact file: `https://www.curseforge.com/minecraft/mc-mods/goety-cataclysm/files/8518940`
- Modrinth exact release: `https://modrinth.com/mod/goety-cataclysm/version/1.21.1-1.8.2`
- Public source repository, non-matching current branch: `https://github.com/Polarice3/Goety_Cataclysm`
