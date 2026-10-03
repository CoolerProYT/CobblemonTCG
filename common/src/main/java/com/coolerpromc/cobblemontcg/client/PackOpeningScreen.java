package com.coolerpromc.cobblemontcg.client;

import com.coolerpromc.cobblemontcg.Constants;
import com.coolerpromc.cobblemontcg.config.TcgClientConfig;
import com.coolerpromc.cobblemontcg.item.ModItems;
import com.coolerpromc.cobblemontcg.network.ClientboundPackOpenedPacket;
import com.coolerpromc.cobblemontcg.sound.ModSounds;
import com.coolerpromc.cobblemontcg.tcg.card.CardDefinition;
import com.coolerpromc.cobblemontcg.tcg.card.CardRarity;
import com.coolerpromc.cobblemontcg.tcg.data.TcgDataManager;
import com.coolerpromc.cobblemontcg.tcg.set.TcgSet;
import com.coolerpromc.cobblemontcg.util.TcgStacks;
import com.mojang.math.Axis;
import net.minecraft.ChatFormatting;
import net.minecraft.Util;
import net.minecraft.client.Minecraft;
import net.minecraft.client.gui.GuiGraphics;
import net.minecraft.client.gui.screens.Screen;
import net.minecraft.client.resources.sounds.SimpleSoundInstance;
import net.minecraft.network.chat.Component;
import net.minecraft.sounds.SoundEvent;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.util.Mth;
import net.minecraft.world.item.ItemStack;
import org.lwjgl.glfw.GLFW;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

/**
 * Pack opening animation: the pack drops in, tears open, and the cards are swiped away one by one,
 * commons first and the rare last like a real pack. Ends on a summary of every pull.
 * Purely visual; the server has already given the cards.
 */
public class PackOpeningScreen extends Screen {
    private static final String KEY = "screen." + Constants.MODID + ".pack_opening.";
    private static final long PACK_IN_MS = 380;
    private static final long TEAR_MS = 900;
    private static final long FLY_MS = 280;
    private static final float SWIPE_DISTANCE = 50.0F;

    private enum Phase { PACK, TEARING, REVEAL, SUMMARY }

    private record Reveal(ItemStack stack, CardRarity rarity, boolean holo) {
    }

    private record Flying(ItemStack stack, float x, float y, float rot, float dir, long start) {
    }

    private final ItemStack pack;
    private final ItemStack cardBack = new ItemStack(ModItems.TCG_CARD);
    private final List<Reveal> reveals;
    private final boolean sounds;
    private final List<Flying> flying = new ArrayList<>();

    private Phase phase = Phase.PACK;
    private long phaseStart = Util.getMillis();
    private long revealStart = Util.getMillis();
    private int index;
    private boolean dragging;
    private boolean moved;
    private double pressX;
    private double pressY;
    private float dragX;
    private float dragY;

    private PackOpeningScreen(ItemStack pack, List<Reveal> reveals, boolean sounds) {
        super(Component.translatable(KEY + "title"));
        this.pack = pack;
        this.reveals = reveals;
        this.sounds = sounds;
    }

    /**
     * Shows the animation for a pack the server just opened, or only plays the sounds when the
     * animation is turned off in the client config.
     */
    public static void show(ClientboundPackOpenedPacket packet) {
        Minecraft minecraft = Minecraft.getInstance();
        Optional<TcgSet> set = TcgDataManager.CLIENT.set(packet.setId());
        boolean holo = packet.cards().stream().anyMatch(ClientboundPackOpenedPacket.Pull::holo);

        if (set.isEmpty() || !TcgClientConfig.animationEnabled() || minecraft.player == null) {
            if (packet.sounds()) {
                play(holo ? ModSounds.BOOSTER_PACK_OPEN_RARE.get() : ModSounds.BOOSTER_PACK_OPEN.get(), 1.0F);
            }
            return;
        }

        // Rolled order is rare, uncommons, commons; a real pack is opened from the back, rare last.
        List<Reveal> reveals = new ArrayList<>();
        List<ClientboundPackOpenedPacket.Pull> pulls = packet.cards();
        for (int i = pulls.size() - 1; i >= 0; i--) {
            ClientboundPackOpenedPacket.Pull pull = pulls.get(i);
            CardRarity rarity = set.get().card(pull.number()).map(CardDefinition::rarity).orElse(CardRarity.COMMON);
            reveals.add(new Reveal(TcgStacks.card(set.get(), pull.number(), pull.holo()), rarity, pull.holo()));
        }
        minecraft.setScreen(new PackOpeningScreen(TcgStacks.pack(set.get(), packet.wrapper(), 1), reveals, packet.sounds()));
    }

