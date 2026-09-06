# Casos de teste candidatos — Blood

A reforma da escola Blood deve validar pelo menos:

- spell Blood nunca consome mana normal após o adapter hemático ser habilitado;
- sangue suficiente + mana zero pode passar o gate de recurso;
- mana cheia + nenhum sangue válido falha fechado;
- entidade `NO_BLOOD` não financia spell hemático;
- ownership/consentimento de fonte vinculada é respeitado;
- uma mesma reserva não pode financiar dois casts;
- rollback/refund é exato quando o cast não comita;
- múltiplos vínculos são resolvidos deterministicamente;
- remoção/morte/despawn da fonte invalida disponibilidade;
- contabilidade do reservatório é exata após restart/reload;
- não existe fallback que converta vital energy, soul, spirit ou mana em sangue;
- custo nativo atual do provider pode ser exibido na Wiki, mas não deve ser debitado após a reforma;
- spells Blood de addons permanecem fail-closed até adapter específico ser aprovado.
