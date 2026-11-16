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

## Evidência e próximo gate

[Auditor](alexscaves_1010_raygun_charge_ammo_flow_probe.py) · [testes sintéticos](alexscaves_1010_raygun_charge_ammo_flow_probe_test.py) · [workflow SHA-exato](../../.github/workflows/alexscaves-1010-raygun-charge-ammo-flow.yml).

A primeira CI deve **extrair o relatório**, não aprovar causalidade apenas por contagem. Após exame dos métodos, será possível selar os sítios individuais, distinguir os ramos elegíveis de `use` e documentar as condições na ficha do Raygun. Até lá, `static_perk_contract=NOT_CERTIFIED`, `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `mutation=NO_MUTATION` e provider não homologado integralmente.
