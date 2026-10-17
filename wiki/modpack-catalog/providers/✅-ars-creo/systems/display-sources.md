# Create Display Sources for Ars infrastructure

State: `SOURCE-PINNED 5.4.0 / PRESENTATION-ONLY`

Ars Creo registers two Create Display Sources:

- `ars_creo:turret`: reads an Ars BasicSpellTurretTile and exposes stored spell name/display string; registered for Basic, Timer, Rotating and Enchanted turret blocks/BEs.
- `ars_creo:source_jar`: reads an Ars SourceJarTile and exposes current Source count.

These values feed Create Display Link/targets. They are observational UI/presentation data and are not a security, cast, resource or Arcane Danger authority surface.

Black Arcana must never use a display value as proof that a spell fired, Source was settled or a player owns the underlying system.

## Engenharia causal para perks — 17/10/2026

**Proveniência:** mod ID `ars_creo`, JAR instalado documentado `ars_creo-1.21.1-5.4.0.jar`, SHA-1 `22a6afd4fbe76354acc9c1ba076c89a94d120d94`. Código da versão `5.4.0`: `baileyholl/Ars-Creo@6a99d36fab441653478fc49de8f28164f0894eb2` (**SOURCE_CAUSALITY**, sem equivalência binária completa nem QA do pack). Hosts: Ars Nouveau `5.13.1`, Create `6.0.10`. **Ars Creo não registra glyph próprio: +0 IDs novos.**

**Create Display Sources — leitura observacional** — efeito do provider externo/integração Create, não nova raiz mágica.

| Eixo | Mecanismo no source pinado | Limite de perk |
|---|---|---|
| Registries | Duas `DeferredHolder<DisplaySource>`: `ars_creo:turret` e `ars_creo:source_jar`. O primeiro é anunciado para turret Basic/Timer/Rotating/Enchanted; o segundo para Source Jar tile/block. Não há registro de moving-cast em Rotating no setup exato. | Visibilidade Display Source não é permissão para cast. |
| Dados | TurretDisplaySource observa spell configurada, SourceJarDisplaySource usa `SourceJarTile.getSource()`. Formatação para lectern/Display Link depende do alvo Create. | UI pode estar obsoleta em ticks e não pode ser usada como prova de settle. |
| Limites UI | SourceJarDisplaySource retorna texto de espaço insuficiente com `stats.maxRows()<2`; sem alvo SourceJarTile retorna Stream.empty; dados são componentes de apresentação. | Não usar strings traduzidas como ResourceLocation de feitiço/atributo. |
| Autoridade | Não executa `spell.cast`, `takeSource`, nem teleporte/ritual no corpo das DisplaySources. Sem Target/Range/Damage/Projectiles. | N/A para perks de dano/XP. Dados de painel não provam efeito. |
| Compat e QA | Display BY_BLOCK e BY_BLOCK_ENTITY são registradas separadamente; podem apresentar comportamento diferente em contraption móvel que não possui BE world normal. | ⚠️ testar display em moving contraption, client screen e remote read. Fail-closed. |

**Âncoras verificáveis:** [CreateCompat.java](https://github.com/baileyholl/Ars-Creo/blob/6a99d36fab441653478fc49de8f28164f0894eb2/src/main/java/com/hollingsworth/ars_creo/CreateCompat.java#L25-L68) · [SourceJarDisplaySource.java](https://github.com/baileyholl/Ars-Creo/blob/6a99d36fab441653478fc49de8f28164f0894eb2/src/main/java/com/hollingsworth/ars_creo/common/display/SourceJarDisplaySource.java#L17-L55) · [TurretDisplaySource.java](https://github.com/baileyholl/Ars-Creo/blob/6a99d36fab441653478fc49de8f28164f0894eb2/src/main/java/com/hollingsworth/ars_creo/common/display/TurretDisplaySource.java#L13-L72).

**Aceitação pendente:** Display Link com turret sem spell/spell inválida, Source Jar 0/10000, Rotating turret sem cast, contraste com servidor, client chunk unload, target lectern, número mínimo de linhas. O RPG Skill Tree não controla o runtime Ars/Create. **0 adapters homologados, +0 IDs de magia.**