    // ------------------------------------------------------------------ layout

    private float cardHeight() {
        return Math.min(height * 0.62F, 190.0F);
    }

    private float centerX() {
        return width / 2.0F;
    }

    private float centerY() {
        return height / 2.0F - 10.0F;
    }

    // ------------------------------------------------------------------ render

    @Override
    public void render(GuiGraphics graphics, int mouseX, int mouseY, float partialTick) {
        super.render(graphics, mouseX, mouseY, partialTick);
        long now = Util.getMillis();
        switch (phase) {
            case PACK -> renderPack(graphics, now);
            case TEARING -> renderTear(graphics, now);
            case REVEAL -> renderReveal(graphics, now);
            case SUMMARY -> renderSummary(graphics, mouseX, mouseY);
        }
        renderFlying(graphics, now);
    }

    private void renderPack(GuiGraphics graphics, long now) {
        float t = Mth.clamp((now - phaseStart) / (float) PACK_IN_MS, 0, 1);
        float scale = easeOutBack(t);
        float bob = (float) Math.sin(now / 300.0) * 2.0F;
        float wiggle = (float) Math.sin(now / 160.0) * 1.5F;
        drawItem(graphics, pack, centerX(), centerY() + bob, wiggle, cardHeight() * 1.1F * scale, 100);
        if (t >= 1 && (now / 500) % 2 == 0) {
            label(graphics, Component.translatable(KEY + "open"), centerY() + cardHeight() * 0.62F + 6, 0xFFFFFF);
        }
    }

    private void renderTear(GuiGraphics graphics, long now) {
        float t = Mth.clamp((now - phaseStart) / (float) TEAR_MS, 0, 1);
        float size = cardHeight() * 1.1F;
        float packTop = centerY() - size / 2;

        if (t < 0.25F) {  // shake
            float shake = (float) Math.sin(t * 90) * 5.0F * (1 - t * 2);
            drawItem(graphics, pack, centerX(), centerY(), shake, size, 100);
            return;
        }
        float u = (t - 0.25F) / 0.75F;

        // the cards rise out of the pack
        float rise = easeOutCubic(Math.min(1, u * 1.3F));
        drawItem(graphics, cardBack, centerX(), centerY() + (1 - rise) * size * 0.35F, 0, cardHeight(), 60);

        // the pack drops away
        drawItem(graphics, pack, centerX(), centerY() + easeInCubic(u) * height, 0, size, 100);

        // the torn-off top strip flies up and fades
        float stripW = size * 0.66F;
        float stripH = size * 0.09F;
        float sy = packTop - easeOutCubic(u) * 70.0F;
        int alpha = (int) (255 * (1 - u));
        graphics.pose().pushPose();
        graphics.pose().translate(centerX() + u * 30.0F, sy + stripH / 2, 300);
        graphics.pose().mulPose(Axis.ZP.rotationDegrees(u * 28.0F));
        graphics.fill((int) (-stripW / 2), (int) (-stripH / 2), (int) (stripW / 2), (int) (stripH / 2), alpha << 24 | 0xC8C8D2);
        for (int x = (int) (-stripW / 2); x < stripW / 2; x += 3) {
            graphics.fill(x, (int) (-stripH / 2), x + 1, (int) (stripH / 2), alpha << 24 | 0x8C8C9A);
        }
        graphics.pose().popPose();

        if (t >= 1) {
            startReveal();
        }
    }

