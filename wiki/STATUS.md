# Wiki Status

`FASE 1 FECHADA — PR #61 PRONTA PARA MERGE`

A PR #61 fecha **arquitetura, planos e Wiki estrutural**. O catálogo completo do modpack e a implementação das novas escolas são deliberadamente pós-merge e estão descritos em `wiki/PHASES.md`.

## Concluído nesta fase

- estrutura canônica `wiki/` e template individual;
- taxonomia de estado;
- inventário inicial de domínios Black Arcana;
- páginas individuais iniciais de Blood & Curses;
- páginas individuais iniciais de Souls & Death;
- páginas individuais de Projection & Arsenal;
- páginas individuais iniciais de Space & Displacement;
- Black Pyre individualizado;
- runtime localized Forbidden Domain documentado;
- reservatório hemático em mB + distinção sangue/vida/mana/soul/spirit;
- lifecycle/eligibilidade de vínculos e HUD conceitual;
- scaffolds e catálogos candidatos de Caos e Ordem;
- Magia Infernal + fonte Lava Infernal Nether-only + catálogo candidato;
- Magia Divina/Celestial + Sanctum/Ressonância sem Aether + catálogo candidato;
- Bruxaria Integrada com Hexalia como núcleo e Toxony como braço toxicologia/mutagênicos + catálogo candidato;
- integração arquitetural com Immersive Portals;
- padrão visual/VFX/animação/áudio;
- política `PROVIDER-NATIVE FIRST` e assinatura semântica de deduplicação;
- reconciliação inicial do inventário: os 94 JARs/providers do guia mágico anterior continuam presentes na modlist atual de 607 entradas, com deltas de versão registrados;
- corpus fornecido pelo usuário para Scarlet Witch, Doctor Strange, Doctor Fate e John Constantine processado e convertido em categorias de gameplay/dedup;
- Constantine formalizado como repertório transversal, não nova escola;
- proveniência da Wiki alinhada ao clean-room: documentação/API pública e observação clean-room são padrão; derivação de código externo exige licença exata compatível + ledger antes da especificação implementável.

## Próxima fase — somente após o merge

### Catálogo completo do modpack

- classificar todos os JARs magic-related atuais como spell/resource/ritual/bridge/library/gear/mixed;
- extrair todos os spells/poderes discretos de cada `SPELL_PROVIDER` usando fontes permitidas e o JAR/config realmente instalado quando necessário;
- registrar acquisition/learning, raridade/tier, mana/resource, cooldown, cast time, damage/effect/scaling e IDs reais;
- catalogar glyphs/forms/augments de Ars sem explodir toda combinação possível;
- catalogar rituais/brews/plants/idols/transmutations de Hexalia;
- catalogar toxicity/mutagens/oils/preparações do Toxony;
- catalogar Holy/Paladin, Cataclysm/Ignis, Asterism/Eidolon, Goety, Malum, Vampirism/Bloodlines e todos os demais providers/addons relevantes;
- produzir a matriz `capacidade → providers existentes → cobertura → lacuna real`.

### Implementação

Somente depois da matriz de deduplicação:

- selecionar os spells/sistemas novos com delta mecânico real;
- fechar números/tier/aquisição;
- implementar Caos, Ordem, Hemática/Vincular, Infernal, Divina/Celestial e Bruxaria integrada conforme os planos aprovados;
- criar texturas, partículas, animações, áudio e HUD originais de alta qualidade;
- validar Immersive Portals e demais bridges no pack real;
- executar testes/CI/QA apropriados e atualizar a Wiki para `IMPLEMENTADO` somente com evidência.

## Pendências canônicas que não bloqueiam o merge documental

- Familiars & Divination continua seguindo o fluxo próprio do Stage 07.07;
- Stage 08 continua dono do balanceamento final onde os números ainda são TBD;
- QA visual/manual no cliente real não é reivindicado por esta PR;
- bugs ou discrepâncias de providers externos são registrados como pendências, não corrigidos nesta fase.
