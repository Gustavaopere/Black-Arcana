# Dark Arrow — projétil e tipo de dano `alexscaves:dark_arrow` (1.0.10)

**Catálogo:** ✅ contrato estático do projétil e do tipo de dano documentado. **Escopo:** `STATIC_TECHNICAL_CATALOG_ONLY` / `SHA_EXACT_BINARY_BEHAVIOR`. **Hooks mutadores:** `NOT_VERIFIED`; **QA física:** `NOT_TESTED`; **integração:** `NO_MUTATION` até homologação específica. A ficha não certifica o provider inteiro nem o resultado de um lançamento no modpack.

## 1. Identidade e autoridade da prova

- **Provider / mod ID:** `Alex's Caves Continued` / `alexscaves`.
- **Versão física:** `alexscaves-1.0.10-neoforge+1.21.1.jar`, Minecraft 1.21.1; 75.279.314 bytes.
- **JAR SHA-1:** `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`.
- **JAR SHA-256:** `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`.
- **Entidade:** `com/github/alexmodguy/alexscaves/server/entity/item/DarkArrowEntity.class`; SHA-256 `089f0a65444078ca42fc1da2d5023384314ef5f5283ddf3fe8484bf31d4136ad`.
- **Tipo de dano:** `data/alexscaves/damage_type/dark_arrow.json`; resource ID `alexscaves:dark_arrow`; SHA-256 `a8c5a9d4d72a4c064c1b0fca923d2059eb6b718e9866fb8d19dc539bb0ffec93`.
- **Owner do lançamento:** [Dreadbow — equipamento e decisões de disparo](../equipment/dreadbow.md). A entidade e o tipo de dano são settlement desse equipamento, sem nova raiz mágica.

**Contabilidade:** **+0 raízes mágicas novas**. Esta ficha consolida o tipo de dano já inventariado e seu projétil consumidor.

O [contrato comum de Dreadbow/Dark Arrow](../EXACT-DREADBOW-CONTRACTS-1.0.10.md) e o [manifesto selado](../EXACT-DREADBOW-CONTRACTS-1.0.10.json) fixam ficha, classes, recursos, descritores JVM e instruções. Todos os offsets abaixo são localizadores de `javap -p -c -s` do JAR SHA-exato. A fonte pública `Codx-org/AlexsCavesContinued@523308608422ab8e31974befa7111ecdf495dd37` declara **1.1.1**; não fornece os parâmetros certificados de 1.0.10.

## 2. Geometria, voo e ciclo de vida

`DarkArrowEntity` estende **`AbstractArrow`**. `ACEntityRegistry.lambda$static$63()Lnet/minecraft/world/entity/EntityType; @0–37` registra categoria `MISC`, dimensões **largura `1.1F` × altura `0.5F`**, update interval `1` e recebimento de atualizações de velocidade `true`. Em `<clinit>()V @1095–1109`, o nome registrado é `dark_arrow`. Dimensões de entidade não são raio de área, hitbox final expandida pelo motor ou tamanho do desenho na tela.

A implementação própria de `tick()V` executa `AbstractArrow.tick()` **primeiro** (`@0–1`); depois atualiza interpolação visual e fading. Não há rotina própria de homing, consulta de candidatos, aquisição de UUID de alvo ou alcance máximo em blocos. Movimento inicial e distribuição dos disparos pertencem ao Dreadbow; gravidade, movimento normal, escolha de colisões e regras prévias de elegibilidade continuam delegados ao motor `AbstractArrow`/`Projectile`. A ausência de override não permite importar números de outra versão do Minecraft como se fossem constantes deste mod.

| Contrato próprio | Localizador em `DarkArrowEntity` |
|---|---|
| `inGround` ativa `startFading` | `tick()V @20–29` |
| Fading escreve `noPhysics = true` e escala o vetor de movimento por **`0.699999988079071D`**, representação double do literal float `0.7F` | `tick @32–55` |
| Fading incrementa `fadeOut`, mas compara o **valor anterior** com `5F`; descarta se o anterior é `>5F` | `tick @58–76` |
| Tiro perfeito faz o parâmetro visual `arrowR = min(arrowR + 0.15F, 1F)` | `tick @79–107` |
| Inércia de água própria `0.9F` | `getWaterInertia()F @0–2` |
| `startFalling()V` apenas escreve `inGround = false`; não limpa `startFading` | `startFalling @0–5` |
| Item padrão de pickup `ItemStack.EMPTY` | `getDefaultPickupItem()Lnet/minecraft/world/item/ItemStack; @0–3` |

