package com.coolerpromc.cobblemontcg.component.custom;

import com.coolerpromc.cobblemontcg.tcg.set.SetDefinition;
import com.mojang.serialization.Codec;
import com.mojang.serialization.codecs.RecordCodecBuilder;
import io.netty.buffer.ByteBuf;
import net.minecraft.network.codec.ByteBufCodecs;
import net.minecraft.network.codec.StreamCodec;
import net.minecraft.resources.ResourceLocation;

public record BoosterPackData(ResourceLocation setId, String variant) {
    public static final Codec<BoosterPackData> CODEC = RecordCodecBuilder.create(instance -> instance.group(
            ResourceLocation.CODEC.fieldOf("set").forGetter(BoosterPackData::setId),
            Codec.STRING.optionalFieldOf("variant", SetDefinition.DEFAULT_WRAPPER).forGetter(BoosterPackData::variant)
    ).apply(instance, BoosterPackData::new));

    public static final StreamCodec<ByteBuf, BoosterPackData> STREAM_CODEC = StreamCodec.composite(
            ResourceLocation.STREAM_CODEC, BoosterPackData::setId,
            ByteBufCodecs.STRING_UTF8, BoosterPackData::variant,
            BoosterPackData::new
    );
}
