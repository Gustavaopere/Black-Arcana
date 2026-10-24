# Almighty Push

**Registro estático:** ✅ `COUNTED_EXACT` no JAR 1.0.5; [prova binária](../EXACT-BINARY-SPELLS-1.0.5.md). Config, números e Survival ⚠️.

- **ID:** `wind_spellbooks:almighty_push`
- **Classe runtime:** `net.raptorzizi.wind_spellbooks.spells.wind.AlmightyPushSpell`
- **School:** Wind
- **Provider/JAR:** Wind's Spellbooks / `wind_spellbooks-1.0.5.jar`
- **Status:** PRESENTE

## Contract confirmado

Fingerprint ASM: `createsEntity` e `usesAddEffect`. O nome/provider indicam um spell de push, mas a geometria, força e seleção de targets **não são inferidas** sem bytecode exato. O que está comprovado é que o cast cria entity e aplica effect provider-native.

## NÃO VERIFICADO

Níveis, rarity, mana, cooldown, cast time, radius/range, force, dano, entity/effect concretos, target/friendly-fire/PvP/boss rules e aquisição.

## Deduplicação / fail-closed

Reservar o contract de push-themed Wind e não criar entity/effect paralelo. Qualquer integração numérica aguarda source/JAR extraction.

## Evidência

Runtime registry + ASM do pack; release oficial 1.0.5.

## Verificação JVM exata dos consumidores por método — 24/10/2026