**Limite exato do fading:** partindo de `fadeOut=0`, os valores anteriores `0…5` não descartam; a sétima execução elegível compara `6`, grava `7` e chama `discard()`. Portanto, não são cinco nem seis ticks fixos desde o lançamento. Se uma colisão em `super.tick` ativar fading, a mesma execução já pode processar o primeiro incremento. O motor pode remover a entidade por outras razões antes disso. Após `discard`, o método não retorna imediatamente: o ramo visual de tiro perfeito ainda é alcançado. `getFadeOut(F)F` e `getArrowRed(F)F` interpolam os pares anterior/atual; não são getters de duração, dano ou precisão.

Não existe override próprio de `onHitBlock`, `canHitEntity` ou rotina de dano em área. O caminho em bloco e os testes de colisão anteriores a `onHitEntity` são herdados. O provider também declara `AbstractArrowMixin` em `alexscaves.mixins.json`: seu `ac_canHitEntity(Lnet/minecraft/world/entity/Entity;Lorg/spongepowered/asm/mixin/injection/callback/CallbackInfoReturnable;)V @0–25` define retorno `false` quando owner e candidato são ambos `DeepOneBaseEntity`. Portanto, os gates próprios de `onHitEntity` não são a lista inteira de elegibilidade do projétil. Colidir com aliado não ativa fading nesse override; isso não garante uma trajetória de atravessamento específica no jogo.

## 3. Estado sincronizado, owner e persistência

`defineSynchedData(Lnet/minecraft/network/syncher/SynchedEntityData$Builder;)V @0–29` primeiro chama o super e define dois accessors próprios:

| Campo | Default | Getter / setter exatos |
|---|---|---|
| `SHADOW_ARROW_DAMAGE` (`Float`) | `0.0F` | `getShadowArrowDamage()F` lê em `@0–16`; `setShadowArrowDamage(F)V` escreve em `@0–14` |
| `PERFECT_SHOT` (`Boolean`) | `false` | `isPerfectShot()Z` lê em `@0–16`; `setPerfectShot(Z)V` escreve em `@0–14` |

Os getters apenas retornam `SynchedEntityData.get` convertido; não recalculam dano ou chance. Seus hashes de método, preservados no [manifesto anterior de helpers](EXACT-DAMAGE-HELPERS-1.0.10.json), são `afe89892cb041a585baf6a4c38a5877942193db84612d830d0f2babdc7c080cf` (`getShadowArrowDamage`) e `c91a50e4a585ac94cd3a7680b8b7faaebe31351cc261c057ae469909551a99cd` (`isPerfectShot`). O default não é o valor final de toda flecha.

O construtor `(Lnet/minecraft/world/level/Level;Lnet/minecraft/world/entity/LivingEntity;)V @0–20` passa o atirador ao construtor `AbstractArrow(EntityType,LivingEntity,Level,ItemStack,ItemStack)`, com `ItemStack.EMPTY` e `null` nos dois últimos argumentos. Os outros construtores recebem `EntityType/Level` ou `Level/x/y/z`, sem parâmetro de atirador. `onHitEntity @5–9` consulta `getOwner()` novamente no impacto; não conserva ali um owner local independente. O callback `AbstractArrowMixin.ac_playerConstructor` chama `ac_offsetForMagnetism(Lnet/minecraft/world/entity/LivingEntity;)V`: se `MagnetUtil.getEntityMagneticDirection(shooter) != Direction.DOWN`, escreve posição `shooter.getEyePosition().add(0D,-0.1D,0D)` (`@0–23`). Esse deslocamento é de origem, sem homing ou mudança da dimensão registrada.

A classe declara `fadeOut`, `prevFadeOut`, `startFading`, `arrowR` e `prevArrowR` como estado próprio, inicializado em zero/false pelos construtores. **Não declara** `readAdditionalSaveData`/`addAdditionalSaveData` nem serialização própria desses campos ou dos dois accessors. Sincronização não constitui persistência. Save/load de owner e estado herdado pertence ao motor; não há contrato nesta classe para restaurar integralmente dano, tiro perfeito e fading depois de reload. Qualquer perk que dependa disso precisa de QA e de um contrato separado de persistência.

O [manifesto de escritores](EXACT-DARK-ARROW-STATE-1.0.10.json) e o [manifesto de decisões](EXACT-DREADBOW-DECISIONS-1.0.10.json) identificam `DreadbowItem.class`, SHA-256 `b9cd6e843f923877775e38b89214e8649c10d4d5be704ed9dd377900439d44ae`. Em `releaseUsing(Lnet/minecraft/world/item/ItemStack;Lnet/minecraft/world/level/Level;Lnet/minecraft/world/entity/LivingEntity;I)V`, `setShadowArrowDamage` recebe `2F` com `PRECISE_VOLLEY` positivo, ou `3F` no ramo alternativo (`@390–402`); `setPerfectShot` recebe a conjunção `TWILIGHT_PERFECTION > 0 && getPerfectShotTicks(stack) > 0` (`@87–108`, escrita `@407–409`). `onUseTick(Lnet/minecraft/world/level/Level;Lnet/minecraft/world/entity/LivingEntity;Lnet/minecraft/world/item/ItemStack;I)V @195–196` possui outro caminho com `2F`. A ficha de equipamento documenta as condições completas de chegada a esses pontos, carga, timing e inserção no mundo.