    private void renderReveal(GuiGraphics graphics, long now) {
        if (index >= reveals.size()) {
            return;
        }
        float h = cardHeight();
        Reveal top = reveals.get(index);

        // rarity glow behind the top card
        if (top.holo() || top.rarity() == CardRarity.RARE) {
            float grow = easeOutCubic(Mth.clamp((now - revealStart) / 400.0F, 0, 1));
            int color = top.holo() ? 0xFFD54A : 0x7FD0FF;
            rays(graphics, centerX(), centerY(), h * 0.85F * grow, now / 40.0F, color, top.holo() ? 16 : 10);
        }

        // the rest of the pile, face down
        int behind = Math.min(3, reveals.size() - index - 1);
        for (int i = behind; i >= 1; i--) {
            drawItem(graphics, cardBack, centerX() + i * 3.0F, centerY() + i * 3.0F, 0, h, 40 + (3 - i) * 10);
        }

        drawItem(graphics, top.stack(), centerX() + dragX, centerY() + dragY, dragX * 0.08F, h, 120);

        float textY = centerY() + h / 2 + 6;
        label(graphics, top.stack().getHoverName(), textY, 0xFFFFFF);
        Component rarity = Component.translatable(top.rarity().translationKey()).withStyle(top.rarity().color());
        if (top.holo() && !top.rarity().isHolo()) {
            rarity = Component.empty().append(rarity).append(Component.literal("  ")).append(Component.translatable(KEY + "holo").withStyle(ChatFormatting.GOLD));
        }
        label(graphics, rarity, textY + 11, 0xFFFFFF);
        label(graphics, Component.translatable(KEY + "counter", index + 1, reveals.size()).withStyle(ChatFormatting.GRAY), height - 26, 0xFFFFFF);
        label(graphics, Component.translatable(KEY + "swipe").withStyle(ChatFormatting.DARK_GRAY), height - 14, 0xFFFFFF);
    }

    private void renderSummary(GuiGraphics graphics, int mouseX, int mouseY) {
        int count = reveals.size();
        int perRow = Math.min(count, 6);
        int rows = (count + perRow - 1) / perRow;
        float h = Math.min((height - 70) / (float) rows - 8, 80);
        float w = h * 0.75F;
        float gap = 6;
        float top = (height - rows * (h + gap)) / 2 + 4;

        label(graphics, Component.translatable(KEY + "summary"), top - 16, 0xFFFFFF);
        ItemStack hovered = ItemStack.EMPTY;
        for (int i = 0; i < count; i++) {
            int row = i / perRow;
            int inRow = Math.min(perRow, count - row * perRow);
            float rowWidth = inRow * w + (inRow - 1) * gap;
            float x = (width - rowWidth) / 2 + (i % perRow) * (w + gap) + w / 2;
            float y = top + row * (h + gap) + h / 2;
            // most valuable pull first
            Reveal reveal = reveals.get(count - 1 - i);
            drawItem(graphics, reveal.stack(), x, y, 0, h, 100);
            if (Math.abs(mouseX - x) < w / 2 && Math.abs(mouseY - y) < h / 2) {
                hovered = reveal.stack();
            }
        }
        label(graphics, Component.translatable(KEY + "close").withStyle(ChatFormatting.GRAY), height - 14, 0xFFFFFF);
        if (!hovered.isEmpty()) {
            graphics.renderTooltip(font, hovered, mouseX, mouseY);
        }
    }

    private void renderFlying(GuiGraphics graphics, long now) {
        float h = cardHeight();
        flying.removeIf(card -> now - card.start() > FLY_MS);
        for (Flying card : flying) {
            float t = (now - card.start()) / (float) FLY_MS;
            float e = easeInCubic(t);
            float x = card.x() + card.dir() * e * width * 0.8F;
            float y = card.y() - e * 20.0F;
            drawItem(graphics, card.stack(), x, y, card.rot() + card.dir() * 35.0F * e, h, 200);
        }
    }

    // ------------------------------------------------------------------ input

    @Override
    public boolean mouseClicked(double mouseX, double mouseY, int button) {
        if (button != 0) {
            return super.mouseClicked(mouseX, mouseY, button);
        }
        switch (phase) {
            case PACK -> startTear();
            case REVEAL -> {
                dragging = true;
                moved = false;
                pressX = mouseX;
                pressY = mouseY;
            }
            case SUMMARY -> onClose();
            default -> {
            }
        }
        return true;
    }

    @Override
    public boolean mouseDragged(double mouseX, double mouseY, int button, double dx, double dy) {
        if (dragging) {
            dragX = (float) (mouseX - pressX);
            dragY = (float) (mouseY - pressY) * 0.35F;
            moved |= Math.abs(dragX) > 3;
            return true;
        }
        return super.mouseDragged(mouseX, mouseY, button, dx, dy);
    }

    @Override
    public boolean mouseReleased(double mouseX, double mouseY, int button) {
        if (dragging && button == 0) {
            dragging = false;
            if (!moved) {
                swipe(1);
            } else if (Math.abs(dragX) >= SWIPE_DISTANCE) {
                swipe(Math.signum(dragX));
            } else {
                dragX = 0;
                dragY = 0;
            }
            return true;
        }
        return super.mouseReleased(mouseX, mouseY, button);
    }

