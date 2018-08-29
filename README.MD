# 密码学仓库
在为实验室师兄师姐做仿真实验时，我发现有很多的代码段是被重复利用的

## HackingCipher

HackingCipher是一本密码学读物，作者给出了众多基本加密签名算法的python实现，包括DES、AES、置换加密等，还有一些攻击方式，如频率攻击等。

在文件夹HackingCipher中

## PKI

### 作用

1. 支持公开密钥管理、认证、加密、完整性、可追溯性服务的基础设施
2. 提供公钥加密和数字签名服务的系统和平台，目的是为了管理密钥和证书
3. 一个机构通过采用PKI框架管理密钥和证书可以建立一个安全的网络环境

### 内容

PKI体系包括：
1. 权威的认证机构CA
2. 数字证书库
3. 密钥备份及恢复系统
4. 证书作废系统
  5 应用接口（API）

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

哈希函数（md5 sha1）：微妙级别，md5是78微秒，sha1是60微秒

模指数：40 ms


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



# libssl库

其安装步骤可以参考 [VDB实验](https://github.com/zhangzhongjun/VDB)

可以参考官方给的文档《openssl cookbook》
