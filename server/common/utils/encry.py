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
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization, hashes
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
                key_pem = file.read().strip()

        match method:
            case "public":
                return cls.rsa_public_decrypt(key_pem, ciphertext)
            case "private":
                return cls.rsa_private_decrypt(key_pem, ciphertext, password, pad_mode, hash_alg)

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
        if pem_key is None:
            app_path: str = get_settings().APP_PATH
            rsa_path: str = f"{app_path}/license/rsa_{method}_key.pem"
            rsa_path = pem_path if pem_path else rsa_path

            if not os.path.exists(rsa_path):
                error: str = str(f"Rsa encrypt error The {method} key file does not exist")
                raise Exception(f"{error}: server/license/rsa_{method}_key.pem")

            with open(rsa_path, mode="r", encoding="utf-8") as file:
                key_pem = file.read().strip()

        match method:
            case "public":
                return cls.rsa_public_encrypt(key_pem, plaintext, pad_mode, hash_alg)
            case "private":
                return cls.rsa_private_encrypt(key_pem, plaintext, password)

    @classmethod
    def rsa_public_decrypt(cls, public_key_pem: str, ciphertext: str) -> str | None:
        """
        RSA公钥解密: https://blog.csdn.net/Kernel_Heart/article/details/111524368
        (pip install rsa)

        Args:
            public_key_pem (str): 公钥
            ciphertext (str): 密文

        Returns:
            str | None

        Author:
            zero
        """
        try:
            # 加载公钥
            public_key = PublicKey.load_pkcs1_openssl_pem(public_key_pem.encode("utf-8"))
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
        private_key_pem: str,
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
            private_key_pem (str): 私钥
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
                private_key_pem.encode(),
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
        public_key_pem: str,
        plaintext: str,
        pad_mode: Literal["OAEP", "PKCS1v15"] = "OAEP",
        hash_alg: Literal["SHA1", "SHA256", "SHA384", "SHA512"] = "SHA1"
    ) -> str | None:
        """
        RSA公钥加密

        Args:
            public_key_pem (str): 公钥
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
                public_key_pem.encode()
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
        private_key_pem: str,
        plaintext: str,
        password: str = None
    ) -> str | None:
        """
        RSA私钥加密 (私钥加密仅支持 PKCS1v15)
        注意: 不需要用私钥加密,应当用公钥加密,私钥解密

        Args:
            private_key_pem (str): 私钥
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
                private_key_pem.encode(),
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
