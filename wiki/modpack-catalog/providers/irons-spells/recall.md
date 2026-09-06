# Recall

- **Status no modpack:** PRESENTE — provider instalado
- **Provider:** Iron's Spells 'n Spellbooks
- **Mod ID:** `irons_spellbooks`
- **JAR/versão:** `irons_spellbooks-1.21.1-3.16.3.jar` / `1.21.1-3.16.3`
- **Escola:** Ender
- **Níveis:** 1
- **Raridade:** Uncommon
- **Cast:** Long
- **Cast time atual:** 5 s
- **Mana:** 100
- **Cooldown:** 300 s
- **Gate atual:** não pode ser castado em combate
- **Cast Time Reduction:** não reduz este cast

## O que faz

Teleporta o caster para o ponto de respawn configurado; quando esse ponto não existe, usa o spawn do mundo conforme a semântica pública do provider.

## Restrições atuais

O changelog oficial da linha atual registra três nerfs/regras que fazem parte do contrato vigente: Recall não pode mais ser castado durante combate, seu cast time foi aumentado de 4 s para 5 s e o spell deixou de ser afetado por Cast Time Reduction.

## Escalonamento

Spell de nível único. Distância máxima, regras cross-dimension, interação com beds/anchors e tratamento de destino inválido ficam `NÃO VERIFICADO` neste passe.

## Obtenção e aprendizado

Segue o pipeline geral de scrolls/spellbooks do Iron's. Fontes específicas de loot/crafting permanecem `NÃO VERIFICADO`.

## Deduplicação

Já cobre retorno mágico ao ponto de respawn. Uma futura magia de retorno Black Arcana precisa de destino/contrato distinto, não apenas outro nome ou VFX. Também não deve contornar silenciosamente o gate de combate ao reutilizar Recall por bridge.

## Authority / fail-closed

Iron's é authority do estado de combate e da admissão deste spell. Se uma bridge não consegue consultar/respeitar esse gate, ela deve falhar fechada em vez de executar um segundo teleporte por fora do provider.

## VFX / animação / áudio

`NÃO VERIFICADO` no runtime real do pack neste passe.

## Fonte / evidência

- Catálogo oficial atual: `https://iron.wiki/spells/`
- Changelog oficial atual: `https://iron.wiki/changelog/`
- Consulta: 2026-09-06.
