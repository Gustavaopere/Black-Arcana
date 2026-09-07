# Iron's Spells 'n Spellbooks — índice canônico do provider

- **Mod ID:** `irons_spellbooks`
- **JAR do pack:** `irons_spellbooks-1.21.1-3.16.3.jar`
- **Runtime:** `1.21.1-3.16.3`
- **Regra:** todo spell ativo recebe ficha canônica individual; implementações deprecated preservadas não inflam a contagem ativa.

## Progresso do catálogo individual

| Escola | Total ativo | Fichas ativas | Estado |
|---|---:|---:|---|
| Blood | 10 | 10 | `COMPLETO` |
| Eldritch | 7 | 7 | `COMPLETO` |
| Ender | 16 | 16 | `COMPLETO` |
| Evocation | 17 | 17 | `COMPLETO` |
| Fire | 13 | 13 | `COMPLETO` |
| Holy | 12 | 12 | `COMPLETO` |
| Ice | 12 | 12 | `COMPLETO` |
| Lightning | 10 | 10 | `COMPLETO` |
| Nature | 13 | 13 | `COMPLETO` |

# Cobertura do Iron's base: **110/110 — COMPLETO**

Todos os spells ativos das nove escolas nativas possuem ficha individual na hierarquia `providers/irons-spells/<escola>/<spell>.md`.

`COMPLETO` significa cobertura documental: cada ficha registra os campos obrigatórios com evidência verificável ou `NÃO VERIFICADO`. Não significa que todos os internals de entities/effects tenham sido decompilados, nem que QA visual/client-real esteja encerrado.

## Provenance

- catálogo player-facing atual: `https://iron.wiki/spells/`;
- source instalado auditado: `iron431/irons-spells-n-spellbooks@e4056af90302d37eb1739f5ff05020b020e6e252`;
- esse commit declara Minecraft `1.21.1` e mod version `1.21.1-3.16.3` no próprio `gradle.properties`;
- quando a documentação pública e o source divergem, ambas as evidências são preservadas e a divergência é explicitada;
- IDs históricos não são renomeados na Wiki: por exemplo Acid Spit=`acid_orb` e Poison Spray=`poison_breath`.

## Spells legados/deprecated fora da contagem ativa

- `holy/cloud-of-regeneration.md` — implementação ainda presente no source 3.16.3, `Deprecated=true`, ausente do catálogo ativo.

## Escolas nativas

Blood 10; Eldritch 7; Ender 16; Evocation 17; Fire 13; Holy 12; Ice 12; Lightning 10; Nature 13. **Total: 110.**

## Estrutura e ownership

`providers/irons-spells/<escola>/<spell>.md`

Spells de addons permanecem no provider que realmente os registra, mesmo quando usam uma escola do Iron's. A cobertura 110/110 **não** significa que o ecossistema Iron's do modpack esteja todo catalogado: addons/providers externos continuam no backlog próprio.

## Próximo gate

Depois do base 110/110, o trabalho migra para os providers/addons instalados e para suas classificações nativas. Fase 3/criação de spells novas continua dependente de deduplicação contra esse ecossistema ampliado; o base completo sozinho não prova uma lacuna.

## Campos obrigatórios

Status/provider/versão/ID/escola; descrição; níveis/raridade; cast/channel; recurso/custo/cooldown; dano/cura/tipo; alcance/área/duração; scaling/caps; targets/PvP/bosses/summons; requisitos/obtenção/aprendizado; itens/focus/rituais; VFX/animação/áudio; bridges; deduplicação; bugs/QA/fail-closed; fonte/evidência.
