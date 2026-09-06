# Black Arcana — Wiki Mestre de Magia

Esta pasta é a fonte canônica de documentação para os feitiços próprios do Black Arcana e para o catálogo de integração/deduplicação dos providers mágicos instalados no modpack.

## Regras de estado

Cada página individual deve marcar claramente um estado, por exemplo:

- `IMPLEMENTADO / CANÔNICO` — presente em `main` com runtime canônico.
- `IMPLEMENTADO / VALIDAÇÃO FINAL DEFERIDA` — runtime presente, mas aceitação final em modpack/cliente ainda pendente.
- `EXTERNAL PROVIDER / INSTALLED` — conteúdo de mod/addon instalado, catalogado sem reivindicar ownership do Black Arcana.
- `PLANEJADO` — design previsto, ainda sem runtime canônico.
- `CONCEITO / PESQUISA` — proposta em estudo.
- `BLOQUEADO / FAIL-CLOSED` — depende de provider/API/authority ainda não confirmados.
- `REDUNDANTE / NÃO APROVADO` — provider existente já cobre o efeito sem delta suficiente.

## Estrutura

### Conteúdo Black Arcana

- `implemented/` — feitiços e mecânicas já implementados/canônicos.
- `planned/` — conteúdo já previsto no roadmap atual.

### Escolas e disciplinas em pesquisa

- `schools/chaos/` — Arcana do Caos, host prioritário Iron's.
- `schools/order/` — Arcana da Ordem, host prioritário Iron's.
- `schools/blood-binding/` — expansão hemática/vincular, sem mana normal.
- `schools/infernal/` — magia infernal, distinta de Fire/Black Flame.
- `schools/divine/` — Holy/Divine/Celestial sem Aether.
- `schools/witchcraft/` — bruxaria integrada com Hexalia como núcleo.

### Sistemas de recurso e integração

- `systems/blood-reservoir/` — sangue armazenado em mB e vínculos de fontes.
- `systems/infernal-source/` — Lava Infernal e reservatório Nether-only.
- `systems/divine-source/` — Sanctum e Ressonância Celestial para Miracle-tier.
- `systems/portal-integration/` — integração com Immersive Portals.
- `systems/visual-language/` — padrão de texturas, partículas, animação, áudio e performance.

### Providers

- `providers/CURRENT-MAGIC-PROVIDERS.md` — reconciliação da base instalada.
- `providers/DEDUPLICATION-POLICY.md` — provider-native first, assinatura semântica e gate de spell novo.
- subpastas futuras por provider — catálogo de spells/glyphs/rituais/poderes e valores reais.

### Fontes

- `sources/` — metodologia e referências externas usadas para inspiração/adaptação; fonte externa nunca substitui runtime/config do provider quando o valor exato é necessário.

## Campos obrigatórios por feitiço/poder discreto

Cada arquivo individual deve documentar, quando aplicável:

1. identidade, ID e fantasia;
2. estado de implementação/provider;
3. escola/domínio/provider/host;
4. tier/raridade/progressão;
5. método de obtenção e aprendizado;
6. requisitos e gates;
7. recurso consumido e custo exato/escala;
8. cooldown;
9. cast time/channel time;
10. alcance, área e seleção de alvos;
11. dano, cura, transferência ou efeito quantitativo;
12. scaling/fórmula;
13. efeitos secundários;
14. PvP/bosses/summons/friendly fire;
15. fallback/fail-closed;
16. segurança, anti-abuso e deduplicação;
17. VFX, animação, áudio, ícone e HUD;
18. integrações com outros mods;
19. receitas, rituais, estruturas ou itens associados;
20. testes/evidência de validação;
21. referências/proveniência;
22. concorrente provider-native mais próximo e justificativa de delta, para conteúdo novo.

## Números e autoridade

Nenhum número de dano, cooldown, custo ou progressão deve ser inventado em páginas `IMPLEMENTADO` ou `EXTERNAL PROVIDER`. Quando o código só fixa hard ceilings, a Wiki registra o teto e deixa o balanceamento normal como `TBD — Stage 08` ou `TBD — provider/config`.

Para providers externos, a prioridade de evidência é:

1. versão/JAR efetivamente instalado;
2. config/runtime/código da versão correspondente;
3. documentação oficial da mesma versão;
4. páginas públicas para descoberta/contexto;
5. inferência apenas quando explicitamente marcada e nunca para um número tratado como canônico.

## Deduplicação

Todo spell novo passa por `providers/DEDUPLICATION-POLICY.md`. Mudar nome, cor, textura ou partículas não cria gameplay novo. Quando um provider instalado já possui o efeito, integrar ou especializar a implementação existente é preferível a criar clone Black Arcana.

## Qualidade visual

Uma página pode estar mecanicamente correta e ainda não estar visualmente aprovada. A validação final de VFX exige cliente real do modpack; automated CI não prova que partículas, animações, portais, shaders ou texturas estão bonitas e legíveis em jogo.
