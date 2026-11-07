# Patch notes — received 2026-11-07

> **Status:** [PATCH] · **Provenance:** Official Binder Town Discord announcement posted by a game admin (per the user, who copied it into chat on 2026-11-07). Exact post date/link not archived here. Not present on the Wiki (no patch-notes page).  
> **Verbatim source:** [_source/patch_received_2026-11-07.txt](_source/patch_received_2026-11-07.txt)  
> **Precedence:** where this patch contradicts Wiki text crawled on 2026-11-07, the patch is newer. The Wiki text is kept unchanged; affected files carry a notice.

## Conflicts / items needing attention

- **#1** แมพทวีปแรก 28 แมพใหญ่ขึ้นประมาณ 3 เท่า จัดจุดมอนและจุด Gathering ใหม่ ไม่มีมอนเกิดใกล้จุด Gathering หรือขอบแมพ — [TO_VERIFY] Which 28 maps form the 'first continent' is not named in the patch; map sizes and spawn layouts on the Wiki may predate this change.
- **#7** แฟชั่นใหม่ 106 ชิ้นในร้านเพชร: ชุด 19, ปีก 15, ออร่า 18, สหาย 26, พาหนะและบอร์ด 28 — CONFLICT-LIKELY: Wiki crawl (2026-11-07) lists 69 fashion items; the 106 new items are not in this knowledge base.
- **#9** พาหนะและบอร์ดจากร้านเพชรวิ่งเร็วขึ้น 50% (เดิม 15%) รวมของที่ซื้อไปแล้ว — CONFLICT: Wiki states mount run speed '+15%'; patch states 50% (was 15%). Patch is newer.
- **#25** DEX ออกบนเกราะ รองเท้า และหมวกได้ — [TO_VERIFY] DEX on armor/boots/headgear is new per patch; the tier-10 per-item affix pools in this KB may not include it yet.
- **#29** Oathbound Band: MATK เท่ากับ ATK และ INT เท่ากับ STR — CONFLICT-LIKELY: Wiki shows Oathbound Band as 'ATK +10% · MATK +10% · Block +5%' with Twin Oath; the patch adds MATK = ATK and INT = STR.
- **#34** Soulforge ชิ้นสุดท้ายข้ามแรงก์ 8 ได้ — [UNKNOWN] 'Soulforge' does not appear anywhere in the crawled Wiki.

## All changes

