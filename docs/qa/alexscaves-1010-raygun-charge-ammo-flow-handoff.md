# Raygun 1.0.10 — ativação, recarga e fluxo de munição (descoberta SHA-exata)

**Protocolo:** a versão publisher `alexscaves-1.0.10-neoforge+1.21.1.jar` é a referência física, fixada pelo SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c` e classe `RaygunItem.class` SHA-256 `3fc60cb7ff8be2744becf8ac9e524799349996972708845a124f02650bfb344c`.

**Contrato desta etapa:** extração read-only de oito métodos previamente inventariados no [selo integral de 26 métodos](../../wiki/modpack-catalog/providers/✅-alexs-caves-continued/EXACT-RAYGUN-ALL-METHODS-1.0.10.json), com **168 instruções JVM** e **15 branches diretos**. Não há hook mutador; o objeto `damage-types/raygun` permanece ⚠️ parcial. Registra apenas fingerprints de métodos, desvios e sítios simbólicos. Não redistribui o código de terceiros.

## Hipóteses a testar contra o JAR

- Ativação: diferenciar `RaygunItem.use` de `onUseTick`; a transição entre `hasCharge`, `findAmmo`, `isCreative`, `isEmpty`, débito eventual de munição e `setCharge` requer sequência JVM causal.
- Munição: `findAmmo` e `lambda$static$0` devem ser tratados como produtores/consumidores distintos. Identidade física esperada: item associado a `URANIUM_ROD`, sujeito a conferência de classfile.
- Carga: `hasCharge` faz seleção em relação ao limiar `1000` e `getCharge`/`setCharge` observam `ChargeUsed`; não presumir clamp, rejeição de valor negativo, antirreplay ou autoridade de servidor.
- Encerramento: `releaseUsing` alcança uma chamada C2S de atualização de tags condicionada ao lado, sem comprovar aceitação, autorização de `entityId` ou saneamento de `CUSTOM_DATA`.
- Duração: `getUseDuration` contém o literal `72000`; isso não é um cooldown de perk.
- Fluxos de `ENERGY_EFFICIENCY`, `SOLAR` e `X_RAY` permanecem nos respectivos certificados/sondas. Não promover sua validade a partir da semelhança de métodos.

## Contrato causal selecionado — oito métodos nativos e 15 branches

O [manifesto JVM SHA-exato](../../wiki/modpack-catalog/providers/✅-alexs-caves-continued/EXACT-RAYGUN-CHARGE-AMMO-FLOW-1.0.10.json) foi extraído do JAR publisher 1.0.10 pela [PR #1101](https://github.com/Gustavaopere/Black-Arcana/pull/1101). Ele sela **8 métodos completos por fingerprints**, **168 instruções JVM** e **15 branches diretos**, com opcode e até três instruções antecessoras de contexto por desvio. A reprodução exige a identidade física do JAR, da classe e de todos os 26 métodos anteriormente selados.

- **Limiar:** `hasCharge` chama `getCharge @1` e compara com `1000 @4`; `if_icmpge @7→14` seleciona falso para inteiro igual/maior que 1000. O predicado local é `ChargeUsed < 1000`, sem prova de clamp inferior.
- **Uso:** `use` chama `hasCharge @9`; `ifeq @12→41` direciona falta de carga para recarga. Caso contrário, `Player.startUsingItem @17` e `ACCompat.useConsume @37` pertencem à via de uso.
- **Recarga:** `findAmmo @43`, `Player.isCreative @49`, `ItemStack.isEmpty @56` e `ifne @59→71` precedem o ramo não vazio com `ItemStack.shrink(1) @65`; a flag local é marcada com `iconst_1/istore 6 @68–69`. `iload 6 @71; ifeq @73→125` diferencia elegibilidade e falha. No caminho elegível `setCharge(...,0) @79` reinicia a marca de carga; sons de recarga/vazio e `ACCompat.useFail @167` pertencem a ramos diferentes. O débito de uma unidade é potencial por recarga elegível, **não por tick de raio**.
- **Munição:** `findAmmo` possui ramo criativo (`Player.isCreative @1; ifeq @4→11`) que devolve `EMPTY`; a via comum percorre `Inventory.getContainerSize @18` e `Inventory.getItem @29` com `Predicate.test(AMMO) @37`, `ifeq @42→47` e loop `goto @50→13`. `lambda$static$0` compara `ItemStack.getItem @1` a `ACBlockRegistry.URANIUM_ROD` convertido por `Block.asItem @15` e `if_acmpne @18→25`. Criativo não é falha automática, porque `use` usa uma flag separada.
- **Tags:** `getCharge` usa `ACCompat.getTag @1`, `ifnull @6→19` e, se existir tag, consulta `ChargeUsed` via `ACCompat.getInt @13`. `setCharge` grava inteiro com `CompoundTag.putInt @10` e `ACCompat.setTag @15`. O setter nativo de onze instruções **não contém clamp próprio observado**; não inferir ausência de saneamento externo.
- **Duração e encerramento:** `getUseDuration` retorna 72000, não cooldown. `releaseUsing` chama `Item.releaseUsing @6`, testa `Level.isClientSide @10` e `ifeq @13→31`; só na via cliente produz `UpdateItemTagMessage @25` e `sendMSGToServer @28`. `clearSoundCacheFor @35` é rotina distinta.

**Limites:** a evidência não atesta autorização servidor de `ChargeUsed`/`CUSTOM_DATA`/`entityId`, antirreplay, persistência física, ataques aceitos, LOS, PvP/claims, custos por tick de `onUseTick` nem hook mutador. O Raygun permanece **⚠️ parcial** e `NO_MUTATION`.

A primeira CI corrigida verificou **6 testes sintéticos**, SHA-256 do publisher e 544 índices/2.393 fichas candidatas sem erros. O HEAD final passa a usar `--snapshot`; seus testes e CI devem ser confirmados separadamente.

## Evidência e próximo gate

[Auditor](alexscaves_1010_raygun_charge_ammo_flow_probe.py) · [testes sintéticos](alexscaves_1010_raygun_charge_ammo_flow_probe_test.py) · [workflow SHA-exato](../../.github/workflows/alexscaves-1010-raygun-charge-ammo-flow.yml).

A primeira CI extraiu os ramos e o HEAD final fixa o snapshot comparável ao JAR; o objeto continua parcial até fechar os consumidores restantes. Até lá, `static_perk_contract=NOT_CERTIFIED`, `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `mutation=NO_MUTATION` e provider não homologado integralmente.
