# spell res penetration — Ace's Spell Utils 1.2.7.2

**ID de atributo:** `aces_spell_utils:spell_res_penetration` · **Tipo:** `PercentageAttribute` · **Status:** ⚠️ source-pinned / integração física e certificação de perk pendentes.

## Registro e parâmetros

- Default: `0`; mínimo do registro: `0`; máximo: `1`; `setSyncable(true)`.
- Registrado em `ASAttributeRegistry` por `DeferredRegister<Attribute>`; adicionado a todos os entity types enumerados em `EntityAttributeModificationEvent`.
- [Fonte do registro e atributos, release pinada](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/registries/ASAttributeRegistry.java#L22-L106).
- Versão do provider: `1.2.7.2-1.21.1`. Artefato da modlist anotado: `aces_spell_utils-1.2.7.2-1.21.1.jar`, SHA-1 `8cbcd535a0b19bef49504c0b5ecafcbcd1cb1cca` (não confrontado com o source/JAR nesta tranche).

## Consumidor, causalidade, targeting e fórmula

**Consumidor do source:** `spellResPenetrationEvent · SpellDamageEvent · L371–419`.

Requer atacante `LivingEntity`, atributo de penetração >0, `SPELL_RESIST` na vítima com `getValue()>1`, e `SpellDamageSource`. Calcula `baseResist = DamageSources.getResist(victim,school)`, `softcappedResist=2-baseResist`, `penModifier=1+attr`, `damageModifier=2-(penModifier>softcappedResist?1:softcappedResist/penModifier)`; escreve `originalAmount*damageModifier/baseResist` para a posterior multiplicação pelo Iron's.

**Targeting / geometria:** Dano de spell fornecido por Iron's `SpellDamageEvent`, escola e vítima derivadas da fonte; não afeta projétil independentemente da fonte.

**Custo, cooldown, duração e projétil próprios:** não se trata de spell cast ou de registro de `AbstractSpell`. O atributo não define mana/cooldown/range/duração/projectile size autônomos; essas propriedades, quando aplicáveis, pertencem ao dano/cast/entidade de Iron's e/ou ao consumidor. Não interpretar como valor global de Black Arcana.

**Evidência localizada:** [`AcesSpellUtilsServerEvents.java` L366–419](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/events/AcesSpellUtilsServerEvents.java#L366-L419) · [auditoria causal complementar](../SOURCE-1.2.7.2-COMBAT-CAUSALITY-AND-DOUBLE-SETTLEMENT-20261027.md).

## Limitações, interoperabilidade e QA

Fórmula host-sensitive, depende de `getResist` e de como Iron's 3.16.3 aplica resistência; sem garantia de divisor/numerador para todos os hosts.

- Ace's Spell Utils controla o consumidor e o registro de atributo. Iron's é autoridade sobre spells e recursos nativos; Black Arcana preserva casting, segurança de mundo, Strain, Corruption e Arcane Danger; RPG Skill Tree fornece apenas progressão por integração comprovada.
- Build pinado do source usa Iron's `1.21.1-3.16.2`; o host físico informado no catálogo está em `3.16.3`. **Paridade binária e assinatura do hook atual: NOT_VERIFIED**.
- **Validação pendente:** confronto com JAR exato instalado, matriz de eventos com dano original/corrente/final, configuração real, side cliente/servidor, competição com atributos/perks de outros mods; `physical_qa=NOT_TESTED` e `mutating_hook=NOT_VERIFIED`.
- Nenhuma alteração de runtime, registro extra, segunda rolagem de proc ou recompensa Mastery foi autorizada por esta ficha.
