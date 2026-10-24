# Tailwind

**Registro estático:** ✅ `COUNTED_EXACT` no JAR 1.0.5; [prova binária](../EXACT-BINARY-SPELLS-1.0.5.md). Config, números e Survival ⚠️.

- **ID:** `wind_spellbooks:tailwind`
- **Classe runtime:** `net.raptorzizi.wind_spellbooks.spells.wind.TailwindSpell`
- **School:** Wind
- **Provider/JAR:** Wind's Spellbooks / `wind_spellbooks-1.0.5.jar`
- **Status:** PRESENTE

## Contract confirmado

Fingerprint ASM: `usesAddEffect`. O changelog 1.0.1 registra um fix específico de **fall damage de Tailwind**, provando que o effect participa de uma interação de mobilidade/queda na linha incorporada pela 1.0.5.

## NÃO VERIFICADO

Níveis, rarity, mana, cooldown, cast time, exact effect, velocidade/movimento, duração, magnitude de redução/negação de fall damage, stacking, target rules e aquisição específica.

## Deduplicação / fail-closed

Tailwind ocupa um buff/effect Wind com interação de queda. Não adicionar segundo listener de fall damage ou modifier de movimento sem identificar o effect/hook provider-native exato.

## Evidência

Runtime registry + ASM do pack; release 1.0.5; changelog 1.0.1.

## Verificação JVM exata dos consumidores por método — 24/10/2026

**✅ Fonte binária exata:** `wind_spellbooks-1.0.5.jar`, SHA-1 `8744886899bc245ae147a44baa2b183689cec7da`; [CI de inspeção Java 21 #40118955224](https://github.com/Gustavaopere/Black-Arcana/actions/runs/40118955224) `SUCCESS` no passo de extração. **⚠️ Somente assinaturas e arestas de chamadas; não é prova de runtime, fórmula, parâmetros configurados nem hook mutador seguro.**

- Classe inspecionada: `net.raptorzizi.wind_spellbooks.spells.wind.TailwindSpell`.
- Contagem de métodos/declarações indexadas pelo parser: **12**; partes omitidas abaixo são deliberadamente fora do recorte de consumidores de perks.
- Grafo observável de invocações (`método de origem → símbolos referenciados`; a ordem causal e a entidade alvo exigem desambiguação adicional):
- `public java.util.List<net.minecraft.network.chat.MutableComponent> getUniqueInfo(int, net.minecraft.world.entity.LivingEntity);` → `getSpellPower:(ILnet/minecraft/world/entity/Entity;)F`
- `public void onCast(net.minecraft.world.level.Level, int, net.minecraft.world.entity.LivingEntity, io.redspace.ironsspellbooks.api.spells.CastSource, io.redspace.ironsspellbooks.api.magic.MagicData);` → `getSpellPower:(ILnet/minecraft/world/entity/Entity;)F`, `net/minecraft/world/effect/MobEffectInstance."<init>":(Lnet/minecraft/core/Holder;IIZZZ)V`, `net/minecraft/world/entity/LivingEntity.addEffect:(Lnet/minecraft/world/effect/MobEffectInstance;)Z`

- **Literais presentes em métodos selecionados (candidatos sem atribuição):** `public void onCast(net.minecraft.world.level.Level, int, net.minecraft.world.entity.LivingEntity, io.redspace.ironsspellbooks` = 0, 1.
- **Estado por campo:** alcance/geometria/dano/tipo/projétil/duração/targeting/cooldown/mana/execução efetiva ficam **NÃO VERIFICADOS** onde as arestas acima não determinarem operandos, guardas, fórmula e beneficiário. Nomes como `setRadius` ou `setDamage` provam apenas chamada simbólica, **não** o valor ou aplicabilidade de perk.
- **Boundary:** provider mantém efeitos/entidades próprias; Iron's mantém cast/mana/cooldown; Black Arcana não injeta segundo efeito nem delega autoridade de runtime ao RPG Skill Tree. Gate de mutação: **⛔ SEM_HOOK_SEGURO** até prova de contrato e QA provider-native.
- **Próxima inspeção:** reconstruir operandos/guards em chamadas relevantes usando bytecode exato, verificar host Iron's 3.16.3 e confirmar em client/servidor. `Stage 06.05` 🟡 e `Stage 09` ⚠️.

## Dependências compiladas adicionais — 24/10/2026

**Fonte:** [workflow de inventário exato #40120464325](https://github.com/Gustavaopere/Black-Arcana/actions/runs/40120464325) (`SUCCESS`) e artefato JSON `wind-spellbooks-105-methods`; SHA-1 físico do provider `8744886899bc245ae147a44baa2b183689cec7da`. Dados extraídos de referências `javap` da classe acima, **não** de execução de gameplay.

| Método / região JVM | Evidência observada | Limite de atribuição |
|---|---|---|
| `getPercentAirSpeed(int)` | `fmul`, `i2f` | Percentual real não determinado. |
| `getPercentJump(int)` | `fadd`, `fmul`, `i2f`, `isub` | Não estabelece bônus efetivo por nível. |
| `onCast(Level, int, LivingEntity, CastSource, MagicData)` | Lê `ModMobEffectRegistry.TAILWIND`; `f2i`, `fmul`, `isub` | Duração, amplificador e stacking não determinados. |

O construtor ainda apresenta escritas de `baseManaCost`, `manaCostPerLevel`, `baseSpellPower`, `spellPowerPerLevel`, `castTime` e `defaultConfig`; seus valores não são inferidos desses nomes. Mesmo com os campos e operadores, **não há fluxo de operandos/guardas homologado, fórmula numérica aprovada, hook mutador seguro, nem QA provider-native**. Manter `NÃO VERIFICADO` e `SEM_HOOK_SEGURO` para integração de perks; denominadores e identidade 7/7 sem alteração.

## Fórmulas escalares adicionais verificadas — 24/10/2026

**🟡 Evidência binária de getters, sem QA de gameplay.** [Execução JVM exata #40126898432](https://github.com/Gustavaopere/Black-Arcana/actions/runs/40126898432), artefato `wind-spellbooks-105-methods/mobility-getters.json`, verificado no JAR SHA-1 `8744886899bc245ae147a44baa2b183689cec7da`. Os getters foram integralmente interpretados por parser conservador; `level` é o parâmetro inteiro no slot JVM 1. Fórmulas reproduzidas em notação matemática explicativa, **não** código do provider.

| Getter | Expressão compilada do retorno | Observação de tipo e operandos | Ainda NÃO VERIFICADO |
|---|---|---|---|
| `getPercentAirSpeed(int)` | `(((float)level * 0.15f) * 100.0f)` | Dois `fmul`, com conversão explícita `i2f`; manter ordem dos cálculos para respeitar arredondamento de `float`. | Nome do método não prova se a porcentagem é aditiva, multiplicativa, exibida na UI ou aplicada no movimento. |
| `getPercentJump(int)` | `((0.5f + (0.3f * ((float)(level - 1)))) * 100.0f)` | Subtração `isub` antes de `i2f`, seguida por `fmul`/`fadd`/`fmul`. | Não determina impulso real de salto, efeito de equipamentos, parâmetros de configuração ou stacking. |

A expressão compilada isolada não autoriza perk mutadora nem alteração em `onCast`. **⛔ SEM_HOOK_SEGURO** até confirmar chamador, geometrias e host; nenhuma alteração de mana, cooldown, efeitos, poderes, duração, entidades ou configuração foi implementada. Wind's/Iron's permanecem autoridades provider-native; Black Arcana possui seu runtime, RPG Skill Tree apenas progressão/perks por boundary real.
