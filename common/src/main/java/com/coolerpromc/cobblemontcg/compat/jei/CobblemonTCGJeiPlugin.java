package com.coolerpromc.cobblemontcg.compat.jei;

import com.coolerpromc.cobblemontcg.Constants;
import com.coolerpromc.cobblemontcg.client.CardStandOwnerScreen;
import mezz.jei.api.IModPlugin;
import mezz.jei.api.JeiPlugin;
import mezz.jei.api.gui.handlers.IGhostIngredientHandler;
import mezz.jei.api.ingredients.ITypedIngredient;
import mezz.jei.api.registration.IGuiHandlerRegistration;
import net.minecraft.client.renderer.Rect2i;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.item.ItemStack;

import java.util.List;
import java.util.Optional;

@JeiPlugin
public class CobblemonTCGJeiPlugin implements IModPlugin {
    private static final ResourceLocation UID = Constants.id("jei_plugin");

    @Override
    public ResourceLocation getPluginUid() {
        return UID;
    }

    @Override
    public void registerGuiHandlers(IGuiHandlerRegistration registration) {
        registration.addGhostIngredientHandler(CardStandOwnerScreen.class, new StandPriceHandler());
        CardStandOwnerScreen.jeiPresent = true;
    }

    private static class StandPriceHandler implements IGhostIngredientHandler<CardStandOwnerScreen> {
        @Override
        public <I> List<Target<I>> getTargetsTyped(CardStandOwnerScreen screen, ITypedIngredient<I> ingredient, boolean doStart) {
            Optional<ItemStack> stack = ingredient.getItemStack();
            if (stack.isEmpty() || stack.get().isEmpty()) {
                return List.of();
            }
            Rect2i area = screen.priceArea();
            ItemStack item = stack.get();
            return List.of(new Target<>() {
                @Override
                public Rect2i getArea() {
                    return area;
                }

                @Override
                public void accept(I ignored) {
                    screen.setPriceItem(item);
                }
            });
        }

        @Override
        public void onComplete() {
        }
    }
}
