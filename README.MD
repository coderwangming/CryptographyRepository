# 密码学仓库
在为实验室师兄师姐做仿真实验时，我发现有很多的代码段是被重复利用的

## 伪随机函数

在论文中经常出现伪随机函数，郭师姐提示我使用hash函数即可实现

```java
    /**
     * 一个随机函数 {0,1}^lambda X {0,1}^lambda -&gt; {0,1}^lambda
     *
     * @param K
     *         密钥
     * @param e
     *         元素
     *
     * @return 随机映射的结果，长度为16的byte数组
     *
     * @throws UnsupportedEncodingException
     *         异常
     */
    public static byte[] F(final byte[] K, final Element e) throws UnsupportedEncodingException {
        byte[] res = CryptoPrimitives.generateCmac(K, e.toString());
        return res;
    }

    /**
     * 一个随机函数 {0,1}^lambda X {0,1}^lambda -&gt; Zp*
     * @param KI 密钥
     * @param id 文件名
     *
     * @return 随机映射的结果，长度为16的byte数组
     *
     * @throws Exception 异常
     */
    public static Element Fp(final byte[] KI,String id) throws Exception {
        byte[] res = CryptoPrimitives.generateCmac(KI, id);
        Element e = pairing.getZr().newElement();
        e.setFromBytes(res);
        return e;
    }
```

## 常用的时间
模指数：40 ms

## 布隆过滤器

参数设置可以参考如下的网址：
http://pages.cs.wisc.edu/~cao/papers/summary-cache/node8.html


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
## 号称是JAVA实现的最快的Bloom Filter
* 官网是 https://alexandrnikitin.github.io/blog/bloom-filter-for-scala/ ,在自己的官网中，他分析了Google的Guava、Twitter的Algebird、ScalaNLP的Breeze有多么的suck
* 其github网址为https://github.com/alexandrnikitin/bloom-filter-scala
* 可以使用maven引入其依赖https://mvnrepository.com/artifact/com.github.alexandrnikitin/bloom-filter_2.11 ，最新的版本为
```xml
<!-- https://mvnrepository.com/artifact/com.github.alexandrnikitin/bloom-filter -->
<dependency>
    <groupId>com.github.alexandrnikitin</groupId>
    <artifactId>bloom-filter_2.11</artifactId>
    <version>0.10.1</version>
</dependency>
```
* 用法 它是在Scala下的一个库，但是在java上也能使用，就是用法有点丑
```scala
import bloomfilter.mutable.BloomFilter

val expectedElements = 1000
val falsePositiveRate = 0.1
val bf = BloomFilter[String](expectedElements, falsePositiveRate)
bf.add("some string")
bf.mightContain("some string")
bf.dispose()
```
```java
import bloomfilter.CanGenerateHashFrom;
import bloomfilter.mutable.BloomFilter;

long expectedElements = 10000000;
double falsePositiveRate = 0.1;
BloomFilter<byte[]> bf = BloomFilter.apply(
        expectedElements,
        falsePositiveRate,
        CanGenerateHashFrom.CanGenerateHashFromByteArray$.MODULE$);

byte[] element = new byte[100];
bf.add(element);
bf.mightContain(element);
bf.dispose();
```
* 效率： 这个库真的很强大，测试了1000 W条数据、0.1的误判率，序列化之后只有区区5.8M。真的很棒！


## 计数型BloomFilter

https://github.com/Baqend/Orestes-Bloomfilter
支持计数型BF 和 redis的BF

```xml
<dependencies>
   <dependency>
       <groupId>com.baqend</groupId>
       <artifactId>bloom-filter</artifactId>
       <version>1.0.7</version>
   </dependency>
</dependencies>
<repositories>
   <repository>
       <snapshots>
        <enabled>false</enabled>
       </snapshots>
       <id>central</id>
       <name>bintray</name>
       <url>http://jcenter.bintray.com</url>
   </repository>
</repositories>
```

## Garbled BloomFilter

参考文献： When Private Set Intersection Meets Big Data An Efficient and Scalable Protocol

### 秘密共享

当t=n时，（t,n）秘密共享方案如下：
![密钥共享](imgs/密钥共享.jpg)

### Garbled BF构造
![GarbledBF](imgs/GarbledBF.jpg)


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
### 签名函数
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
### 加解密函数
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
### 一个独立的AES加解密
在AESCoder.java中，我们实现了AES加解密的算法

