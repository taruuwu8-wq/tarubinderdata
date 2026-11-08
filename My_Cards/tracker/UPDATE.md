# อัปเดตข้อมูลเกมในหน้าเว็บคลังการ์ด

หน้าเว็บ: https://claude.ai/artifact/WATr8pLuf6PA81z5rzucAh

หน้าเว็บอ่านข้อมูลการ์ด (ผล ★1/★5, สี, Load, สาย, ภูมิภาค, แมพ, ราคาแลกวิญญาณ, โอกาสดรอปวิญญาณ) จาก
ฐานข้อมูลของหน้าเว็บ เอกสาร `meta/catalog` ก่อน ถ้าไม่มีจะใช้ชุดที่ฝังในหน้า
ข้อมูลผู้เล่น (การ์ดที่มี, ตัวละคร, Codex, รายการฟาม) อยู่ในฐานข้อมูลคนละส่วน **อย่าแตะ**

## ขั้นตอน (สำหรับแชทที่ดึงข้อมูล wiki หลังอัปเดต repo แล้ว)

1. อัปเดต `Monsters/*.md` / `Maps/_All_Maps.md` ตามปกติ
   ค่าที่ยืนยันจากในเกมหรือแพตช์ แต่ wiki ยังไม่แก้ → ใส่ใน `My_Cards/tracker/overrides.json`
2. สร้างข้อมูลใหม่ (จาก root ของ repo):

   ```bash
   python3 My_Cards/tracker/build.py
   ```

   ต้องขึ้น `160 cards · built YYYY-MM-DD` (หรือมากกว่าถ้ามีมอนใหม่)
3. ส่งข้อมูลเข้าเว็บ — **ทางหลัก ไม่ต้องเผยแพร่หน้าใหม่**:
   ใช้เครื่องมือ `ArtifactData` → `set` · url = ลิงก์ด้านบน · collection `meta` · doc_id `catalog`
   · `file_path` = `My_Cards/tracker/catalog_doc.json`
   (ถ้าเอกสารมีอยู่แล้ว ต้อง `get` ก่อนเพื่อเอา `version` มาใส่ `if_version`)
4. ถ้าแก้หน้าตาหรือโค้ดหน้าเว็บ (`card-vault.template.html`) → รัน build แล้วเผยแพร่
   `My_Cards/tracker/card-vault.html` ด้วยเครื่องมือ `Artifact` โดยใส่ `url` เป็นลิงก์ด้านบน (ห้ามสร้างลิงก์ใหม่)
5. commit ไฟล์ใน `My_Cards/tracker/` ที่เปลี่ยน

## ไฟล์

| ไฟล์ | คืออะไร |
| --- | --- |
| `build.py` | อ่าน repo → สร้าง catalog + หน้าเว็บ |
| `overrides.json` | ค่าที่ทับข้อมูล wiki (ยืนยันในเกม/แพตช์) |
| `card-vault.template.html` | โค้ดหน้าเว็บ (`__CATALOG__` = จุดที่ฝังข้อมูล) |
| `catalog.json` / `catalog_doc.json` | ผลลัพธ์จาก build |
| `card-vault.html` | หน้าเว็บพร้อมเผยแพร่ |

หน้าเว็บจะแสดงใต้รายการการ์ดว่า "ข้อมูลเกม: N การ์ด · อัปเดต วันที่ · จากฐานข้อมูล" ใช้เช็กว่าอัปเดตเข้าแล้ว
