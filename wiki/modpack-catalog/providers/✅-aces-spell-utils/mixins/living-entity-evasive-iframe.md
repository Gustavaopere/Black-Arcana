# LivingEntityMixin — iframes e atributo evasive — Ace's Spell Utils 1.2.7.2

**Mixin source:** `net.acetheeldritchking.aces_spell_utils.mixins.server.LivingEntityMixin` · **Target:** LivingEntity · **Estado:** ⚠️ source-pinned; carregamento/paridade física não testados.

## Mixin registration e ponto de injeção

- [`src/main/resources/aces_spell_utils.mixins.json`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/resources/aces_spell_utils.mixins.json): `required:true`, `defaultRequire:1`, `compatibilityLevel:JAVA_17`, `minVersion:0.8` e exatos dois mixins `server.LivingEntityMixin` / `server.PlayerMixin`; `client:[]`. A exigência `required` não demonstra por si execução bem-sucedida no host.
- [`LivingEntityMixin.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/mixins/server/LivingEntityMixin.java) — implementação da release pinada.
- **Operação exata:** `@Mixin(LivingEntity.class)` injeta, com `@At(value="FIELD", target="Lnet/minecraft/world/entity/LivingEntity;invulnerableTime:I", opcode=Opcodes.PUTFIELD, shift=At.Shift.AFTER)`, nos métodos `hurt(DamageSource,float)` e `handleDamageEvent(DamageSource)`. Ambos executam `asu$applyEvasiveAttributeIframeTicks()`, cujo cálculo observado é `int bonusTicks=(int)entity.getAttributeValue(ASAttributeRegistry.EVASIVE)`, seguido de `entity.invulnerableTime += bonusTicks`.

## Causalidade, targeting e risco de conflito

Entidade LivingEntity quando os pontos de escrita são atingidos. Não é rolagem de esquiva, cast, seleção de alvo, projétil ou bônus de dano.

**Riscos e não duplicação:** Há também `AcesSpellUtilsServerEvents.evasiveEvent(LivingIncomingDamageEvent)` que altera ticks de invulnerabilidade pelo mesmo atributo. Não supor soma exata ou dupla aplicação em toda ocorrência; hooks são sensíveis à ordem/eventos e exigem JAR+host testados. O source não adiciona clamp neste método do mixin, apesar de bounds do registro do atributo. Não adicionar terceiro modificador de iframe.

Este mixin altera comportamento de entidade que pertence ao provider/vanilla, não é spell, nem `AbstractSpell` registrado na Ace. Mana/cooldown/range/AoE/duração de magia/projétil não são parâmetros da injeção. O Black Arcana não deve instalar substituto sem contrato real, nem o RPG Skill Tree interceptar morte/iframes para procs a partir de observação indireta.

## Proveniência, aceitação e status

Fonte `AceTheEldritchKing/Aces_Spell_Utils@a0b2f4c2fcfa938c8e47239279c77c2ef82647ac`, `mod_version=1.2.7.2-1.21.1`. Modlist: `aces_spell_utils-1.2.7.2-1.21.1.jar`, SHA-1 `8cbcd535a0b19bef49504c0b5ecafcbcd1cb1cca` anotado, source→classfile sem prova; source build usa Iron's `3.16.2`, pack `3.16.3`. **QA:** inspeção do mixins.json no JAR, injection target/method mappings no NeoForge 21.1.x exato, multiplayer/dedicated server, ordem de eventos e interação com Epic Fight/Curios e demais mods que alteram morte/iframes. `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `COMPLETE_PERK_READY=false`. +0 magias próprias.