## 4. Impacto, fórmula e filtros causais

`onHitEntity(Lnet/minecraft/world/phys/EntityHitResult;)V` contém um único ponto próprio de solicitação de dano. A reconstrução dos operandos e saltos produz:

```text
victim = hit.getEntity()
owner = getOwner()
requested = getShadowArrowDamage()
if isPerfectShot(): requested *= 2F
source = causeDarkArrowDamage(victim.level().registryAccess(), owner)
if owner != null:
    if victim.is(owner): return
    if victim.isAlliedTo(owner): return
    if owner.isAlliedTo(victim): return
if startFading: return
if ACCompat.hurt(victim, source, requested):
    startFading = true
```

- `@10–27`: o multiplicador de tiro perfeito é **`2F`** sobre o float armazenado. Assim, um valor armazenado `2F` solicita `4F` se perfeito; `3F` solicita `6F`. Não há escala própria por velocidade, sorteio de crítico, clamp ou arredondamento inteiro nesse cálculo. Dano solicitado não equivale a vida efetivamente removida.
- `@29–40`: constrói a fonte **antes** dos filtros de owner/aliança/fading. O registro do tipo precisa existir mesmo quando um gate posterior rejeitaria o dano.
- `@42–67`: owner **não nulo** ativa identidade e alianças nos dois sentidos; owner nulo salta diretamente para `@70`. A classe não restringe aqui a vítima a `LivingEntity`, não faz consulta de área, teste próprio de distância ou linha de visão e não exige owner vivo. Os filtros herdados de colisão ocorrem antes e não devem ser substituídos por essa lista.
- `@70–90`: se `startFading` já é verdadeiro, pula `hurt`; se `hurt` retorna falso, não ativa fading. Portanto, dano recusado não consome esse gate próprio e outra chamada futura pode tentar novamente. Após retorno verdadeiro, chamadas posteriores são bloqueadas enquanto o flag permanecer ativo; isso não prova número de hits por lançamento diante de outros consumidores.

O override não chama `super.onHitEntity` e não possui teste próprio `Level.isClientSide`, autorização de PvP, proteção territorial, consumo de mana ou cooldown. Não se deve presumir que a classificação de projétil reproduz todo o pós-impacto vanilla de flechas. A autoridade de lançamento/colisão e a aceitação final de `Entity.hurt` continuam nos caminhos nativos; a ausência de um teste local não comprova execução cliente nem uma falha física.

## 5. Factory, attribution e classificação do dano

`ACDamageTypes.causeDarkArrowDamage` tem descritor `(Lnet/minecraft/core/RegistryAccess;Lnet/minecraft/world/entity/Entity;)Lnet/minecraft/world/damagesource/DamageSource;`. Classe `com/github/alexmodguy/alexscaves/server/misc/ACDamageTypes.class`, SHA-256 `389fb88f8d6e1515e3dfe7f401a728bb33629666bd2319ae7e25668f710e4ef6`.

A factory consulta `Registries.DAMAGE_TYPE`, obtém o holder `DARK_ARROW` com `getHolderOrThrow` (`@4–22`) e cria `ACDamageTypes$DamageSourceRandomMessages(holder, entity, 1)` (`@27–29`). A entidade passada é o **owner consultado no impacto**, não `this` DarkArrowEntity. O construtor `(Lnet/minecraft/core/Holder$Reference;Lnet/minecraft/world/entity/Entity;I)V @0–11` delega a `DamageSource(Holder,Entity)` e guarda `messageCount=1`; não recebe um par separado projétil/atirador. Portanto, consumidores de `getDirectEntity`, `getEntity` e crédito de morte devem seguir essa construção nativa, sem presumir uma factory equivalente a `arrow(projectile, owner)` só por existir o tag `is_projectile`.

`ACCompat.hurt(Entity,DamageSource,float)` possui descritor `(Lnet/minecraft/world/entity/Entity;Lnet/minecraft/world/damagesource/DamageSource;F)Z`, classe `com/github/alexmodguy/alexscaves/server/misc/ACCompat.class`, SHA-256 `333738f324e6e9d77a488e14b7e81b169c2b2d4f6db5171206a016ad0271f57b`. Seu corpo de cinco instruções encaminha os mesmos alvo/fonte/float para `Entity.hurt` e retorna diretamente o booleano, sem branch ou cálculo adicional. Armadura, resistências, invulnerabilidade, eventos e modificadores de outros mods são settlement externo; o wrapper não certifica dano líquido nem permissões.

