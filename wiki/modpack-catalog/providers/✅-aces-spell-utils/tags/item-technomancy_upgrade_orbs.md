# technomancy_upgrade_orbs — Ace's Spell Utils 1.2.7.2

**Registry associado:** `minecraft:item` · **tag:** `aces_spell_utils:technomancy_upgrade_orbs` · **símbolo:** `ASTags.TECHNOMANCY_UPGRADE_ORB` · **estado:** ⚠️ fonte pinada / membership condicionado.

## Contrato e consumers

- [`ASTags.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/utils/ASTags.java) declara a tag no registry correto. Contrato de unificação de upgrade orbs Technomancy.
- **Membros do source:** Sem membros/receitas definidos nas fontes do provider.
- Nenhuma lista de membros da tag de item foi comprovada em `data/aces_spell_utils/tags/item/` nessa fonte.
- **Limites:** não é receita, magia, ação autônoma, evento de cast nem entidade nova. Mana, cooldown, range, targets, duration, projectile dimensions e dano não são declarados nesta tag. A categoria `item` não deve ser confundida com `item` ou `spell`.
- **Integração:** consultar a tag pela API real do provider/host; sem inventar mutador nem pipeline Black Arcana, sem atribuir Mastery por pertinência à tag.

## Validação

Source `AceTheEldritchKing/Aces_Spell_Utils@a0b2f4c2fcfa938c8e47239279c77c2ef82647ac`; JAR catalogado `aces_spell_utils-1.2.7.2-1.21.1.jar`, SHA-1 `8cbcd535a0b19bef49504c0b5ecafcbcd1cb1cca`, sem bytecode parity. `build.gradle` depende de Iron's `3.16.2`, modpack usa `3.16.3`. Confirmar carregamento das tags, membros, datapacks e consumers em servidor dedicado. `physical_qa=NOT_TESTED`; `mutating_hook=NOT_VERIFIED`; `COMPLETE_PERK_READY=false`.
