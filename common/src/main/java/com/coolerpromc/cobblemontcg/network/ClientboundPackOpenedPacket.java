package com.coolerpromc.cobblemontcg.network;

import com.coolerpromc.cobblemontcg.Constants;
import com.coolerpromc.cobblemontcg.platform.util.PayloadContext;
import io.netty.buffer.ByteBuf;
import net.minecraft.network.RegistryFriendlyByteBuf;
import net.minecraft.network.codec.ByteBufCodecs;
import net.minecraft.network.codec.StreamCodec;
import net.minecraft.network.protocol.common.custom.CustomPacketPayload;
import net.minecraft.resources.ResourceLocation;

import java.util.List;

/**
 * Tells the opening player what came out of a pack so the client can play the opening animation.
 * The cards are already in the player's inventory when this arrives; the animation is only a reveal.
 */
public record ClientboundPackOpenedPacket(ResourceLocation setId, String wrapper, List<Pull> cards, boolean sounds) implements HandledCustomPacketPayload {
    public static final Type<ClientboundPackOpenedPacket> TYPE = new Type<>(Constants.id("pack_opened"));

    public record Pull(int number, boolean holo) {
        public static final StreamCodec<ByteBuf, Pull> STREAM_CODEC = StreamCodec.composite(
                ByteBufCodecs.VAR_INT, Pull::number,
                ByteBufCodecs.BOOL, Pull::holo,
                Pull::new
        );
    }

    public static final StreamCodec<RegistryFriendlyByteBuf, ClientboundPackOpenedPacket> STREAM_CODEC = StreamCodec.composite(
            ResourceLocation.STREAM_CODEC, ClientboundPackOpenedPacket::setId,
            ByteBufCodecs.STRING_UTF8, ClientboundPackOpenedPacket::wrapper,
            Pull.STREAM_CODEC.apply(ByteBufCodecs.list()), ClientboundPackOpenedPacket::cards,
            ByteBufCodecs.BOOL, ClientboundPackOpenedPacket::sounds,
            ClientboundPackOpenedPacket::new
    );

    @Override
    public void handle(PayloadContext context) {
        context.execute(() -> ClientPacketHooks.packOpened.accept(this));
    }

    @Override
    public Type<? extends CustomPacketPayload> type() {
        return TYPE;
    }
}
