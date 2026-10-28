# magic damage crit damage — Ace's Spell Utils 1.2.7.2

**ID de atributo:** `aces_spell_utils:magic_damage_crit_damage` · **Tipo:** `PercentageAttribute` · **Status:** ⚠️ source-pinned / integração física e certificação de perk pendentes.

## Registro e parâmetros

- Default: `1.5`; mínimo do registro: `1`; máximo: `100`; `setSyncable(true)`.
- Registrado em `ASAttributeRegistry` por `DeferredRegister<Attribute>`; adicionado a todos os entity types enumerados em `EntityAttributeModificationEvent`.
- [Fonte do registro e atributos, release pinada](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/registries/ASAttributeRegistry.java#L22-L106).
- Versão do provider: `1.2.7.2-1.21.1`. Artefato da modlist anotado: `aces_spell_utils-1.2.7.2-1.21.1.jar`, SHA-1 `8cbcd535a0b19bef49504c0b5ecafcbcd1cb1cca` (não confrontado com o source/JAR nesta tranche).

## Consumidor, causalidade, targeting e fórmula

**Consumidor do source:** `magicDamageCriticalStrike · LivingIncomingDamageEvent LOWEST · L469–536`.

Modificador de dano crítico para spell `SpellDamageSource`, compartilhado com `magic_damage_crit_chance`. Loop inicializa `damage = event.getAmount()`, e a cada sucesso soma `event.getAmount()*(critDamage-1)`, depois `critDamage *= 0.85`.

Para n sucessos, antes dos arredondamentos float, o fator sobre o amount B de entrada é `1+Σ(i=0..n-1)(m0*(0.85F)^i-1)`. Com m0=1.5, as três primeiras parcelas são aproximadamente `.5`, `.275`, `.08375`: se a chance permitir os três sucessos, solicita `1.85875*B`; o multiplicador então cai abaixo de 1 e encerra novas parcelas. Não é `1.5^n`. O par precisa existir, com `c>0.05` e `m>1`; ver [chance e RNG](magic_damage_crit_chance.md) e [gates/loop](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/events/AcesSpellUtilsServerEvents.java#L477-L508).

**Targeting / geometria:** Mesmo dano/evento do spell; não cria novo ataque. Só tem efeito quando a chance supera o threshold de `0.05`.

**Custo, cooldown, duração e projétil próprios:** não se trata de spell cast ou de registro de `AbstractSpell`. O atributo não define mana/cooldown/range/duração/projectile size autônomos; essas propriedades, quando aplicáveis, pertencem ao dano/cast/entidade de Iron's e/ou ao consumidor. Não interpretar como valor global de Black Arcana.

**Evidência localizada:** [`AcesSpellUtilsServerEvents.java` L464–536](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/events/AcesSpellUtilsServerEvents.java#L464-L536) · [auditoria causal complementar](../SOURCE-1.2.7.2-COMBAT-CAUSALITY-AND-DOUBLE-SETTLEMENT-20261027.md).

## Limitações, interoperabilidade e QA

O default multiplier `1.5` não significa 50% de dano extra em todo evento; precisa ocorrer proc e o valor é consumido pelo algoritmo com iterações sucessivas.

- Ace's Spell Utils controla o consumidor e o registro de atributo. Iron's é autoridade sobre spells e recursos nativos; Black Arcana preserva casting, segurança de mundo, Strain, Corruption e Arcane Danger; RPG Skill Tree fornece apenas progressão por integração comprovada.
- Build pinado do source usa Iron's `1.21.1-3.16.2`; o host físico informado no catálogo está em `3.16.3`. **Paridade binária e assinatura do hook atual: NOT_VERIFIED**.
- **Validação pendente:** confronto com JAR exato instalado, matriz de eventos com dano original/corrente/final, configuração real, side cliente/servidor, competição com atributos/perks de outros mods; `physical_qa=NOT_TESTED` e `mutating_hook=NOT_VERIFIED`.
- Nenhuma alteração de runtime, registro extra, segunda rolagem de proc ou recompensa Mastery foi autorizada por esta ficha.
