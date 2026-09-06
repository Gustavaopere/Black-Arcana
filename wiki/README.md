# Black Arcana — Wiki Mestre de Magia

Esta pasta é a fonte canônica de documentação para os feitiços próprios do Black Arcana e para o catálogo integral de integração/deduplicação dos providers mágicos instalados no modpack.

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

### Escolas

`wiki/schools/` representa tanto escolas que **já existem no modpack** quanto expansões/escolas em pesquisa.

- `schools/blood/` — Blood do Iron's; reforma hemática planejada para eliminar mana normal e usar sangue próprio/vinculado/armazenado.
- `schools/eldritch/`, `ender/`, `evocation/`, `fire/`, `holy/`, `ice/`, `lightning/`, `nature/` — escolas base já existentes do Iron's.
- `schools/holy/` — também recebe a expansão celestial/divina; **não existe uma escola separada Divine**.
- `schools/chaos/` — Arcana do Caos, host prioritário Iron's, sujeita à deduplicação completa.
- `schools/order/` — Arcana da Ordem, host prioritário Iron's, sujeita à deduplicação completa.
- `schools/infernal/` — candidata, distinta de Fire/Black Flame e dependente da auditoria dos providers infernais existentes.
- `schools/witchcraft/` — bruxaria integrada com Hexalia como núcleo, compondo providers existentes sem cloná-los.

### Sistemas de recurso e integração

- `systems/blood-reservoir/` — sangue armazenado em mB e vínculos de fontes.
- `systems/infernal-source/` — Lava Infernal e reservatório Nether-only.
- `systems/celestial-resonance/` — Sanctum e Ressonância Celestial para spells Holy `MIRACLE_TIER`; não cria nova escola.
- `systems/portal-integration/` — integração com Immersive Portals.
- `systems/visual-language/` — padrão de texturas, partículas, animação, áudio e performance.

### Catálogo integral do modpack

A única árvore canônica de providers é:

`modpack-catalog/providers/<provider>/<classificação-nativa>/<capacidade>.md`

Exemplos:

- Iron's: `modpack-catalog/providers/irons-spells/<school>/<spell>.md`;
- Ars Nouveau: `.../ars-nouveau/glyphs/forms|effects|augments/<glyph>.md`, além de `rituals/` e `systems/`;
- Goety/Malum/Hexalia/Toxony: categorias nativas comprovadas do próprio provider.

A antiga árvore `wiki/providers/` foi consolidada em `wiki/modpack-catalog/` e não deve ser recriada.

Metadados globais do catálogo ficam em `modpack-catalog/meta/`:

- `CURRENT-MAGIC-PROVIDERS.md` — reconciliação da base instalada;
- `DEDUPLICATION-POLICY.md` — provider-native first e gate de spell novo;
- `PROVIDER-AUDIT-QUEUE.md` — fila operacional da auditoria.

Conteúdo já existente entra na Wiki mesmo quando não sofrerá alteração. `JÁ EXISTE / SEM ALTERAÇÃO PLANEJADA` é um estado válido e obrigatório.

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
2. config/runtime da versão correspondente;
3. documentação/API pública da mesma versão;
4. código-fonte externo apenas quando licença/proveniência permitirem o uso previsto;
5. páginas públicas para descoberta/contexto;
6. inferência apenas quando explicitamente marcada e nunca para um número tratado como canônico.

## Deduplicação

Todo spell novo passa por `modpack-catalog/meta/DEDUPLICATION-POLICY.md`. Mudar nome, cor, textura ou partículas não cria gameplay novo. Quando um provider instalado já possui o efeito, integrar ou especializar a implementação existente é preferível a criar clone Black Arcana.

## Qualidade visual

Uma página pode estar mecanicamente correta e ainda não estar visualmente aprovada. A validação final de VFX exige cliente real do modpack; automated CI não prova que partículas, animações, portais, shaders ou texturas estão bonitas e legíveis em jogo.
