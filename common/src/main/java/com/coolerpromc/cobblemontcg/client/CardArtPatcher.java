package com.coolerpromc.cobblemontcg.client;

import com.coolerpromc.cobblemontcg.Constants;
import com.coolerpromc.cobblemontcg.tcg.card.CardDefinition;
import com.coolerpromc.cobblemontcg.tcg.data.TcgDataManager;
import com.coolerpromc.cobblemontcg.tcg.set.TcgSet;
import com.mojang.blaze3d.platform.NativeImage;
import com.mojang.blaze3d.systems.RenderSystem;
import net.minecraft.client.Minecraft;
import net.minecraft.client.renderer.texture.MipmapGenerator;
import net.minecraft.client.renderer.texture.SpriteContents;
import net.minecraft.client.renderer.texture.TextureAtlas;
import net.minecraft.client.renderer.texture.TextureAtlasSprite;
import net.minecraft.resources.ResourceLocation;
import org.lwjgl.opengl.GL11;
import org.lwjgl.opengl.GL12;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;

/**
 * Replaces the drawn Pokémon on card textures with renders from another mod (Cobblemon) at runtime.
 * <p>
 * Every Pokémon card has its illustration in its own sprite ({@code tcg/<set>/illustration/<number>}),
 * evolution cards the previous stage in {@code tcg/<set>/evolution/<number>} and every pack wrapper its
 * mascot in {@code tcg/pack/<set>_<wrapper>_mascot}. Once a {@link PortraitRenderer}
 * is ready, each of those sprites is redrawn and uploaded straight into the block atlas, so cards show the
 * new art everywhere (inventory, hand, item frames, the opening animation). A resource reload restores the
 * drawn art; it is redrawn on the next ticks. Only a few sprites are redrawn per tick to avoid a hitch.
 */
public final class CardArtPatcher {
    public static final CardArtPatcher INSTANCE = new CardArtPatcher();

    private static final int PER_TICK = 4;
    private static final int SUPERSAMPLE = 4;
    // the portrait window shows 32x24 of its 32x32 texture, see tools/art/layout.py
    private static final int PORTRAIT_W = 32;
    private static final int PORTRAIT_H = 24;
    /**
     * Dev tool: with {@code -Dcobblemontcg.exportArt=<dir>}, every redrawn sprite is also saved to
     * {@code <dir>/<namespace>/<sprite path>.png} and the game quits once all of them are drawn. The wiki
     * in {@code docs/} shows these renders on its cards.
     */
    private static final String EXPORT_DIR = System.getProperty(Constants.MODID + ".exportArt");

    /**
     * Draws one species on a transparent background, full body, centred and standing on the bottom third.
     */
    public interface PortraitRenderer {
        /**
         * True once species data is available (Cobblemon syncs species when joining a world).
         */
        boolean ready();

        /**
         * @return the render as RGBA, or empty to keep the drawn art (unknown species, render error)
         */
        Optional<NativeImage> render(int pokedex, int width, int height);
    }

    private enum Framing { ILLUSTRATION, PORTRAIT, PACK }

    private record Job(ResourceLocation sprite, int pokedex, Framing framing) {
    }

    private PortraitRenderer renderer;
    private List<Job> jobs = List.of();
    private boolean jobsDirty = true;
    // the sprite contents each job was drawn into; a reload creates new contents, which marks it as pending again
    private final Map<ResourceLocation, SpriteContents> done = new HashMap<>();

    private CardArtPatcher() {
        TcgDataManager.CLIENT.addListener(() -> jobsDirty = true);
    }

    public void setRenderer(PortraitRenderer renderer) {
        this.renderer = renderer;
    }

    public void tick() {
        Minecraft minecraft = Minecraft.getInstance();
        if (renderer == null || minecraft.level == null || !renderer.ready()) {
            return;
        }
        if (jobsDirty) {
            jobs = buildJobs();
            done.clear();
            jobsDirty = false;
        }
        TextureAtlas atlas = minecraft.getModelManager().getAtlas(TextureAtlas.LOCATION_BLOCKS);
        int budget = PER_TICK;
        for (Job job : jobs) {
            TextureAtlasSprite sprite = atlas.getSprite(job.sprite());
            SpriteContents contents = sprite.contents();
            if (!contents.name().equals(job.sprite()) || done.get(job.sprite()) == contents) {
                continue;   // missing texture (custom set without one) or already drawn
            }
            done.put(job.sprite(), contents);
            draw(atlas, sprite, job);
            if (--budget == 0) {
                return;
            }
        }
        if (EXPORT_DIR != null && budget == PER_TICK && !jobs.isEmpty()) {
            // a whole pass without drawing anything: every sprite is done
            Constants.LOG.info("Exported the card art to {}, quitting", EXPORT_DIR);
            minecraft.stop();
        }
    }

