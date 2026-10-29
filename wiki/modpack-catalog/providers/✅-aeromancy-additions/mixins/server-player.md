# Mixin — ServerPlayer.onExplosionHit

**Contrato:** suporte de Aeromancy Additions `1.2.8`, source fixo `snackerpirater/aero-additions@ae282b32d25ad76ef8d01c637ec05566a767ae4c`. Não é nova identidade de magia. `hooks=NOT_VERIFIED`; `physical_runtime=NOT_TESTED`; **0 certificações / +0 magias / +0 adapters aprovados**. O JAR oficial de publicação foi adquirido separadamente; isso não comprova paridade com o JAR instalado historicamente (SHA-1 histórico de 35 caracteres inválido). [Proveniência e limites](../SOURCE-CONTRACTS-1.2.8.md).

## Binding e alteração

`aeromancy.mixins.json` é `required=true`, compatibilidade `JAVA_21`, `minVersion=0.8` e `injectors.defaultRequire=1`; inclui `ServerPlayerMixin` na lista comum. O template `neoforge.mods.toml` declara esse config. A exigência do config é demonstrada no source; aplicação da injeção no host atual permanece `NOT_VERIFIED`.

`@Mixin(ServerPlayer.class)` injeta em **`onExplosionHit`, `TAIL`**. Após a lógica alvo, se o argumento `Entity` for `MagicWindCharge`, chama `setIgnoreFallDamageFromCurrentImpulse` com o predicado abaixo:

```text
windCharge.owner != null &&
(owner.is(player) ||
 (SummonManager.getOwner(owner) != null &&
  SummonManager.getOwner(owner).isAlliedTo(player)))
```

O alvo é o próprio `ServerPlayer` da instância mixada. O primeiro caminho exige owner idêntico ao player; o segundo resolve dono do **owner do projétil** e exige que esse dono seja aliado do player. Não basta o owner direto ser um player aliado se o segundo lookup não retorna dono. Owner nulo ou predicado falso **escreve false** para MagicWindCharge. Para outras entidades, o mixin não chama o setter.

Não atribui imunidade geral a queda nem marca qualquer explosão como segura: altera a flag de ignorar dano da **impulsão atual**, usando API vanilla. A duração/consumo dessa flag é do host Minecraft. O evento `ExplosionKnockbackEvent` de tentativa alternativa em AAServerEvents está comentado.

| Eixo | Contrato para perks |
|---|---|
| Dano | Controle condicional de dano de queda posterior; não muda dano direto/explosivo do wind charge. |
| Alcance | N/A local: recebe entidade de `onExplosionHit`; sem raio novo. |
| Alvo | ServerPlayer atingido; classe de projétil exata por `instanceof MagicWindCharge`. |
| Tempo | TAIL de cada `onExplosionHit`; lifetime da flag delegado ao engine. |
| Custo | N/A: sem mana/cooldown; cast continua na [magia Wind Charge](../spells/wind-charge.md). |

Não substituir esse mixin por outro settlement no mod do pack. Owner chain, allied summons, explosões consecutivas e fall damage com outros mods exigem teste físico; **0 mixins certificados**.


**Fonte imutável:** [ServerPlayerMixin.java](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/mixin/ServerPlayerMixin.java#L15-L27) · [Config obrigatório](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/resources/aeromancy.mixins.json#L1-L14) · [Declaração no template](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/templates/META-INF/neoforge.mods.toml#L28-L30) · [Alternativa de evento comentada](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/AAServerEvents.java#L129-L139).
