# CryptoPrimitives.java

需要引入如下的依赖
```xml
<!-- https://mvnrepository.com/artifact/org.bouncycastle/bcprov-jdk15on -->
<dependency>
	<groupId>org.bouncycastle</groupId>
	<artifactId>bcprov-jdk15on</artifactId>
	<version>1.54</version>
</dependency>
```

## 签名函数

消息认证函数 CMAC-AES
签名函数HMAC-SHA256 


## 加解密函数

CBC模式下的AES加解密算法，AES_CBC_128
CTR模式下的AES加解密算法，AES_CTR_128

# AESCoder.java

AES加解密的算法

# MyUtils.java

作用包括：
1. 固定初始向量
2. 简化调用接口，加密函数和解密函数的输入输出都是字符串类型

通常将此函数放在MyUtils中，static类型


# AES_ECB.java

ECB模式下的AES加解密算法，支持AES_ECB_128和AES_ECB_256的加解密

AES_ECB_128 的密钥要求为128 bits

AES_ECB_256的密钥要求为256 bits

## AES_ECB_256中遇到的问题

```bash
Exception in thread "main" java.security.InvalidKeyException: Illegal key size or default parameters
```

Illegal key size or default parameters是指密钥长度是受限制的，最长为128 比特，java运行时环境读到的是受限的policy文件。文件位于${java_home}/jre/lib/security 

这种限制是因为美国对软件出口的控制。 

去掉这种限制需要下载Java Cryptography Extension (JCE) Unlimited Strength Jurisdiction Policy Files.网址为 http://www.oracle.com/technetwork/java/javase/downloads/jce8-download-2133166.html    文件名为jce_policy-8.zip

注意，上面的网址是JDK8的，其他版本的需要另外找

# CryptoPrimitives2.java

MD5签名函数