### 对加解密函数进行进一步的封装
固定初始向量，简化调用接口，通常将此函数放在MyUtils中，static类型
```java
/**
 * AES加密时候使用的初始向量
 */
private static final byte[] ivBytes = new byte[]{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
/**
 * 使用CBC模式下的AES加密算法加密
 *
 * @param Ke 密钥 16 byte
 * @param mingWen 要加密的明文
 * @return 加密之后得到的密文
 * @throws IOException 异常
 * @throws InvalidAlgorithmParameterException 异常
 * @throws NoSuchAlgorithmException 异常
 * @throws NoSuchPaddingException 异常
 * @throws NoSuchProviderException 异常
 * @throws InvalidKeyException 异常
 */
public static byte[] encrypt_AES_CBC(byte[] Ke, String mingWen) throws IOException, InvalidAlgorithmParameterException, NoSuchAlgorithmException, NoSuchPaddingException, NoSuchProviderException, InvalidKeyException {
	final byte[] miWen = CryptoPrimitives.encryptAES_CBC(Ke, ivBytes, mingWen.getBytes("utf-8"));
	return miWen;
}

/**
 * 使用CBC模式下的AES加密算法解密
 * @param Ke 解密密钥
 * @param miWen 需要解密的密文
 * @return 解密之后得到的明文
 * @throws InvalidAlgorithmParameterException 异常
 * @throws NoSuchAlgorithmException 异常
 * @throws NoSuchPaddingException 异常
 * @throws NoSuchProviderException 异常
 * @throws InvalidKeyException 异常
 * @throws IOException 异常
 */
public static String decrypt_AES_CBC(byte[] Ke,byte[] miWen) throws InvalidAlgorithmParameterException, NoSuchAlgorithmException, NoSuchPaddingException, NoSuchProviderException, InvalidKeyException, IOException {
	byte[] s = CryptoPrimitives.decryptAES_CBC(miWen, Ke);
	return new String(s,"utf-8");
}
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
踩过的坑：
1. 没有将params文件夹拷贝到项目中
2. 在使用元素时候没有使用duplicate()，从而使得原始值发生变化
### JBPC中元素的大小
![双线性对中元素的大小](imgs/双线性对中元素的大小.PNG)

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
## 基于双线性对的聚合器
参考我的另外一个Github项目：https://github.com/zhangzhongjun/BilinearMapAccumulator
参考论文：Supporting Non-membership Proofs with Bilinear-map Accumulators.pdf
k是私钥 h=g^k是公钥
* 算法1：计算一个集合的accumulator
  ![1](imgs/1.PNG)
  其中k是私钥，X是要聚合的集合，x是X中的元素

* 算法2：计算某元素的witness
  ![2](imgs/2.PNG)

* 算法3：判断一个元素是否在集合中
  需要判断两件事：
  ![3](imgs/3.PNG)
  如果不成立，则说明用户提交了一个非法的请求
  ![4](imgs/4.PNG)
  如果成立，则y在X中；否则y不在X中

* 算法4：计算一个集合的witness
  ![5](imgs/5.PNG)
* 算法5：判断一个集合Y是不是集合X的子集

## hash函数
hash函数是抗碰撞的，
MurMurHash

## ABE 基于属性的加密方式
> 基于属性的加密，又称模糊的基于身份的加密（Fuzzy Identity-Based Encryption）。
> 基于属性的加密分为CP-ABE 和 KP-ABE，即基于密文策略的ABE 和 基于密钥策略ABE

### CP-ABE

https://github.com/junwei-wang/cpabe 一直在更新的，其官网为https://junwei.co/cpabe/

### DET-ABE

https://github.com/mmoraless/DET-ABE/tree/v1.0 一种ABE，名字叫DET-ABE，论文发表在IFIP上：https://link.springer.com/chapter/10.1007%2F978-3-319-24018-3_7

### junwei的实现
依赖于jpbc库，版本是1.2.1，注意1.2.1与2.0.0的接口有很大的不同之处，不建议修改他的源码。建立使用1.2.1
1. 修改pom文件
```xml
    <dependencies>
        <dependency>
            <groupId>it.unisa.dia.gas</groupId>
            <artifactId>jpbc-api</artifactId>
            <version>1.2.1</version>
            <scope>system</scope>
            <systemPath>${pom.basedir}/lib/jpbc-api-1.2.1.jar</systemPath>
        </dependency>
        <dependency>
            <groupId>it.unisa.dia.gas</groupId>
            <artifactId>jpbc-plaf</artifactId>
            <version>1.2.1</version>
            <scope>system</scope>
            <systemPath>${pom.basedir}/lib/jpbc-plaf-1.2.1.jar</systemPath>
        </dependency>
    <dependencies>