| Campo | Valor literal do recurso | Limite de interpretação |
|---|---|---|
| `message_id` | `desolate_dagger` | Chave de mensagem; não é sinônimo do registro nem classe de implementação |
| `scaling` | `never` | Campo `scaling` do tipo de dano; não fixa dano causado nem curva de perks |
| `exhaustion` | `0.3` | Valor do campo `exhaustion`; **não** é mana, stamina, custo do feitiço ou dano |

Tags declaradas diretamente para `alexscaves:dark_arrow` nos seis JSONs de damage-type tags do JAR:

- `minecraft:bypasses_cooldown`
- `minecraft:is_projectile`
- `minecraft:no_impact`

São entradas textuais do artefato, não tags finais após datapacks, dependências e overrides. `bypasses_cooldown` classifica a invulnerabilidade/cooldown de **dano do Minecraft**, não o cooldown de carga/casting do equipamento. Não há entrada direta neste JAR para Dark Arrow em `is_explosion` ou `is_fire`; isso não prova a ausência nas tags finais do modpack.

**Nomenclatura:** `dark_arrow.json` e `desolate_dagger.json` possuem conteúdo/hash idêntico e o mesmo `message_id`, mas são **dois resource IDs diferentes**; não corrigir os dados nem mesclar contratos de ataque. `DamageSourceRandomMessages.getLocalizedDeathMessage(Lnet/minecraft/world/entity/LivingEntity;)Lnet/minecraft/network/chat/Component;` usa `nextInt(messageCount)`, o `message_id` e o nome de entidade disponível; para esta factory o contador é `1`, logo o índice sorteado é `0`. A geração de mensagem não define escola mágica nem dano.

## 6. Custos, integração e limites de perks

O tipo de dano e a entidade não têm custo próprio de recurso, tempo de carga ou cooldown de uso. [Dreadbow](../equipment/dreadbow.md) é a autoridade dos consumíveis, desgaste, modo de tiro, condições de luz, duração de uso e velocidade inicial. Não transformar `exhaustion=0.3`, update interval `1` ou fading em custos do lançamento. O pickup padrão vazio também não constitui uma política de reembolso de munição implementada por Black Arcana.

Para perks, são eixos distintos: valor sincronizado de dano, multiplicador do flag perfeito, timing do Dreadbow, distribuição/velocidade dos projéteis, dimensão registrada e regras de aliança. Alterar um não altera automaticamente os demais. `setShadowArrowDamage`/`setPerfectShot` são métodos internos de estado do provider, **não hooks seguros homologados**. Trocar a factory por uma fonte com outra attribution altera consumidores de dano e crédito; reaplicar dano depois de `hurt` duplicaria o settlement.

A ficha cobre os sete campos estáticos — identidade, comportamento, parâmetros, targeting, custos por emissor, integração e validação — com limites de responsabilidade explícitos. **Não** certifica adapter Black Arcana/Enshrouded/RPG Skill Tree, QA multiplayer, configurações efetivas ou proteção de mundo. Esses estados permanecem `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED` e `NO_MUTATION`, sem promoção de Stage.

## 7. Reprodução e evidências preservadas

A prova atual amplia as sondagens anteriores; elas continuam disponíveis como recortes reproduzíveis, sem serem confundidas com o manifesto integral desta ficha:

- [JSONs e tags SHA-exatos](EXACT-RESOURCE-MANIFEST-1.0.10.json) — [CI](https://github.com/Gustavaopere/Black-Arcana/actions/runs/40985275338).
- [Factory e callsites diretos](EXACT-CONSUMERS-1.0.10.json) — [CI](https://github.com/Gustavaopere/Black-Arcana/actions/runs/40993193816).
- [Janelas de fluxo e branches](EXACT-DAMAGE-PATH-ANCHORS-1.0.10.json) — recorte anterior, complementado pela análise causal de `onHitEntity` acima.
- [Getters e wrapper de dano](EXACT-DAMAGE-HELPERS-1.0.10.json) — [CI](https://github.com/Gustavaopere/Black-Arcana/actions/runs/40997154302).
- [Accessors, defaults e escritores](EXACT-DARK-ARROW-STATE-1.0.10.json) — [CI](https://github.com/Gustavaopere/Black-Arcana/actions/runs/41001621930).
- [Decisões Precise Volley / Twilight Perfection](EXACT-DREADBOW-DECISIONS-1.0.10.json) — [CI](https://github.com/Gustavaopere/Black-Arcana/actions/runs/41003421569).

QA física necessária: colisões e dano recusado; alvos aliados/não aliados; owner ausente; PvP e proteção; atribuição observada em eventos; tiro perfeito; pickup; descarregamento/reload e término do fading. São testes pendentes, sem defeito reproduzido declarado. O fechamento deste contrato estático não encerra o universo maior de Alex's Caves nem acrescenta uma raiz mágica.
