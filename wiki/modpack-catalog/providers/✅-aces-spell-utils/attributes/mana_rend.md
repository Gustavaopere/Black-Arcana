# mana rend — Ace's Spell Utils 1.2.7.2

**ID de atributo:** `aces_spell_utils:mana_rend` · **Tipo:** `MagicPercentAttribute` · **Status:** ⚠️ source-pinned / integração física e certificação de perk pendentes.

## Registro e parâmetros

- Default: `0`; mínimo do registro: `-100`; máximo: `100`; `setSyncable(true)`.
- Registrado em `ASAttributeRegistry` por `DeferredRegister<Attribute>`; adicionado a todos os entity types enumerados em `EntityAttributeModificationEvent`.
- [Fonte do registro e atributos, release pinada](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/registries/ASAttributeRegistry.java#L22-L106).
- Versão do provider: `1.2.7.2-1.21.1`. Artefato da modlist anotado: `aces_spell_utils-1.2.7.2-1.21.1.jar`, SHA-1 `8cbcd535a0b19bef49504c0b5ecafcbcd1cb1cca` (não confrontado com o source/JAR nesta tranche).

## Consumidor, causalidade, targeting e fórmula

**Consumidor do source:** `manaRendEvent · LivingIncomingDamageEvent · L228–273`.

Requer `source.getEntity()` como `LivingEntity`, directEntity presente e whitelist opcional. Exige atributo >0, mana máxima da vítima >0 e multiplica `event.getAmount()` por `1 + attr*(victimMaxMana-victimBaseMana)/1000`.

**Targeting / geometria:** Entidade vivente atacante, vítima atual de `LivingIncomingDamageEvent`; afeta valor de um ataque existente, sem novo dano/projétil/AOE.

**Custo, cooldown, duração e projétil próprios:** não se trata de spell cast ou de registro de `AbstractSpell`. O atributo não define mana/cooldown/range/duração/projectile size autônomos; essas propriedades, quando aplicáveis, pertencem ao dano/cast/entidade de Iron's e/ou ao consumidor. Não interpretar como valor global de Black Arcana.

**Evidência localizada:** [`AcesSpellUtilsServerEvents.java` L222–273](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/events/AcesSpellUtilsServerEvents.java#L222-L273) · [auditoria causal complementar](../SOURCE-1.2.7.2-COMBAT-CAUSALITY-AND-DOUBLE-SETTLEMENT-20261027.md).

## Limitações, interoperabilidade e QA

`victimMaxMana-victimBaseMana` não é garantidamente positivo; mutação do amount não prova HP perdido. Config se chama `Mana Rend entity blacklist` mas implementa `manaRendWhitelist`.

- Ace's Spell Utils controla o consumidor e o registro de atributo. Iron's é autoridade sobre spells e recursos nativos; Black Arcana preserva casting, segurança de mundo, Strain, Corruption e Arcane Danger; RPG Skill Tree fornece apenas progressão por integração comprovada.
- Build pinado do source usa Iron's `1.21.1-3.16.2`; o host físico informado no catálogo está em `3.16.3`. **Paridade binária e assinatura do hook atual: NOT_VERIFIED**.
- **Validação pendente:** confronto com JAR exato instalado, matriz de eventos com dano original/corrente/final, configuração real, side cliente/servidor, competição com atributos/perks de outros mods; `physical_qa=NOT_TESTED` e `mutating_hook=NOT_VERIFIED`.
- Nenhuma alteração de runtime, registro extra, segunda rolagem de proc ou recompensa Mastery foi autorizada por esta ficha.
