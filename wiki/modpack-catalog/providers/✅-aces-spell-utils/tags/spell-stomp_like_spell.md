# stomp_like_spell — Ace's Spell Utils 1.2.7.2

**Registry associado:** `Iron's SpellRegistry` · **tag:** `aces_spell_utils:stomp_like_spell` · **símbolo:** `ASTags.STOMP_LIKE_SPELL` · **estado:** ⚠️ fonte pinada / membership condicionado.

## Contrato e consumers

- [`ASTags.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/utils/ASTags.java) declara a tag no registry correto. `TagKey<AbstractSpell>` construída usando `SpellRegistry.SPELL_REGISTRY_KEY` do Iron's; é categorização de spell, não um novo spell.
- **Membros do source:** Datapack em namespace `aces_spell_utils` / caminho `tags/irons_spellbooks/spells`: `irons_spellbooks:stomp`, `irons_spellbooks:earthquake` e `cataclysm_spellbooks:tectonic_tremble` opcional (`required:false`).
- [Datapack da versão pinada](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/resources/data/aces_spell_utils/tags/irons_spellbooks/spells/stomp_like_spell.json) confirma a lista declarada; `replace:false` onde presente. A composição instalada poderá incorporar outros datapacks.
- **Limites:** não é receita, magia, ação autônoma, evento de cast nem entidade nova. Mana, cooldown, range, targets, duration, projectile dimensions e dano não são declarados nesta tag. A categoria `spell` não deve ser confundida com `item` ou `spell`.
- **Integração:** consultar a tag pela API real do provider/host; sem inventar mutador nem pipeline Black Arcana, sem atribuir Mastery por pertinência à tag.

## Validação

Source `AceTheEldritchKing/Aces_Spell_Utils@a0b2f4c2fcfa938c8e47239279c77c2ef82647ac`; JAR catalogado `aces_spell_utils-1.2.7.2-1.21.1.jar`, SHA-1 `8cbcd535a0b19bef49504c0b5ecafcbcd1cb1cca`, sem bytecode parity. `build.gradle` depende de Iron's `3.16.2`, modpack usa `3.16.3`. Confirmar carregamento das tags, membros, datapacks e consumers em servidor dedicado. `physical_qa=NOT_TESTED`; `mutating_hook=NOT_VERIFIED`; `COMPLETE_PERK_READY=false`.
