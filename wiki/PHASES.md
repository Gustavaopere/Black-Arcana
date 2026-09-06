# Fases da Wiki Mestre de Magia

## Fase 1 — arquitetura, planos e Wiki estrutural

**Estado:** `MERGED / CANÔNICA`

Checkpoint canônico:

- PR #61 — `docs: build canonical spell wiki catalog`
- `main@edcc9f8cf1d582681d4b7d2aa1facbcb39b99ae9`

Objetivo desta fase: transformar as decisões de design em documentação canônica suficiente para orientar o trabalho posterior sem iniciar implementação nova nem exigir que o catálogo completo do modpack estivesse pronto antes do primeiro merge.

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
- política de proveniência alinhada ao clean-room do projeto.

A Fase 1 não autorizou implementação das novas escolas nem declarou o catálogo do modpack completo.

## Fase 2 — catálogo completo do modpack

**Estado:** `ATIVA / EM PROGRESSO`

Checkpoint inicial já mergeado:

- PR #62 — `docs: catalog all modpack magic providers`
- `main@17f87619bc8ed71023bc80d0adb752c13dc8c6c4`
- post-merge CI `34056029588` / #1477 — `SUCCESS`

O checkpoint #62 estabeleceu o baseline de 101 componentes magic-relevant contra a modlist de 607 entradas e criou a primeira matriz de deduplicação, mas não concluiu a Fase 2.

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

Ars deve ser catalogado por forms/glyphs/augments/rituals e capacidades composicionais, não por enumerar infinitamente todas as combinações possíveis.

### Regra de classificação

Magic-relevant não significa spell provider. Bridges, gear, libraries e compat podem ser essenciais para authority/dedup sem oferecer novos spells. Quando a auditoria granular contradiz a classe inicial do registry baseline, a correção deve ser registrada explicitamente e prevalecer sobre a classificação antiga.

### Saída principal

`capability → provider(s) → current coverage → semantic overlap → real gap`

Nenhuma linha é liberada para Fase 3 apenas porque a apresentação/nome de um candidato Black Arcana difere do conteúdo instalado.

## Fase 3 — seleção final e implementação

**Estado:** `BLOQUEADA PELA FASE 2`

Só começa depois de a matriz da Fase 2 permitir deduplicação segura.

Ordem de trabalho:

1. selecionar spells/sistemas que possuam delta mecânico real;
2. fechar números, tiers, aquisição e progressão;
3. registrar provenance/ledger requerido para cada referência implementável;
4. implementar provider-native first e bridges necessárias;
5. produzir assets originais de alta qualidade;
6. executar unit tests/GameTests/build/servidor/cliente conforme aplicável;
7. atualizar Wiki de conceito para `IMPLEMENTADO` somente com evidência.

### Invariantes para transição

- generic randomness/probability não basta para justificar Caos;
- geometry/boolean logic/runes/walls/counters não bastam para justificar Ordem;
- generic life/damage linking não basta para justificar Arcana Vincular;
- generic Ars Nouveau ↔ Iron's mana/spellbook unification não é lacuna enquanto Ars 'n' Spells 3.2.4 cobre esse papel;
- generic contingency/event-triggered casting não é lacuna enquanto o ecossistema Ars já cobre esse comportamento;
- magic-on-Create/moving contraptions não é lacuna por si só enquanto Ars Creo/Technica cobrem partes substanciais desse espaço;
- unknown provider behavior remains fail-closed rather than being replaced by a generic Black Arcana bonus.

## Regra de transição

O projeto está atualmente entre Fase 2 e Fase 3: **Fase 1 está canônica; Fase 2 está em execução; Fase 3 continua bloqueada.**

O próximo merge documental da Fase 2 pode aumentar cobertura e corrigir classificações sem significar que a Fase 2 inteira terminou. A Fase 3 só é liberada quando as capability rows pertinentes deixarem de depender de provider audits incompletos e uma lacuna real puder ser demonstrada com evidência suficiente.
