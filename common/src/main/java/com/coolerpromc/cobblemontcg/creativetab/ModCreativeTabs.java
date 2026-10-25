package com.coolerpromc.cobblemontcg.creativetab;

import com.coolerpromc.cobblemontcg.Constants;
import com.coolerpromc.cobblemontcg.block.ModBlocks;
import com.coolerpromc.cobblemontcg.component.ModDataComponents;
import com.coolerpromc.cobblemontcg.component.custom.BoosterPackData;
import com.coolerpromc.cobblemontcg.item.ModItems;
import com.coolerpromc.cobblemontcg.platform.Services;
import com.coolerpromc.cobblemontcg.platform.util.CreativeTabOutput;
import com.coolerpromc.cobblemontcg.platform.util.RegistryHandler;
import com.coolerpromc.cobblemontcg.tcg.card.CardDefinition;
import com.coolerpromc.cobblemontcg.tcg.data.TcgDataManager;
import com.coolerpromc.cobblemontcg.tcg.set.TcgSet;
import com.coolerpromc.cobblemontcg.util.TcgStacks;
import net.minecraft.core.component.DataComponents;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.item.CreativeModeTab;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.component.CustomModelData;

import java.util.ArrayList;
import java.util.List;
import java.util.Set;
import java.util.stream.Collectors;

public class ModCreativeTabs {
    private record ShippedSet(String path, String iconWrapper, int modelDataBase) {
        ResourceLocation id() {
            return Constants.id(path);
        }
    }

    private static final List<ShippedSet> SHIPPED = List.of(
            new ShippedSet("base1", "charizard", 1000),
            new ShippedSet("base2", "scyther", 2000),
            new ShippedSet("base3", "aerodactyl", 4000),
            new ShippedSet("base4", "mewtwo", 5000),
            new ShippedSet("base5", "dark_charizard", 6000),
            new ShippedSet("basep", "pikachu", 3000));
    private static final Set<ResourceLocation> SHIPPED_IDS = SHIPPED.stream().map(ShippedSet::id).collect(Collectors.toSet());

    public static final RegistryHandler<CreativeModeTab, CreativeModeTab> TAB = Services.REGISTRY.registerCreativeTab(Constants.MODID, ModItems.BOOSTER_PACK::toStack, Component.translatable("itemGroup." + Constants.MODID), (output, parameters) -> {
        output.accept(ModItems.CARD_BINDER.toStack());
        output.accept(ModBlocks.CARD_DEALER_TABLE_ITEM.toStack());
        output.accept(ModBlocks.CARD_DISPLAY_STAND_ITEM.toStack());
        for (TcgSet set : TcgDataManager.forDisplay().sets()) {
            if (!SHIPPED_IDS.contains(set.id())) {
                addSet(output, set);
            }
        }
    });

    public static final List<RegistryHandler<CreativeModeTab, CreativeModeTab>> SET_TABS = registerSetTabs();

    private static List<RegistryHandler<CreativeModeTab, CreativeModeTab>> registerSetTabs() {
        List<RegistryHandler<CreativeModeTab, CreativeModeTab>> tabs = new ArrayList<>();
        for (ShippedSet shipped : SHIPPED) {
            tabs.add(Services.REGISTRY.registerCreativeTab(Constants.MODID + "_" + shipped.path(), () -> icon(shipped),
                    Component.translatable("itemGroup." + Constants.MODID + "." + shipped.path()),
                    (output, parameters) -> TcgDataManager.forDisplay().set(shipped.id()).ifPresent(set -> addSet(output, set))));
        }
        return List.copyOf(tabs);
    }

    private static ItemStack icon(ShippedSet shipped) {
        ItemStack stack = ModItems.BOOSTER_PACK.toStack();
        stack.set(ModDataComponents.BOOSTER_PACK.get(), new BoosterPackData(shipped.id(), shipped.iconWrapper()));
        stack.set(DataComponents.CUSTOM_MODEL_DATA, new CustomModelData(shipped.modelDataBase()));
        return stack;
    }

    private static void addSet(CreativeTabOutput output, TcgSet set) {
        for (String wrapper : set.wrappers()) {
            output.accept(TcgStacks.pack(set, wrapper, 1));
        }
        for (CardDefinition card : set.cards()) {
            output.accept(TcgStacks.card(set, card.number(), card.rarity().isHolo()));
        }
    }

    public static List<RegistryHandler<CreativeModeTab, CreativeModeTab>> all() {
        List<RegistryHandler<CreativeModeTab, CreativeModeTab>> tabs = new ArrayList<>();
        tabs.add(TAB);
        tabs.addAll(SET_TABS);
        return tabs;
    }

    public static void init(){
        Constants.LOG.info("Registering creative tabs.");
    }
}
