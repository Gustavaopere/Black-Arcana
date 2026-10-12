# Slime Aspect — Backported Spellbooks

- **ID estático exato:** `backportedspellbooks:slime_aspect`
- **Classe do JAR físico:** `net.redreaper.backported_spellbooks.spells.nature.AspectOfTheSlimeSpell`
- **Registry:** `ModSpellRegistry.SLIME_ASPECT`
- **JAR certificado:** `backportedspellbooks-0.1.2.jar` (metadata embutido `0.1.0`)
- **Evidência:** ✅ `COUNTED_EXACT` para registro estático no [dossiê 0.1.2](../EXACT-BINARY-SPELLS-0.1.2.md); não é PASS de gameplay

## Comportamento documentado (fonte de referência)

Status effect Slime Aspect e interações de mobilidade (source de referência); impulse, air drag, bounce e parâmetros efetivos ainda não certificados no JAR 0.1.2 ou no jogo.

A descrição de gameplay é uma leitura limitada da fonte oficial [`@07cb65efca0c`](https://github.com/RedReaper28/BackportedSpellbooks-1.21.1/tree/07cb65efca0c264762a21c2d6bce0f83e3947226), não uma garantia de bytecode funcional exato ou configuração do pack.

## Contratos e pendências

- **Authority:** Iron's para cast, mana, cooldown; addon para efeitos/projéteis; Black Arcana não replica o settlement.
- **⚠️ Não verificados no modpack:** parâmetros finais de dano/mana/cooldown, targeting, friendly-fire/PvP, duração, rareza, nível máximo efetivo, aquisição, sincronização MP e Survival.
- **Deduplicação:** esta identidade já estava contada antes da prova; **+0** novas magias.

