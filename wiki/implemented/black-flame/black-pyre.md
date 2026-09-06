# Black Pyre

## Estado

`IMPLEMENTADO / CANÔNICO — REAL-MODPACK HOST ACCEPTANCE DEFERRED`

## Identidade

- **ID:** `black_arcana:black_pyre`
- **Domínio:** Black Flame
- **Provider de apresentação/custo:** Iron's quando hook exato suportado
- **Authority de propagação/world effects:** Black Arcana
- **Função:** forbidden soul-fire, dano/status + frontier visual + terrain plane opcional

## Descrição

Black Pyre não usa vanilla fire spread como mecânica. Um scheduler server-authoritative mantém uma frontier bounded e separa três planos:

1. entity plane — dano/status autorizado;
2. visual plane — propagação visual;
3. terrain plane — mutação opcional governada por World Effect Mode e proteção.

## Obtenção e aprendizado

`TBD — Stage 08 / provider / RPG progression`.

## Custo e casting

- **Recurso/custo:** `TBD — Stage 08/provider`;
- **Cooldown:** `TBD — Stage 08/provider`;
- **Cast time:** `TBD — Stage 08/provider`.

## Dano

Dano normal, PvP multiplier, boss multiplier e cooldown final são `TBD — Stage 08`.

O settlement:

- reautoriza `EntityInteractionType.DAMAGE` imediatamente antes do side effect;
- respeita aliados/PvP/boss policy;
- reporta perda de vida efetivamente confirmada, não dano nominal;
- não interpreta cap >1.0 como amplificação implícita.

## Hard ceilings confirmados

- raio da frontier: `<= 12` blocos;
- células por frontier: `<= 256`;
- candidatos processados/admitidos por tick/frontier: `<= 16`;
- frontiers concorrentes por servidor: `<= 8`;
- lifetime: `<= 1.200 ticks`;
- unloaded candidate é descartado, nunca vira force-load/deferred work.

Esses são tetos técnicos, não valores finais normais.

## World Effect Modes

### COSMETIC

Visual somente; zero mutação de bloco. Entity effects continuam política independente.

### TEMPORARY

Mutação reversível bounded, proteção por célula, compare-and-set e restoration que só reverte estado ainda owned pelo Black Arcana.

### LIMITED

Mutação permanente bounded apenas quando mode permite, via gateway protegido/compare-and-set.

### FULL

Opt-in explícito do servidor. Continua obedecendo todos os hard ceilings; FULL nunca significa propagação infinita ou bypass de claim.

### OFF

Terrain work negado.

## Proteção de mundo

Terrain plane usa world-mutation protection próprio, com posição exata, caster, dimensão, mutation type/class, spell e cast provenance. Adapter instalado que negar/falhar é fail-closed. Block entities/unbreakable targets são rejeitados antes de replacement para evitar perda de inventário/NBT.

## Deduplicação

Black Pyre é diferente de:

- fogo vanilla;
- Lava Infernal / Magia Infernal;
- Soul Fire visual simples;
- spells Ignis do Cataclysm: Spellbooks.

A diferença é o frontier server-authoritative, world-effect modes e lifecycle/protection próprios.

## Provider optional amplification

Malum só pode amplificar quando hook causal/value-bearing comprovar o spirit correspondente ao cast. Presença genérica de spirit em inventário não basta.

## VFX

Black Flame deve possuir identidade de forbidden soul-fire, com frontier visual agressivo. `VFX VALIDADO` continua pendente de teste real no modpack/cliente; CI automatizada não prova qualidade visual.

## Testes/evidência

PR #54 canônica, merge `f57f2547977e48ac2bbd3bb912371913784ea1ba`. Head final passou JUnit, diff sanity, NeoForge build, JAR inspection, GameTests e dedicated-server smoke; post-merge exact-SHA também verde. O plano registra 92/92 GameTests em um dos heads de implementação e hardening posterior antes do merge.