**✅ Fonte binária exata:** `wind_spellbooks-1.0.5.jar`, SHA-1 `8744886899bc245ae147a44baa2b183689cec7da`; [CI de inspeção Java 21 #40118955224](https://github.com/Gustavaopere/Black-Arcana/actions/runs/40118955224) `SUCCESS` no passo de extração. **⚠️ Somente assinaturas e arestas de chamadas; não é prova de runtime, fórmula, parâmetros configurados nem hook mutador seguro.**

- Classe inspecionada: `net.raptorzizi.wind_spellbooks.spells.wind.AlmightyPushSpell`.
- Contagem de métodos/declarações indexadas pelo parser: **13**; partes omitidas abaixo são deliberadamente fora do recorte de consumidores de perks.
- Grafo observável de invocações (`método de origem → símbolos referenciados`; a ordem causal e a entidade alvo exigem desambiguação adicional):
- `public float getStrength(int, net.minecraft.world.entity.LivingEntity);` → `getSpellPower:(ILnet/minecraft/world/entity/Entity;)F`
- `public java.util.List<net.minecraft.network.chat.MutableComponent> getUniqueInfo(int, net.minecraft.world.entity.LivingEntity);` → `getRange:(ILnet/minecraft/world/entity/LivingEntity;)F`, `getStrength:(ILnet/minecraft/world/entity/LivingEntity;)F`
- `public void onCast(net.minecraft.world.level.Level, int, net.minecraft.world.entity.LivingEntity, io.redspace.ironsspellbooks.api.spells.CastSource, io.redspace.ironsspellbooks.api.magic.MagicData);` → `getRange:(ILnet/minecraft/world/entity/LivingEntity;)F`, `getStrength:(ILnet/minecraft/world/entity/LivingEntity;)F`, `net/minecraft/world/level/Level.addFreshEntity:(Lnet/minecraft/world/entity/Entity;)Z`, `net/raptorzizi/wind_spellbooks/entity/spells/almighty_push/AlmightyPushEntity.setLifetime:(I)V`, `net/raptorzizi/wind_spellbooks/entity/spells/almighty_push/AlmightyPushEntity.setRadius:(F)V`

- **Literais presentes em métodos selecionados (candidatos sem atribuição):** `public void onCast(net.minecraft.world.level.Level, int, net.minecraft.world.entity.LivingEntity, io.redspace.ironsspellbooks` = 1.
- **Estado por campo:** alcance/geometria/dano/tipo/projétil/duração/targeting/cooldown/mana/execução efetiva ficam **NÃO VERIFICADOS** onde as arestas acima não determinarem operandos, guardas, fórmula e beneficiário. Nomes como `setRadius` ou `setDamage` provam apenas chamada simbólica, **não** o valor ou aplicabilidade de perk.
- **Boundary:** provider mantém efeitos/entidades próprias; Iron's mantém cast/mana/cooldown; Black Arcana não injeta segundo efeito nem delega autoridade de runtime ao RPG Skill Tree. Gate de mutação: **⛔ SEM_HOOK_SEGURO** até prova de contrato e QA provider-native.
- **Próxima inspeção:** reconstruir operandos/guards em chamadas relevantes usando bytecode exato, verificar host Iron's 3.16.3 e confirmar em client/servidor. `Stage 06.05` 🟡 e `Stage 09` ⚠️.

## Dependências compiladas adicionais — 24/10/2026

**Fonte:** [workflow de inventário exato #40120464325](https://github.com/Gustavaopere/Black-Arcana/actions/runs/40120464325) (`SUCCESS`) e artefato JSON `wind-spellbooks-105-methods`; SHA-1 físico do provider `8744886899bc245ae147a44baa2b183689cec7da`. Dados extraídos de referências `javap` da classe acima, **não** de execução de gameplay.

| Método / região JVM | Evidência observada | Limite de atribuição |
|---|---|---|
| `getRange(int, LivingEntity)` | `fadd`, `fmul`, `i2f` | Fórmula e alcance efetivo não reconstruídos. |
| `getStrength(int, LivingEntity)` / `getDuration(int)` | `fmul` / `iadd`, `imul` | Escalas e unidades não verificadas. |
| `onCast(Level, int, LivingEntity, CastSource, MagicData)` | Escreve `AlmightyPushEntity.amplifier:I` e `AlmightyPushEntity.strength:F` | Não prova o valor passado nem quem recebe o efeito. |

O construtor ainda apresenta escritas de `baseManaCost`, `manaCostPerLevel`, `baseSpellPower`, `spellPowerPerLevel`, `castTime` e `defaultConfig`; seus valores não são inferidos desses nomes. Mesmo com os campos e operadores, **não há fluxo de operandos/guardas homologado, fórmula numérica aprovada, hook mutador seguro, nem QA provider-native**. Manter `NÃO VERIFICADO` e `SEM_HOOK_SEGURO` para integração de perks; denominadores e identidade 7/7 sem alteração.

## Getter escalar com proveniência de operandos — 24/10/2026

**🟡 Expressão aritmética compilada verificada, sem homologação de gameplay.** A inspeção do JAR exato `wind_spellbooks-1.0.5.jar` (SHA-1 `8744886899bc245ae147a44baa2b183689cec7da`) reconstruiu a pilha JVM integral do método selecionado, mediante gramática estrita e sem opcodes desconhecidos. Fonte: [CI específico #40124346655](https://github.com/Gustavaopere/Black-Arcana/actions/runs/40124346655), artefato `wind-spellbooks-105-methods/scalar-getters.json`.

- **Método:** `getDuration(int)`.
- **Expressão observável:** `25 + (level * 3)`, onde `level` é o primeiro parâmetro `int` (local JVM 1), e as operações seguem semântica de inteiros da JVM.
- **Limite de interpretação:** O método retorna esse inteiro; não há comprovação da unidade, de conversão para ticks nem do consumo real pela entidade.
- **Escopo da promoção:** esta evidência atualiza exclusivamente o getter acima; as advertências anteriores continuam válidas para alcance, targeting, dano, impulso, efeitos, custo, cooldown e integração.
- **Perk mutadora:** ⛔ `SEM_HOOK_SEGURO`, até demonstrar consumidor, lifecycle, bounds e contrato host/provider com QA em runtime; Black Arcana não duplica efeitos e RPG Skill Tree não assume autoridade de casting.
