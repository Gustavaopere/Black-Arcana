# technomancy magic resist — Ace's Spell Utils 1.2.7.2

**Attribute ID:** `aces_spell_utils:technomancy_magic_resist` · **família:** escola `aces_spell_utils:technomancy` · **status:** ⚠️ source-pinned, host/JAR runtime QA e perk-ready não homologados.

## Registro, parâmetros e autoridade

- [`ASAttributeRegistry.TECHNOMANCY_MAGIC_RESIST`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/registries/ASAttributeRegistry.java#L66-L105) registra `technomancy_magic_resist` via `registerResistanceAttribute("technomancy")`.
- Tipo: `MagicPercentAttribute` (Iron's API); default **`1.0`**, mínimo **`-100`**, máximo **`100`**, `setSyncable(true)`.
- `ASAttributeRegistry.modifyEntityAttributes` adiciona as 19 entradas registradas a todos os `EntityType` enumerados pelo evento, sem provar que toda entidade possa lançar spells.
- O [`ASSchoolRegistry.TECHNOMANCY`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/registries/ASSchoolRegistry.java) referencia diretamente o holder `ASAttributeRegistry.TECHNOMANCY_MAGIC_RESIST` na definição de `aces_spell_utils:technomancy`.

## Consumidor, efeito, targeting e geometria

Este registro participa da descrição de `SchoolType`: valor de resistência da escola acessado por consumidores Iron's que conheçam o SchoolType. Não possui consumidor independente em Ace que registre uma magia ou dispare dano, cura ou outro efeito por conta própria. A maneira exata pela qual Iron's 3.16.3 aplica potência/resistência exige leitura e teste do host atual.

**Targeting:** atributo da entidade que participa da resolução da escola; target, projétil, distância, área e seleção do alvo são definidos pelo consumidor Iron's e pela magia real de outro provider. **Não** assumir que a escola ou o atributo criam novo feitiço.

**Custo, duração, cooldown, escola e recursos:** sem custo de mana, duração ou cooldown nativo deste registro; escalas de spell/cast continuam sob Iron's. Família `aces_spell_utils:technomancy` e damage key `aces_spell_utils:technomancy_magic` não são um registro Black Arcana.

## Contrato para perks e limites

- Progressão do RPG Skill Tree poderia modificar um atributo sob contrato de versão real; não inserir segunda lógica de cálculo nem tomar posse do damage-source/casting do Iron's.
- Fonte exata [`AceTheEldritchKing/Aces_Spell_Utils@a0b2f4c2fcfa938c8e47239279c77c2ef82647ac`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/commit/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac), versão source `1.2.7.2-1.21.1`; JAR catalogado SHA-1 `8cbcd535a0b19bef49504c0b5ecafcbcd1cb1cca` **sem paridade binária confirmada nesta tranche**.
- Build upstream vincula Iron's `3.16.2`; modpack informa `3.16.3`. `mutating_hook=NOT_VERIFIED`; `physical_qa=NOT_TESTED`.
- **QA:** assinatura do `SchoolType`, agregação de atributo no Iron's 3.16.3, efeitos de amplificação/resistência, sincronização, escala, teto e compatibilidade com outros atributos do modpack.
