package com.coolerpromc.cobblemontcg.platform.services;

import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.packs.resources.PreparableReloadListener;

public interface IReloadListenerRegistrar {
    void registerServerReloadListener(ResourceLocation id, PreparableReloadListener listener);
    void applyServerReloadListenerRegistrations(ReloadListenerRegistrar registrar);

    interface ReloadListenerRegistrar {
        void register(ResourceLocation id, PreparableReloadListener listener);
    }
}
