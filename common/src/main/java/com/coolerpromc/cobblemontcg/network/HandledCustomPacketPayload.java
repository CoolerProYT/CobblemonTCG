package com.coolerpromc.cobblemontcg.network;

import com.coolerpromc.cobblemontcg.platform.util.PayloadContext;
import net.minecraft.network.protocol.common.custom.CustomPacketPayload;

public interface HandledCustomPacketPayload extends CustomPacketPayload {
    void handle(PayloadContext context);
}
