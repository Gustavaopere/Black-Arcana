# Restoration

Status: `SOURCE-PINNED 5.13.1 / HEALING-CURE RITUAL`

- Registry id: `ars_nouveau:ritual_restoration`
- Class: `RitualHealing`
- Source cost declaration: `200`
- Processing cadence: every `100` game ticks
- Radius: `5` blocks
- Exact release checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`

## Provider-native behavior

Every 100 ticks, Restoration scans LivingEntities in radius 5 and selects the first nearby player, if any, for Zombie Villager cure attribution.

For each entity:

- `ZombieVillager`: starts conversion immediately (`conversion time = 0`) using the nearby player's UUID when available;
- inverted heal/harm entities: receive `10.0` damage from an Ars fake-player attack source;
- other damaged living entities: heal `10.0` health.

If at least one eligible operation occurs, the ritual marks the work cycle as needing Source.

The provider description notes that cured villagers can grant discounts when a player was nearby; the exact discount semantics remain vanilla/provider conversion behavior rather than a separate Black Arcana reward.

## Authority / Black Arcana boundary

Healing, undead harm, villager conversion attribution and Source settlement remain Ars Nouveau/vanilla authority. Black Arcana must not replay healing/damage or create a second cure/reputation credit.

## QA

Source behavior is pinned to 5.13.1. Effective Source debit timing and interactions with altered villager curing/undead tags in the full pack remain runtime QA.

## Engenharia para perks — execução do ritual

- **Source pin:** [`RitualHealing.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/ritual/RitualHealing.java), versão Ars Nouveau 5.13.1.
- **Frequência/targets:** `RitualHealing.tick()` a cada `100` game ticks usa AABB `inflate(5)` e `LivingEntity`, procurando primeiro `Player` na lista para possível UUID de atribuição de cura.
- **Três destinos:** `ZombieVillager.startConverting(optionalPlayerUUID,0)` diretamente; para `isInvertedHealAndHarm`, `hurt(...playerAttack(ANFakePlayer),10.0f)`; para outros danificados, `heal(10.0f)`. Marca `didWorkOnce` e `setNeedsSource(true)` quando algo foi processado. O dano a entidades inverted é playerAttack fake, **não** magic damage de Ars glyph Heal.
- **Custos/perks:** `getSourceCost()=200` no source; débito efetivo pelo contexto Ritual requer validação. Cure credit/reputation, XP e life-steal não devem ser atribuídos como ataque/cast independente por sinais indiretos.
- **Status:** ✅ código fonte exato; ⚠️ configurações e comportamento físico dos providers adicionais pendentes; ⛔ mutabilidade em ritual ou integração com Mastery não é provada pelos eventos de glyph. Ritual runtime permanece Ars Nouveau.

## Certificação técnica estática de ritual — segundo lote (25/10/2026)

**✅ `STATIC_TECHNICAL_CATALOG_ONLY` — contrato estático completo da ficha; ⛔ `mutating_hook=NOT_VERIFIED`; ⚠️ `physical_qa=NOT_TESTED`.** Prova não cobre hook seguro, config implantada nem aceitação do modpack.

| Campo de perk | Evidência estática no provider |
|---|---|
| Identidade e release | `ars_nouveau:ritual_restoration`; `RitualHealing`; Ars Nouveau 5.13.1. [Source imutável](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/ritual/RitualHealing.java) e [registry exato do publisher](../EXACT-BINARY-GLYPH-RITUAL-IDS-5.13.1.md). |
| Execução, ramificações e settlement | Em servidor a cada `gameTime%100==0`, captura `LivingEntity` em `AABB(brazier).inflate(5)`, escolhe o **primeiro Player na lista** para UUID de conversão, depois: `ZombieVillager.startConverting(optionalPlayerUUID,0)` e continua; entidade com `isInvertedHealAndHarm()` usa `ANFakePlayer.getPlayer(ServerLevel)` e `hurt(DamageSources.playerAttack(fakePlayer),10.0f)`; demais entidades com saúde abaixo de máximo recebem `heal(10.0f)`. `didWorkOnce` é marcado por ramo admitido e, ao final, `setNeedsSource(true)`; **não** se verifica o retorno de `hurt`, portanto não concluir dano realmente aplicado. |
| Fórmulas, parâmetros, limites e caps | Cadência `100 game ticks`, volume `AABB.inflate(5)` sobre `LivingEntity`, `10.0f` de dano fake-player ou heal, tempo da conversão `0` no chamado a `startConverting`. Ordem: `ZombieVillager` antes de `isInvertedHealAndHarm`; First Player da lista para UUID não é necessariamente o caster nem há critério de proximidade adicional dentro da AABB. |
| Targeting, área/volume, duração, dano e projétil | Zombie Villager converte com atribuição optional UUID, undead/inverted recebe `playerAttack` de fake-player, outras entidades feridas recebem heal; **DamageType não é `MAGIC` de spell Heal**. Não há distância de projétil, duração de debuff, raycast, efeito de mana glyph ou alvo de Form. Discount/reputation no Minecraft downstream requer QA. |
| Resource cost, cooldown, receita/admissão | `getSourceCost()=200 Source`. `setNeedsSource(true)` **uma vez por ciclo com tentativa elegível**, não uma vez por entidade, e sem provar débito final ou success de dano/reputação. Não modelar 200 Source por hit nem per-cure XP. Custo de magia `SpellResolver` de Form/Effect é N/A neste ritual. |
| Política de mundo e integração entre projetos | Não duplicar cura, dano, conversão de villager, descontos, assassinato atribuído a fake-player ou XP/Mastery por sinais secundários. Provider Ars e vanilla são authority das alterações; não assumir que o helper de mundo do Black Arcana filtra automaticamente essas chamadas. Autoridade de execução e fonte/Source pertence ao Ars; RPG Skill Tree fornece progressão/atributos/Mastery/gates mediante contrato real, Black Arcana detém seu runtime/rituais e WorldEffectPolicy para suas mutações próprias, sem interceptar automaticamente este ritual. |
| Grau de evidência/QA | `PINNED_SOURCE_PLUS_SHA_EXACT_BINARY_IDENTITY`: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157` para métodos e publisher `ars_nouveau-1.21.1-5.13.1.jar` SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd` para **ID/classe registrada**. Não foi comprovada equivalência byte-a-byte dos métodos, configuração atual, side/claims reais, multiplayer ou QA físico. |

**Gate fail-closed:** alteração de geometria, itens, persistência, energia/Source ou consumer exige hook real, orçamento, transação e deduplicação provados; o ✅ é documental, não implementação de perk ou promoção de Stage 06.05/09.
