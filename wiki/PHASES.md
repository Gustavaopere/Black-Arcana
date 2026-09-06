# Fases da Wiki Mestre de Magia

## Fase 1 — arquitetura, planos e Wiki estrutural

**Estado:** `FECHADA PARA MERGE na PR #61`

Objetivo desta fase: transformar as decisões de design em documentação canônica suficiente para orientar o trabalho posterior sem iniciar implementação nova nem exigir que o catálogo completo do modpack esteja pronto antes do primeiro merge.

Entregas desta fase:

- estrutura canônica `wiki/` e template por feitiço;
- taxonomia de estados e regras para números confirmados/TBD;
- documentação dos domínios Black Arcana já presentes;
- planos de Caos, Ordem, Hemática/Vincular, Infernal, Divina/Celestial e Bruxaria Integrada;
- arquitetura do reservatório hemático em mB e vínculos tipados;
- arquitetura da Lava Infernal Nether-only e seu vínculo de infraestrutura;
- arquitetura de Sanctum/Ressonância Celestial sem Aether;
- integração planejada com Immersive Portals;
- padrão visual de texturas, partículas, animações, áudio e HUD;
- política `PROVIDER-NATIVE FIRST` e deduplicação semântica;
- corpus de pesquisa de Wanda/Scarlet Witch, Doctor Strange, Doctor Fate e Constantine convertido em candidatos originais bounded;
- fila dos providers mágicos atuais que precisam de catalogação granular;
- documentação inicial de alguns providers usada somente para validar a forma do catálogo e detectar redundâncias/QA, sem tornar a catalogação completa pré-requisito deste merge;
- política de proveniência alinhada ao clean-room do projeto.

### Fora do escopo da Fase 1

- implementar as novas escolas/sistemas;
- alterar runtime de Iron's, Ars, Hexalia, Toxony ou outros providers;
- fechar números finais de Stage 08 onde ainda são TBD;
- catalogar todos os spells/glyphs/rituais/efeitos do modpack;
- corrigir bugs de providers externos;
- declarar QA visual do pack como concluído.

## Fase 2 — catálogo completo do modpack

**Início:** somente depois do merge da Fase 1.

Objetivo: catalogar integralmente o conteúdo mágico jogável do pack antes de aprovar duplicações ou fechar a lista final das novas escolas.

Para cada provider relevante, registrar conforme aplicável:

- IDs reais de spells/glyphs/rituais/efeitos;
- escola/domínio;
- função semântica;
- dano/cura/controle e fórmulas observáveis/documentadas;
- custo e recurso real;
- cooldown, cast/channel time, alcance, área e duração;
- aquisição, crafting, loot, progressão, unlocks e gates;
- summons, terrain/world mutation e persistência;
- VFX/animação/áudio relevantes;
- compatibilidades e bridges;
- authority, causalidade, fail-closed e riscos de deduplicação;
- versão/JAR realmente presente na modlist;
- proveniência da informação.

Ars deve ser catalogado por formas/glyphs/augments e capacidades composicionais, não por enumerar infinitamente todas as combinações possíveis.

A saída principal desta fase é uma matriz `capacidade → providers existentes → cobertura → lacuna real`.

## Fase 3 — seleção final e implementação

Só começa depois de a matriz da Fase 2 permitir deduplicação segura.

Ordem de trabalho:

1. selecionar spells/sistemas que possuam delta mecânico real;
2. fechar números, tiers, aquisição e progressão;
3. registrar provenance/ledger requerido para cada referência implementável;
4. implementar provider-native first e bridges necessárias;
5. produzir assets originais de alta qualidade;
6. executar unit tests/GameTests/build/servidor/cliente conforme aplicável;
7. atualizar Wiki de conceito para `IMPLEMENTADO` somente com evidência.

## Regra de transição

O merge da PR #61 significa apenas: **o plano e a estrutura documental estão canônicos**.

Ele não significa que todos os spells do modpack já foram catalogados nem que as novas escolas já existem em runtime. Esses trabalhos começam no ciclo seguinte, a partir de `main` pós-merge.
