# งานต่อบน Codex Cloud — Taru Build Lab

## เริ่มตรงนี้

ข้อมูลเกมและโค้ดแดชบอร์ดอยู่ใน repo นี้แล้ว โค้ดอยู่ `Dashboard/` พร้อมรูปและข้อมูลที่เปิดใช้งานได้โดยไม่ดึง Wiki ใหม่

สร้าง Cloud environment โดยเลือก repo `taruuwu8-wq/tarubinderdata` ใช้ Node.js 22+ แล้วรัน:

```sh
cd Dashboard
npm test
npm run preview
```

ไม่มี npm dependencies ให้ติดตั้ง ไม่ต้องใส่ API key เพื่อเปิดเว็บหรือทดสอบข้อมูลเดิม หากระบบ preview ต้องรับการเชื่อมต่อภายนอก ใช้ `HOST=0.0.0.0 PORT=4173 npm run preview` และระบบ forward port ของ Cloud

คู่มือทางการ: https://learn.chatgpt.com/docs/environments/cloud-environments

## สถานะที่ย้ายมา

- เว็บเดิม: https://taru-build-lab-1109.tallraisin4.chatgpt.site
- รุ่นหน้าเว็บ v1.4 · GEAR SELECTOR
- Sites project: `appgprj_6af1e04581c88191bc21ba4e25fcb1b4` — คงเว็บเดิมและสิทธิ์ private
- โค้ดจาก Sites commit `d9cdc059468d98a0fe6d32710d4667098f641b36`
- ข้อมูลเกมที่เว็บใช้อยู่ pin ที่ commit `00356620a50e4f358d35d0acc369ba7dd04c1da9`
- ดึงสดเพิ่ม 148 หน้า ล่าสุด 2026-11-10 ใช้ 148 เครดิต Firecrawl มีหลักฐานใน `Sources/LIVE_CAPTURE.json`
- มีของ Tier 10 จำนวน 279 ชิ้น พร้อมรูป Wiki; 138 ชิ้นผ่านเงื่อนไข Rogue แล้วกรองตามช่องอีกชั้น
- มีตัวเลือกของ/ออฟ/ตีบวก/ความหายาก พร้อมตรวจช่วงค่า และแท็บแมพใหม่ 8 แมพ
- รวมรายละเอียดแมพแล้ว 56 แมพ แต่ยังมีข้อมูลเดิมวันที่ 7 พ.ย. 640 หน้า และ URL ไม่ได้ดึง 1,671 รายการ หลายรายการตั้งใจข้ามตามขอบเขต

## เป้าหมายผู้เล่น

Taru เป็น Rogue ฟาร์มออนไลน์ AUTO ที่ Shellforge Basin เน้นหาเงินและตี Mini-boss เพื่อสะสมวิญญาณแลกการ์ด ใช้ชุดเดิมเป็นฐานทดลอง ตอบสั้นและประหยัด token

การ์ดเดิม ★5 จำนวน 9 ใบ: Brass Mimic, Crucible Hound, Lamp Wisp, Muster Hound, Reed Crane, Shrine Firefly, Throne Guard, Tide Brute, Vale Keeper

เก็บข้อมูลเกียร์และค่าสเตตัสจากภาพไว้ใน `Dashboard/dist/data.json` ไม่ตีความ ATK/HP ในภาพว่าเป็นผลคำนวณของบิลด์ทดลอง ค่ามือรองยังเป็นสมมติฐานผู้ใช้ ส่วน Moth Mask Crit DMG ที่อ่านเป็น 245% ยังขัดกับ Wiki จึงไม่นำมารวม ห้ามเดาแก้เป็น 24.5%

## เมื่ออัปเดตข้อมูลใน repo

รัน `cd Dashboard && npm run sync:data && npm test` เพื่อสร้างแค็ตตาล็อกจากข้อมูลที่มีแล้ว รัน `npm run export:html` ได้ไฟล์ HTML เปิดแยกได้

การดึง Wiki เพิ่มต้องเชื่อม Firecrawl ใน environment นั้นก่อน ไม่ถือว่าการเชื่อมในแชตเดิมย้ายไปด้วยอัตโนมัติ ใช้รายการเฉพาะเป้าหมายและ `maxAge: 0` เมื่อขอข้อมูลสด เก็บ Markdown/JSON เต็ม URL วันที่ และเครดิตที่ใช้

ขอบเขตเดิม: รายละเอียดของ Tier 10 เท่านั้น วัตถุดิบสำคัญและยา/อาหารระดับสูง ไม่ต้องดึง Tier 1–9 แฟชั่น หรือขยะขาย NPC ทั้งหมด ดู `CRAWL_REPORT.md` และ `MISSING_DATA.md`

งานที่อาจทำต่อ: รีเฟรชสกิล Rogue ที่ใช้และการ์ดนอก Shellforge, ปรับตัวกรองและ UX ของออฟ, จำลองค่าต่อสู้เฉพาะเมื่อมีกติกาคำนวณที่ตรวจสอบแล้ว

## ข้อจำกัดของการย้าย

- ย้ายโค้ด รูป ข้อมูลตั้งต้น การทดสอบ และเอกสารแล้ว ไม่ได้ย้าย localStorage ของเบราว์เซอร์ ผู้ใช้ส่งออก JSON จากเว็บเพื่อย้ายบิลด์ที่บันทึกเองได้
- GitHub เป็นที่เก็บ source; เว็บ Sites เดิมยังทำงาน การ push ที่นี่ไม่ deploy เว็บโดยอัตโนมัติ
- หาก Cloud มี Sites ให้เปิด source ของ project เดิมตาม skill แล้วนำการแก้ไขจาก `Dashboard/` ไปเผยแพร่ หากไม่มี ให้ commit งานไว้และ deploy ผ่าน session ที่เชื่อม Sites
- ไม่ย้าย credential, token, session login หรือเครื่องมือส่วนตัวจากคอมพิวเตอร์เดิม

## ข้อความเริ่มงานที่ใช้ได้

> อ่าน AGENTS.md และ CLOUD_HANDOFF.md แล้วทำงานต่อที่ Dashboard/ ใช้ข้อมูลใน repo เป็นหลัก รัน npm test ก่อนแก้ไข คงข้อมูลผู้เล่นและเว็บ Sites เดิม หากต้องดึง Wiki ใหม่ให้ยึดขอบเขต Tier 10 และรายงานเฉพาะส่วนที่เปลี่ยน
