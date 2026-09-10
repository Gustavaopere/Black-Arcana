# Ignis Soulfires: Spellbooks — provider audit gate

Status: `INSTALLED 1.1.0 / EXACT OFFICIAL RELEASE PINNED / EXACT SOURCE UNAVAILABLE / SEMANTIC REGISTRY OPEN / FAIL-CLOSED`

- **JAR do pack:** `ignissoulfires_spellbooks-1.1.0.jar`
- **Mod ID:** `ignissoulfires_spellbooks`
- **Runtime local:** `1.1.0`
- **Physical SHA-1:** `dcde77db35b6de3562b4e6de0025746eaf68f119`
- **Publicação oficial exata:** CurseForge project `1572171`, file `8620663`, `Ignis_Soulfires_Spellbooks-1.1.0`, Release NeoForge 1.21.1 de 2026-08-11
- **Source público 1.1.0:** não localizado
- **Próximo requisito:** source exato 1.1.0 ou inspeção autorizada do JAR/registry instalado para fechar inventário semântico

## Regra de provenance

A publicação oficial atual confirma a build **1.1.0** para NeoForge 1.21.1 e descreve o projeto como um pequeno addon de compatibilidade entre Cataclysm: Ignis Soulfires e Cataclysm: Spellbooks. O conteúdo explicitamente publicado é um **Souled Ignitium Wizard Armor set** voltado a spellcasting.

Isso resolve a antiga anomalia de rastreabilidade da versão, mas não fecha o inventário interno. Descrição pública de escopo de equipamento **não é prova de ausência** de registrations de spell, ritual ou outra identidade semântica dentro do JAR. Portanto o provider permanece `OPEN` para a métrica semântica até existir evidência de registry/source/JAR suficiente.

Nenhum conteúdo da antiga release 1.0.0 é promovido por inferência à 1.1.0, e nenhuma ausência de conteúdo é inferida apenas porque a página do publisher enumera armor.

## Deduplicação / integração

Ignis Soulfires: Spellbooks é uma bridge de equipamento mágico entre providers já autoritativos. Cataclysm: Ignis Soulfires continua owner de Souled Ignitium e de suas propriedades-base; Cataclysm: Spellbooks / Iron's continuam owners do framework mágico correspondente; este addon é owner somente do conteúdo/compatibilidade que efetivamente registra.

Black Arcana não deve reaplicar atributos, armor modifiers, spell modifiers ou efeitos por reconhecer nomes/materials. Qualquer bridge futura depende de contrato real e deve preservar exactly-once processing.

## Evidência atual

- modlist física: `ignissoulfires_spellbooks-1.1.0.jar`, runtime `1.1.0`, SHA-1 `dcde77db35b6de3562b4e6de0025746eaf68f119`;
- CurseForge oficial: project `1572171`, exact file `8620663`, `Ignis_Soulfires_Spellbooks-1.1.0`, Release NeoForge 1.21.1 de 2026-08-11;
- descrição oficial: addon de integração entre Cataclysm: Ignis Soulfires e Cataclysm: Spellbooks, com Souled Ignitium Wizard Armor set explicitamente declarado;
- Notion da Auditoria Mestre: provenance 1.1.0 já revalidada e source exato não localizado;
- pesquisa pública de source 1.1.0: sem pin verificável localizado;
- runtime/registry granular: **não auditado** nesta closure.

## Estado semântico

`OPEN` — a existência da release exata está fechada, mas o conjunto de spells/rituals/equivalent actions da 1.1.0 não está. O strict semantic counted minimum global não muda por esta correção de provenance.