| # | Change (verbatim) | Topic | System | Affected KB files | Wiki comparison |
|---|---|---|---|---|---|
| 1 | แมพทวีปแรก 28 แมพใหญ่ขึ้นประมาณ 3 เท่า จัดจุดมอนและจุด Gathering ใหม่ ไม่มีมอนเกิดใกล้จุด Gathering หรือขอบแมพ | — | Maps | [_All_Maps.md](../Maps/_All_Maps.md) | [TO_VERIFY] Which 28 maps form the 'first continent' is not named in the patch; map sizes and spawn layouts on the Wiki may predate this change. |
| 2 | ปรับแมพให้ใหญ่ขึ้น มอนกระจายตัวมากขึ้น ลดจำนวนแชแนลที่ไม่จำเป็นออก | — | Maps | [_All_Maps.md](../Maps/_All_Maps.md) | Channel counts / spawn spread: not compared. |
| 3 | มอนไล่ตามแล้วเดินอ้อมเสา ต้นไม้ และหินแทนการติด | — | Monsters (AI) | [_All_Monsters.md](../Monsters/_All_Monsters.md) | No Wiki statement found to compare. |
| 4 | แมพเริ่มต้นมีมอนใกล้จุดเกิดเท่าเดิม | มอนไล่ตามแล้วเดินอ้อมเสา ต้นไม้ และหินแท | Maps | [_All_Maps.md](../Maps/_All_Maps.md) | No Wiki statement found to compare. |
| 5 | ลดอาการตัวละครเดินกระตุกตอนเซิร์ฟเวอร์ยุ่ง และลดการค้างของเซิร์ฟเวอร์ | — | Server | — | Not a game-data change. |
| 6 | ร้านเพชร, Premium, Daily, Party, Guild ไม่ค้างหน้าโหลดแล้ว หน้าต่างอื่นเปิดเร็วขึ้น | ลดอาการตัวละครเดินกระตุกตอนเซิร์ฟเวอร์ยุ | UI | [shop.md](../Game_Systems/shop.md) · [premium.md](../Game_Systems/premium.md) · [pass.md](../Game_Systems/pass.md) · [social.md](../Game_Systems/social.md) · [windows.md](../Game_Systems/windows.md) | Performance fix; no data impact. |
| 7 | แฟชั่นใหม่ 106 ชิ้นในร้านเพชร: ชุด 19, ปีก 15, ออร่า 18, สหาย 26, พาหนะและบอร์ด 28 | — | Fashion | [fashion.md](../Game_Systems/fashion.md) · [fashion.md](../Items/_Listings/fashion.md) · [shop.md](../Game_Systems/shop.md) | CONFLICT-LIKELY: Wiki crawl (2026-11-07) lists 69 fashion items; the 106 new items are not in this knowledge base. |
| 8 | ย้อมสีหมวกและอาวุธได้ ใช้น้ำยา 1 ขวดต่อส่วนที่เปลี่ยน | — | Fashion / Dye | [fashion.md](../Game_Systems/fashion.md) · [mat.md](../Items/_Listings/mat.md) | Wiki dye item text describes hair/outfit colour; hat/weapon dyeing is new per patch. |
| 9 | พาหนะและบอร์ดจากร้านเพชรวิ่งเร็วขึ้น 50% (เดิม 15%) รวมของที่ซื้อไปแล้ว | — | Fashion / Mounts | [fashion.md](../Game_Systems/fashion.md) · [fashion.md](../Items/_Listings/fashion.md) · [shop.md](../Game_Systems/shop.md) | CONFLICT: Wiki states mount run speed '+15%'; patch states 50% (was 15%). Patch is newer. |
| 10 | Bank ฝาก / ถอนหลายกองในครั้งเดียว และมีปุ่มรวมกองในคลัง | — | Bank | [rules.md](../Game_Systems/rules.md) | New UI feature; Wiki Bank rules otherwise unaffected. |
| 11 | ค้นหาเพื่อนจากชื่อหรือ UID ได้ คำขอเป็นเพื่อนรอคนออฟไลน์ 14 วัน | — | Social | [social.md](../Game_Systems/social.md) | New feature. |
| 12 | ซ่อนอุปกรณ์จากโปรไฟล์ได้ (แฟชั่นยังเห็น) | ค้นหาเพื่อนจากชื่อหรือ UID ได้ คำขอเป็นเ | Social / Profile | [social.md](../Game_Systems/social.md) · [windows.md](../Game_Systems/windows.md) | New feature. |
| 13 | Guild War: Leader ยอมแพ้ได้หลังรบผ่าน 1 รอบ (นับแพ้เต็ม) | — | Guild War | [pvp.md](../Game_Systems/pvp.md) · [social.md](../Game_Systems/social.md) | No Wiki statement found to compare. |
| 14 | CH10 นับแต้มสงครามได้ทุกเวลา | Guild War: Leader ยอมแพ้ได้หลังรบผ่าน 1  | Guild War | [pvp.md](../Game_Systems/pvp.md) | No Wiki statement found to compare. |
| 15 | PvP Warrior: Rend / Gash หลบไม่ได้ | — | Class: Warrior (PvP) | [Warrior.md](../Classes/Warrior.md) · [rend.md](../Skills/Warrior/rend.md) · [gash.md](../Skills/Warrior/gash.md) | PvP trait changes; Wiki class traits may predate this patch. |
| 16 | HP ต่ำกว่า 60% เริ่มดูดเลือดจากผู้เล่น สูงสุด 20% | PvP Warrior: Rend / Gash หลบไม่ได้ | Class: Warrior (PvP) | [Warrior.md](../Classes/Warrior.md) | PvP trait change. |
| 17 | HP ต่ำกว่า 30% ได้โล่ 15% ของ HP นาน 6 วิ (ทุก 60 วิ) | PvP Warrior: Rend / Gash หลบไม่ได้ | Class: Warrior (PvP) | [Warrior.md](../Classes/Warrior.md) | PvP trait change. |
| 18 | PvP Rogue: Assassinate ใส่เป้า HP ต่ำกว่า 30% แรงขึ้น 60% | — | Class: Rogue (PvP) | [Rogue.md](../Classes/Rogue.md) · [assassinate.md](../Skills/Rogue/assassinate.md) | PvP trait change. |
| 19 | ฮิตแรกหลัง Dash / Fade แรงขึ้น 35% | PvP Rogue: Assassinate ใส่เป้า HP ต่ำกว่ | Class: Rogue (PvP) | [Rogue.md](../Classes/Rogue.md) · [fade.md](../Skills/Rogue/fade.md) | PvP trait change. |
| 20 | ฆ่าผู้เล่นแล้วได้ Dash คืน | PvP Rogue: Assassinate ใส่เป้า HP ต่ำกว่ | Class: Rogue (PvP) | [Rogue.md](../Classes/Rogue.md) | PvP trait change. |
| 21 | PvP Mage: โดนตีประชิดแล้วปล่อย Frost Nova ผลัก 3 ช่องและตรึง 1.5 วิ (ทุก 12 วิ) | — | Class: Mage (PvP) | [Mage.md](../Classes/Mage.md) | New PvP trait. Note: on the Wiki 'Frost Nova' is also the name of Nova's Evolution A (Skills/Mage/nova.md) — different mechanic. |
| 22 | PvP Scout: เป้าที่ติด Mark หลบได้ครึ่งเดียว | — | Class: Scout (PvP) | [Scout.md](../Classes/Scout.md) | PvP trait change. |
| 23 | ยิงจาก 5 ช่องขึ้นไปแรงขึ้น 20% | PvP Scout: เป้าที่ติด Mark หลบได้ครึ่งเด | Class: Scout (PvP) | [Scout.md](../Classes/Scout.md) | PvP trait change. |
| 24 | โดนตีประชิดแล้วกระโดดหนี 4 ช่อง (ทุก 10 วิ) | PvP Scout: เป้าที่ติด Mark หลบได้ครึ่งเด | Class: Scout (PvP) | [Scout.md](../Classes/Scout.md) | PvP trait change. |
| 25 | DEX ออกบนเกราะ รองเท้า และหมวกได้ | PvP Scout: เป้าที่ติด Mark หลบได้ครึ่งเด | Affixes | [affix.md](../Affixes/affix.md) · [Scout.md](../Classes/Scout.md) | [TO_VERIFY] DEX on armor/boots/headgear is new per patch; the tier-10 per-item affix pools in this KB may not include it yet. |
| 26 | PvP Acolyte: ฮีลจาก Acolyte หลายคนซ้อนกันใน 4 วิจะเบาลง | — | Class: Acolyte (PvP) | [Acolyte.md](../Classes/Acolyte.md) | PvP rule change. |
| 27 | Rend, Gash, Assassinate ลดฮีลที่เป้าได้รับ 40% นาน 5 วิ | PvP Acolyte: ฮีลจาก Acolyte หลายคนซ้อนกั | Class: Acolyte (PvP) | [Acolyte.md](../Classes/Acolyte.md) · [rend.md](../Skills/Warrior/rend.md) · [gash.md](../Skills/Warrior/gash.md) · [assassinate.md](../Skills/Rogue/assassinate.md) | Grouping under Acolyte follows the bullet layout of the source text [INFERENCE]; the effect itself names Rend, Gash, Assassinate. |
| 28 | Summoner: ตีเป้าใหญ่ได้วิญญาณทุก 3 วิ และ Soul Surge ซ้อนบนเป้าใหญ่ได้ | — | Class: Summoner | [Summoner.md](../Classes/Summoner.md) · [class-resources.md](../Combat_Mechanics/class-resources.md) | Class resource rule change. |
| 29 | Oathbound Band: MATK เท่ากับ ATK และ INT เท่ากับ STR | — | Unique item | [oathbound_band.md](../Equipment/oathbound_band.md) · [uniques.md](../Blacksmith/uniques.md) | CONFLICT-LIKELY: Wiki shows Oathbound Band as 'ATK +10% · MATK +10% · Block +5%' with Twin Oath; the patch adds MATK = ATK and INT = STR. |
| 30 | แก้บั๊ก: สถานะกลัวทำให้มอนวิ่งหนีจริง | — | Bug fix: Fear status | [statuses.md](../Combat_Mechanics/statuses.md) | Bug fix. |
| 31 | เปลี่ยนอาชีพแล้วบัฟสกิลอาชีพเดิมหาย | แก้บั๊ก: สถานะกลัวทำให้มอนวิ่งหนีจริง | Bug fix: class change | [_All_Classes.md](../Classes/_All_Classes.md) | Bug fix. |
| 32 | ป้าย KILL ขึ้นทุกการฆ่าผู้เล่น | แก้บั๊ก: สถานะกลัวทำให้มอนวิ่งหนีจริง | Bug fix: PvP | [pvp.md](../Game_Systems/pvp.md) | Bug fix. |
| 33 | สู้กับผู้เล่นยังไม่จบ ดูดเลือดจากมอนไม่ได้ | แก้บั๊ก: สถานะกลัวทำให้มอนวิ่งหนีจริง | Bug fix: PvP lifesteal | [pvp.md](../Game_Systems/pvp.md) | Bug fix. |
| 34 | Soulforge ชิ้นสุดท้ายข้ามแรงก์ 8 ได้ | แก้บั๊ก: สถานะกลัวทำให้มอนวิ่งหนีจริง | Bug fix: Soulforge | — | [UNKNOWN] 'Soulforge' does not appear anywhere in the crawled Wiki. |
| 35 | Gate Brute กับ Golden Sentinel เกิดอีกครั้ง | แก้บั๊ก: สถานะกลัวทำให้มอนวิ่งหนีจริง | Bug fix: monster spawn | [gate_brute.md](../Monsters/gate_brute.md) · [golden_sentinel.md](../Monsters/golden_sentinel.md) | Bug fix (spawn restored). |
| 36 | การ์ด World Boss ไม่ต้องเปิดซอง | แก้บั๊ก: สถานะกลัวทำให้มอนวิ่งหนีจริง | Cards / World Boss | [world-boss.md](../Monsters/world-boss.md) · [Cards_and_Spirits.md](../Cards/Cards_and_Spirits.md) | Card delivery change. |
