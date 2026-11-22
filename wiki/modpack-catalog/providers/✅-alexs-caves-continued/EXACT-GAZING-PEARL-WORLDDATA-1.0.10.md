# Gazing Pearl — ACWorldData reputação Deep One, descoberta transitiva 1.0.10

**Status:** 🟡 EM AUDITORIA; contrato da Gazing Pearl continua **⚠️ PARCIAL**, `static_contract=NOT_CERTIFIED`, `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `mutation=NO_MUTATION`. Este dossiê de suporte **não cria magia, cast, perk ou nova raiz semântica**, e não modifica o runtime.

## Fonte de autoridade

- Modlist sibling: `Gustavaopere/neoforge-rpg-skilltree/PROJECT-INSTRUCTIONS/modlist/World Gen/✅-alexs-caves-continued v1.0.10.md`, versão física `alexscaves-1.0.10-neoforge+1.21.1.jar`, mod id `alexscaves`, Minecraft/NeoForge 1.21.1; SHA-1 físico registrado `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`.
- Publisher JAR 1.0.10 previamente observado: 75.279.314 bytes, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`. A igualdade dos bytes da cópia instalada com a cópia publisher **NÃO VERIFICADA**.
- Caller confirmado pelo [relatório local da Gazing Pearl](EXACT-GAZING-PEARL-DISCOVERY-1.0.10.md): `GazingPearlItem.acInventoryTick` @44 invoca `ACWorldData.get(level)` e @83 invoca `ACWorldData.getDeepOneReputation(entity.getUUID())`. O snapshot é mantido na stack; não é a autoridade sobre reputação global.

## Descoberta read-only pendente de artefato

A [sonda SHA-exata](../../../../docs/qa/alexscaves_1010_gazing_pearl_worlddata_probe.py) e seu [workflow](../../../../.github/workflows/alexscaves-1010-gazing-pearl-worlddata-discovery.yml) vão enumerar métodos e campos nativos de `com/github/alexmodguy/alexscaves/server/level/storage/ACWorldData`, especialmente produtores/consumidores de reputação Deep One, e sites de invocação JVM de classes referenciadoras. A sonda exige os 1.555 classfiles do publisher, igualdade dos hashes do artefato e presença do caller @83; executa **somente `javap` e leitura ZIP**, não classes do mod.

**Nenhuma conclusão nova sobre setters, persistência, fórmula de reputação, SavedData, client sync ou permissão de perks é autorizada antes do relatório JAR e análise de cada body/caller.** O escopo da sonda limita-se a referências tipadas ao owner exato `ACWorldData` em classfiles no JAR publisher; consumidores por reflexão, mixins dinâmicos, datapacks, comandos, subclasses ou motores externos podem ficar de fora.

## Próximos gates

1. Executar CI e preservar report com hash, tamanho, classfile SHA, métodos + offsets, referências tipadas e sites de invoke.
2. Inspecionar o relatório para distinguir getter, mutação de reputação e armazenamento/serialização sem atribuir APIs ou semântica presumidas.
3. Adicionar manifesto/contrato técnico SHA-exato e checker fail-closed de invariantes e casos negativos, se as evidências sustentarem; reexecutar CI final.
4. Auditar canais client/servidor, SavedData e ciclo de vida; QA física e comparação da cópia instalada seguem **NOT_TESTED/NOT_VERIFIED**, sem promoção da ficha para ✅.

O Black Arcana mantém sua autoridade sobre o runtime mágico; RPG Skill Tree é somente sibling/provider de progressão. Sem hook nativo seguro por usuário: **NO_MUTATION / fail-closed**.
