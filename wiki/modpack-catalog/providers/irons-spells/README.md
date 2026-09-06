# Iron's Spells 'n Spellbooks — índice canônico do provider

- **Mod ID:** `irons_spellbooks`
- **JAR do pack:** `irons_spellbooks-1.21.1-3.16.3.jar`
- **Runtime:** `1.21.1-3.16.3`
- **Regra desta Wiki:** todo spell **ativo** do catálogo corrente recebe um arquivo `.md`, mesmo quando não há alteração planejada pelo Black Arcana. Entradas source-only explicitamente `deprecated` permanecem documentadas na auditoria do provider e não são contadas como spell ativo.

## Progresso do catálogo individual

| Escola | Total | Fichas individuais | Estado |
|---|---:|---:|---|
| Blood | 10 | 10 | `COMPLETO` |
| Eldritch | 7 | 7 | `COMPLETO` |
| Ender | 16 | 16 | `COMPLETO` |
| Evocation | 17 | 17 | `COMPLETO` |
| Fire | 13 | 13 | `COMPLETO` |
| Holy | 12 | 12 | `COMPLETO` |
| Ice | 12 | 0 | `PENDENTE` |
| Lightning | 10 | 0 | `PENDENTE` |
| Nature | 13 | 0 | `PENDENTE` |

**Cobertura atual:** 75/110 spells ativos do Iron's base possuem ficha individual canônica.

`COMPLETO` aqui significa que a ficha individual existe para todos os spells ativos da escola e contém tudo que pôde ser confirmado no passe atual. Não significa que todo detalhe visual, fórmula interna ou rota de loot tenha sido observado no cliente real.

### Nota sobre Holy e `cloud_of_regeneration`

A auditoria de source 3.16.3 ainda encontra `irons_spellbooks:cloud_of_regeneration` no registry/source e o marca como **deprecated**, mas o catálogo público atual de spells expõe 12 Holy ativos e não inclui esse spell. Por isso ele permanece documentado na auditoria histórica/source em `wiki/providers/irons-spellbooks/spells/holy/cloud-of-regeneration.md`, mas **não entra no total ativo 110 nem nas 12 fichas canônicas de Holy desta pasta**.

## Escolas nativas do Iron's base

A build atual do provider-base possui 9 escolas nativas:

1. Blood — 10 spells
2. Eldritch — 7 spells
3. Ender — 16 spells
4. Evocation — 17 spells
5. Fire — 13 spells
6. Holy — 12 spells ativos no catálogo público atual
7. Ice — 12 spells
8. Lightning — 10 spells
9. Nature — 13 spells

**Total ativo do Iron's base adotado pela Wiki: 110 spells.**

## Escolas adicionais no modpack

As 9 acima NÃO representam todas as escolas existentes no pack. Um snapshot real do runtime registrou **36 escolas Iron's** depois que os addons foram carregados.

Escolas adicionais já comprovadas no stack incluem, entre outras:

- Astral — Asterism Arcanum
- Radiance — HazentouveLib/Hazen ecosystem
- Shadow — HazentouveLib/Hazen ecosystem
- Cosmic — HazentouveLib/Hazen ecosystem
- Aqua — Somake
- Symmetry — Somake
- Empty — Dreamless Spells
- Sound — infraestrutura FamiliarsLib/addons associados

A lista exata das 36 escolas será reconstruída a partir do runtime/JARs atuais; nenhum nome será inventado para completar a contagem.

## Estrutura obrigatória

Cada spell ativo do Iron's base fica diretamente nesta pasta:

`providers/irons-spells/<spell>.md`

Spells de addons ficam na pasta do addon que realmente os fornece, por exemplo:

`providers/asterism-arcanum/<spell>.md`
`providers/paladin-spells/<spell>.md`
`providers/dreamless-spells/<spell>.md`

Assim a origem real nunca é perdida mesmo quando vários mods compartilham a mesma escola.

## Campos obrigatórios por magia

Cada ficha deve registrar, quando a informação existir e puder ser verificada:

- status no modpack;
- provider e mod ID;
- JAR/versão;
- escola/tipo;
- descrição funcional;
- níveis e raridade;
- cast type / cast time / channel;
- recurso usado;
- custo;
- cooldown;
- dano/cura e tipo de dano;
- alcance, raio/área e duração;
- scaling/fórmulas/caps;
- targets, PvP, bosses e summons;
- condições e requisitos;
- como obter, fabricar, ganhar e aprender;
- itens/focus/rituais necessários;
- VFX, partículas, textura, animação e áudio;
- integrações/bridges;
- deduplicação e sobreposições;
- bugs/QA/fail-closed relevantes;
- fonte/evidência e estado de verificação.

Campos ainda não comprovados ficam `NÃO VERIFICADO`; nunca são preenchidos por suposição.