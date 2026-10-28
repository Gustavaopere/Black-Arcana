# PlayerMixin — cancelamento de drop de equipamentos — Ace's Spell Utils 1.2.7.2

**Mixin source:** `net.acetheeldritchking.aces_spell_utils.mixins.server.PlayerMixin` · **Target:** Player · **Estado:** ⚠️ source-pinned; carregamento/paridade física não testados.

## Mixin registration e ponto de injeção

- [`src/main/resources/aces_spell_utils.mixins.json`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/resources/aces_spell_utils.mixins.json): `required:true`, `defaultRequire:1`, `compatibilityLevel:JAVA_17`, `minVersion:0.8` e exatos dois mixins `server.LivingEntityMixin` / `server.PlayerMixin`; `client:[]`. A exigência `required` não demonstra por si execução bem-sucedida no host.
- [`PlayerMixin.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/mixins/server/PlayerMixin.java) — implementação da release pinada.
- **Operação exata:** `@Mixin(Player.class)` injeta na cabeça de `Player.dropEquipment` com `cancellable=true`. Dentro do método, usa `Object player=this`, só age se `player instanceof ServerPlayer` e `serverPlayer.getData(ASAttachmentRegistry.KEEP_INV_ON_DEATH.get())` verdadeiro; então chama `CallbackInfo.cancel()`. Com attachment ausente/falso e em outros sides, não cancela nessa condição.

## Causalidade, targeting e risco de conflito

Player ServerPlayer durante death/equipment drop; não confere invulnerabilidade, resurrection/cast ou novo feitiço.

**Riscos e não duplicação:** Coopera com `AcesSpellUtilsServerEvents` em `LivingDeathEvent`, `LivingExperienceDropEvent`, `DropRulesEvent` e `PlayerEvent.Clone`. O campo de attachment usa `Codec.BOOL`, `copyOnDeath()` e remoção no Clone; ordem exata do host pode causar duplicação/perda se outro sistema repetir a cópia/drop. Testar keepInventory gamerule, Curios, XP, offhand/armor, death/relog e ciclo de clone.

Este mixin altera comportamento de entidade que pertence ao provider/vanilla, não é spell, nem `AbstractSpell` registrado na Ace. Mana/cooldown/range/AoE/duração de magia/projétil não são parâmetros da injeção. O Black Arcana não deve instalar substituto sem contrato real, nem o RPG Skill Tree interceptar morte/iframes para procs a partir de observação indireta.

## Proveniência, aceitação e status

Fonte `AceTheEldritchKing/Aces_Spell_Utils@a0b2f4c2fcfa938c8e47239279c77c2ef82647ac`, `mod_version=1.2.7.2-1.21.1`. Modlist: `aces_spell_utils-1.2.7.2-1.21.1.jar`, SHA-1 `8cbcd535a0b19bef49504c0b5ecafcbcd1cb1cca` anotado, source→classfile sem prova; source build usa Iron's `3.16.2`, pack `3.16.3`. **QA:** inspeção do mixins.json no JAR, injection target/method mappings no NeoForge 21.1.x exato, multiplayer/dedicated server, ordem de eventos e interação com Epic Fight/Curios e demais mods que alteram morte/iframes. `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `COMPLETE_PERK_READY=false`. +0 magias próprias.
