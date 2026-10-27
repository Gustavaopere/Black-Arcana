# Goety 3.1.4 — `leeching_focus`

Status: **✅ CATALOGADO / COUNTED_EXACT** · identificador factual obtido da auditoria do **JAR 3.1.4 hash-matched** · **⚠️ funcionamento físico/números não validados nesta etapa**.

## Identidade canônica

- **Provider:** Goety (mod id `goety`).
- **JAR instalado e auditado:** `goety-3.1.4.jar` (NeoForge/Minecraft 1.21.1); SHA-1 `a0770e180e4e8b1b87d8fa9c8356e9dbf34d82a7`.
- **Identidade de Focus no artefato:** `leeching_focus` — item/ação de Focus ativo do conjunto exato de 123. Não é o `empty_focus` proxy.
- **Posição no inventário exato:** 61/123. Número ordinal editorial, não identificador de registry ou ordem de carregamento.
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

## Auditoria complementar — canalização, dano e cura não comprovada (27/10/2026)

**Escopo estrito:** identidade `leeching_focus` provada no JAR **3.1.4** hash-matched; semântica exclusivamente da [fonte pública Goety 3.1.1](https://github.com/Vivideru/Goety-3/blob/6c41a04f2d712097c4461f969a6bb8ee277149ef/src/main/java/com/Polarice3/Goety/common/magic/spells/necromancy/LeechingSpell.java), commit `6c41a04f2d712097c4461f969a6bb8ee277149ef`. Nenhuma equivalência de classes/métodos com o binário instalado ou QA físico foi demonstrada. Relatório transversal: [Lightning/Leeching — causalidade e world safety](../SOURCE-ADJACENT-LIGHTNING-LEECHING-3.1.1-20261027.md).

| Eixo | Consumidor observado na fonte 3.1.1 | Limite para perks |
|---|---|---|
| Custos / canais de tempo | [SpellConfig L844–856](https://github.com/Vivideru/Goety-3/blob/6c41a04f2d712097c4461f969a6bb8ee277149ef/src/main/java/com/Polarice3/Goety/config/SpellConfig.java#L844-L856): defaults `leechingCost=8`, `leechingChargeUp=0`, `leechingTime=0`, `leechingCoolDown=0`, `leechingPercent=100` e `leechingDamage=1.0`. `LeechingSpell` herda `EverChargeSpell`, `shotsNumber()` usa `leechingTime`, e `defaultSpellCooldown()` lê config, enquanto `EverChargeSpell.Cooldown()=0`. | Sem prova do controlador de canalização, não inferir ticks de `SpellResult`, Soul por segundo, heal percentual, custo final ou cooldown efetivo. |
| Target / range | `defaultStats().setRange(8)`; `getTarget(caster,range)` usa raytrace para player (raio de seleção 3) ou alvo de Mob. [Spell L95–104](https://github.com/Vivideru/Goety-3/blob/6c41a04f2d712097c4461f969a6bb8ee277149ef/src/main/java/com/Polarice3/Goety/common/magic/Spell.java#L95-L104). | Single target no `SpellResult`; multi-target, AoE, range per-player ou LOS customizado sem hook homologado. |
| Dano / fraqueza | [Leeching L75–99](https://github.com/Vivideru/Goety-3/blob/6c41a04f2d712097c4461f969a6bb8ee277149ef/src/main/java/com/Polarice3/Goety/common/magic/spells/necromancy/LeechingSpell.java#L75-L99): `potency` considera multiplicador/enchantment e `SpellStat`; `hurt(lifeLeech,...)` no alvo; apenas após `hurt == true`, `rightStaff` aplica Weakness 60 ticks, amplificador 0. | Não criar segundo dano, nem aplicar Weakness se o dano foi negado. Dano exato e duração efetiva no pack não verificados. |
| Cura / DamageType | `ModDamageSource.lifeLeech` resolve fonte `LIFE_LEECH`; `LeechingSpell.SpellResult` **não chama `heal`**. [ModDamageSource L260–266](https://github.com/Vivideru/Goety-3/blob/6c41a04f2d712097c4461f969a6bb8ee277149ef/src/main/java/com/Polarice3/Goety/utils/ModDamageSource.java#L260-L266). | A eventual transferência de vida e uso de `leechingPercent` dependem de consumidor não rastreado; cura e modificador de perk ficam ⛔ bloqueados. |

**Conclusão:** `SOURCE_ADJACENT_311`, `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`. O 0/361 perk-ready do Goety não muda com este aprofundamento.
