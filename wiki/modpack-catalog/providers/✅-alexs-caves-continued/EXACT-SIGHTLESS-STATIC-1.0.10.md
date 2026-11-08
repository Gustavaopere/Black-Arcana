# Sightless — auditoria técnica estática individual da versão 1.0.10

**Contrato individual delimitado:** `STATIC_TECHNICAL_CATALOG_ONLY`, `SHA_EXACT_BINARY_BEHAVIOR`. O [dossier](enchantments/sightless.md) documenta identidade, ativação, todos os efeitos específicos do encantamento, condições, geometria, custos, consumidores, estado e oportunidades/limites de perks. **Sem hook verificado (`NOT_VERIFIED`), QA física (`NOT_TESTED`) ou mutação (`NO_MUTATION`).** A conclusão do recorte estático depende da CI e não encerra o Totem completo nem o provider.

## Autoridade física e hashes

A modlist atual do `Gustavaopere/neoforge-rpg-skilltree` declara **`alexscaves-1.0.10-neoforge+1.21.1.jar`**, Minecraft 1.21.1 NeoForge, Java 21. O publisher JAR tem 75.279.314 bytes, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570` e SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`. O JSON `data/alexscaves/enchantment/sightless.json` possui 369 bytes e SHA-256 `1e7d093a0d459e2e6a29b40cd625b4fb1f990285343b53e4421c8f3727b2ecb9`. O item-tag do Totem tem SHA-256 `185a085206993877d91ca6d8c697273c14f945b1d55cb6179e3236c138c357cf`.

O [manifesto de evidências read-only](EXACT-SIGHTLESS-STATIC-1.0.10.json) fixa hashes de três classes, quatro resources selecionados (JSON, tag, `en_us`, `pt_br`), **1.555 classfiles examinados**, apenas dois classfiles com referência binária direta `SIGHTLESS` (`ACEnchantmentRegistry` e `TotemOfPossessionItem`) e **11 métodos de Totem** com descritores, digests completos e janelas causais esparsas. A classe `TotemOfPossessionItem.class` tem SHA-256 `bad9dd8b88eb621b558d1ede477d2b4ba6a21befdec31b4a0233adcac701773e`.

Os métodos de `TotemOfPossessionItem` com prova de corpo compilado integral incluem `use` (66 instruções), `onUseTick` (478), `releaseUsing` (29), `isEntityLookingAt` (70), `getControlledEntity` (44), `isBound`, `resetBound`, `getBoundEntityUUID`, `updateEntityIdFromServer`, `setPossessed` e `getUseDuration`. Os 478 elementos do corpo de `onUseTick` têm fingerprint `4d366c998c89884f53bc9554f52c6477c5c6bbb8e6aea1bf0f93867dc1b41d39`, igual à [prova anterior independente de Astral Transferring](EXACT-ASTRAL-TRANSFERRING-1.0.10.json). As âncoras já catalogadas em `EXACT-TECHNICAL-CONTRACTS-1.0.10.json` foram verificadas individualmente contra a mesma versão. O arquivo JSON publica apenas instruções relevantes para interoperabilidade, **não** exporta implementação integral de terceiros.

## Decisões observadas no bytecode publisher

| Decisão | Instruções e limites |
|---|---|
| Entrada | `use @83–150`: bound+alvo; helper de olhar com argumento **5D** `@99–102`; `SIGHTLESS @110`, `enchantLevel @113`, **`ifle @116→145`**. Início sem olhar requer `L>0`. Retornos separados `useConsume @141` / `usePass @147`. |
| Continuidade | `onUseTick @143–229`: bound/entidade; checagem de olhar `@158–161`; `SIGHTLESS @168`, nível `@171`, **`ifeq @174→203`**. Interrupção por falha de olhar exige **`L==0`**; controle de Player ainda depende do config `totemOfPossessionPlayers`. |
| Glow | No ramo `Mob` após navegação, `SIGHTLESS @409`, `enchantLevel @412`, **`ifle @415→424`**, `setGlowingTag(true) @420–421`. Logo glow só é solicitado por `L>0` nesse ramo; não generalizar para Player ou não-Mob. |
| Limpeza | `releaseUsing @8–19`: com entidade resolvida, solicita **`setGlowingTag(false)` @15–16**, sem guardar ou restaurar valor anterior. Também envia `UpdateItemTagMessage` do cliente `@20–38`, e solicita `stack.shrink(1)` quando dano atual alcança máximo `@42–54`. |
| Desgaste | `onUseTick @230–272`: `timeUsing % 2 == 0`, `Level.isClientSide()`, jogador não-criativo; chamada **`ItemStack.setDamageValue(getDamageValue()+1)`**. Isso só prova escrita no caminho cliente, não débito autoritativo do servidor. |
| Olhar | Helper `isEntityLookingAt`: `distanceTo × 0,1` ajusta a tolerância angular, consulta visão normalizada, produto escalar e **`hasLineOfSight`**; o predicado matemático de `@99–124` envolve divisão pelo comprimento do vetor. O literal 5D **não** define alcance de 5 blocos. |
| Bound / redes | `getControlledEntity` resolve `ControllingEntityID` (cliente) ou `BoundEntityUUID` (ServerLevel); `resetBound` remove ambos e `BoundEntityTag`. Não se conclui autorização segura da mensagem ou persistência da entidade. |
| Runtime irmão | O mesmo `onUseTick` executa navegação, ataque/transferência e branches de outros encantamentos. Sightless **não** deve ganhar contagem própria de cast, projectile, dano ou mana por coincidência do método. |

## Reexecução e perímetro de segurança

```bash
python3 docs/qa/alexscaves_1010_sightless_static_probe.py \
  --jar /caminho/alexscaves-1.0.10-neoforge+1.21.1.jar \
  --javap javap \
  --seal 'wiki/modpack-catalog/providers/✅-alexs-caves-continued/EXACT-SIGHTLESS-STATIC-1.0.10.json'
python3 docs/qa/alexscaves_1010_sightless_static_probe_test.py -v
python3 docs/qa/alexscaves_1010_sightless_cards_test.py -v
python3 scripts/catalog/check_perk_ready_indexes.py
python3 scripts/catalog/generate_perk_ready_indexes.py --check
```

O workflow `.github/workflows/alexscaves-1010-sightless-static.yml` baixa o JAR original e executa exatamente os gates de identidade, método, manifesto, regressão e índice. CI pré-merge não substitui o cliente/modpack real. Sem API/hook mutador verificado, **`NO_MUTATION` / fail-closed**; não alterar gameplay, Mastery, Stage ou dano. QA física pendente: PvP/claims, raio/LOS obstruído, alvo nulo/morto, permissões, glow previamente ativo, desgaste/sync cliente-servidor, interrupção, duração, detonação nativa, mensagens, troca de dimensão, unload e reconexão.
