# Goety 3.1.4 — `soul_bolt_focus`

Status: **✅ CATALOGADO / COUNTED_EXACT** · identificador factual obtido da auditoria do **JAR 3.1.4 hash-matched** · **⚠️ funcionamento físico/números não validados nesta etapa**.

## Identidade canônica

- **Provider:** Goety (mod id `goety`).
- **JAR instalado e auditado:** `goety-3.1.4.jar` (NeoForge/Minecraft 1.21.1); SHA-1 `a0770e180e4e8b1b87d8fa9c8356e9dbf34d82a7`.
- **Identidade de Focus no artefato:** `soul_bolt_focus` — item/ação de Focus ativo do conjunto exato de 123. Não é o `empty_focus` proxy.
- **Posição no inventário exato:** 93/123. Número ordinal editorial, não identificador de registry ou ordem de carregamento.
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

## Dossiê de engenharia causal — Soul Bolt (26/10/2026)

**Evidência separada por versão.** A identidade `soul_bolt_focus` e a aquisição constam da auditoria SHA-exata do **JAR Goety 3.1.4** acima. Todos os métodos, defaults e efeitos detalhados a seguir foram auditados somente no source público **Goety 3.1.1**, fixado em [Vivideru/Goety-3@6c41a04f2d712097c4461f969a6bb8ee277149ef](https://github.com/Vivideru/Goety-3/commit/6c41a04f2d712097c4461f969a6bb8ee277149ef). **Não há prova de equivalência de classfile, config instalada, ABI mutadora ou comportamento físico de 3.1.4.** Grau: `SOURCE_ADJACENT_311`; `mutating_hook=NOT_VERIFIED`; `physical_qa=NOT_TESTED`.

**Resumo do comportamento da fonte 3.1.1:** dispara um projétil alinhado ao vetor visual do conjurador. A escolha de staff/equipamento pode convertê-lo em Poison Bolt, Wither Bolt ou Necro Bolt, que possuem efeitos e custos downstream distintos. A seleção não registra quatro novos Focuses.

### Código localizável (source 3.1.1; nenhum contrato de 3.1.4 inferido)

- [`ModItems.SOUL_BOLT_FOCUS`](https://github.com/Vivideru/Goety-3/blob/6c41a04f2d712097c4461f969a6bb8ee277149ef/src/main/java/com/Polarice3/Goety/common/items/ModItems.java#L301) registra `new MagicFocus(new SoulBoltSpell())` na versão adjacente; a identidade do item 3.1.4 possui prova independente.
- [`SoulBoltSpell`](https://github.com/Vivideru/Goety-3/blob/6c41a04f2d712097c4461f969a6bb8ee277149ef/src/main/java/com/Polarice3/Goety/common/magic/spells/SoulBoltSpell.java): `defaultSoulCost`, `defaultCastDuration`, `defaultSpellCooldown`, `acceptedEnchantments` e `SpellResult(ServerLevel,LivingEntity,ItemStack,SpellStat)`.
- [`SpellConfig.java` linhas 1028–1043](https://github.com/Vivideru/Goety-3/blob/6c41a04f2d712097c4461f969a6bb8ee277149ef/src/main/java/com/Polarice3/Goety/config/SpellConfig.java#L1028-L1043): defaults source 3.1.1 de **Soul Bolt** `cost=4`, `cast duration=0`, `cooldown=20`, `base damage=4.0`; damage defaults alternativos `PoisonBoltDamage=3.0`, `WitherBoltDamage=4.0`, `NecroBoltDamage=12.0`. São definições de config, **não** custo/dano líquido ou valores ativos no mundo.
- [`SpellHurtingProjectile`](https://github.com/Vivideru/Goety-3/blob/6c41a04f2d712097c4461f969a6bb8ee277149ef/src/main/java/com/Polarice3/Goety/common/entities/projectiles/SpellHurtingProjectile.java): estado `DATA_EXTRA_DAMAGE`, `boltSpeed`, persistência `BoltSpeed/ExtraDamage`, `setBoltSpeed(int)` e filtro `canHitEntity`.
- Entidades downstream: [`SoulBolt`](https://github.com/Vivideru/Goety-3/blob/6c41a04f2d712097c4461f969a6bb8ee277149ef/src/main/java/com/Polarice3/Goety/common/entities/projectiles/SoulBolt.java), [`PoisonBolt`](https://github.com/Vivideru/Goety-3/blob/6c41a04f2d712097c4461f969a6bb8ee277149ef/src/main/java/com/Polarice3/Goety/common/entities/projectiles/PoisonBolt.java), [`WitherBolt`](https://github.com/Vivideru/Goety-3/blob/6c41a04f2d712097c4461f969a6bb8ee277149ef/src/main/java/com/Polarice3/Goety/common/entities/projectiles/WitherBolt.java) e [`NecroBolt`](https://github.com/Vivideru/Goety-3/blob/6c41a04f2d712097c4461f969a6bb8ee277149ef/src/main/java/com/Polarice3/Goety/common/entities/projectiles/NecroBolt.java).

### Matriz de parâmetros útil para perks

| Eixo | Cadeia causal documentada em 3.1.1 | Limite e viabilidade em 3.1.4 |
|---|---|---|
| Custo / timing | Métodos default leem `SoulBoltCost/Duration/CoolDown` (config defaults 4/0/20); o `SpellResult` é executado no servidor segundo a classe base `Spell`. | Unidade/ciclo de débito/refund real **NÃO VERIFICADOS**; não aplicar desconto por evento presumido. |
| Escolha de variante | Ordem observada: staff do tipo `WILD` → `PoisonBolt`; senão `NETHER` **e** Nether Set → `WitherBolt`; senão `NAMELESS_STAFF` → `NecroBolt`; senão `SoulBolt`. | Ordem é do source 3.1.1; não supor que as condições sejam simultâneas, intercambiáveis ou modificáveis por perk 3.1.4. |
| Alvo / alcance / área | `SpellResult` parte de `caster.getViewVector` e cria **uma** entidade `SpellHurtingProjectile`; a colisão e o filtro de allies/owner/projectiles ficam no objeto downstream. | Raycast de seleção, alcance terminal, LOS de impacto, hitbox, área, PvP e máximo de alvos **NÃO VERIFICADOS**; não converter automaticamente em AOE. |
| Dano e tipo | `SoulBolt.onHitEntity` usa `indirectMagic` quando há dono vivo, com `config SoulBoltDamage × WandUtil.damageMultiply`, possível substituição por atributo `ATTACK_DAMAGE` do dono `Mob`, mais `extraDamage`. Se sem dono `LivingEntity`, usa outro ramo `magic`. `PoisonBolt/WitherBolt/NecroBolt` têm consumidores próprios. | Atributo/configuração são entradas nominais de source, não dano realizado, elemento único ou garantia para 3.1.4. |
| Potency | `POTENCY` do `SpellStat` recebe bônus do Focus encantado e é enviado a `setExtraDamage(potency)`. | Não há prova de cap por jogador nem hook antes da colisão. |
| Velocidade | `VELOCITY` do `SpellStat` recebe níveis de encantamento; há truncamento `(int)velocity` antes de `setBoltSpeed`, que **soma** `increase/50.0f` ao `boltSpeed`. Base `getInertia=0.82f+boltSpeed`, mas subclasses podem sobrescrever. | Não equivale a blocos/tick, velocidade absoluta, dimensão do projétil ou API pública para perk. Mudança de trajetória exige contrato e medição. |
| Status / efeitos | `PoisonBolt` aplica, após `hurt` aceito, `POISON` ou `ACID_VENOM` conforme robe; `WitherBolt` pode aplicar `WITHER` e criar explosão; `NecroBolt` e `SoulBolt` sob condição necro podem realizar conversões de mobs **após morte confirmada na rotina**. | Duration/elegibilidade/dano de explosão são dos respectivos consumidores, não um segundo cast; details físicos de 3.1.4 pendentes. |
| Descarte e persistência | `SoulBolt/PoisonBolt` descartam após `secondsToTicks(10)` no tick; `NecroBolt` tem limite de `secondsToTicks(20)` nessa versão. `SpellHurtingProjectile` grava `BoltSpeed` e `ExtraDamage`. | Lifetime e save do source; não assumir mesmo tempo para `WitherBolt`, cliente real ou JAR atual sem prova específica. |

### Fronteiras causais e integração

O fluxo observado é **um** Focus → **uma** entidade variante → resultado de colisão (dano, debuff, explosão ou possível transformação pós-morte). Esses efeitos derivados não são novas conjurações. Uma futura Mastery do RPG Skill Tree deve ter autoria do cast ou efeito final verificada no servidor, IDs de correlação e regra de crédito única; não somar prêmio por projeção, partículas, dano e conversão de forma independente. Conversão também pertence ao lifecycle de servants do Goety.

**Matriz de mutabilidade:** A — config e `SpellStat` internos observados somente em 3.1.1, sem prova de override 3.1.4; B — eventos/API públicos de mutação **NÃO VERIFICADOS**; C — adapter de observação somente após QA/ABI; D — `range`, `target`, `projectile size`, `velocity`, `damage source`, quantidade de projéteis, cooldown e conversão **⛔ FAIL-CLOSED** para alteração per-player sem hook seguro. Black Arcana não assume Soul Energy nem converte efeitos Goety em Corruption/Strain.

**Próximos testes:** confrontar registro/classe e quatro entidades no **JAR 3.1.4 SHA-exato**, dados configurados e linha de débito, colisão sob staff e robes incompatíveis, LOS/claims/friendly-fire, truncamento de velocidade, efeitos após hit rejeitado e morte, owner/persistência e teste in-game/Survival. **Certificado perk-ready: ainda não; índices ficam inalterados.**
