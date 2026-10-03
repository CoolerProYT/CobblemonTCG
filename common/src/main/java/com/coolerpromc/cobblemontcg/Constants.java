package com.coolerpromc.cobblemontcg;

import net.minecraft.resources.ResourceLocation;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class Constants {
	public static final String MODID = "cobblemontcg";
	public static final String MOD_NAME = "Cobblemon: TCG";
	public static final Logger LOG = LoggerFactory.getLogger(MOD_NAME);

	public static ResourceLocation id(String path){
		return ResourceLocation.fromNamespaceAndPath(MODID, path);
	}
}
