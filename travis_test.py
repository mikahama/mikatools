#encoding: utf-8
import unittest
from mikatools import *
from mikatools import crypto


class TestFSTS(unittest.TestCase):

    def setUp(self):
        self.private, self.public = crypto.generate_keys()

    def test_json(self):
        result = {"äfdfer" : "009id"}
        json_dump(result, "test.json")
        d = json_load("test.json")
        self.assertEqual(result["äfdfer"], d["äfdfer"])

    def test_pickle(self):
        result = {"äfdfer" : "009id"}
        pickle_dump(result, "test.bin")
        d = pickle_load("test.bin")
        self.assertEqual(result["äfdfer"], d["äfdfer"])

    def test_sym_json(self):
        result = {'Росси́я': 'العربية'}
        json_dump(result, "test_sym.json", password="kissa", salt="koira")
        d = json_load("test_sym.json", password="kissa", salt="koira")
        self.assertEqual(result["Росси́я"], d["Росси́я"])

    def test_sym_json2(self):
        #Tests that the file gets encrypted... If not, then load without password won't fail
        result = {'Росси́я': 'العربية'}
        json_dump(result, "test_sym2.json", password="kissa", salt="koira")
        try:
            d = json_load("test_sym2.json")
            self.assertEqual(1,2)
        except:
            self.assertEqual(1,1)

    def test_sym_pickle(self):
        result = {'Росси́я': 'العربية'}
        pickle_dump(result, "test_sym.bin", password="kissa", salt="koira")
        d = pickle_load("test_sym.bin", password="kissa", salt="koira")
        self.assertEqual(result["Росси́я"], d["Росси́я"])

    def test_sym_pickle2(self):
        #Tests that the file gets encrypted... If not, then load without password won't fail
        result = {'Росси́я': 'العربية'}
        pickle_dump(result, "test_sym2.bin", password="kissa", salt="koira")
        try:
            d = pickle_load("test_sym2.bin")
            self.assertEqual(1,2)
        except:
            self.assertEqual(1,1)

    def test_asym_json(self):
        result = {'Росси́я': 'العربية'}
        json_dump(result, "test_asym.json", key=self.public)
        d = json_load("test_asym.json", key=self.private)
        self.assertEqual(result["Росси́я"], d["Росси́я"])

    def test_asym_json2(self):
        #Tests that the file gets encrypted... If not, then load without password won't fail
        result = {'Росси́я': 'العربية'}
        json_dump(result, "test_asym2.json", key=self.public)
        try:
            d = json_load("test_asym2.json")
            self.assertEqual(1,2)
        except:
            self.assertEqual(1,1)

    def test_asym_pickle(self):
        result = {'Росси́я': 'العربية'}
        pickle_dump(result, "test_asym.bin", key=self.public)
        d = pickle_load("test_asym.bin", key=self.private)
        self.assertEqual(result["Росси́я"], d["Росси́я"])

    def test_asym_pickle2(self):
        #Tests that the file gets encrypted... If not, then load without password won't fail
        result = {'Росси́я': 'العربية'}
        pickle_dump(result, "test_asym2.bin", key=self.public)
        try:
            d = pickle_load("test_asym2.bin")
            self.assertEqual(1,2)
        except:
            self.assertEqual(1,1)
    
    def test_save_load_keys(self):
        crypto.save_key(self.private,"id_rsa")
        crypto.save_key(self.public,"id_rsa.pub")

        public = crypto.load_key("id_rsa.pub")
        private = crypto.load_key("id_rsa")

    def test_save_load_keys_encrypted(self):
        crypto.save_key(self.private,"id_rsa_c", key_password="juujuu")
        private = crypto.load_key("id_rsa_c", key_password="juujuu")

    def test_save_load_keys_text(self):
        crypto.save_key(self.private,"id_rsa")
        crypto.save_key(self.public,"id_rsa.pub")

        public = crypto.load_key(open_read("id_rsa.pub").read())
        private = crypto.load_key(open_read("id_rsa").read())

    def test_save_load_keys_text_encrypted(self):
        crypto.save_key(self.private,"id_rsa_c", key_password="juujuu")
        private = crypto.load_key(open_read("id_rsa_c").read(), key_password="juujuu")
    
    def test_password_and_key(self):
        try:
            open_read("file", password="kissa", key="kissa")
            self.assertEqual(1, 2)
        except:
            #should crash
            self.assertEqual(1, 1)

    def test_password_and_key_write(self):
        try:
            open_write("file", password="kissa", key="kissa")
            self.assertEqual(1, 2)
        except:
            #should crash
            self.assertEqual(1, 1)

    def test_malformed_key(self):
        try:
            crypto.save_key(self.private,"id_rsa")
            private = crypto.load_key(open_read("id_rsa").read().replace("PRIVATE", ""))
            self.assertEqual(1, 2)
        except:
            #should crash
            self.assertEqual(1, 1)
    
    def test_no_pass_no_key_write(self):
        try:
            crypto.CryptoWriteStream("file")
            self.assertEqual(1, 2)
        except:
            #should crash
            self.assertEqual(1, 1)

    def test_no_pass_no_key_read(self):
        try:
            crypto.CryptoReadStream("file")
            self.assertEqual(1, 2)
        except:
            #should crash
            self.assertEqual(1, 1)



    def test_crypto_write_load(self):
        text = "salainen viestini\nsala_sala\n"
        o = open_write("secret.txt", password="super", salt="secret")
        o.write(text)
        o.close()
        i = open_read("secret.txt", password="super", salt="secret")
        t = ""
        for x in i:
            t += x
        self.assertEqual(t, text)

    def test_crypto_write_load_no_new(self):
        text = "salainen viestini\nsala_sala"
        o = open_write("secret2.txt", password="super", salt="secret")
        o.write(text,line_breaks=False)
        o.close()
        i = open_read("secret2.txt", password="super", salt="secret")
        t = i.read()
        self.assertEqual(t, text)

    def test_regular_write_load(self):
        text = "salainen viestini\nsala_sala"
        o = open_write("no_secret.txt")
        o.write(text)
        o.close()
        i = open_read("no_secret.txt")
        t = ""
        for x in i:
            t += x
        self.assertEqual(t, text)   
if __name__ == '__main__':
    unittest.main()