# Ignis Soulfires: Spellbooks — provider audit gate

Status: `INSTALLED 1.1.0 / EXACT SOURCE UNAVAILABLE / CATALOG BLOCKED FAIL-CLOSED`

- **JAR do pack:** `ignissoulfires_spellbooks-1.1.0.jar`
- **Mod ID:** `ignissoulfires_spellbooks`
- **Runtime local:** `1.1.0`
- **Publicação oficial rastreada:** somente `Ignis_Soulfires_Spellbooks-1.0.0` para NeoForge 1.21.1
- **Source público 1.1.0:** não localizado
- **Próximo requisito:** extração/auditoria do JAR instalado ou source exato 1.1.0

## Regra de provenance

A release pública 1.0.0 descreve um addon de compatibilidade entre Cataclysm: Ignis Soulfires e Cataclysm: Spellbooks, com variante Souled Ignitium Wizard Armor. Isso **não** prova que a build local 1.1.0 tenha inventário idêntico, nem prova ausência/presença de registrations adicionais.

Por isso este provider permanece fail-closed: nenhum spell, equipamento, atributo, hook ou comportamento da 1.0.0 é promovido ao catálogo granular da 1.1.0 sem evidência da build instalada.

## Deduplicação / integração

Nenhum contract granular deve ser reservado ou recriado a partir da release pública divergente. Bridges e perks que dependam deste provider devem aguardar autoridade exata da 1.1.0.

## Evidência atual

- modlist local: `ignissoulfires_spellbooks-1.1.0.jar`;
- Notion da Auditoria Mestre: runtime 1.1.0 e anomalia de rastreabilidade já registrada;
- CurseForge/Modrinth oficiais consultados: release pública 1.0.0;
- pesquisa pública de source 1.1.0: sem pin verificável localizado.