```
2. 生成PublicKey和MasterKey，并将他们序列化到文件中
```java
String pubfile = MyUtils.getFile("abe_keys","pub_key").getAbsolutePath();
String mskfile = MyUtils.getFile("abe_keys","master_key").getAbsolutePath();
Cpabe cpabe = new Cpabe();
cpabe.setup(pubfile,mskfile);
```
3. 根据PublicKey、MasterKey、属性列表 生成 PrivateKey，并将其序列化到文件中
```java
String pubfile = MyUtils.getFile("abe_keys","pub_key").getAbsolutePath();
String mskfile = MyUtils.getFile("abe_keys","master_key").getAbsolutePath();
String prvfile = MyUtils.getFile("abe_keys","prv_key").getAbsolutePath();
//属性列表
String student_attr = "objectClass:inetOrgPerson objectClass:organizationalPerson "
+ "sn:student2 cn:student2 uid:student2 userPassword:student2 "
+ "ou:idp o:computer mail:student2@sdu.edu.cn title:student";
Cpabe cpabe = new Cpabe();
cpabe.keygen(pubfile,prvfile,mskfile,student_attr);
```
4. 对字符串加解密。这里使用到了加密属性和policy，更多的知识请参考https://junwei.co/cpabe/
```java
String pubfile = MyUtils.getFile("abe_keys","pub_key").getAbsolutePath();
String mskfile = MyUtils.getFile("abe_keys","master_key").getAbsolutePath();
String prvfile = MyUtils.getFile("abe_keys","prv_key").getAbsolutePath();
String policy =  "sn:student2 cn:student2 uid:student2 3of3";

Cpabe cpabe = new Cpabe();
ArrayList<byte[]> res = cpabe.enc(pubfile,policy,"hello world".getBytes("utf-8"));
System.out.println((cpabe.dec(pubfile,prvfile,res)));
res = cpabe.enc(pubfile,policy,"java sse implement".getBytes("utf-8"));
System.out.println((cpabe.dec(pubfile,prvfile,res)));
```
5. 对文件加解密
```java
String pubfile = MyUtils.getFile("abe_keys","pub_key").getAbsolutePath();
String mskfile = MyUtils.getFile("abe_keys","master_key").getAbsolutePath();
String prvfile = MyUtils.getFile("abe_keys","prv_key").getAbsolutePath();
String policy =  "sn:student2 cn:student2 uid:student2 3of3";

test.enc(pubfile, policy, inputfile, encfile);
test.dec(pubfile, prvfile, encfile, decfile);
```
6. 提高效率
  每次加密和解密时候都需要从文件中加载PublicKey MasterKey PrivateKey，会造成较大的存储开销，当加密的是一个文件的时候，这是没有问题的；但当加密的是字符串时，频繁地加载太耗时了
```java
/* get BswabePub from pubfile */
byte[] pub_byte = Common.suckFile(pubfile);
BswabePub pub = SerializeUtils.unserializeBswabePub(pub_byte);
/* get BswabePrv form prvfile */
byte[] prv_byte = Common.suckFile(prvfile);
BswabePrv prv = SerializeUtils.unserializeBswabePrv(pub, prv_byte);
```
```java
//加密
ArrayList<byte[]> res = cpabe.enc(pub, policy, "hello world".getBytes("utf-8"));
//解密
System.out.println((cpabe.dec(pub, prv, res)));
```
```bash
实验结果：
未提高效率100次加解密 40844 ms
提高效率100次加解密 33265 ms
```
## Patrick P. C. Lee教授的主页
http://www.cse.cuhk.edu.hk/~pclee/www/pubs.html

其主页上有他的工作的论文下载，ppt，代码，甚至是在会议上讲论文的视频，我认为这个人很优秀，愿意开源，敢于开源。
