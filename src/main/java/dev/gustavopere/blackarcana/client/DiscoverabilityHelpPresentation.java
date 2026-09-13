package dev.gustavopere.blackarcana.client;

import net.minecraft.network.chat.Component;

import java.util.ArrayList;
import java.util.List;

/** Localized presentation composition for Stage 05.16 help surfaces. */
final class DiscoverabilityHelpPresentation {
    private DiscoverabilityHelpPresentation() { }

    static Component bindingValue(DiscoverabilityModel.BindingPresentation binding) {
        if (binding.unbound()) {
            return Component.translatable("help.black_arcana.binding.unbound");
        }
        return Component.literal(binding.currentLabel().orElseThrow());
    }

    static Component bindingLine(DiscoverabilityModel.BindingPresentation binding) {
        return Component.translatable(
                "help.black_arcana.binding.line",
                Component.translatable(binding.actionTranslationKey()),
                bindingValue(binding));
    }

    static List<Component> hintLines(DiscoverabilityModel.Hint hint) {
        List<Component> lines = new ArrayList<>();
        lines.add(Component.translatable(hint.topic() == DiscoverabilityModel.Topic.UNBOUND_EDITOR
                ? "help.black_arcana.hint.editor_unbound"
                : "help.black_arcana.hint.core"));
        lines.add(bindingLine(hint.bindings().radial()));
        lines.add(bindingLine(hint.bindings().castSelected()));
        lines.add(bindingLine(hint.bindings().editLoadout()));
        lines.add(Component.translatable("help.black_arcana.hint.quick_cast"));
        lines.add(Component.translatable("help.black_arcana.hint.reentry"));
        return List.copyOf(lines);
    }

    static List<Component> editorLines(DiscoverabilityModel.BindingSnapshot bindings) {
        long unboundQuickCasts = bindings.quickCasts().stream()
                .filter(DiscoverabilityModel.BindingPresentation::unbound)
                .count();
        List<Component> lines = new ArrayList<>();
        lines.add(Component.translatable("help.black_arcana.editor.core"));
        lines.add(bindingLine(bindings.radial()));
        lines.add(bindingLine(bindings.castSelected()));
        lines.add(bindingLine(bindings.editLoadout()));
        lines.add(Component.translatable(
                "help.black_arcana.editor.quick_cast_summary",
                bindings.quickCasts().size() - unboundQuickCasts,
                unboundQuickCasts));
        lines.add(Component.translatable("help.black_arcana.editor.authority"));
        lines.add(Component.translatable("help.black_arcana.editor.close"));
        return List.copyOf(lines);
    }
}
