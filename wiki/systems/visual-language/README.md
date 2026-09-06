# Padrão visual, animação e áudio da magia

## Estado

`DESIGN CANÔNICO DA WIKI — validação visual real ainda pendente`

## Objetivo

Nenhum spell novo de alto nível deve ser aprovado apenas porque a mecânica funciona. A página individual precisa definir uma apresentação coerente com sua escola e suficientemente distinta para o jogador reconhecer o tipo de magia antes de ler o nome.

## Stack disponível no pack

Prioridades de integração visual:

- Ace's Spell Utils — infraestrutura de casting/VFX/shaders/helpers, versão instalada atual 1.2.7.2;
- AAA Particles e AAA Particles: World — partículas de alta qualidade e efeitos de mundo;
- GeckoLib 4 — animações/modelos quando entidade, equipamento, constructo ou objeto animado exigir;
- Epic Fight & Iron's Spellbook Animation Compat — coerência entre casting e Battle Mode;
- texturas/modelos próprios e recursos do provider original quando licenciados/permitidos e tecnicamente adequados.

A implementação deve confirmar API exata antes de depender de capability específica.

## Requisitos mínimos por spell importante

Cada página deve definir:

1. pose/gesto de conjuração;
2. anticipation — leitura visual antes do impacto;
3. emissão/forma da magia;
4. trajetória ou formação;
5. impacto;
6. efeito persistente, se houver;
7. dissipação/cleanup;
8. som de cast;
9. som de impacto/loop;
10. ícone e linguagem de HUD;
11. LOD/culling/fallback de partículas;
12. comportamento em primeira e terceira pessoa.

## Linguagem por escola

### Caos

Carmesim/magenta profundo, ribbons, fragmentos, runas incompletas, assimetria, ruído espacial controlado, trajetórias quebradas e distorção localizada. Evitar 'partícula vermelha genérica'.

### Ordem

Mandalas, círculos concêntricos, polígonos perfeitos, tesselações, linhas limpas, anéis contrarrotativos, grades e selos. Construção em etapas transmite precisão.

### Hemática

Sangue visual deve ter massa/fluxo, não partículas vermelhas soltas. Vínculos usam tether/spline e pulsos somente quando existe transferência real confirmada pelo servidor. Sangue especial pode ter materiais distintos.

### Infernal

Vermelho incandescente escuro, preto queimado, lava extremamente quente, brasas densas, distorção térmica e flame fronts. O componente mágico deve ser visualmente diferente de fogo vanilla e de Black Flame.

### Divina/Celestial

Luz branca-dourada com acentos celestes, feixes verticais, estrelas, halos, constelações, prismas, plumas/traços luminosos abstratos e geometria sagrada. Evitar estética que dependa de Aether.

### Bruxaria

Fumaça herbal, líquidos, vapor de caldeirão, runas/diagramas no solo, folhas, sementes, pó, velas, frascos, mudança de cor conforme reagentes e sinais visuais do efeito/provider incorporado.

## Texturas

- priorizar materiais legíveis de perto e em movimento;
- evitar upscale artificial de pixel art ruim;
- usar emissive maps onde a pipeline suportar;
- separar textura-base, emissivo e máscara quando o renderer/provider permitir;
- portais e fluidos especiais precisam de animação/material próprios;
- ícones devem permanecer legíveis no tamanho real da spellbar.

A resolução final deve ser definida por ativo e pipeline; não fixar 32/64/128 px de forma universal sem testar memória, mipmaps e estética do pack.

## Performance

VFX não podem alterar gameplay por queda de FPS ou saturar rede/servidor.

- servidor transmite eventos/estado mínimo, não centenas de partículas individuais;
- cliente gera apresentação a partir do evento confirmado;
- distância e quantidade usam LOD;
- partículas fora de visão devem ser reduzidas/cortadas quando possível;
- loops têm lifetime explícito e cleanup;
- bosses/domains precisam de budgets próprios;
- fallback visual nunca altera dano, custo ou targeting.

## Critério de aprovação visual

`VFX PLANEJADO` não equivale a `VFX VALIDADO`. Aceitação final exige teste no cliente real do modpack, inclusive com shaders/render stack relevante, primeira/terceira pessoa, Epic Fight e cenas com múltiplos casts simultâneos.
