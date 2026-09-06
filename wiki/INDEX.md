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

## Novas escolas/disciplinas em pesquisa

### Iron's-hosted / spellcasting

- Arcana do Caos — host prioritário: Iron's Spells.
- Arcana da Ordem — host prioritário: Iron's Spells.
- Magia Infernal — host prioritário: Iron's; fonte especial Nether-only para conteúdo de alto nível.
- Magia Divina / Celestial — Holy/Divine sobre Iron's, sem Aether e sem confundir com Astral.

### Hemática / recursos próprios

- Arcana Hemática e Vincular — combustível de sangue próprio/vinculado/armazenado; não usa mana normal.

### Bruxaria

- Bruxaria Integrada — Hexalia como núcleo de witchcraft, com composição provider-native de Toxony, Eidolon, Malum, Goety, Vampirism/Bloodlines, Ars, Iron's e outros apenas quando houver delta real e hook/efeito verificável.

## Sistemas transversais

- Reservatório Hemático e Vínculos (`systems/blood-reservoir/`)
- Fonte Infernal / Lava Infernal Nether-only (`systems/infernal-source/`)
- Sanctum / Ressonância Celestial para Miracle-tier (`systems/divine-source/`)
- Integração de portais com Immersive Portals (`systems/portal-integration/`)
- Padrão visual, partículas, animação e áudio (`systems/visual-language/`)

## Providers e deduplicação

- `providers/CURRENT-MAGIC-PROVIDERS.md` — inventário/reconciliação da base instalada.
- `providers/DEDUPLICATION-POLICY.md` — regra `PROVIDER-NATIVE FIRST` e assinatura semântica.
- Catálogo provider-by-provider e spell-by-spell: em andamento.

### Prioridade atual da auditoria externa

1. Paladin Spells / Holy — valores de fonte 1.21.1 sendo extraídos.
2. Cataclysm: Spellbooks / Ignis — necessário antes de aprovar Magia Infernal.
3. Hexalia — rituals/brews/idols/plants/transmutation.
4. Toxony — toxicity/mutagens/oils/alchemy.
5. Asterism/Eidolon — separar Astral, Holy e Theurgy.
6. Demais providers mágicos da modlist atual.

## Regra de documentação

Cada spell ou poder nomeado deve possuir página própria quando for discreto e catalogável. Sistemas combinatórios como Ars Nouveau recebem inventário de glyph/form/augment e apenas combinações nomeadas/canônicas; não serão criadas páginas para toda permutação matemática possível.

Nenhum spell novo do Black Arcana é aprovado antes de ser comparado com o concorrente provider-native mais próximo.