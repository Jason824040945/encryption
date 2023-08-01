'''
Author: Jason
Date: 2023-07-28 10:10:33
LastEditors: Jason 824040945@qq.com
LastEditTime: 2023-07-28 17:58:12
FilePath: file_encryption/encryption.py
'''

import os
import sys
import datetime
import subprocess

base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
ssl_exe_path = os.path.join(base_path, 'openssl-3', 'x86/bin/openssl.exe')

def finish_func():
    print("----------------------------------------------------\n")
    input("按任意键退出...")
    exit(0)

def print_errinfo(cmd, result):
    if cmd: print(f"\033[0;31m 命令: {' '.join(cmd)}  \033[0m")
    print(f"\033[0;31m 错误信息: {result.stderr}  \033[0m")
    finish_func()

def add_privkey():
    args = [ssl_exe_path, 'genrsa', '-out', 'rsa_private_key.pem', '2048']
    result = subprocess.run(args, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"\033[0;31m 生成私钥文件失败！  \033[0m")
        print_errinfo(result=result)
    return True

def add_pubkey():
    args = [ssl_exe_path, 'rsa', '-in', 'rsa_private_key.pem', '-pubout', '-out', 'rsa_public_key.pem']
    result = subprocess.run(args, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"\033[0;31m 生成公钥文件失败！  \033[0m")
        print_errinfo(result=result)
    return True

def fix_input(file_path, key_path):
    if file_path == "key.bin.enc":
        temp_file_path = file_path
        file_path = key_path
        key_path = temp_file_path
    return file_path, key_path

def encrypt_file(file_path):
    print(f"\033[0;32m 正在加密文件：{file_path}  \033[0m")
    create_key = [ssl_exe_path, 'rand', '-base64', '32']
    result = subprocess.run(create_key, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"\033[0;31m 生成随机密钥失败！  \033[0m")
        print_errinfo(result=result)
    key = result.stdout
    with open('key.bin', 'w') as f:
        f.write(key)

    cmd1 = [ssl_exe_path, 'enc', '-aes-256-cbc', '-salt', '-in', file_path, '-out', file_path + '.enc', '-pass', 'file:./key.bin']
    cmd2 = [ssl_exe_path, 'pkeyutl', '-encrypt', '-inkey', './rsa_public_key.pem', '-pubin', '-in',  './key.bin', '-out', 'key.bin.enc']
    for cmd in [cmd1, cmd2]:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"\033[0;31m 命令执行失败！  \033[0m")
            print_errinfo(cmd, result)
    os.remove('key.bin')
    print(f"\033[0;32m 加密文件成功！  \033[0m")

def decrypt_file(file_path, key_path):
    print(f"\033[0;32m 正在解密文件：{file_path}  \033[0m")
    fix_input(file_path, key_path)
    file_name = file_path[:-4]
    cmd1 = [ssl_exe_path, 'pkeyutl', '-decrypt', '-inkey', './rsa_private_key.pem', '-in', key_path, '-out', 'key.bin']
    cmd2 = [ssl_exe_path, 'enc', '-d', '-aes-256-cbc', '-in', file_path, '-out', file_name, '-pass', 'file:./key.bin']
    for cmd in [cmd1, cmd2]:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"\033[0;31m 命令执行失败！  \033[0m")
            print_errinfo(cmd, result)
    os.remove('key.bin')
    print(f"\033[0;32m 解密文件成功！  \033[0m")

def keys_info():
    priv_mtime = os.path.getmtime('rsa_private_key.pem')
    priv_size = os.path.getsize('rsa_private_key.pem')
    priv_ctime = datetime.datetime.fromtimestamp(priv_mtime).strftime("%Y-%m-%d %H:%M:%S")
    pub_mtime = os.path.getmtime('rsa_public_key.pem')
    pub_size = os.path.getsize('rsa_public_key.pem')
    pub_ctime = datetime.datetime.fromtimestamp(pub_mtime).strftime("%Y-%m-%d %H:%M:%S")

    print(f"\033[0;34m 私钥文件大小：{priv_size}  ,创建日期：{priv_ctime} \033[0m")
    print(f"\033[0;34m 公钥文件大小：{pub_size}  ,创建日期：{pub_ctime} \033[0m")

def modify_keys():
    if not os.path.isfile('rsa_private_key.pem') or input('是否重新生成私钥？(y/n)') == 'y':
        add_privkey()
        print(f"\033[0;32m 私钥文件已生成！  \033[0m")

    add_pubkey()
    print(f"\033[0;32m 公钥文件已生成！  \033[0m")
    keys_info()

    finish_func()

def check_keys():
    if not os.path.isfile('rsa_public_key.pem') or not os.path.isfile('rsa_private_key.pem'):
        print("检测到密钥文件不存在，正在生成密钥文件...")
        modify_keys()
    else:
        print("----------------------------------------------------\n\
文件加解密工具\n\
使用方法:\n\
将需要加解密的文件拖拽到本程序图标中，即可完成加解密\n\
直接运行将检测密钥文件是否存在，不存在则将生成\n\
----------------------------------------------------\n")
        keys_info()
        if input('----------------------------------------------------\n\
检测到密钥文件存在,是否重新生成?(y/任意退出)') == 'y':
            modify_keys()
    exit(0)

def check_files(model):
    if model == 'encrypt' and not os.path.isfile('rsa_public_key.pem'):
        print(f"\033[0;31m 公钥文件不存在！  \033[0m")
        finish_func()
    elif model == 'decrypt' and not os.path.isfile('rsa_private_key.pem'):
        print(f"\033[0;31m 私钥文件不存在！  \033[0m")
        finish_func()

def check_model():
    if len(sys.argv) == 1:
        check_keys()
    elif len(sys.argv) == 2:
        check_files("encrypt")
        encrypt_file(sys.argv[1])
    else:
        check_files("decrypt")
        decrypt_file(sys.argv[1], sys.argv[2])

check_model()
    