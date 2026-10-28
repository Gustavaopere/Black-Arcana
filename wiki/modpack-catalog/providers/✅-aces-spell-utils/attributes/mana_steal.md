# mana steal — Ace's Spell Utils 1.2.7.2

**ID de atributo:** `aces_spell_utils:mana_steal` · **Tipo:** `MagicPercentAttribute` · **Status:** ⚠️ source-pinned / integração física e certificação de perk pendentes.

## Registro e parâmetros

- Default: `0`; mínimo do registro: `-100`; máximo: `10000`; `setSyncable(true)`.
- Registrado em `ASAttributeRegistry` por `DeferredRegister<Attribute>`; adicionado a todos os entity types enumerados em `EntityAttributeModificationEvent`.
- [Fonte do registro e atributos, release pinada](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/registries/ASAttributeRegistry.java#L22-L106).
- Versão do provider: `1.2.7.2-1.21.1`. Artefato da modlist anotado: `aces_spell_utils-1.2.7.2-1.21.1.jar`, SHA-1 `8cbcd535a0b19bef49504c0b5ecafcbcd1cb1cca` (não confrontado com o source/JAR nesta tranche).

## Consumidor, causalidade, targeting e fórmula

**Consumidor do source:** `manaStealEvent · LivingDamageEvent.Post · L151–218`.

Em `LivingDamageEvent.Post`, exige `source.getEntity()` como `ServerPlayer`, `source.getDirectEntity()!=null`, filtro opcional `mana_steal_whitelist` e valor positivo. Calcula `int(attr * event.getOriginalDamage())`; se a vítima for `ServerPlayer` e `manaStealDrain=true`, retira até a mana disponível na vítima, creditando ao atacante até o máximo. Caso contrário, credita até seu máximo.

Os defaults globais de `manaStealDrain` e `manaStealWhitelist` são **true**; o segundo vem da chave textual `Mana Steal entity blacklist`, mas implementa uma whitelist ([config](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/utils/AcesSpellUtilsConfig.java#L13-L16), [whitelist](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/utils/AcesSpellUtilsConfig.java#L33-L52)). Com ela ativa, a entidade direta precisa ser o próprio atacante ou ter tipo na tag; o [JSON default](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/resources/data/aces_spell_utils/tags/entity_type/mana_steal_whitelist.json#L1-L8) contém `irons_spellbooks:magic_missile`, `firebolt` e `icicle`, com `replace=false`. São tipos de entidade, não IDs de spell ou lista de vítimas ([gate](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/events/AcesSpellUtilsServerEvents.java#L156-L171)).

Mana atual e máxima de atacante/vítima são convertidas a int antes das contas, e o atributo a float. Não há mínimo de 1 ou acúmulo de frações; mesmo potencial zero pode chamar o setter com o snapshot inteiro. Na drenagem, máxima da vítima <=0 encerra sem ganho alternativo. A retirada `S=min(potencial,manaVítima)` ignora o espaço livre do atacante; só depois limita o crédito a seu máximo: atacante 99/100, vítima 10 e S=3 solicitam vítima 7 e atacante 100. Portanto não é transferência conservativa, e o source não relê o resultado do primeiro `setMana` antes de creditar o segundo ([snapshots e duas escritas](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/events/AcesSpellUtilsServerEvents.java#L173-L212)).

**Targeting / geometria:** Atacante player, alvo do dano; não é raycast/AOE/projétil novo. O `getDirectEntity` pode ser diferente de `getEntity`.

**Custo, cooldown, duração e projétil próprios:** não se trata de spell cast ou de registro de `AbstractSpell`. O atributo não define mana/cooldown/range/duração/projectile size autônomos; essas propriedades, quando aplicáveis, pertencem ao dano/cast/entidade de Iron's e/ou ao consumidor. Não interpretar como valor global de Black Arcana.

**Evidência localizada:** [`AcesSpellUtilsServerEvents.java` L145–219](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/events/AcesSpellUtilsServerEvents.java#L145-L219) · [auditoria causal complementar](../SOURCE-1.2.7.2-COMBAT-CAUSALITY-AND-DOUBLE-SETTLEMENT-20261027.md).

## Limitações, interoperabilidade e QA

O fluxo sincroniza `victimMagicData` para o atacante no ramo de drenagem, sem `sendToPlayer(victim,...)` explícito neste handler; avaliar UI da vítima. Dano original não é dano efetivo liquidado.

- Ace's Spell Utils controla o consumidor e o registro de atributo. Iron's é autoridade sobre spells e recursos nativos; Black Arcana preserva casting, segurança de mundo, Strain, Corruption e Arcane Danger; RPG Skill Tree fornece apenas progressão por integração comprovada.
- Build pinado do source usa Iron's `1.21.1-3.16.2`; o host físico informado no catálogo está em `3.16.3`. **Paridade binária e assinatura do hook atual: NOT_VERIFIED**.
- **Validação pendente:** confronto com JAR exato instalado, matriz de eventos com dano original/corrente/final, configuração real, side cliente/servidor, competição com atributos/perks de outros mods; `physical_qa=NOT_TESTED` e `mutating_hook=NOT_VERIFIED`.
- Nenhuma alteração de runtime, registro extra, segunda rolagem de proc ou recompensa Mastery foi autorizada por esta ficha.
