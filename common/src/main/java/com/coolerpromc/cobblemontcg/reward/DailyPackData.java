package com.coolerpromc.cobblemontcg.reward;

import com.mojang.serialization.Codec;
import com.mojang.serialization.codecs.RecordCodecBuilder;

public record DailyPackData(long day, int count) {
    public static final DailyPackData EMPTY = new DailyPackData(0L, 0);

    public static final Codec<DailyPackData> CODEC = RecordCodecBuilder.create(instance -> instance.group(
            Codec.LONG.fieldOf("day").forGetter(DailyPackData::day),
            Codec.INT.fieldOf("count").forGetter(DailyPackData::count)
    ).apply(instance, DailyPackData::new));

    public int countOn(long today) {
        return day == today ? count : 0;
    }

    public DailyPackData add(long today, int amount) {
        return new DailyPackData(today, countOn(today) + amount);
    }
}
