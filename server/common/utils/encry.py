# +----------------------------------------------------------------------
# | WaitAdmin(fastapi)快速开发后台管理系统
# +----------------------------------------------------------------------
# | 欢迎阅读学习程序代码,建议反馈是我们前进的动力
# | 程序完全开源可支持商用,允许去除界面版权信息
# | gitee:   https://gitee.com/wafts/waitadmin-python
# | github:  https://github.com/topwait/waitadmin-python
# | 官方网站: https://www.waitadmin.cn
# | WaitAdmin团队版权所有并拥有最终解释权
# +----------------------------------------------------------------------
# | Author: WaitAdmin Team <2474369941@qq.com>
# +----------------------------------------------------------------------
import os
import base64
from typing import Literal, Dict, Any
from rsa import core, PublicKey, transform
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from config import get_settings


class EncryUtil:
    """
    加密/解密工具
    温馨提示: 建议您使用【公钥加密,私钥解密】
    """

    MGF: Dict[str, hashes.HashAlgorithm] = {
        "SHA1": hashes.SHA1(),       # 遗留系统[默认] (不推荐,存在弱点)
        "SHA256":  hashes.SHA256(),  # 现代安全标准 (推荐)
        "SHA384":  hashes.SHA384(),  # 高安全需求场景
        "SHA512":  hashes.SHA512()   # 超高安全需求场景
    }

    @classmethod
    def rsa_decrypt(
        cls,
        ciphertext: str,
        method: Literal["public", "private"] = "private",
        pad_mode: Literal["OAEP", "PKCS1v15"] = "OAEP",
        hash_alg: Literal["SHA1", "SHA256", "SHA384", "SHA512"] = "SHA1",
        password: str = None,
        pem_path: str = None,
        pem_key: str = None
    ):
        """
        RSA解密
        生成密钥网站[1]: https://apiked.com/rsa
        生成密钥网站[2]: https://cryptotools.net/rsagen

        Args:
            ciphertext (str): 密文
            method (str): 解密方式: [public,private]
            pad_mode (Literal["OAEP", "PKCS1v15"]): 填充标识
            hash_alg (Literal["SHA1", "SHA256", "SHA384", "SHA512"]): OAEP算法
            password (str): 私钥密码,没有可以流空
            pem_path (str): 密钥文件路径,pem_key不为真时才生效
            pem_key (str): 密钥(公钥/私钥),不传则自动读取根目录

        Returns:
            str

        Author:
            zero
        """
        if pem_key is None:
            app_path: str = get_settings().APP_PATH
            rsa_path: str = f"{app_path}/license/rsa_{method}_key.pem"
            rsa_path = pem_path if pem_path else rsa_path

            if not os.path.exists(rsa_path):
                error: str = f"Rsa decrypt error The {method} key file does not exist"
                raise Exception(f"{error}: server/license/rsa_{method}_key.pem")

            with open(rsa_path, mode="r", encoding="utf-8") as file:
                pem_key = file.read().strip()

        match method:
            case "public":
                return cls.rsa_public_decrypt(pem_key, ciphertext)
            case "private":
                return cls.rsa_private_decrypt(pem_key, ciphertext, password, pad_mode, hash_alg)

    @classmethod
    def rsa_encrypt(
        cls,
        plaintext: str,
        method: Literal["public", "private"] = "public",
        pad_mode: Literal["OAEP", "PKCS1v15"] = "OAEP",
        hash_alg: Literal["SHA1", "SHA256", "SHA384", "SHA512"] = "SHA1",
        password: str = None,
        pem_path: str = None,
        pem_key: str = None
    ):
        """
        RSA加密 (生成密钥网站: https://apiked.com/rsa)

        Args:
            plaintext (str): 明文
            method (str): 加密方式: [public,private]
            pad_mode (Literal["OAEP", "PKCS1v15"]): 填充标识
            hash_alg (Literal["SHA1", "SHA256", "SHA384", "SHA512"]): OAEP算法
            password (str): 私钥密码,没有可以流空
            pem_path (str): 密钥文件路径,pem_key不为真时才生效
            pem_key (str): 密钥(公钥/私钥),不传则自动读取根目录

        Returns:
            str: Base64编码的密文

        Author:
            zero
        """
        print(pem_key)
        if pem_key is None:
            app_path: str = get_settings().APP_PATH
            rsa_path: str = f"{app_path}/license/rsa_{method}_key.pem"
            rsa_path = pem_path if pem_path else rsa_path

            if not os.path.exists(rsa_path):
                error: str = str(f"Rsa encrypt error The {method} key file does not exist")
                raise Exception(f"{error}: server/license/rsa_{method}_key.pem")

            with open(rsa_path, mode="r", encoding="utf-8") as file:
                pem_key = file.read().strip()

        match method:
            case "public":
                return cls.rsa_public_encrypt(pem_key, plaintext, pad_mode, hash_alg)
            case "private":
                return cls.rsa_private_encrypt(pem_key, plaintext, password)

    @classmethod
    def rsa_public_decrypt(cls, public_pem_key: str, ciphertext: str) -> str | None:
        """
        RSA公钥解密: https://blog.csdn.net/Kernel_Heart/article/details/111524368
        (pip install rsa)

        Args:
            public_pem_key (str): 公钥
            ciphertext (str): 密文

        Returns:
            str | None

        Author:
            zero
        """
        try:
            # 加载公钥
            public_key = PublicKey.load_pkcs1_openssl_pem(public_pem_key.encode("utf-8"))
            # 将密文转换为整数形式: RSA算法需要处理大整数
            cipher_bytes = transform.bytes2int(base64.b64decode(ciphertext.strip()))
            # 用公钥对密文进行解密: 指数(e)和模数(n)
            decrypted_text = core.decrypt_int(cipher_bytes, public_key.e, public_key.n)
            # 将解密整数转换回字节
            final_text = transform.int2bytes(decrypted_text)
            # 提取有效数据
            plaintext = final_text[final_text.index(0) + 1:]
            # 返回解密内容
            return plaintext.decode("utf-8")
        except Exception as e:
            print("Rsa public decrypt error: " + str(e))

    @classmethod
    def rsa_private_decrypt(
        cls,
        private_pem_key: str,
        ciphertext: str,
        password: str = None,
        pad_mode: Literal["OAEP", "PKCS1v15"] = "OAEP",
        hash_alg: Literal["SHA1", "SHA256", "SHA384", "SHA512"] = "SHA1"
    ) -> str | None:
        """
        RSA私钥解密
        报错: Password was not given but private key is encrypted.
        说明: 私钥没有设置密码为什么还会报错呢? 请注意你的私钥是不是 ... ENCRYPTED PRIVATE KEY-----
             如果是就是私钥给加密码了,没密码的应该是这样的(没有ENCRYPTED) ...PRIVATE KEY-----
             建议你换一个生成RSA的网站生成密钥, 如: https://cryptotools.net/rsagen

        Args:
            private_pem_key (str): 私钥
            ciphertext (str): 密文
            password (str): 私钥密码
            pad_mode (Literal["OAEP", "PKCS1v15"]): 填充标识
            hash_alg (Literal["SHA1", "SHA256", "SHA384", "SHA512"]): OAEP算法

        Returns:
            str

        Author:
            zero
        """
        try:
            # 加载私钥
            private_key = serialization.load_pem_private_key(
                private_pem_key.encode(),
                password=password.encode() if password else None,
                backend=default_backend()
            )

            # 使用私钥解密
            if pad_mode == "OAEP":
                alg: hashes.HashAlgorithm = cls.MGF.get(hash_alg)
                plaintext = private_key.decrypt(
                    base64.b64decode(ciphertext),
                    padding.OAEP(
                        mgf=padding.MGF1(algorithm=alg),
                        algorithm=alg,
                        label=None
                    )
                )
            elif pad_mode == "PKCS1v15":
                plaintext = private_key.decrypt(
                    base64.b64decode(ciphertext),
                    padding.PKCS1v15()
                )

            # 返回解密内容
            return plaintext.decode("utf-8")
        except Exception as e:
            print("Rsa private decrypt error: " + str(e))

    @classmethod
    def rsa_public_encrypt(
        cls,
        public_pem_key: str,
        plaintext: str,
        pad_mode: Literal["OAEP", "PKCS1v15"] = "OAEP",
        hash_alg: Literal["SHA1", "SHA256", "SHA384", "SHA512"] = "SHA1"
    ) -> str | None:
        """
        RSA公钥加密

        Args:
            public_pem_key (str): 公钥
            plaintext (str): 明文
            pad_mode (Literal["OAEP", "PKCS1v15"]): 填充标识
            hash_alg (Literal["SHA1", "SHA256", "SHA384", "SHA512"]): OAEP算法

        Returns:
            str: Base64编码的密文

        Author:
            zero
        """
        try:
            # 加载公钥
            public_key = serialization.load_pem_public_key(
                public_pem_key.encode()
            )

            # 使用公钥加密
            if pad_mode == "OAEP":
                alg: hashes.HashAlgorithm = cls.MGF.get(hash_alg)
                ciphertext = public_key.encrypt(
                    plaintext.encode("utf-8"),
                    padding.OAEP(
                        mgf=padding.MGF1(algorithm=alg),
                        algorithm=alg,
                        label=None
                    )
                )
            elif pad_mode == "PKCS1v15":
                ciphertext = public_key.encrypt(
                    plaintext.encode("utf-8"),
                    padding.PKCS1v15()
                )

            # 返回Base64编码的密文
            buf: Any = ciphertext
            return base64.b64encode(buf).decode("utf-8")
        except Exception as e:
            print("Rsa public encrypt error: " + str(e))

    @classmethod
    def rsa_private_encrypt(
        cls,
        private_pem_key: str,
        plaintext: str,
        password: str = None
    ) -> str | None:
        """
        RSA私钥加密 (私钥加密仅支持 PKCS1v15)
        注意: 不需要用私钥加密,应当用公钥加密,私钥解密

        Args:
            private_pem_key (str): 私钥
            plaintext (str): 明文
            password: str = None
        Returns:
            str: 密文

        Author:
            zero
        """
        try:
            # 加载私钥
            private_key = serialization.load_pem_private_key(
                private_pem_key.encode(),
                password=password.encode() if password else None,
                backend=default_backend()
            )

            # 取私钥和公钥参数
            private_numbers = private_key.private_numbers()
            public_numbers = private_key.public_key().public_numbers()
            n = public_numbers.n
            d = private_numbers.d

            # 将明文转换为字节
            plaintext_bytes: Any = plaintext.encode("utf-8")

            # 计算需要的填充长度
            key_size_bytes = (private_key.key_size + 7) // 8
            padding_length = key_size_bytes - len(plaintext_bytes) - 3
            if padding_length < 8:
                raise ValueError(f"明文太长，无法应用PKCS#1 v1.5填充")

            # 生成非零随机填充
            padding_bytes = b""
            while len(padding_bytes) < padding_length:
                byte = os.urandom(1)
                if byte != b"\x00":
                    padding_bytes += byte

            # 构造并假面数据
            bt: Any = b'\x00'
            padded_message = b'\x00\x02' + padding_bytes + bt + plaintext_bytes
            padded_int = int.from_bytes(padded_message, byteorder="big")
            ciphertext_int = pow(padded_int, d, n)
            ciphertext: Any = ciphertext_int.to_bytes(key_size_bytes, byteorder="big")

            # 返回Base64编码的密文
            return base64.b64encode(ciphertext).decode("utf-8")
        except Exception as e:
            print("Rsa private encrypt error: " + str(e))
            return None
            
    @classmethod
    def generate_rsa_pem(
        cls,
        key_size: Literal[512, 1024, 2048, 3072, 4096] = 2048,
        password: str = None,
        save_path: str = None,
        file_prefix: str = "rsa",
        public_exponent: int = 65537,
        private_format: Literal["PKCS8", "TraditionalOpenSSL"] = "PKCS8",
        overwrite: bool = False
    ) -> Dict[str, str]:
        """
        生成RSA密钥对
        
        Args:
            key_size (int): 密钥长度: 推荐2048或4096位
            password (str): 私钥密码: 不需要可留空
            save_path (str): 保存路径: 不指定则不保存到文件
            file_prefix (str): 文件名前缀: 默认为rsa
            public_exponent (int): 公钥指数:通常为65537,不建议修改
            private_format (str): 私钥格式: PKCS8(现代标准)或TraditionalOpenSSL(传统格式)
            overwrite (bool): 是否覆盖已存在的文件,默认为False
            
        Returns:
            Dict[str, str]

        Author:
            zero
        """
        try:
            # 生成私钥
            private_key = rsa.generate_private_key(
                public_exponent=public_exponent,
                key_size=key_size,
                backend=default_backend()
            )

            # 选择私钥格式
            if private_format == "PKCS8":
                format_type = serialization.PrivateFormat.PKCS8
            else:
                format_type = serialization.PrivateFormat.TraditionalOpenSSL
            
            # 设置私钥序列化选项
            if password:
                encryption_algorithm = serialization.BestAvailableEncryption(password.encode())
            else:
                encryption_algorithm = serialization.NoEncryption()
            
            # 序列化私钥为PEM格式
            private_pem = private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=format_type,
                encryption_algorithm=encryption_algorithm
            ).decode("utf-8")

            # 序列化公钥为PEM格式
            public_key = private_key.public_key()
            public_pem = public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ).decode("utf-8")
            
            # 准备返回结果
            result = {
                "private_key": private_pem,
                "public_key": public_pem,
                "key_size": key_size,
                "private_format": private_format,
                "has_password": password is not None
            }

            # 如果指定了保存路径,则保存到文件
            if save_path:
                # 确保目录存在
                os.makedirs(save_path, exist_ok=True)

                # 构建文件路径
                private_key_path = f"{save_path}/{file_prefix}_private_key.pem"
                public_key_path = f"{save_path}/{file_prefix}_public_key.pem"

                # 检查文件是否已存在
                if not overwrite:
                    if os.path.exists(private_key_path):
                        raise FileExistsError(f"The private key file already exists: {private_key_path}")
                    if os.path.exists(public_key_path):
                        raise FileExistsError(f"The public key file already exists: {public_key_path}")

                # 保存私钥
                with open(private_key_path, "w", encoding="utf-8") as f:
                    f.write(private_pem)
                    
                # 保存公钥
                with open(public_key_path, "w", encoding="utf-8") as f:
                    f.write(public_pem)

                # 添加文件路径到结果
                result["private_path"] = private_key_path
                result["public_path"] = public_key_path
            return result
        except Exception as e:
            raise Exception(f"RSA key pair generation error: {str(e)}")