    private static List<Job> buildJobs() {
        List<Job> list = new ArrayList<>();
        for (TcgSet set : TcgDataManager.CLIENT.sets()) {
            ResourceLocation id = set.id();
            for (CardDefinition card : set.cards()) {
                String base = "tcg/" + id.getPath() + "/";
                card.pokedex().ifPresent(dex -> list.add(new Job(
                        ResourceLocation.fromNamespaceAndPath(id.getNamespace(), base + "illustration/" + card.number()), dex, Framing.ILLUSTRATION)));
                card.evolvesFromPokedex().ifPresent(dex -> list.add(new Job(
                        ResourceLocation.fromNamespaceAndPath(id.getNamespace(), base + "evolution/" + card.number()), dex, Framing.PORTRAIT)));
            }
            set.definition().wrapperPokedex().forEach((wrapper, dex) -> list.add(new Job(
                    ResourceLocation.fromNamespaceAndPath(id.getNamespace(), "tcg/pack/" + id.getPath() + "_" + wrapper + "_mascot"), dex, Framing.PACK)));
        }
        return list;
    }

    // ------------------------------------------------------------------ drawing

    private void draw(TextureAtlas atlas, TextureAtlasSprite sprite, Job job) {
        int width = sprite.contents().width();
        int height = sprite.contents().height();
        // portraits are a close up of a full body render the size of a card illustration
        boolean portrait = job.framing() == Framing.PORTRAIT;
        int renderW = portrait ? 208 : width;
        int renderH = portrait ? 144 : height;
        Optional<NativeImage> rendered;
        try {
            rendered = renderer.render(job.pokedex(), renderW * SUPERSAMPLE, renderH * SUPERSAMPLE);
        } catch (Throwable e) {
            Constants.LOG.warn("Could not draw Pokédex #{} for {}, keeping the drawn art", job.pokedex(), job.sprite(), e);
            return;
        }
        if (rendered.isEmpty()) {
            return;
        }
        try (NativeImage big = rendered.get()) {
            int[] bounds = bounds(big);
            if (bounds == null) {
                return;
            }
            NativeImage image = new NativeImage(width, height, true);
            try {
                switch (job.framing()) {
                    case PORTRAIT -> portrait(big, bounds, image);
                    case ILLUSTRATION -> fit(big, bounds, image, 0.74F, 0.9F, 0.88F, true);
                    // the mascot is much bigger on the pack and stands on the booster banner, without a shadow
                    case PACK -> fit(big, bounds, image, 0.86F, 0.98F, 0.97F, false);
                }
                upload(atlas, sprite, image);
                if (EXPORT_DIR != null) {
                    export(job.sprite(), image);
                }
            } finally {
                image.close();
            }
        }
    }

    /**
     * Head and shoulders: a 4:3 crop around the top of the body, scaled into the portrait window.
     */
    private static void portrait(NativeImage big, int[] b, NativeImage out) {
        float bodyH = b[3] - b[1];
        float cropH = Math.max(bodyH * 0.62F, big.getHeight() * 0.3F);
        float cropW = cropH * PORTRAIT_W / PORTRAIT_H;
        float cx = (b[0] + b[2]) / 2.0F;
        float x0 = clamp(cx - cropW / 2, 0, big.getWidth() - cropW);
        float y0 = clamp(b[1] - cropH * 0.06F, 0, big.getHeight() - cropH);
        downscale(big, x0, y0, cropW, cropH, out, 0, 0, PORTRAIT_W, PORTRAIT_H);
    }

    /**
     * Fits the Pokémon into the image the same way for every species: as large as fits in {@code heightShare}
     * of the height and {@code widthShare} of the width, centred, feet at {@code feetAt} of the height,
     * optionally standing on a soft contact shadow like the drawn art.
     */
    private static void fit(NativeImage big, int[] b, NativeImage out, float heightShare, float widthShare, float feetAt, boolean withShadow) {
        float w = out.getWidth();
        float h = out.getHeight();
        float bodyW = b[2] - b[0];
        float bodyH = b[3] - b[1];
        // output pixels per source pixel; never above 1, so the supersampled render is only ever scaled down
        float scale = Math.min(Math.min(h * heightShare / bodyH, w * widthShare / bodyW), 1.0F);
        float feetY = h * feetAt;
        float cx = (b[0] + b[2]) / 2.0F;
        // the source region that lands on the whole image
        float sx = cx - w / 2 / scale;
        float sy = b[3] - feetY / scale;
        if (withShadow) {
            shadow(out, w / 2, feetY - 1, Math.max(bodyW * scale * 0.42F, 6));
        }
        downscale(big, sx, sy, w / scale, h / scale, out, 0, 0, (int) w, (int) h);
    }

    private static void shadow(NativeImage out, float cx, float cy, float rx) {
        float ry = rx * 0.2F;
        for (int y = 0; y < out.getHeight(); y++) {
            for (int x = 0; x < out.getWidth(); x++) {
                float d = ((x - cx) * (x - cx)) / (rx * rx) + ((y - cy) * (y - cy)) / (ry * ry);
                if (d < 1) {
                    int alpha = (int) (95 * (1 - d) * (1 - d));
                    out.setPixelRGBA(x, y, alpha << 24);
                }
            }
        }
    }

