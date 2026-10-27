# Goety 3.1.4 — `lightning_focus`

Status: **✅ CATALOGADO / COUNTED_EXACT** · identificador factual obtido da auditoria do **JAR 3.1.4 hash-matched** · **⚠️ funcionamento físico/números não validados nesta etapa**.

## Identidade canônica

- **Provider:** Goety (mod id `goety`).
- **JAR instalado e auditado:** `goety-3.1.4.jar` (NeoForge/Minecraft 1.21.1); SHA-1 `a0770e180e4e8b1b87d8fa9c8356e9dbf34d82a7`.
- **Identidade de Focus no artefato:** `lightning_focus` — item/ação de Focus ativo do conjunto exato de 123. Não é o `empty_focus` proxy.
- **Posição no inventário exato:** 62/123. Número ordinal editorial, não identificador de registry ou ordem de carregamento.
- **Aquisição documental:** o JAR exato contém receita base de aquisição homônima para este Focus e sem condition de mod carregado; o conjunto tem 80 recipes de tipo `goety:ritual` e 43 shaped. **O tipo específico desta receita não é deduzido apenas pela lista agregada.** A execução real com recursos/progressão do modpack não foi comprovada nesta etapa.
- **Conta semântica:** `COUNTED_EXACT`, já incluída nos 123 Focuses Goety do ledger; materializar a ficha **não acrescenta uma nova identidade**. Receitas alternativas de obtenção não criam outros spells.
- **Escola/categoria exata, classe e método runtime, cast-time, Soul Energy, cooldown, alcance, dano, efeitos, targeting, PVP/proteção, progressão/research e numeric balance:** **NÃO VERIFICADO nesta ficha**. A identificação factual do item não estabelece automaticamente contrato de API/efeito.

## Authority e deduplicação

Goety é a autoridade de Soul Energy, Focus/Staff casting, custos, recipe execution, servants, cleanup e estado persistente. Black Arcana não cria outro Soul ledger, uma segunda conjuração, um débito adicional, novo summon ou uma segunda world mutation; quaisquer bridges futuras exigem boundary server-safe comprovada e comportamento fail-closed.

## Evidência

- [Inventário semântico exato 3.1.4](../EXACT-3.1.4-SEMANTIC-INVENTORY.md): lista de **123** nomes `_focus` ativos, com `empty_focus` excluído e aquisição agregada 80/43.
- [Auditoria do artefato](../EXACT-3.1.4-ARTIFACT-AUDIT.md): hash físico verificado e exclusões.
- [Fronteira de integração](../INTEGRATION-RULES.md) e [catálogo anterior](../FOCUS-CATALOG.md).

**Clean-room:** a ficha contém dados factuais de identidade e proveniência, não código, assets, tradução de tooltip ou implementação upstream.

## Auditoria complementar — raio, alvo e impacto do relâmpago (27/10/2026)

**Escopo estrito:** a identidade `lightning_focus` e o SHA-1 do JAR **3.1.4** permanecem os comprovados acima; toda a mecânica abaixo vem **somente** do [fonte pública Goety 3.1.1 pinada](https://github.com/Vivideru/Goety-3/blob/6c41a04f2d712097c4461f969a6bb8ee277149ef/src/main/java/com/Polarice3/Goety/common/magic/spells/storm/LightningSpell.java), commit `6c41a04f2d712097c4461f969a6bb8ee277149ef`. **Não certifica ABI, valores finais ou hooks 3.1.4.** Relatório transversal: [Lightning/Leeching — causalidade e world safety](../SOURCE-ADJACENT-LIGHTNING-LEECHING-3.1.1-20261027.md).

| Eixo | Consumidor observado na fonte 3.1.1 | Limite para perks |
|---|---|---|
| Config / recursos | `lightningCost=16`, `lightningTime=0`, `lightningCoolDown=100`, `lightningDamage=5.0` são defaults de [SpellConfig L1630–1638](https://github.com/Vivideru/Goety-3/blob/6c41a04f2d712097c4461f969a6bb8ee277149ef/src/main/java/com/Polarice3/Goety/config/SpellConfig.java#L1630-L1638). `SpellResult` lê `SpellStat.getRange/getRadius/getPotency`, multiplicador de WandUtil e enchantments RANGE/POTENCY. | Custo debitado, segundos, duração real, callbacks de modificação e config do pack **não verificados**. |
| Seleção / alcance | Range base comum 16 na [interface ISpell](https://github.com/Vivideru/Goety-3/blob/6c41a04f2d712097c4461f969a6bb8ee277149ef/src/main/java/com/Polarice3/Goety/api/magic/ISpell.java#L45-L46). `rayTrace` escolhe mira; busca de para-raios em até **128 do ponto de mira**, com prioridade quando `!rightStaff`; senão target de entidade ou bloco. [Lightning L60–94](https://github.com/Vivideru/Goety-3/blob/6c41a04f2d712097c4461f969a6bb8ee277149ef/src/main/java/com/Polarice3/Goety/common/magic/spells/storm/LightningSpell.java#L60-L94). | Raio 128 é procura de POI, **não** alcance de conjuração; nada prova extensão segura de LOS, retarget ou filtragem de aliados. |
| Entidade / dano | `SpellLightningBolt` tem área de impacto AABB local e chama tanto eventos de lightning/`thunderHit` quanto `hurt` sob condições próprias. [Bolt L226–259](https://github.com/Vivideru/Goety-3/blob/6c41a04f2d712097c4461f969a6bb8ee277149ef/src/main/java/com/Polarice3/Goety/common/entities/projectiles/SpellLightningBolt.java#L226-L259). | Aumentar `SpellStat.radius` de aquisição não altera AABB; não duplicar evento, dano ou awards. |
| Mundo / world safety | Bolt pode ativar para-raios, modificar cobre e condicionalmente colocar fogo. [Bolt L188–203, L264–341](https://github.com/Vivideru/Goety-3/blob/6c41a04f2d712097c4461f969a6bb8ee277149ef/src/main/java/com/Polarice3/Goety/common/entities/projectiles/SpellLightningBolt.java#L188-L203). | Não alegar interceptação de efeitos Goety por `WorldEffectPolicy`; claims, gamerules e modpack físico pendentes. |

**Conclusão:** `SOURCE_ADJACENT_311`, `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`. Perks que alterem range, radius, damage, target count, área de impacto ou mundo ficam ⛔ **fail-closed** até inspeção exata 3.1.4 e testes no provider.
