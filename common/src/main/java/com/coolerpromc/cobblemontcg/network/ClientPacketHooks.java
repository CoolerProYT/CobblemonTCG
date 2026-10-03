package com.coolerpromc.cobblemontcg.network;

import java.util.function.Consumer;

/**
 * Client-side reactions to packets. Common code only sees these plain callbacks; the client entry
 * point fills them in, so no client class is ever referenced from a server path.
 */
public final class ClientPacketHooks {
    public static Consumer<ClientboundPackOpenedPacket> packOpened = packet -> {
    };

    private ClientPacketHooks() {
    }
}