    /**
     * Box-filters a region of {@code src} into a region of {@code dst} (alpha-weighted, so edges don't go
     * dark), drawing it over what {@code dst} already holds.
     */
    private static void downscale(NativeImage src, float sx, float sy, float sw, float sh, NativeImage dst, int dx, int dy, int dw, int dh) {
        float fx = sw / dw;
        float fy = sh / dh;
        for (int y = 0; y < dh; y++) {
            for (int x = 0; x < dw; x++) {
                int x0 = (int) Math.floor(sx + x * fx);
                int y0 = (int) Math.floor(sy + y * fy);
                int x1 = Math.max(x0 + 1, (int) Math.floor(sx + (x + 1) * fx));
                int y1 = Math.max(y0 + 1, (int) Math.floor(sy + (y + 1) * fy));
                float r = 0, g = 0, b = 0, a = 0;
                int n = 0;
                for (int yy = Math.max(y0, 0); yy < y1 && yy < src.getHeight(); yy++) {
                    for (int xx = Math.max(x0, 0); xx < x1 && xx < src.getWidth(); xx++) {
                        int p = src.getPixelRGBA(xx, yy);   // ABGR
                        float pa = (p >>> 24) / 255.0F;
                        r += (p & 0xFF) * pa;
                        g += ((p >> 8) & 0xFF) * pa;
                        b += ((p >> 16) & 0xFF) * pa;
                        a += pa;
                        n++;
                    }
                }
                if (n == 0 || a <= 0) {
                    continue;
                }
                float alpha = a / n;
                int pr = Math.round(r / a);
                int pg = Math.round(g / a);
                int pb = Math.round(b / a);
                over(dst, dx + x, dy + y, pr, pg, pb, alpha);
            }
        }
    }

    /**
     * Draws a colour over a pixel (source over, straight alpha).
     */
    private static void over(NativeImage dst, int x, int y, int r, int g, int b, float a) {
        int p = dst.getPixelRGBA(x, y);   // ABGR
        float da = (p >>> 24) / 255.0F;
        float oa = a + da * (1 - a);
        if (oa <= 0) {
            return;
        }
        float k = da * (1 - a);
        int or = Math.round((r * a + (p & 0xFF) * k) / oa);
        int og = Math.round((g * a + ((p >> 8) & 0xFF) * k) / oa);
        int ob = Math.round((b * a + ((p >> 16) & 0xFF) * k) / oa);
        dst.setPixelRGBA(x, y, Math.round(oa * 255) << 24 | ob << 16 | og << 8 | or);
    }

    /**
     * Bounding box {x0, y0, x1, y1} of the visible pixels, or null when the render is empty.
     */
    private static int[] bounds(NativeImage image) {
        int x0 = Integer.MAX_VALUE, y0 = Integer.MAX_VALUE, x1 = -1, y1 = -1;
        for (int y = 0; y < image.getHeight(); y++) {
            for (int x = 0; x < image.getWidth(); x++) {
                if ((image.getPixelRGBA(x, y) >>> 24) > 16) {
                    x0 = Math.min(x0, x);
                    y0 = Math.min(y0, y);
                    x1 = Math.max(x1, x);
                    y1 = Math.max(y1, y);
                }
            }
        }
        return x1 < 0 ? null : new int[]{x0, y0, x1 + 1, y1 + 1};
    }

    private static void export(ResourceLocation sprite, NativeImage image) {
        Path file = Path.of(EXPORT_DIR, sprite.getNamespace(), sprite.getPath() + ".png");
        try {
            Files.createDirectories(file.getParent());
            image.writeToFile(file);
        } catch (IOException e) {
            Constants.LOG.warn("Could not export {}", sprite, e);
        }
    }

    /**
     * Writes the image and its mipmaps into the atlas where the sprite lives.
     */
    private static void upload(TextureAtlas atlas, TextureAtlasSprite sprite, NativeImage image) {
        RenderSystem.bindTexture(atlas.getId());
        int mipLevels = GL11.glGetTexParameteri(GL11.GL_TEXTURE_2D, GL12.GL_TEXTURE_MAX_LEVEL);
        NativeImage[] levels = MipmapGenerator.generateMipLevels(new NativeImage[]{image}, mipLevels);
        for (int level = 0; level < levels.length; level++) {
            levels[level].upload(level, sprite.getX() >> level, sprite.getY() >> level, 0, 0,
                    image.getWidth() >> level, image.getHeight() >> level, false, false, levels.length > 1, false);
        }
        for (int level = 1; level < levels.length; level++) {
            levels[level].close();
        }
    }

    private static float clamp(float v, float min, float max) {
        return Math.max(min, Math.min(max, v));
    }
}
