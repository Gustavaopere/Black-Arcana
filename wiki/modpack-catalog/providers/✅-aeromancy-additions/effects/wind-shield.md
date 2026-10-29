# Wind Shielded — efeito Wind Shield

- Registro: `aero_additions:wind_shield`, `MobEffect`, classe `WindShieldEffect extends MagicMobEffect implements ISyncedMobEffect`, categoria `BENEFICIAL`, cor `0xd3ebea`.
- Ativação: **REGISTERED**; produtor ativo: [Wind Shield](../spells/wind-shield.md). Mesmo path em registries diferentes identifica magia e efeito distintos. Contribuição estrita de novas magias **0**.
- Estado: `documentary=SOURCE_PINNED`; `mutating_hook=NOT_VERIFIED`; `physical_qa=NOT_TESTED`; identidade instalada **NOT_VERIFIED**; certificação **0**.

Source `snackerpirater/aero-additions@ae282b32d25ad76ef8d01c637ec05566a767ae4c`, versão `1.2.8`. [Prova comum](../SOURCE-CONTRACTS-1.2.8.md) · [manifesto](../SOURCE-CATALOG-MANIFEST-1.2.8.json) · [limites](../SOURCE-CATALOG-CLOSURE-1.2.8.md). Publisher não identifica o JAR instalado cujo SHA-1 histórico possui 35 caracteres inválidos.

## Dois mecanismos nativos independentes

`WindShieldSpell.onCast` aplica o efeito no próprio caster, amplifier `spellLevel−1` (**0–4**), duração `20×[10+5×spellLevel+(int)sqrt(10×getSpellPower(level,caster))]` ticks; flags da instância `ambient=false`, `visible=false`, `showIcon=true`. Não há aura, varredura de aliados ou raio adicional.

O registro adiciona ao atributo **`IronsLibRegistries.AttributeRegistry.DODGE_CHANCE`** um modifier `aero_additions:wind_shield_dodge`, quantidade base **0.03**, operação **ADD_VALUE**. A [escala de modifier do host Minecraft 1.21.1](../SOURCE-CONTRACTS-1.2.8.md#host-minecraft-1211) multiplica a quantidade base por `(amplifier+1)`; com essa escala, os amplifiers default correspondem nominalmente a **+0.03/+0.06/+0.09/+0.12/+0.15** no atributo. O source do addon fornece o modifier, mas não implementa o settlement de dodge do IronsLib; não confundir esses valores com os percentuais de reflexão abaixo.

`AAServerEvents.Game.windShieldDeflection` lê `ProjectileImpactEvent` somente quando o resultado é `EntityHitResult` de `LivingEntity`. Se a vítima tem o efeito e o tipo do projétil **não** pertence a `reflection_immune`, sorteia `nextFloat() < 0.3 + amplifier/10f`. Nos níveis default: **30/40/50/60/70%**. Sucesso cancela o evento, toca `BREEZE_DEFLECT` e chama `projectile.deflect(REVERSE, entity, entity, entity instanceof Player)`. A atribuição de owner e a trajetória final seguem o método de deflexão da entidade/host. Não há clamp local para amplifier nem evento de dano aceito.

O `else if` seguinte protege **`summoned_breeze`** automaticamente com reverse e owner `SummonManager.getOwner(entity)`, sem repetir o filtro `reflection_immune`. Se um breeze tiver Wind Shield e projétil não imune, entra no primeiro ramo e não recebe fallback quando o sorteio falha; para projétil imune, o primeiro ramo é falso e o fallback pode ocorrer. Essa ordem de ramos importa para perks de imunidade/proteção.

`WindShieldEffect` apenas delega add/remove ao superclass. Não possui tick, NBT, flags mutáveis ativas ou dano próprio. Código de flags comentado não é API de sincronização; a camada visual ativa lê diretamente `hasEffect`.

## Consumidores e matriz para perks

| Eixo | Consumidor real | Fronteira de mutação por perk |
|---|---|---|
| Duração/nível | `WindShieldSpell.onCast`/`getDurationSeconds` | Spell power altera duração; amplifier altera chance e modifier host. Hook individual adicional **NOT_VERIFIED**. |
| Dodge | Modifier em `AASpells.MobEffects.WIND_SHIELD`, consumidor downstream IronsLib | Definição localizada; cálculo final/stacking e esquiva de melee não auditados no addon. |
| Reflexão | `AAServerEvents.Game.windShieldDeflection` | Constante `chanceToDeflect`, tag global e ramo breeze são provider-owned. Cancelar impacto não certifica todos os pipelines de dano. |
| Visual | `WindySwirlRenderer.Vanilla` renderiza corpo/braços/pernas quando flag 2 consulta o efeito | Camada ativa só para skins de jogador; `Geo` existe mas sua instalação está comentada. Não comprova proteção. |
| Causalidade | Efeito não chama `hurt`; projétil refletido mantém seu próprio contrato | Mastery/crédito de hit exigem dano aceito e owner demonstrado; reflexão não cria novo cast Wind. |

QA: dodge final com outros modificadores, amplifiers externos, sequência dos ramos breeze/imunidade, owner após reflexão, custo/latência client-server e compatibilidade de projéteis. Nenhum adapter certificado.

## Localizadores fixos

- [AASpells.java — dodge L150–153](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/spells/AASpells.java#L150-L153).
- [WindShieldSpell.java — aplicação/fórmulas L56–73](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/spells/wind_shield/WindShieldSpell.java#L56-L73).
- [AAServerEvents.java — ramos completos L68–90](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/AAServerEvents.java#L68-L90).
- [WindShieldEffect.java L8–27](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/spells/wind_shield/WindShieldEffect.java#L8-L27); [WindySwirlRenderer.java L49–70](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/spells/wind_shield/WindySwirlRenderer.java#L49-L70); [leitura do efeito L139–144](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/spells/wind_shield/WindySwirlRenderer.java#L139-L144).
