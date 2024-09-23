import ssl
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.ssl_ import create_urllib3_context


# SSL 配置


class SSLAdapter(HTTPAdapter):
    def __init__(self, cert=None, key=None, bundle=None, **kwargs):
        self.cert = cert
        self.key = key
        self.bundle = bundle
        super().__init__(**kwargs)

    def init_poolmanager(self, *args, **kwargs):
        context = create_urllib3_context()
        if self.cert and self.key:
            context.load_cert_chain(certfile=self.cert, keyfile=self.key)
        if self.bundle:
            context.load_verify_locations(cafile=self.bundle)
        context.check_hostname = False  # 不检查主机名
        context.verify_mode = ssl.CERT_NONE  # 不验证证书
        kwargs['ssl_context'] = context
        return super().init_poolmanager(*args, **kwargs)


def _addSsl(cert, key, hundle):
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile=cert, keyfile=key)
    context.load_verify_locations(cafile=hundle)
    context.verify_mode = ssl.CERT_REQUIRED  # 表示需要进行客户端认证。
    context.check_hostname = False  # 禁用主机名验证
    return context


def _ssl_session(cert, key, hundle):
    session = requests.Session()
    adapter = SSLAdapter(cert=cert, key=key, bundle=hundle)
    session.mount('https://', adapter)
    session.verify = False  # 禁用证书验证
    return session

