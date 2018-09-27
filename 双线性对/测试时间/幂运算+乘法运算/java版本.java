package com.zhong.accumulator;

import it.unisa.dia.gas.jpbc.Element;
import it.unisa.dia.gas.jpbc.Pairing;
import it.unisa.dia.gas.plaf.jpbc.pairing.PairingFactory;
import org.junit.Test;

public class TimeTest {
    @Test
    public void t1(){
        int times = 10000;
        /**
         * 双线性对
         */
        Pairing pairing = PairingFactory.getPairing("params/curves/a.properties");
        // 从G1群中随机选一个元素 生成元
        Element g = pairing.getG1().newRandomElement();
        // 从Zr群中随机选择一个元素 私钥
        Element s = pairing.getZr().newRandomElement();

        Element res = pairing.getG1().newOneElement();
        long t1 = System.currentTimeMillis();
        for(int i=0;i<times;i++) {
            Element temp = g.duplicate().powZn(s.duplicate());
            res = res.duplicate().mul(temp.duplicate());
        }
        long t2 = System.currentTimeMillis();

        System.out.println(times+" 次幂运算和 "+times+" 次乘法运算 耗时 "+(t2-t1)+" ms");
    }
}
