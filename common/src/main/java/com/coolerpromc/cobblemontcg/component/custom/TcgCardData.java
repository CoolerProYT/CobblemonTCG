package com.coolerpromc.cobblemontcg.component.custom;

import com.mojang.serialization.Codec;
import com.mojang.serialization.codecs.RecordCodecBuilder;
import io.netty.buffer.ByteBuf;
import net.minecraft.network.codec.ByteBufCodecs;
import net.minecraft.network.codec.StreamCodec;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.util.ExtraCodecs;

public record TcgCardData(ResourceLocation setId, int cardNumber, boolean holo) {
    public static final Codec<TcgCardData> CODEC = RecordCodecBuilder.create(instance -> instance.group(
            ResourceLocation.CODEC.fieldOf("set").forGetter(TcgCardData::setId),
            ExtraCodecs.POSITIVE_INT.fieldOf("number").forGetter(TcgCardData::cardNumber),
            Codec.BOOL.optionalFieldOf("holo", false).forGetter(TcgCardData::holo)
    ).apply(instance, TcgCardData::new));

    public static final StreamCodec<ByteBuf, TcgCardData> STREAM_CODEC = StreamCodec.composite(
            ResourceLocation.STREAM_CODEC, TcgCardData::setId,
            ByteBufCodecs.VAR_INT, TcgCardData::cardNumber,
            ByteBufCodecs.BOOL, TcgCardData::holo,
            TcgCardData::new
    );
}
