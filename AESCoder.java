package co.junwei.cpabe;

import javax.crypto.Cipher;
import javax.crypto.KeyGenerator;
import javax.crypto.SecretKey;
import javax.crypto.spec.SecretKeySpec;
import java.security.SecureRandom;

/**
 * AES加密算法
 */
public class AESCoder {

    /**
     * 获得随机密钥
     * @param seed 随机种子
     * @return 密钥
     * @throws Exception 异常
     */
    private static byte[] getRawKey(byte[] seed) throws Exception {
        KeyGenerator kgen = KeyGenerator.getInstance("AES");
        SecureRandom sr = SecureRandom.getInstance("SHA1PRNG");
        sr.setSeed(seed);
        kgen.init(128, sr); // 192 and 256 bits may not be available
        SecretKey skey = kgen.generateKey();
        byte[] raw = skey.getEncoded();
        return raw;
    }

    /**
     * 加密算法
     * @param seed 种子
     * @param plaintext 明文
     * @return 返回值
     * @throws Exception 异常
     */
    public static byte[] encrypt(byte[] seed, byte[] plaintext)
            throws Exception {
        byte[] raw = getRawKey(seed);
        SecretKeySpec skeySpec = new SecretKeySpec(raw, "AES");
        Cipher cipher = Cipher.getInstance("AES/ECB/PKCS5Padding");
        cipher.init(Cipher.ENCRYPT_MODE, skeySpec);
        byte[] encrypted = cipher.doFinal(plaintext);
        return encrypted;
    }

    /**
     * 解密
     * @param seed 随机种子
     * @param ciphertext 密文
     * @return 明文
     * @throws Exception 异常
     */
    public static byte[] decrypt(byte[] seed, byte[] ciphertext)
            throws Exception {
        byte[] raw = getRawKey(seed);
        SecretKeySpec skeySpec = new SecretKeySpec(raw, "AES");
        Cipher cipher = Cipher.getInstance("AES/ECB/PKCS5Padding");
        cipher.init(Cipher.DECRYPT_MODE, skeySpec);
        byte[] decrypted = cipher.doFinal(ciphertext);

        return decrypted;
    }

}