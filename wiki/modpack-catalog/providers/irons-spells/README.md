# Iron's Spells 'n Spellbooks — índice canônico do provider

- **Mod ID:** `irons_spellbooks`
- **JAR do pack:** `irons_spellbooks-1.21.1-3.16.3.jar`
- **Runtime:** `1.21.1-3.16.3`
- **Regra desta Wiki:** TODO spell existente recebe um arquivo `.md`, mesmo quando não há alteração planejada pelo Black Arcana. Spells deprecated ainda presentes no provider recebem ficha histórica/semântica, mas não inflam a contagem ativa do catálogo oficial.

## Progresso do catálogo individual

| Escola | Total ativo | Fichas ativas | Estado |
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

**Cobertura ativa atual:** 75/110 spells do Iron's base possuem ficha individual canônica.

`COMPLETO` aqui significa que existe ficha individual para todos os spells **ativos** da escola e que cada campo obrigatório foi preenchido com evidência verificável ou marcado explicitamente `NÃO VERIFICADO`. Não significa que campos ainda desconhecidos tenham sido observados ou inferidos. VFX/runtime, fórmulas internas, loot específico, PvP/boss/summon policy, itens/rituais e QA client-real permanecem desconhecidos quando a respectiva ficha assim registrar.

### Spells legados/deprecated preservados fora da contagem ativa

- `holy/cloud-of-regeneration.md` — implementação Holy ainda presente no source 3.16.3, `Deprecated=true` no `DefaultConfig`, ausente do catálogo oficial ativo atual. Mantido para provenance/deduplicação histórica sem alterar a cobertura ativa 75/110 nem o total ativo de 110 spells.

## Escolas nativas do Iron's base

A build atual do catálogo oficial ativo possui 9 escolas nativas:

1. Blood — 10 spells
2. Eldritch — 7 spells
3. Ender — 16 spells
4. Evocation — 17 spells
5. Fire — 13 spells
6. Holy — 12 spells
7. Ice — 12 spells
8. Lightning — 10 spells
9. Nature — 13 spells

**Total ativo do Iron's base: 110 spells.**

## Estrutura física obrigatória

O catálogo do Iron's é organizado pela classificação nativa mais forte do provider: **escola**.

```text
providers/irons-spells/
├── README.md
├── PROVIDER-AUDIT.md
├── blood/
├── eldritch/
├── ender/
├── evocation/
├── fire/
├── holy/
├── ice/
├── lightning/
└── nature/
```

Cada spell fica em:

`providers/irons-spells/<escola>/<spell>.md`

Exemplos:

- `providers/irons-spells/blood/acupuncture.md`
- `providers/irons-spells/ender/portal.md`
- `providers/irons-spells/holy/sunbeam.md`

Spells de addons **não são movidos para a pasta do Iron's base**. A origem real permanece sendo o addon que registrou o spell, mesmo quando ele usa uma escola do Iron's. Exemplos:

- `providers/asterism-arcanum/astral/<spell>.md`
- `providers/paladin-spells/holy/<spell>.md`
- `providers/dreamless-spells/empty/<spell>.md`

Isso preserva simultaneamente duas dimensões úteis para auditoria: **provider de origem** e **escola/classificação**.

## Escolas adicionais no modpack

As 9 escolas acima NÃO representam todas as escolas existentes no pack. Um snapshot real do runtime registrou **36 escolas Iron's** depois que os addons foram carregados.

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

## Campos obrigatórios por magia

Cada ficha deve registrar, quando a informação existir e puder ser verificada:

- status no modpack;
- provider e mod ID;
- JAR/versão;
- spell ID;
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

Campos ainda não comprovados ficam `NÃO VERIFICADO`; nunca são preenchidos por suposição. Uma escola só recebe `COMPLETO` quando todos os spells ativos têm ficha e os campos obrigatórios estão explicitamente resolvidos como evidência ou `NÃO VERIFICADO`.
