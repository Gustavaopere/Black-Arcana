# Fases da Wiki Mestre de Magia

## Fase 1 — arquitetura, planos e Wiki estrutural

**Estado:** `MERGED / CANÔNICA`

Checkpoint canônico:

- PR #61 — `docs: build canonical spell wiki catalog`
- `main@edcc9f8cf1d582681d4b7d2aa1facbcb39b99ae9`

Objetivo desta fase: transformar as decisões de design em documentação canônica suficiente para orientar o trabalho posterior sem iniciar implementação nova nem exigir que o catálogo completo do modpack estivesse pronto antes do primeiro merge.

Entregas históricas da fase incluíram os conceitos de Caos, Ordem, Blood/Vínculo, Infernal, Celestial e Bruxaria. Decisões posteriores da Fase 2 corrigiram duas classificações importantes:

- Celestial/Divino **não é escola separada**; qualquer expansão aprovada entra na escola Holy do Iron's;
- Blood Binding **não é escola separada**; é uma reforma da escola Blood existente, com objetivo de `0 mana normal` e custo hemático próprio.

A Fase 1 também estabeleceu:

- arquitetura do reservatório hemático em mB e vínculos tipados;
- arquitetura da Lava Infernal Nether-only e seu vínculo de infraestrutura;
- arquitetura de Sanctum/Ressonância Celestial sem Aether para Holy `MIRACLE_TIER`;
- integração planejada com Immersive Portals;
- padrão visual de texturas, partículas, animações, áudio e HUD;
- política `PROVIDER-NATIVE FIRST` e deduplicação semântica;
- corpus de pesquisa de Wanda/Scarlet Witch, Doctor Strange, Doctor Fate e Constantine convertido em candidatos originais bounded;
- fila dos providers mágicos atuais que precisam de catalogação granular;
- política de proveniência alinhada ao clean-room do projeto.

A Fase 1 não autorizou implementação das novas escolas nem declarou o catálogo do modpack completo.

## Fase 2 — catálogo completo do modpack

**Estado:** `ATIVA / EM PROGRESSO`

Checkpoint inicial:

- PR #62 — `docs: catalog all modpack magic providers`
- `main@17f87619bc8ed71023bc80d0adb752c13dc8c6c4`
- post-merge CI `34056029588` / #1477 — `SUCCESS`

Checkpoints documentais posteriores são mergeados incrementalmente quando coerentes e com CI verde; isso **não** significa que a Fase 2 inteira terminou.

Objetivo: catalogar integralmente o conteúdo mágico jogável do pack antes de aprovar duplicações ou fechar a lista final das novas escolas/expansões.

### Árvore canônica única

A única árvore de provider catalog é:

`wiki/modpack-catalog/providers/<provider>/<classificação-nativa>/<capacidade>.md`

A antiga `wiki/providers/` foi consolidada e removida. Auditorias técnicas preservadas ficam dentro do próprio provider (`audits/` ou `TECHNICAL-AUDIT.md`), e os metadados globais ficam em `wiki/modpack-catalog/meta/`.

### Para cada provider relevante

Registrar conforme aplicável:

- IDs reais de spells/glyphs/rituais/efeitos;
- escola/domínio/categoria nativa;
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

Conteúdo que já existe no modpack continua obrigatório no catálogo mesmo quando nenhuma alteração for planejada.

### Regras específicas

- Iron's e addons baseados em schools: uma subpasta por escola e um `.md` por spell ativo.
- Ars Nouveau: forms/effects/augments/rituals/systems; não enumerar combinações arbitrárias infinitas.
- Outros providers: usar a classificação nativa comprovada do próprio mod; não inventar categorias por conveniência.
- Magic-relevant não significa spell provider. Bridges, gear, libraries e compat podem ser essenciais para authority/dedup sem oferecer novos spells.
- Quando a auditoria granular contradiz a classe inicial do registry baseline, a correção é registrada explicitamente.

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
- generic life/damage linking não basta para justificar a reforma/vínculos de Blood;
- Holy já existe; conteúdo Celestial deve entrar em Holy somente quando houver delta real;
- generic Ars Nouveau ↔ Iron's mana/spellbook unification não é lacuna enquanto Ars 'n' Spells cobre esse papel;
- generic contingency/event-triggered casting não é lacuna enquanto o ecossistema Ars já cobre esse comportamento;
- magic-on-Create/moving contraptions não é lacuna por si só enquanto Ars Creo/Technica cobrem partes substanciais desse espaço;
- unknown provider behavior permanece fail-closed em vez de ser substituído por bônus Black Arcana genérico.

## Regra de transição

Fase 1 está canônica; Fase 2 está em execução; Fase 3 continua bloqueada.

Merges documentais incrementais da Fase 2 são permitidos para manter a Wiki consultável e auditável durante o trabalho. A Fase 3 só é liberada quando as capability rows pertinentes deixarem de depender de provider audits incompletos e uma lacuna real puder ser demonstrada com evidência suficiente.
