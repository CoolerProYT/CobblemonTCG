package com.coolerpromc.cobblemontcg.network;

import com.coolerpromc.cobblemontcg.Constants;
import com.coolerpromc.cobblemontcg.platform.util.PayloadContext;
import com.coolerpromc.cobblemontcg.tcg.card.CardDefinition;
import com.coolerpromc.cobblemontcg.tcg.data.TcgDataManager;
import com.coolerpromc.cobblemontcg.tcg.set.SetDefinition;
import com.mojang.serialization.Codec;
import net.minecraft.network.RegistryFriendlyByteBuf;
import net.minecraft.network.codec.ByteBufCodecs;
import net.minecraft.network.codec.StreamCodec;
import net.minecraft.network.protocol.common.custom.CustomPacketPayload;
import net.minecraft.resources.ResourceLocation;

import java.util.List;
import java.util.Map;

public record ClientboundTcgDataSyncPacket(Map<ResourceLocation, SetDefinition> sets, Map<ResourceLocation, List<CardDefinition>> cards) implements HandledCustomPacketPayload {
    public static final Type<ClientboundTcgDataSyncPacket> TYPE = new Type<>(Constants.id("tcg_data_sync"));
    public static final StreamCodec<RegistryFriendlyByteBuf, ClientboundTcgDataSyncPacket> STREAM_CODEC = StreamCodec.composite(
            ByteBufCodecs.fromCodec(Codec.unboundedMap(ResourceLocation.CODEC, SetDefinition.CODEC)),
            ClientboundTcgDataSyncPacket::sets,
            ByteBufCodecs.fromCodec(Codec.unboundedMap(ResourceLocation.CODEC, CardDefinition.CODEC.listOf())),
            ClientboundTcgDataSyncPacket::cards,
            ClientboundTcgDataSyncPacket::new
    );

    public static ClientboundTcgDataSyncPacket fromServer() {
        return new ClientboundTcgDataSyncPacket(TcgDataManager.SERVER.rawSets(), TcgDataManager.SERVER.rawCards());
    }

    @Override
    public void handle(PayloadContext context) {
        context.execute(() -> TcgDataManager.CLIENT.replace(this.sets, this.cards));
    }

    @Override
    public Type<? extends CustomPacketPayload> type() {
        return TYPE;
    }
}
