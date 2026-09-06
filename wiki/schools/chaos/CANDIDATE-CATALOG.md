# Arcana do Caos — Catálogo candidato

## Estado

`CONCEITO / PESQUISA — NOMES E NÚMEROS AINDA NÃO FECHADOS`

A lista abaixo traduz categorias de feats pesquisadas para mecânicas bounded de Minecraft. Não representa spells implementados.

| Codinome de design | Categoria | Conceito |
|---|---|---|
| Hex de Falha | Probability/Hex | Impõe uma janela bounded em que uma ação elegível do alvo pode falhar/degradar segundo hook real, sem RNG universal. |
| Distorção Vetorial | Telekinesis | Redireciona impulso/projéteis/alvos por Stage 07.04 quando elegível. |
| Ruptura Entrópica | Entropy | Degrada temporariamente estabilidade/duração de um efeito ou construct autorizado. |
| Nó Improvável | Probability | Enviesa um conjunto explícito de resultados permitidos em favor do caster, com cap e cooldown altos. |
| Transmutação Caótica | Transmutation | Converte um bloco/estado permitido para outra variante autorizada; sem arbitrary terrain rewrite. |
| Descompasso | Countermagic | Aumenta cast time/interrompe uma janela de cast quando o provider expõe hook causal seguro. |
| Espelho Instável | Reality | Cria cópia visual/decoy sem duplicar entidade/item/state real. |
| Campo de Dissonância | Reality Field | Stage 07.06 field que altera regras bounded de movimento/projéteis/casting. |
| Rasgo Carmesim | Space | Threshold/short displacement com custo e strain elevados. |
| Colapso de Probabilidade | Keystone spell | Converte múltiplas chances bounded em um resultado garantido dentro de um conjunto pequeno, com cooldown/custo/backlash muito altos. |
| Reescrita Local | Endgame Reality | Altera temporariamente uma propriedade autorizada de uma área/participante, usando Domain authority e restoration bounded. |
| Negação Anômala | Countermagic | Suprime uma categoria mágica explicitamente reconhecida por curto tempo; fail-closed sem adapter. |
| Falha Sistêmica | Anti-construct / Probability | Explora falhas internas de mecanismo, construct, gear ou sistema reconhecido pelo provider. Pode jam/degradar/desligar temporariamente um componente elegível sem virar dano genérico a qualquer máquina/bloco. |
| Égide de Reversão | Reactive Hex / Defense | Ward reativa que liquida **um evento elegível reconhecido** como neutralização, desvio ou ricochete bounded. Sem hook para o projétil/spell/damage provenance, apenas bloqueia/falha fechado conforme contrato; nunca reflete dano desconhecido universalmente. |
| Reversão de Forma | Biological/Transformation | Tenta desfazer shapechange/transformation mágica explicitamente registrada. Sem provider de transformação reversível, falha fechado. |
| Correção Improvável | Support/Probability | Remove ou mitiga um estado negativo somente quando houver outcome registrado e sem duplicar cleanse/heal Holy. A fantasia é causalidade improvável, não cura genérica. |
| Remendo Caótico | Matter/World Effect | Reorganiza temporariamente matéria autorizada para cobertura/fechamento de abertura/reparo bounded, com Stage 04 protection e rollback ownership. |
| Dor de Causalidade | Hex/Control | Aplica dor/controle por família mágica própria, com caps de PvP/boss. Não é simplesmente outro bolt de dano. |

## Feats adicionados pelo corpus Wanda 616

A pesquisa fornecida pelo usuário reforça estes deltas mecânicos:

- armas e mecanismos que falham/engasgam justificam `Falha Sistêmica`;
- projectiles que mudam de direção e momentum cancelado pertencem a `Distorção Vetorial`/`Égide de Reversão`;
- transmutações e reversões biológicas justificam `Reversão de Forma`, mas só com provider hook explícito;
- reparo/rearranjo de estrutura pode existir como `Remendo Caótico`, sempre bounded e protegido;
- cura/ressurreição observada nos quadrinhos **não** justifica novos heals/resurrections de Chaos se Holy/Souls já cobrem o mesmo resultado;
- reality warping de escala global é reduzido a `Reescrita Local`/`Campo de Dissonância`, nunca gamerule global ou edição ilimitada do mundo.

## Notas de deduplicação da pesquisa 2026-09-06

- Feats de reversão de projétil/momentum já pertencem a `Distorção Vetorial`; não criar outro spell só porque a origem narrativa mudou.
- Reversão de banimento/counterspell é extensão possível de `Negação Anômala`/`Descompasso`, não um terceiro countermagic automático.
- Healing, ressurreição e manipulação biológica encontrados em histórias da Scarlet Witch **não entram automaticamente em Caos**: devem ser deduplicados contra Holy/Blood/Souls/witchcraft e só permanecer se a mecânica de probability produzir gameplay realmente diferente.
- Probability aplicada a máquinas justificou `Falha Sistêmica` porque o delta é semântico: atacar causalidade/falha interna, não causar outro raio de dano.
- Hex shield com ricochete justificou `Égide de Reversão` porque o settlement reativo/reflection é diferente de um ward puramente absorvente.

## Regras

- feats de escala cósmica são reduzidos a efeitos localizados;
- nenhuma habilidade altera história/mundo global;
- nenhuma transmutação arbitrária de inventories/entities;
- probability nunca controla loot/RNG global sem boundary próprio;
- grandes efeitos usam Arcane Danger/strain/corruption/backlash;
- Iron's hospeda apresentação/progressão do spell quando a integração final for confirmada;
- efeitos anti-machine devem integrar Create/Sable/outros sistemas somente por adapters próprios; block tag ou nome de classe não é prova de mecanismo elegível.
