# Índice da Wiki de Feitiços

## Implementados / canônicos — Black Arcana

A Wiki é reconciliada contra o runtime/plans atuais. A presença de uma página não transforma hard ceiling em valor final de balanceamento; números ordinários ainda não fechados permanecem `TBD — Stage 08`.

### Blood & Curses

- Blood Price
- Equilibrium Rite
- Sanguine Harvest
- Law of Recurrence
- Sympathetic Wound

### Souls & Death

- Mortal Ledger / Soul Anchor
- Spirit Sight

### Projection & Arsenal

- Echo Armament
- Ephemeral Tempering
- Spectral Arsenal
- Rift Blades
- Oathforged Ascension — progression/ledger seam, não spell ofensivo

### Space & Displacement

- Threshold Gate
- Veilstep Reflex
- Anchor Recall
- Reciprocal Transposition
- Vector Reversal

### Black Flame

- Black Pyre (`black_arcana:black_pyre`)

### Forbidden Domains

- Localized Forbidden Domain runtime — efeitos provider-native específicos permanecem fail-closed quando não aprovados.

## Planejado no roadmap atual

- Familiars & Divination (Stage 07.07)
- Progression & Balance (Stage 08)
- Hardening & Release (Stage 09)

## Escolas / expansões em pesquisa

### Iron's-hosted / spellcasting

- Arcana do Caos — candidata a escola nova do Iron's; depende da deduplicação completa.
- Arcana da Ordem — candidata a escola nova do Iron's; depende da deduplicação completa.
- Magia Infernal — candidata; deve provar delta real contra Fire, Goety, Cataclysm/Ignis e demais providers.
- Expansão Celestial — **entra em Holy**, não cria escola Divine separada.

### Blood

- A escola Blood já existe no Iron's e será reformada para usar **0 mana normal**; custos futuros usam sangue próprio, sangue drenado quando semanticamente válido, vínculos hemáticos e/ou reservatório em mB.
- `BLOOD != VITAL_ENERGY != SOUL != SPIRIT != MANA`.

### Bruxaria

- Bruxaria Integrada — Hexalia como núcleo de witchcraft, com composição provider-native de Toxony, Eidolon, Malum, Goety, Vampirism/Bloodlines, Ars, Iron's e outros apenas quando houver delta real e hook/efeito verificável.

## Sistemas transversais

- Reservatório Hemático e Vínculos (`systems/blood-reservoir/`)
- Fonte Infernal / Lava Infernal Nether-only (`systems/infernal-source/`)
- Sanctum / Ressonância Celestial para Holy `MIRACLE_TIER` (`systems/celestial-resonance/`)
- Integração de portais com Immersive Portals (`systems/portal-integration/`)
- Padrão visual, partículas, animação e áudio (`systems/visual-language/`)

## Catálogo integral do modpack

A árvore canônica é:

`modpack-catalog/providers/<provider>/<classificação-nativa>/<capacidade>.md`

Não existe uma segunda árvore canônica em `wiki/providers/`; o conteúdo legado foi consolidado em `wiki/modpack-catalog/`.

Metadados globais:

- `modpack-catalog/meta/CURRENT-MAGIC-PROVIDERS.md` — inventário/reconciliação da base instalada;
- `modpack-catalog/meta/DEDUPLICATION-POLICY.md` — regra `PROVIDER-NATIVE FIRST` e assinatura semântica;
- `modpack-catalog/meta/PROVIDER-AUDIT-QUEUE.md` — fila da auditoria.

O catálogo provider-by-provider e capacidade-by-capacidade continua em andamento. Conteúdo já existente também recebe ficha, mesmo quando `JÁ EXISTE / SEM ALTERAÇÃO PLANEJADA`.

## Regra de documentação

Cada spell ou poder nomeado deve possuir página própria quando for discreto e catalogável. Sistemas combinatórios como Ars Nouveau recebem inventário de glyph/form/augment/ritual/system e apenas combinações nomeadas/canônicas; não serão criadas páginas para toda permutação matemática possível.

Nenhum spell novo do Black Arcana é aprovado antes de ser comparado com o concorrente provider-native mais próximo.
