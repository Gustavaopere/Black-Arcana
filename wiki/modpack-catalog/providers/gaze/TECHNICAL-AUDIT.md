# Auditoria técnica — Gaze 1.1.7.1

## Evidence level

**RELEASE-PINNED / PUBLIC-SURFACE AUDITED / BYTECODE PENDING**.

A identidade do artefato está fechada pelo CurseForge (`gaze-1.1.7.1.jar`, file `7261638`) e pela release Modrinth 1.1.7.1. O conteúdo técnico granular não está fechado porque não há source público localizado e o JAR ainda não foi extraído.

## Relação com Malum

Malum 1.8 alterou Spirit Types e Spirit Rites para Deferred Registries; o changelog do próprio Malum alerta que addons como Gaze precisam acompanhar essa mudança. Gaze 1.1.7 declara permanecer em Malum 1.8 e atualiza seus Rites para deferred registry.

**Authority:** Malum/Gaze são authority de spirit type, rite registry, soul/spirit resource, rite activation, rune/item effects e progression. Black Arcana não deve manter estado paralelo.

## Public release delta 1.1.7 → 1.1.7.1

A 1.1.7.1 é um hotfix/release posterior para Malum 1.8. O changelog público cita:

- fixes de Anima Bestiary;
- Fafnir bonus com Malignant armor;
- movimentação de book entries.

O file page não anuncia novo registry mágico entre 1.1.7 e 1.1.7.1, mas isso **não prova** que o bytecode é idêntico.

## Public 1.1.7 mechanics observados

- Domain of Swords como novo Geas;
- Spirit-Channel pouch;
- projectiles de Seidhr alterados;
- Spirit Saber forms com abilities atualizadas;
- Veil's Edge com mechanic ao matar players e Umbral drops;
- Splintered World com balance/targeting/splinter uptime;
- Rites migrados a deferred registry e vários efeitos reworked;
- Meditation Ring, Mage Ethics Ring e Charge Necklace receberam buffs;
- compat Iron's descrita como pequena/trial run.

## Deduplicação

- não reinterpretar Geas como Iron's spell;
- não duplicar Malum Spirit Rites com um segundo ritual state machine;
- não duplicar Umbral/spirit drop settlement;
- não conceder soul/spirit resources por inferência visual;
- qualquer bridge Iron's↔Gaze deve esperar hook/bytecode exato; a própria release chama a compat de experimental/pequena.

## QA pendente

- registry IDs e contagem exata de Rites;
- os dois Geas e seus IDs/condições completos;
- 8 Runes e modifiers finais;
- 6 weapons e mechanics finais;
- 5 Curios e slots/effects;
- spirit costs/recipes/rite inputs/outputs;
- server authority, idempotência e persistence;
- PvP/loot/farming de Umbrals;
- compatibilidade real com Malum 1.8.2 do pack e Iron's 3.16.3.

Até o JAR/source existir, todos esses campos permanecem **NÃO VERIFICADO**.