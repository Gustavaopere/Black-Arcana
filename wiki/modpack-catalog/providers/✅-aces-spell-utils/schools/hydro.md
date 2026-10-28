# Escola Hydro — Ace's Spell Utils 1.2.7.2

**SchoolType ResourceLocation:** `aces_spell_utils:hydro` · **Status:** ⚠️ registro source-pinned, host e JAR instalado não homologados.

## Identidade e registro

O [`ASSchoolRegistry`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/registries/ASSchoolRegistry.java) registra via `DeferredRegister<SchoolType>` a escola `aces_spell_utils:hydro` com os seguintes argumentos, observados no registro real:

- **Constante Java:** `ABYSSAL` — nome legado ABYSSAL, **não** ID `abyssal`.
- **Item tag de foco:** `aces_spell_utils:hydro_focus` — [`ASTags.HYDRO_FOCUS`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/utils/ASTags.java).
- **Localization key:** `school.aces_spell_utils.hydro`; display style `#36156c`. 
- **Atributo spell power:** `aces_spell_utils:hydro_spell_power` — [ficha](../attributes/hydro_spell_power.md).
- **Atributo magic resistance:** `aces_spell_utils:hydro_magic_resist` — [ficha](../attributes/hydro_magic_resist.md).
- **Som de cast:** `SoundRegistry.EVOCATION_CAST` do Iron's.
- **DamageType key:** `aces_spell_utils:hydro_magic` — [`ASDamageTypes.HYDRO_MAGIC`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/registries/ASDamageTypes.java).
- **Registro inicial:** construtor de `AcesSpellUtils` chama `ASSchoolRegistry.register(modEventBus)`; nenhuma identidade de spell registrada nesta classe.

## Contrato de uso e limites para perks

**O que a escola faz:** oferece identidade de escola, foco, atributos, som e tipo de dano para feitiços que *outros providers* optem por registrar usando este `SchoolType`. Esse registro **não cria** um cast, projétil, ritual, custo, dano ou poder individual.

**Target/range/tamanho/área/duração/cooldown/mana:** não determinados pela escola; pertencem aos feitiços concretos no Iron's e ao seu provider. Não associar defaults de custos ou scaling sem identificar o consumidor real.

**Interoperabilidade:** Black Arcana conserva seu próprio runtime, hazards e políticas; Iron's controla cast e seleção de SpellType; RPG Skill Tree fornece atributos, progressão ou gates apenas por interfaces verificadas. A criação de escola não concede Mastery e não autoriza adapter mutador.

## Evidência e validação

- Source pin da release: [`AceTheEldritchKing/Aces_Spell_Utils@a0b2f4c2fcfa938c8e47239279c77c2ef82647ac`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/commit/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac), `mod_version=1.2.7.2-1.21.1`.
- JAR físico **anotado** na modlist: `aces_spell_utils-1.2.7.2-1.21.1.jar`, SHA-1 `8cbcd535a0b19bef49504c0b5ecafcbcd1cb1cca`; não aberto para confirmar bytecode.
- Source declara Iron's build dependency `3.16.2`; pack tem `3.16.3`, portanto assinatura/compilação/registro de `SchoolType` no conjunto instalado: **NOT_VERIFIED**.
- **QA pendente:** Registry sync/load, efetividade do focus tag, resolução de damage type, spell producer de outro provider e balanceamento de poder/resistência com a versão exata do host. `physical_qa=NOT_TESTED`; `mutating_hook=NOT_VERIFIED`.
