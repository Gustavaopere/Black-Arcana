# Wiki Status

`IN PROGRESS — PR #61 — NÃO MERGEAR AINDA`

## Concluído até esta passagem

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
- auditoria de fonte do Paladin Spells 1.21.1 iniciada e possível problema de authority em Sworn Protector identificado para validação;
- Cataclysm: Spellbooks baseline público auditado como referência, com discrepância explícita frente ao JAR 1.1.13 instalado;
- corpus fornecido pelo usuário para Scarlet Witch, Doctor Strange, Doctor Fate e John Constantine processado e convertido em categorias de gameplay/dedup;
- Constantine formalizado como repertório transversal, não nova escola, com técnicas roteadas para Witchcraft/Order/Infernal/Blood/Binding/Divine conforme semântica.

## Pendente na mesma Wiki

### Catálogo Black Arcana

- reconciliar valores runtime/config já existentes em cada página;
- Familiars & Divination quando 07.07 for efetivamente desenhado/implementado pelo fluxo correto;
- Stage 08: fechar dano/cooldown/custos/progressão finais.

### Catálogo completo do modpack

- classificar todos os JARs magic-related atuais como spell/resource/ritual/bridge/library/gear/mixed;
- extrair todos os spells/poderes discretos de cada `SPELL_PROVIDER`;
- registrar acquisition/learning, raridade/tier, mana/resource, cooldown, cast time, damage/effect/scaling e IDs reais;
- catalogar glyphs/forms/augments de Ars sem explodir toda combinação possível;
- catalogar rituais/brews/plants/idols/transmutations de Hexalia;
- catalogar toxicity/mutagens/oils/preparações do Toxony;
- catalogar Holy/Paladin completamente e validar o JAR real;
- extrair o JAR Cataclysm: Spellbooks 1.1.13 instalado antes de canonizar sua lista/valores;
- catalogar Cataclysm/Ignis Soulfires/Soul Fire'd antes de fechar o delta da Magia Infernal;
- catalogar Asterism/Eidolon antes de fechar o delta Divino/Astral/Theurgy;
- percorrer todos os demais addons de Iron's, Ars, Goety, Malum, Vampirism/Bloodlines e providers relacionados.

### Novas escolas

- concluir deduplicação de Caos/Ordem contra todos os providers;
- selecionar somente spells com delta mecânico real depois da deduplicação;
- fechar receitas/multiblocks/resources de Blood, Infernal e Divine;
- fechar witchcraft cross-mod recipes somente depois do inventário dos efeitos providers.

### Qualidade/validação

- testar VFX no cliente real do pack;
- validar API da versão instalada do Immersive Portals addon;
- revalidar warnings históricos de assets do Toxony;
- nenhuma observação pública ou source audit substitui teste do JAR/config efetivamente instalado quando comportamento for material.
