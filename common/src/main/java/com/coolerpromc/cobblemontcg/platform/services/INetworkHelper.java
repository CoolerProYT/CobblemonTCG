package com.coolerpromc.cobblemontcg.platform.services;

import net.minecraft.network.protocol.common.custom.CustomPacketPayload;
import net.minecraft.server.level.ServerPlayer;

public interface INetworkHelper {
    <T extends CustomPacketPayload> void sendToPlayer(ServerPlayer player, T packet);
}
