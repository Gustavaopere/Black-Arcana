# Ars Nouveau 5.13.1 — cinco contratos estáticos de Rituals para planejamento de perks

**Recorte estático:** 5/24 rituais com contrato técnico revisado (Sunrise, Moonfall, Fertility, Flight, Scrying). A identidade dos **24 rituais** já havia sido auditada no JAR; isto não adiciona rituais novos. Mutação por RPG Skill Tree/Black Arcana **⛔ NÃO VALIDADA** e QA físico **⚠️ NÃO TESTADO**. 0/164 providers integrais.

Versionamento: `ars_nouveau-1.21.1-5.13.1.jar` SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd`, source fixo `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`. [Registry binário exato dos rituais](EXACT-BINARY-GLYPH-RITUAL-IDS-5.13.1.md) ≠ equivalência integral de métodos do JAR instalado.

| Ritual | Evidência estática de ritmo/alvo/custo | Boundary |
|---|---|---|
| [Sunrise](rituals/sunrise.md) | Overworld: dayTime+=100 fora da janela 1000..11999; incrementProgress acelera dentro dela; conclusão progress>=18 em gate gameTime%20==0; Source getter herdado 0 | Relógio global e `ClientboundSetTimePacket` de sync Ars, não cast novo por pacote |
| [Moonfall](rituals/moonfall.md) | Overworld: dayTime+=100 até night threshold 13000; acelerador de progress no else, gate >=18; Source getter herdado 0 | Não assumir duração fixa nem autoridade de dimensão local |
| [Fertility](rituals/fertility.md) | AABB inflada 5; trabalho a cada 200 ticks, cap >=20 animais antes da blacklist; Source cost 500 solicitado após mudança | Não cobrar Source nem Mastery por animal |
| [Flight](rituals/flight.md) | RangeEffectRitual: ServerPlayer <=60 via BlockUtil, buff 1200 ticks; Source cost 200 por refresh aceito; onJumpEvent condicional | Não duplicar voo, refresh e packets |
| [Scrying](rituals/scrying.md) | Progress>=15; AABB 5; 6000/18000 ticks; recipe BlockItem/TagScryer; chave an_scryer no persisted NBT; Source getter herdado 0 | Modifier isolado pode concluir sem target e efeito, sem promessa de visão |

**Auditoria de custos:** os três rituais sem override de `getSourceCost()` herdam `AbstractRitual.getSourceCost()=0`. **Não equivale a ritual grátis**; setup, catalisadores, custos de itens, consumidores do brasier e condições de disponibilidade não são fechados por esses getters. `RitualFlight` usa `RangeEffectRitual/RangeRitual` e `setNeedsSource(true)` somente após refresh aceito. `RitualBreed` solicita Source após trabalho; não por entidade.

**Causalidade para perks:** spans de tempo, AABB, Source, buffs, persistência, estado de ritual e pacotes são contratos diferentes. Não trocar seleção, duração ou world time via eventos de spells/glyphs do Ars sem demonstração de API real. QA físico, modpack, side e mods concorrentes seguem pendentes; estágios do Black Arcana permanecem independentes.
