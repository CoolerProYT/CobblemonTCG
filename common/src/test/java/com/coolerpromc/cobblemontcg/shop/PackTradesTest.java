package com.coolerpromc.cobblemontcg.shop;

import com.coolerpromc.cobblemontcg.config.TcgConfig;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;

class PackTradesTest {
    @Test
    void cardDealerUnlocksOneSetPerLevelAndTwoAtMaster() {
        assertEquals(1, PackTrades.levelOf(0), "Novice");
        assertEquals(4, PackTrades.levelOf(3), "Expert");
        assertEquals(5, PackTrades.levelOf(4), "Master");
        assertEquals(5, PackTrades.levelOf(5), "Master sells the sixth set too");
        assertEquals(PackTrades.MAX_SETS, TcgConfig.DEFAULT_SHOP_SETS.size(), "every default set has a Card Dealer level");
    }
}
