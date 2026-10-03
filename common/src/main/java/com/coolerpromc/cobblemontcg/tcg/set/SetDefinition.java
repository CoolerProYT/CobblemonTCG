package com.coolerpromc.cobblemontcg.tcg.set;

import com.mojang.serialization.Codec;
import com.mojang.serialization.codecs.RecordCodecBuilder;
import net.minecraft.util.ExtraCodecs;

import java.util.List;
import java.util.Map;

/**
 * A card set as defined in {@code data/<namespace>/tcg/sets/<set>.json}.
 * {@code model_data_base} is the first {@code custom_model_data} value used by this set's cards,
 * see {@link com.coolerpromc.cobblemontcg.tcg.set.TcgSet#modelData}.
 * {@code wrapper_pokedex} maps a wrapper to the National Pokédex number of its mascot; the client
 * draws that species' Cobblemon model on the pack.
 */
public record SetDefinition(String name, int total, int modelDataBase, List<String> wrappers, List<PackSlot> packSlots,
                            Map<String, Integer> wrapperPokedex) {
    public static final String DEFAULT_WRAPPER = "default";

    public static final Codec<SetDefinition> CODEC = RecordCodecBuilder.create(instance -> instance.group(
            Codec.STRING.fieldOf("name").forGetter(SetDefinition::name),
            ExtraCodecs.POSITIVE_INT.fieldOf("total").forGetter(SetDefinition::total),
            ExtraCodecs.POSITIVE_INT.fieldOf("model_data_base").forGetter(SetDefinition::modelDataBase),
            Codec.STRING.listOf().optionalFieldOf("wrappers", List.of(DEFAULT_WRAPPER)).forGetter(SetDefinition::wrappers),
            PackSlot.CODEC.listOf().fieldOf("pack_slots").forGetter(SetDefinition::packSlots),
            Codec.unboundedMap(Codec.STRING, ExtraCodecs.POSITIVE_INT).optionalFieldOf("wrapper_pokedex", Map.of()).forGetter(SetDefinition::wrapperPokedex)
    ).apply(instance, SetDefinition::new));

    public int packSize() {
        return packSlots.stream().mapToInt(PackSlot::count).sum();
    }
}