    @Override
    public boolean keyPressed(int key, int scanCode, int modifiers) {
        boolean next = key == GLFW.GLFW_KEY_SPACE || key == GLFW.GLFW_KEY_ENTER || key == GLFW.GLFW_KEY_RIGHT || key == GLFW.GLFW_KEY_D;
        boolean back = key == GLFW.GLFW_KEY_LEFT || key == GLFW.GLFW_KEY_A;
        if (next || back) {
            switch (phase) {
                case PACK -> startTear();
                case REVEAL -> swipe(back ? -1 : 1);
                case SUMMARY -> onClose();
                default -> {
                }
            }
            return true;
        }
        return super.keyPressed(key, scanCode, modifiers);
    }

    @Override
    public boolean isPauseScreen() {
        return false;
    }

    // ------------------------------------------------------------------ steps

    private void startTear() {
        if (phase != Phase.PACK) {
            return;
        }
        phase = Phase.TEARING;
        phaseStart = Util.getMillis();
        if (sounds) {
            play(ModSounds.BOOSTER_PACK_OPEN.get(), 1.0F);
        }
    }

    private void startReveal() {
        phase = Phase.REVEAL;
        phaseStart = Util.getMillis();
        index = 0;
        announceTop();
    }

    private void swipe(float dir) {
        if (phase != Phase.REVEAL || index >= reveals.size()) {
            return;
        }
        long now = Util.getMillis();
        flying.add(new Flying(reveals.get(index).stack(), centerX() + dragX, centerY() + dragY, dragX * 0.08F, dir == 0 ? 1 : dir, now));
        dragX = 0;
        dragY = 0;
        index++;
        if (sounds) {
            play(SoundEvents.BOOK_PAGE_TURN, 0.9F + (float) Math.random() * 0.2F);
        }
        if (index >= reveals.size()) {
            phase = Phase.SUMMARY;
            phaseStart = now;
        } else {
            announceTop();
        }
    }

    private void announceTop() {
        revealStart = Util.getMillis();
        Reveal top = reveals.get(index);
        if (!sounds) {
            return;
        }
        if (top.holo()) {
            play(ModSounds.BOOSTER_PACK_OPEN_RARE.get(), 1.0F);
        } else if (top.rarity() == CardRarity.RARE) {
            play(ModSounds.BOOSTER_PACK_OPEN_RARE.get(), 0.8F);
        }
    }

    // ------------------------------------------------------------------ helpers

    /**
     * Draws an item model centred at (x, y), {@code size} pixels tall, rotated by {@code rot} degrees.
     */
    private void drawItem(GuiGraphics graphics, ItemStack stack, float x, float y, float rot, float size, float z) {
        graphics.pose().pushPose();
        graphics.pose().translate(x, y, z);
        graphics.pose().mulPose(Axis.ZP.rotationDegrees(rot));
        float scale = size / 16.0F;
        graphics.pose().scale(scale, scale, 1.0F);
        graphics.renderItem(stack, -8, -8);
        graphics.pose().popPose();
    }

    private void rays(GuiGraphics graphics, float x, float y, float length, float angle, int rgb, int count) {
        graphics.pose().pushPose();
        graphics.pose().translate(x, y, 10);
        for (int i = 0; i < count; i++) {
            graphics.pose().pushPose();
            graphics.pose().mulPose(Axis.ZP.rotationDegrees(angle + i * 360.0F / count));
            graphics.fill(-5, (int) -length, 5, 0, 0x50 << 24 | rgb);
            graphics.fill(-2, (int) -length, 2, 0, 0x70 << 24 | rgb);
            graphics.pose().popPose();
        }
        graphics.pose().popPose();
    }

    private void label(GuiGraphics graphics, Component text, float y, int color) {
        graphics.pose().pushPose();
        graphics.pose().translate(0, 0, 500);
        graphics.drawCenteredString(font, text, width / 2, (int) y, color);
        graphics.pose().popPose();
    }

    private static void play(SoundEvent sound, float pitch) {
        Minecraft.getInstance().getSoundManager().play(SimpleSoundInstance.forUI(sound, pitch));
    }

    private static float easeOutCubic(float t) {
        float f = 1 - t;
        return 1 - f * f * f;
    }

    private static float easeInCubic(float t) {
        return t * t * t;
    }

    private static float easeOutBack(float t) {
        float c1 = 1.70158F;
        float c3 = c1 + 1;
        return 1 + c3 * (float) Math.pow(t - 1, 3) + c1 * (float) Math.pow(t - 1, 2);
    }
}
