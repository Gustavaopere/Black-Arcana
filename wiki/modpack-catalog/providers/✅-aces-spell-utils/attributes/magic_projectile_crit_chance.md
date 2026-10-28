# magic projectile crit chance — Ace's Spell Utils 1.2.7.2

**ID de atributo:** `aces_spell_utils:magic_projectile_crit_chance` · **Tipo:** `PercentageAttribute` · **Status:** ⚠️ source-pinned / integração física e certificação de perk pendentes.

## Registro e parâmetros

- Default: `0.05`; mínimo do registro: `0`; máximo: `10`; `setSyncable(true)`.
- Registrado em `ASAttributeRegistry` por `DeferredRegister<Attribute>`; adicionado a todos os entity types enumerados em `EntityAttributeModificationEvent`.
- [Fonte do registro e atributos, release pinada](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/registries/ASAttributeRegistry.java#L22-L106).
- Versão do provider: `1.2.7.2-1.21.1`. Artefato da modlist anotado: `aces_spell_utils-1.2.7.2-1.21.1.jar`, SHA-1 `8cbcd535a0b19bef49504c0b5ecafcbcd1cb1cca` (não confrontado com o source/JAR nesta tranche).

## Consumidor, causalidade, targeting e fórmula

**Consumidor do source:** `magicProjectileDamageCriticalStrike · LivingIncomingDamageEvent LOWEST · L546–613`.

Requer atacante `LivingEntity`, `source.getDirectEntity() instanceof AbstractMagicProjectile` **e** `source instanceof SpellDamageSource`; ambos os atributos do par precisam existir. Exige `c>0.05` e `m>1`. Com B=amount na entrada e d=B, usa RNG da vítima em `nextFloat()<=c && m>1`; a cada sucesso faz `c-=1`, `d+=float(B*(m-1))`, `m*=0.85F`; só depois escreve d. Não multiplica o acumulado por m ([admissão](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/events/AcesSpellUtilsServerEvents.java#L548-L575), [loop](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/events/AcesSpellUtilsServerEvents.java#L577-L605)).

Chance não é limitada a 100%: c>=1 garante um teste enquanto m>1, e c local=0 ainda pode passar com RNG exatamente zero. O teto 10 admite até 11 sucessos pelo critério de chance, frequentemente menos por decaimento de m. Não há cooldown ou trava por cast/tick; os atributos não são drenados pelo loop ([loop](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/events/AcesSpellUtilsServerEvents.java#L577-L585)).

**Targeting / geometria:** Dano do projétil mágico de Iron's no evento existente; não cria projétil, altera tamanho, velocidade ou trajetória.

**Custo, cooldown, duração e projétil próprios:** não se trata de spell cast ou de registro de `AbstractSpell`. O atributo não define mana/cooldown/range/duração/projectile size autônomos; essas propriedades, quando aplicáveis, pertencem ao dano/cast/entidade de Iron's e/ou ao consumidor. Não interpretar como valor global de Black Arcana.

**Evidência localizada:** [`AcesSpellUtilsServerEvents.java` L540–613](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/events/AcesSpellUtilsServerEvents.java#L540-L613) · [auditoria causal complementar](../SOURCE-1.2.7.2-COMBAT-CAUSALITY-AND-DOUBLE-SETTLEMENT-20261027.md).

## Limitações, interoperabilidade e QA

Pode coexistir com crítico genérico de spell no mesmo dano; não presumir exclusão/ordem dentro da prioridade LOWEST.

- Ace's Spell Utils controla o consumidor e o registro de atributo. Iron's é autoridade sobre spells e recursos nativos; Black Arcana preserva casting, segurança de mundo, Strain, Corruption e Arcane Danger; RPG Skill Tree fornece apenas progressão por integração comprovada.
- Build pinado do source usa Iron's `1.21.1-3.16.2`; o host físico informado no catálogo está em `3.16.3`. **Paridade binária e assinatura do hook atual: NOT_VERIFIED**.
- **Validação pendente:** confronto com JAR exato instalado, matriz de eventos com dano original/corrente/final, configuração real, side cliente/servidor, competição com atributos/perks de outros mods; `physical_qa=NOT_TESTED` e `mutating_hook=NOT_VERIFIED`.
- Nenhuma alteração de runtime, registro extra, segunda rolagem de proc ou recompensa Mastery foi autorizada por esta ficha.
