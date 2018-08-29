package com.zhong;

import sun.misc.BASE64Encoder;

import java.security.MessageDigest;
/**
 *
 * 密码原语
 *
 * @author 张中俊
 **/
public class CryptographyRepository2 {
    public static byte[]generateMD5(String msg) {
        try {
            MessageDigest md5 = MessageDigest.getInstance("MD5");
            return md5.digest(msg.getBytes("utf-8"));
        }catch (Exception e){
            System.err.println("签名时发生错误");
            return null;
        }
        }

    public static String generateMD5_String(String msg){
        try {
            BASE64Encoder base64en = new BASE64Encoder();
            return base64en.encode(generateMD5(msg));
        }catch(Exception e){
            System.out.println("签名时发生错误");
            return null;
        }
        }
}
