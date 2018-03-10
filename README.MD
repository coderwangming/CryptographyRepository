# 密码学仓库
在为实验室师兄师姐做仿真实验时，我发现有很多的代码段是被重复利用的

## 布隆过滤器
BloomFilter.java
```java
List<String> keywords = GenerateBloomFilter.getKeywordsFromFile(inputAbsolutePath);
BloomFilter<String> bf = new BloomFilter<String>(0.01,keywords.size()+20);
bf.addAll(keywords);
```

```java
bf.contains("test")
bf.contains(keys) //只要包含集合中的一个元素即可
bf.containsAll() //需要包含集合中的所有的元素
```

## 密码学原语
CryptoPrimitives.java

需要引入如下的依赖
```xml
<!-- https://mvnrepository.com/artifact/org.bouncycastle/bcprov-jdk15on -->
<dependency>
	<groupId>org.bouncycastle</groupId>
	<artifactId>bcprov-jdk15on</artifactId>
	<version>1.54</version>
</dependency>
```

```java
 /**
     * CMAC-AES 算法,CMAC-AES算法是一种消息认证函数
     *
     * @param key
     *         密钥
     * @param msg
     *         要认证的信息
     *
     * @return 对msg的签名。长度为128 bits
     *
     * @throws UnsupportedEncodingException
     *         未知
     */
    public static byte[] generateCmac(byte[] key, String msg) throws UnsupportedEncodingException 
```
```java
    /**
     * HMAC-SHA256 签名函数
     *
     * @param key
     *         密钥
     * @param msg
     *         要签名的信息
     *
     * @return 消息的签名，长度为256 bits
     *
     * @throws UnsupportedEncodingException
     *         未知
     */
    public static byte[] generateHmac(byte[] key, String msg) throws UnsupportedEncodingException
    //同理 还有HMAC-SHA512 签名算法
    public static byte[] generateHmac512(byte[] key, String msg) throws UnsupportedEncodingException
```
```java
  /**
     * 生成随机的byte数组
     *
     * @param sizeOfSalt
     *         byte数组额的长度
     *
     * @return 随机的byte数组
     */
    public static byte[] randomBytes(int sizeOfSalt)
```
```java
    /**
     * CTR模式下的AES加密算法
     *
     * @param keyBytes
     *         密钥
     * @param ivBytes
     *         初始向量
     * @param identifier
     *         要加密的字符串
     * @param sizeOfFileName
     *         未知
     *
     * @return 未知
     */
    public static byte[] encryptAES_CTR_String(byte[] keyBytes, byte[] ivBytes, String identifier, int sizeOfFileName)
    //相应的解密算法
    public static byte[] decryptAES_CBC(byte[] input, byte[] keyBytes)
    //同理，还有CBC模式下的AES加密
    public static byte[] encryptAES_CBC(byte[] keyBytes, byte[] ivBytes, byte[] input)
```
## JPBC 
是Pairing Based Cryptography的Java版本，访问 [JPBC官方网站](http://gas.dia.unisa.it/projects/jpbc/#.WqM_ldeWbIV "Title") 

* 需要引入三个jar包
* 需要引入params文件夹，这个文件夹中包含着初始化双线性对的参数
* 配置pom文件
```xml
 <!-- 将本地的jar包安装到仓库中，注意parse标签是clean -->
<plugin>
	<groupId>org.apache.maven.plugins</groupId>
	<artifactId>maven-install-plugin</artifactId>
	<version>2.5.1</version>
	<executions>
		<execution>
			<id>install-jpbc</id>
			<goals>
				<goal>install-file</goal>
			</goals>
			<phase>clean</phase>
			<configuration>
				<groupId>it.unisa.dia.gas.jpbc</groupId>
				<artifactId>jpbc</artifactId>
				<version>2.0</version>
				<packaging>jar</packaging>
				<file>${project.basedir}/lib/jpbc-api-2.0.0.jar</file>
			</configuration>
		</execution>
		<execution>
			<id>install-plaf</id>
			<goals>
				<goal>install-file</goal>
			</goals>
			<phase>clean</phase>
			<configuration>
				<groupId>it.unisa.dia.gas.plaf</groupId>
				<artifactId>plaf</artifactId>
				<version>2.0</version>
				<packaging>jar</packaging>
				<file>${project.basedir}/lib/jpbc-plaf-2.0.0.jar</file>
			</configuration>
		</execution>
	</executions>
</plugin>
```
```xml
<dependency>
	<groupId>it.unisa.dia.gas.jpbc</groupId>
	<artifactId>jpbc</artifactId>
	<version>2.0</version>
</dependency>
<dependency>
	<groupId>it.unisa.dia.gas.plaf</groupId>
	<artifactId>plaf</artifactId>
	<version>2.0</version>
</dependency>
```
```java
    /**
     * 双线性对
     */
    final public Pairing pairing = PairingFactory.getPairing("params/curves/a.properties");
    /**
     * 私钥 从Zr群中随机选择一个元素 作为私钥
     */
    final public Element s = pairing.getZr().newRandomElement();
```
## SerializableElement.java
一个可以序列化的Element，JPBC中提供的Element是不可以序列化的
需要引入如下的依赖
```xml
<!-- https://mvnrepository.com/artifact/commons-io/commons-io -->
<dependency>
	<groupId>commons-io</groupId>
	<artifactId>commons-io</artifactId>
	<version>2.6</version>
</dependency>
```

