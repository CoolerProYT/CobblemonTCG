package com.coolerpromc.cobblemontcg.network;

import com.coolerpromc.cobblemontcg.Constants;
import com.coolerpromc.cobblemontcg.menu.CardStandOwnerMenu;
import com.coolerpromc.cobblemontcg.platform.util.PayloadContext;
import net.minecraft.network.RegistryFriendlyByteBuf;
import net.minecraft.network.codec.ByteBufCodecs;
import net.minecraft.network.codec.StreamCodec;
import net.minecraft.network.protocol.common.custom.CustomPacketPayload;
import net.minecraft.world.item.ItemStack;

public record ServerboundSetStandPricePacket(int containerId, ItemStack item) implements HandledCustomPacketPayload {
    public static final Type<ServerboundSetStandPricePacket> TYPE = new Type<>(Constants.id("set_stand_price"));
    public static final StreamCodec<RegistryFriendlyByteBuf, ServerboundSetStandPricePacket> STREAM_CODEC = StreamCodec.composite(
            ByteBufCodecs.VAR_INT, ServerboundSetStandPricePacket::containerId,
            ItemStack.OPTIONAL_STREAM_CODEC, ServerboundSetStandPricePacket::item,
            ServerboundSetStandPricePacket::new
    );

    @Override
    public void handle(PayloadContext context) {
        context.execute(() -> {
            if (context.player().containerMenu instanceof CardStandOwnerMenu menu && menu.containerId == containerId && menu.stillValid(context.player())) {
                menu.setPriceItem(item);
            }
        });
    }

    @Override
    public Type<? extends CustomPacketPayload> type() {
        return TYPE;
    }
}
