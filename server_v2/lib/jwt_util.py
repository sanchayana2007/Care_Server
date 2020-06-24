#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

sys.path.append('./utils')

import jwt, random
from .fernet_crypto import *
from .log_util import Log
from .time_util import timeNow
from bson.objectid import ObjectId

SECRETS = [
        'IS-*HGJHFKJL^%&*O(PTDJFKGHJKRE%^UR&IT*O^(&P&TRYJFK^%^*&(*^*%%*^(^&O^*(*P(UYUFHGJLKKJGFHRTO&^*&YUTYII',
        'IS-%*^&*YUTIFUKGLH:GCMGV<JHB>KJNLKML&^*&(POUIOUGH<GKJLJKJHJFHG<GBJKL:TOO:IY>UGBJNMJJKJuBKMLFGHJ**UJH',
        'IS-%*^&*P(*F<HGBJHNKJLKLJJRTUYIUOIP&^%&*&(*(*&^&(*IPOJHJGJBJNKMLK:IUTYYIUOUO&*&(**^&%$#@$%$^%&^*&(*)',
        'IS-&%^$*&*(&$^&%O*^*P&YUTYFGHJOKIYUYTRTYUIOIYTYUFGHJKY^&(*$#!@#$%$^%&^*&(*)_)GUHIJOKPFCVBNM$^%&^*^&(',
        'IS-$*%^&(&^*{(*})(_TYGHJKLGFJHJKL%$^%&^*&(*)(&^&%^ERTFGYHJK^%$&^*&(*)(YTFYGHJK^%&*()(FGHJK&^$%%&^*&(',
        'IS-^$%&^*%&(*&({)(})_UYTIFHVBJNKMLK!@#$%^&*()POIUYGFVBNJKLP*&^%$%^&*()UYTFGHJK*&^%$^&*()UYTFGHJKL&^&',
        'IS-$#^%^&*()_)(YTGHUIOP{(*&^%$%^&*(OIUGFGHJKY#$%^&*()_IUYTFGHJKL!@#$%^&*()DFGHJKL@#$%^&*IOJHG@#RTY^^',
        'IS-!@#$%^&*()_IUYTREDFGHJIOPUY$#$%^&*(#$^%&^&**(&^%RTGYHJ@#$%^&*(*UYTRFGHJKL#$%^&U*()(*&^%TYU((^&*()',
        'IS-!@#$%^&*()OIUYTREDFGHNM@#$%^&OFDGGHJKYTR$%$^&*()(RTDFGHJKOU%$^%&^*&(&*&^%$#%$^%&^*&(*(*%$^%&^*&(*',
        'IS-#$%^&*()UYTRYUIOPHRE!@#$%^&*()_(*&^%$#@#$%^&*())(*&^%$#@#$%^&*(*&^%$#@!@#$%^&*(UYTRERTYUIOGFVBJKJ',
        'IS-#$%^&*()UYTRYUIOPHREi*&v^o*&v^SDLKFJHSDLFUU8OSYO876SO87D6%*&^(*&^*&^ @!@#$%^&*(UYTRERTYUIOGFVBJKJ'
        ]
OPTIONS = {
        'verify_signature': True,
        'verify_exp': True,
        'verify_nbf': False,
        'verify_iat': True,
        'verify_aud': False
        }

def JWT_ENCODE(payload = str):
    try:
        kyE = FN_ENCRYPT(payload, True)
        if (kyE):
            index = random.randint(0, len(SECRETS) - 1)
            kyEn = jwt.encode(
                    {
                        'key': kyE.decode(),
                        'exp': dtime.datetime.utcnow() + dtime.timedelta(seconds=31536000)
                    },
                    SECRETS[index],
                    algorithm='HS256'
                )
            return kyEn
        else:
            return False
    except:
        return False

    return False


def JWT_DECODE(token = str):
    try:
        if len(SECRETS):
            for s in SECRETS:
                try:
                    tokenObj = jwt.decode(token, s, options=OPTIONS)
                    kyDe = FN_DECRYPT(tokenObj['key'])
                    if kyDe:
                        return kyDe
                except:
                    continue

    except:
        return False

    return False

