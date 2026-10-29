# SnackPirate's Aeromancy Additions 1.2.8 — catálogo técnico

**✅ Catálogo da versão-fonte: 58/58 fichas documentadas.** O escopo inclui os dez spells ativos e 48 contratos de suporte encontrados nos **205 arquivos rastreados, incluindo 73 Java**, da revisão `ae282b32d25ad76ef8d01c637ec05566a767ae4c`. O [fechamento](SOURCE-CATALOG-CLOSURE-1.2.8.md) e o [manifesto com hashes e mapa de arquivos](SOURCE-CATALOG-MANIFEST-1.2.8.json) delimitam essa conclusão. [Índice e barras atualizados](INDEX.md).

**Barra documental do provider:** `████████████████████ 100.0%` — 58/58 no escopo da fonte. **Certificação estática para perks: 0/58**; hooks mutadores `NOT_VERIFIED`; QA física `NOT_TESTED`. O [índice geral](../INDEX.md) calcula as barras globais e a fila alfabética. Nenhum Stage ou runtime foi promovido por este fechamento.

## Conteúdo e autoridade

| Família de fichas | Quantidade | Contratos |
|---|---:|---|
| Spells ativos | 10 | [Airblast](spells/airblast.md), [Airstep](spells/airstep.md), [Asphyxiate](spells/asphyxiate.md), [Dash](spells/dash.md), [Feather Fall](spells/feather-fall.md), [Flush](spells/flush.md), [Updraft](spells/updraft.md), [Wind Blade](spells/wind-blade.md), [Wind Charge](spells/wind-charge.md), [Wind Shield](spells/wind-shield.md) |
| Efeitos e entidades | 11 | [Efeitos](effects/) e [entidades](entities/): aplicação, movimento, impacto, owner, duração, persistência e visual |
| Itens, atributos e escola | 12 | [Nove itens](items/), [dois atributos](attributes/) e [Wind](schools/wind.md) |
| Estado, rede e sistemas | 16 | [Attachment](attachments/), [quatro payloads](payloads/), [dois mixins](mixins/) e [nove sistemas](systems/) |
| Dados e aquisição | 9 | [Dano, tags, receitas, loot, sons, orb, jewelry e helpers não registrados](data-contracts/) |

São **10 raízes semânticas ativas**, preservadas como `COUNTED_SOURCE_PINNED`; as novas fichas não acrescentam magias ao ledger semântico. Cinco chamadas de registro comentadas têm [disposição por classe](systems/unregistered-spell-code.md). Entidades e efeitos registrados podem existir mesmo quando o spell correspondente está inativo; assets e nomes de classes não criam IDs ativos.

Iron's mantém autoridade sobre casting, mana, cooldown, aquisição de scrolls e contratos herdados. Aeromancy fornece os spells concretos e seu estado, entidades e efeitos. Um futuro adapter deve usar um consumidor comprovado, respeitar essa autoridade e impedir liquidação duplicada. [Mapa técnico e proveniência](SOURCE-CONTRACTS-1.2.8.md).

## Limites de evidência e prioridades de integração

Physical JAR SHA-1: **NÃO VERIFICADO** — o hash do publisher não comprova a identidade instalada.

O publisher oficial, arquivo CurseForge `8251034`, tem SHA-1 `dee32c9fa84a9b3796e39846608f8f77591ea56f`. Os 119 recursos da fonte foram comparados e as classes relacionadas por nome e `SourceFile`. Isso não certifica equivalência dos corpos de métodos. O SHA-1 histórico atribuído ao arquivo instalado, `dee32c9fa84d6e39846608f8f77591ea56f`, tem somente **35 caracteres**; a identidade do JAR instalado continua **NOT_VERIFIED**. [Auditoria binária anterior](EXACT-PUBLISHER-SPELLS-1.2.8-PHYSICAL-SHA-BLOCKED.md).

A fonte compila contra NeoForge `21.1.228` / Iron's `3.16.1`; Black Arcana usa NeoForge `21.1.248` em compile/dev; a autoridade física do pack registra NeoForge `21.1.250` / Iron's `3.16.3`. Aceitação pelo intervalo de dependências não comprova compatibilidade em execução.

As fichas destacam mutação de mundo em Flush, estado e autoridade C2S de Airstep, contadores e cleanup, owner após reflexão, força versus dano direto em Wind Charge, deflexão e dodge em Wind Shield, duração aplicada versus tooltip em Updraft e modifiers de Flight. Esses são contratos estáticos e casos de QA; nenhuma falha de gameplay foi declarada reproduzida. [Plano físico pendente](UPSTREAM-TESTS-RUNTIME-QA.md).

Os relatórios anteriores de [spells](SPELL-CARDS-1.2.8.md), [matriz causal](PERK-CAUSAL-ENGINEERING-MATRIX-1.2.8.md) e [inventário fonte](EXACT-1.2.8-SPELL-INVENTORY.md) permanecem como evidência histórica. O manifesto e os índices atuais estabelecem o recorte documental vigente. A catalogação registra identificadores e contratos, sem importar implementação ou assets do provider.
