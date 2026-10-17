# Iron's 3.16.3 — Angel Wings: buff self e elegibilidade Elytra via mixin

**Identidade:** `irons_spellbooks:angel_wing` (*singular*, diferente do efeito `angel_wings`) · Holy · níveis 1–5 · ✅ magia no inventário ativo 110; 🟡 dossiê causal novo; ⚠️ fonte fixa sem classfile exato nem cliente físico; ⛔ perk para voo/stacking ou bypass de Elytra sem adapter. **+0 novo spell.**

**Fonte upstream fixa:** `iron431/irons-spells-n-spellbooks@e4056af90302d37eb1739f5ff05020b020e6e252` (Minecraft 1.21.1, Iron's 3.16.3). A modlist física registra `irons_spellbooks-1.21.1-3.16.3.jar` / NeoForge 21.1.250; o build Black Arcana usa NeoForge 21.1.248. Isto documenta o *source* do provider, sem equivalência do classfile instalado ou observação de gameplay. Pesquisa destinada à interoperabilidade e clean-room, não reutilização de código upstream.

## Admissão e instância de efeito

1. `AngelWingsSpell` define `Holy`, raridade mínima LEGENDARY, `CastType.INSTANT`, `castTime=0`, maxLevel **5**, cooldown-default **120 s**, mana `80+20×(level−1)` (**80–160**) e spell power nominal `10+10×(level−1)` (**10–50**). [AngelWingsSpell.java L26–52](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/holy/AngelWingsSpell.java#L26-L52).
2. Aplicação exclusivamente ao próprio `LivingEntity` caster via `entity.addEffect(new MobEffectInstance(MobEffectRegistry.ANGEL_WINGS, duration,0,false,false,true), entity)`. Amplifier **0**, duração `(int)getSpellPower(spellLevel,entity)*20` ticks; com multiplicadores neutros, **200–1.000 ticks = 10–50 s**. Não há projétil, range de aquisição ou AoE. Gera 35 partículas `WISP` via `SwirlingParticleOptions`, apenas VFX. [AngelWingsSpell.java L54–74](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/holy/AngelWingsSpell.java#L54-L74).
3. O registro do `MobEffectRegistry` é `angel_wings`; `AngelWingsEffect` estende `MagicMobEffect` e implementa `ISyncedMobEffect` **sem lógica própria de voo**. O efeito atua como condição para outro ponto de execução. [MobEffectRegistry.java L20–25](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/registries/MobEffectRegistry.java#L20-L25); [AngelWingsEffect.java L1–11](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/effect/AngelWingsEffect.java#L1-L11).

## Contrato real de voo — ponto de compatibilidade

- `IItemExtensionMixin` injeta em `IItemStackExtension.canElytraFly` e `IItemStackExtension.elytraFlightTick` com `@At("RETURN")`, `cancellable=true`, `remap=false`, `priority=0`. Quando `entity.hasEffect(ANGEL_WINGS)`, executa `cir.setReturnValue(true)` em ambos. Isso é um **override de retorno em extensão de item/Elytra**, não um atributo padrão de `MOVEMENT_SPEED`, `GRAVITY`, mana ou um hook oferecido ao Black Arcana/RPG Skill Tree. A presença do código não prova composição sem conflito com outros mixins. [IItemExtensionMixin.java L12–28](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/mixin/IItemExtensionMixin.java#L12-L28).
- Renderizadores e partículas são apresentação; a física do voo passa pelo motor NeoForge/Minecraft e pelos métodos interceptados. A origem da condição é `MobEffectRegistry.ANGEL_WINGS` no caster, não item Elytra permanente nem uma segunda ability de RPG. Se outros mods alterarem as duas extensões, prioridade, permissões e comportamento real devem ser medidos com o modpack completo; **não** afirmar compatibilidade com addons apenas porque mixin foi encontrado.
- Como o efeito é self e duradouro, a mesma conjuração pode produzir muitos ticks de voo/vento/render sem criar novo cast. `removeEffect`, dispel, morte/relog e retorno de métodos injetados devem ser testados, especialmente se o jogador cair quando a duração terminar.

## Perks e integração

| Eixo | Causalidade | Recomendação/estado |
|---|---|---|
| Duração | spell power do Iron's em segundos convertidos a ticks | **A condicionado:** amplificação via atributo nativo se contratada, não alterar duration com setter especulativo |
| Intensidade | amplifier zero, não determina velocidade/elevação aqui | **D/⛔:** não inventar +velocidade/+altura de voo |
| Eligible-to-fly | mixin `IItemStackExtension` exige efeito ativo | **C/⛔:** mixin interno não é API estável extensível por perk |
| Equipamentos/Elytra | retorno forçado true em dois métodos | **C:** conflito com atributos, armaduras, APIs de flight de terceiros deve ser testado |
| Recast / mana / cooldown | um cast com effect self, provider-owned | **A condicionado:** não cobrar duas vezes |
| Mastery | 1 cast → buff duradouro → N ticks de voo | **D/⛔:** ticks/render/planagem não representam casts extras |
| Cancelamento/queda | remover efeito desabilita condição de mixin | **C:** observar segurança na queda, não inferir fall immunity automática |

## QA físico pendente

- [ ] JAR instalado: identificar `IItemExtensionMixin` no conjunto de mixins ativo; conferir target/signatures e `MobEffectRegistry`.
- [ ] Testar Elytra equipada, sem Elytra, armadura externa e mixins concorrentes; `canElytraFly`/ `elytraFlightTick` em cliente e servidor.
- [ ] Recast/reapply, dispel, morte, mudança de dimensão, logout e término do buff enquanto voa; verificar movimento e dano de queda.
- [ ] Medir duração efetiva e multiplicadores; garantir que skills/perks de RPG não ativem outro caminho de flight sem contrato.

**Estado:** ✅ source de cast e mixin localizada · ⚠️ compatibility e física de voo não homologadas · ⛔ extensão de voo sem API estável · Stage 06.05 🟡.
