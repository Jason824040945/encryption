# encryption
文件加解密工具
使用开源openssl预编译x86

---
加密步骤:
1、生成一个32位随机密钥
2、将该密钥保存到文件 key.bin 中，并使用该密钥对指定的文件进行加密。加密后的文件将保存在原文件路径加上 .enc 后缀的文件中。
3、使用公钥对密钥文件 key.bin 进行加密，并将加密后的密钥文件保存为 key.bin.enc 文件。
4、删除生成的 key.bin 文件。


---
解密步骤:
1、使用私钥解密随机密钥。
2、使用解密后的随机密钥解密文件。
3、删除生成的 key.bin 文件。


编译命令:
pyinstaller --onefile --add-data "openssl-3;openssl-3" encryption.py -i test.ico
