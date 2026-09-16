# Goety Cataclysm 1.21.1-1.8.2 — auditoria técnica e provenance

## Identidade física

A modlist corrente fixa:

- `goety_cataclysm-1.21.1-1.8.2.jar`
- mod ID `goety_cataclysm`
- runtime `1.21.1-1.8.2`
- SHA-1 `4e3052a082200371b36e1a88fdce05e294d82757`
- CurseForge fingerprint `588833616`

A publicação oficial fixa:

- CurseForge project `1224214`;
- file `8518940`;
- NeoForge;
- Minecraft 1.21.1;
- release publicada em 2026-07-27;
- tamanho público aproximado de 1.7 MB;
- projeto `All Rights Reserved`;
- changelog público da build: `First 1.21.1 release!`.

## Provenance do source

O projeto oficial fornece link para `Polarice3/Goety_Cataclysm`, porém o repositório público auditável não corresponde à build instalada:

- única branch pública observada: `master`;
- head auditado: `ae0277177a866c4b689600dddfe14359573903a8`;
- `gradle.properties` nesse head: Minecraft `1.20.1`, `mod_version=1.20-1.9.1`;
- nenhum commit público retornado no intervalo 2026-07-20..2026-08-01.

Conclusão: **não existe, na evidência pública localizada, um pin de source que possa ser tratado como implementação exata de `1.21.1-1.8.2`.**

## Consequência clean-room

Como a build exata não possui revisão pública correspondente localizada e o projeto declara ARR:

1. não decompilar bytecode para reconstruir implementação;
2. não copiar assets, textos ou modelos;
3. não transportar internals do branch 1.20.1 para 1.21.1;
4. não derivar hooks, registries, signatures ou comportamento transacional de versões diferentes;
5. usar apenas identidade física, publicação/changelog oficial e descrição pública para classificação semântica.

## Superfície semanticamente confirmada

Confirmado publicamente:

- addon de compatibilidade Goety ↔ L_Ender's Cataclysm;
- acesso a spells/abilities inspirados em monstros poderosos do Cataclysm;
- client + server;
- build NeoForge 1.21.1 correspondente ao artefato instalado.

Confirmado pelo guia canônico do modpack, sem promoção a detalhes internos:

- integração participa de Soul Energy/Focus/summon/servant do Goety;
- não constitui provider autônomo de mana/casting paralelo.

## Não confirmado na build exata

- contagem e nomes completos de Focuses/spells;
- registry IDs;
- recipes e ritual types;
- servant types e ownership implementation;
- acquisition/progression gates;
- Soul Energy costs;
- cooldown, cast time, potency, duration e targeting;
- eventos/hooks de cast;
- lifecycle de summons/servants;
- datapack tags/registries consumíveis por Black Arcana;
- APIs públicas ou extension points estáveis.

Todos esses campos são `UNVERIFIED / FAIL-CLOSED`.

## Critério para promoção futura

Uma promoção para `GRANULAR CATALOG COMPLETE` requer pelo menos uma das seguintes evidências:

- source oficial publicamente identificável que corresponda exatamente à build `1.21.1-1.8.2` e cuja licença permita o uso pretendido; ou
- documentação oficial pública que enumere integralmente as superfícies necessárias; ou
- API/provider contract oficialmente publicado para essa versão.

Validação real em runtime continua separada mesmo após eventual source/catalog completion.
