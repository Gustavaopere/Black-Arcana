# Aeropic — prova conservadora do produtor de receiver JVM

**Estado:** 🟡 aguardando análise do JAR congelado Wind's 1.0.5. **Não implementa integração, cast nem perks.**

## Contexto verificado

- Modlist sibling RPG Skill Tree: `wind_spellbooks-1.0.5.jar` (posição 571), host `irons_spellbooks-1.21.1-3.16.3.jar` (342), `ironsable-wind-1.0.0.jar` (345). SHA-1 do JAR Wind's publicado `8744886899bc245ae147a44baa2b183689cec7da`.
- PR #892 trouxe duas vizinhanças de `AeropicEffect.invokevirtual AbstractSpell.getRecastCount(int, LivingEntity)`: `onEffectAdded` inclui `ACROBATICS_SPELL`/`Supplier.get`/`checkcast AbstractSpell`; `applyEffectTick` inclui `PlayerRecasts`/`RecastInstance` próximo ao invoke.
- A campanha host PR #891 verificou ABI publicada Iron's 3.16.3, não igualdade com o binário local.

## Prova de fluxo suportada

O auditor `docs/qa/winds_105_aeropic_supplier_receiver_slice.py` faz **somente** um recorte direto de cinco instruções produtoras imediatamente anteriores ao `invokevirtual`: `getstatic ModSpellRegistry.ACROBATICS_SPELL: Supplier` → `invokeinterface Supplier.get(): Object` → `checkcast AbstractSpell` → carga de argumento inteiro → carga de `LivingEntity` → `invokevirtual AbstractSpell.getRecastCount`.

Para declarar **`COMPILED_ACROBATICS_SPELL_SUPPLIER_GET_CAST_TO_ABSTRACTSPELL`**, todas as instruções devem existir exatamente na sequência, sem saltos para o interior da janela e com owner, field e descriptor exatos. Se houver qualquer passo adicional, origem alternativa, salto ou transformação, a classificação retorna `NOT_PROVEN`. Nenhum caminho alternativo é inferido.

**Nota de segurança:** mesmo que essa sequência seja confirmada, só comprova o **valor de retorno do Supplier, após conversão estática para AbstractSpell, como operando receiver da chamada JVM naquele caminho compilado**. Não prova que o Supplier produz `AeropicSpell`, que aquela rota executa no cliente, que o override seja escolhido ou que exista um hook autorizado para o RPG Skill Tree.

Um padrão adjacente `iconst_1, iadd` após o invoke, se encontrado, só comprova a **operação aritmética local de incremento**, não que o número chega a NBT ou `PlayerRecasts`. Qualquer consumo final permanece `NOT_PROVEN`. O recorte não executa o JAR nem publica instruções completas/offsets.

## Acceptance

- Onze testes sintéticos com fail-closed para owner JVM, field e descriptor, branch de entrada, overload, offset duplicado e afirmações de recast/hook.
- Rodar scanner somente no JAR do publicador com SHA-1 congelado, inspecionar artefato JSON antes de documentar o resultado na ficha de Aeropic.
- CI focal + Black Arcana CI (`verify` e companion QA) no SHA final. Revalidar `main`, diff e trabalho simultâneo de outros PRs antes de merge.
- Zero mudanças em Java, runtime, `PlayerRecasts`, atributos, hooks, configs, balanceamento ou Stages.
- **⛔ `SEM_HOOK_SEGURO`** até contrato provider-native e QA físico. Stage 06.05 🟡; Stage 09 real-client pendente. Catálogo Wind's 7/7 spells, 9/9 getters selecionados, identidade binária geral 38/39, global ≥1.856 objetos e denominador desconhecido.

## Segundo gate: pilha simbólica restrita a bloco

Quando a sequência exata de cinco instruções não existe (resultado **`NOT_PROVEN`** no CI #40156210481), `docs/qa/winds_105_aeropic_stack_slice.py` faz uma tentativa adicional **sem presumir resultado positivo**: localiza a última leitura de `ModSpellRegistry.ACROBATICS_SPELL` anterior a cada invocação e modela no máximo 72 instruções dentro de um bloco sem desvio/entrada alternativa.

O intérprete acompanha apenas operações JVM suportadas, descritores integrais de chamadas e transferência de um token simbólico `ACROBATICS_SPELL_SUPPLIER_GET_RESULT` por `checkcast AbstractSpell`; diferencia chamadas intermediárias, duplicação simples e loads/stores de índices explícitos. Falha fechada para opcodes desconhecidos, fluxo de controle não linear, saltos para o interior do segmento, valores de locais genéricos sem índice e contagens inesperadas de chamadas.

Somente a presença desse token na posição **receiver efetiva** do `invokevirtual AbstractSpell.getRecastCount` permite declarar `COMPILED_SUPPLIER_GET_CAST_RECEIVER` **no bytecode compilado**. Nem mesmo tal resultado resolveria o tipo concreto devolvido pelo `Supplier`, dispatch em jogo, chamada do override ou destino do retorno. Todo campo relacionado a PlayerRecasts e hooks permanece `NOT_PROVEN`.

Há **12 testes sintéticos adicionais** para fontes válidas, chamadas intermediárias, classes/tipos incorretos, saltos, opcodes desconhecidos e não promoção de runtime. O workflow inclui o JSON `aeropic-jvm-stack-slice.json` no mesmo artefato, sem publicar bytecode ou offsets.
