package com.zhong;

import org.bouncycastle.jce.provider.BouncyCastleProvider;

import javax.crypto.Cipher;
import javax.crypto.spec.SecretKeySpec;
import java.security.Security;
import java.util.Arrays;

public class AES_ECB {
    static {
        // PC上的Java里面只有"AES/ECB/PKCS5Padding"算法，没有"AES/ECB/PKCS7Padding"算法
        // 故需要引入BouncyCastle的库，
        Security.addProvider(new BouncyCastleProvider());
    }

    public static byte[] encryptAES_ECB_128(byte[] keyBytes, byte[] input)
            throws Exception {
        SecretKeySpec key = new SecretKeySpec(keyBytes, "AES");
        Cipher cipher = Cipher.getInstance("AES/ECB/PKCS5Padding");
        cipher.init(Cipher.ENCRYPT_MODE, key);
        byte[] cipherText = cipher.doFinal(input);
        return cipherText;
    }

    public static byte[] encryptAES_ECB_256(byte[] keyBytes, byte[] input)
            throws Exception {
        SecretKeySpec key = new SecretKeySpec(keyBytes, "AES");
        Cipher cipher = Cipher.getInstance("AES/ECB/PKCS7Padding", "BC");
        cipher.init(Cipher.ENCRYPT_MODE, key);
        byte[] cipherText = cipher.doFinal(input);
        return cipherText;
    }

    public static byte[] decryptAES_ECB_256(byte[] keyBytes, byte[] input)
            throws Exception {
        SecretKeySpec key = new SecretKeySpec(keyBytes, "AES");
        Cipher cipher = Cipher.getInstance("AES/ECB/PKCS7Padding", "BC");
        cipher.init(Cipher.DECRYPT_MODE, key);
        byte[] original = cipher.doFinal(input);
        return original;
    }

    public static byte[] decryptAES_ECB_128(byte[] keyBytes, byte[] input) throws Exception {
        SecretKeySpec key = new SecretKeySpec(keyBytes, "AES");
        Cipher cipher = Cipher.getInstance("AES/ECB/PKCS5Padding");
        cipher.init(Cipher.DECRYPT_MODE, key);
        byte[] original = cipher.doFinal(input);
        return original;
    }

    public static void main(String[] args) throws Exception {
        /*
         * 此处使用AES-128-ECB加密模式，key需要为16位。
         */
        String key = "1234567890123456";
        byte[] key_bytes = key.getBytes("utf-8");
        // 需要加密的字串
        String src = "www.gowhere.so";
        byte[] src_bytes = src.getBytes("utf-8");
        System.out.println("加密前的字串是：" + Arrays.toString(src_bytes));
        // 加密
        byte[] res = AES_ECB.encryptAES_ECB_128(key_bytes, src_bytes);
        System.out.println("加密后的字串是：" + Arrays.toString(res));
        // 解密
        byte[] DeString = AES_ECB.decryptAES_ECB_128(key_bytes, res);
        System.out.println("解密后的字串是：" + Arrays.toString(DeString));

        key = "12345678901234561234567890123456";
        key_bytes = key.getBytes("utf-8");
        res = AES_ECB.encryptAES_ECB_256(key_bytes, src_bytes);
        System.out.println("加密后的字串是：" + Arrays.toString(res));
        DeString = AES_ECB.decryptAES_ECB_256(key_bytes, res);
        System.out.println("解密后的字串是：" + Arrays.toString(DeString));
    }
}
