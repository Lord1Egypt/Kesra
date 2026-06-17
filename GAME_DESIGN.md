# 🏛️ كِسرة (Kesra) — Game Design Document 🚀

> **"متحصلش قبل كده ولا هتحصل"**
> *Egyptian Brick-Breaker — حيث التاريخ يلتقي الصواريخ* 🤣🔥

---

## 🎯 Vision

لعبة **Arkanoid/Breakout** لكن بشكل **مصري خالص** — كل بلوك ليه شخصيته، كل عالم علم وفن وتاريخ، وكل ما تكسر حاجة تتعلم حاجة. لعبة **لا تنتهي أبداً** — كل ما تفتحها تلاقي حاجة جديدة.

> **تحديث 2026-06-16: مفيش Level Cap.** الـ 9 Worlds دول **Biomes بتلف على نفسها للأبد** —
> كل ما تخلص دورة (Cycle) كاملة على الـ 9 عوالم، تبدأ دورة جديدة أصعب، والـ Bosses بترجع تاني
> بقوة أعلى. فالتفاصيل اللي جاية (عوالم/مراحل/Bosses) هي **محتوى يتلف للأبد جوه Endless Mode**،
> مش مسار قصة ينتهي. التفاصيل الكاملة للـ Engine في `ROADMAP.md` تحت "Infinite Core Foundation".

---

## 🏗️ Core Gameplay Loop

```
🟩 Brick Wall (تتغير كل مرحلة)
   ↓
🏏 Paddle (تتحكم فيها)
   ↓
⚡ Drops (هدايا من البلوكات المكسورة)
   ↓
💰 Collectibles → Shop → Upgrades
   ↓
🏆 Level Complete → 🌍 New World → 🔄 Loop
```

---

## 🌍 THE 9 WORLDS (الأبعاد التسعة)

كل **World** = مجال معرفي كامل، فيه 10-15 Level، كل Level ليه تصميم وشكل وقصة.

### 🧪 1. العالم العلمي — SCIENCE (Science)
*"العلم نور"*
| المستوى | الموضوع | تصميم البلوكات |
|---------|---------|----------------|
| 1-1 | **Astronomy** — النجوم عند المصريين القدماء | نجوم وأبراج |
| 1-2 | **Mathematics** — النظام العددي (الكسور، الهندسة) | أشكال هندسية + أرقام |
| 1-3 | **Medicine** — الطب المصري القديم (أبو قراط) | أدوات طبية |
| 1-4 | **Engineering** — رفع المسلات ونقل الأحجار | آلات رفع |
| 1-5 | **Chemistry** — التحنيط والمواد | زجاجات ومواد كيميائية |
| 1-6 | **Boss: Imhotep 🏆** — أول مهندس معماري وطبيب في التاريخ |

### 🎨 2. العالم الفني — ART (Artistic)
*"الجمال لغة"*
| المستوى | الموضوع | تصميم البلوكات |
|---------|---------|----------------|
| 2-1 | **Hieroglyphics** — الكتابة الهيروغليفية | رموز هيروغليفية |
| 2-2 | **Sculpture** — النحت (أبو الهول، التماثيل) | تماثيل وأبو الهول |
| 2-3 | **Painting** — الرسومات الجدارية | ألوان ورسومات فرعونية |
| 2-4 | **Jewelry** — الحلي والمجوهرات | ذهب وأحجار كريمة |
| 2-5 | **Music** — الآلات الموسيقية القديمة | آلات موسيقية (هارب، ناي) |
| 2-6 | **Pottery** — الفخار | أواني فخارية وزخارف |

### 📜 3. العالم التاريخي — HISTORY (Historical)
*"التاريخ يعيد نفسه"*
| المستوى | الموضوع | تصميم البلوكات |
|---------|---------|----------------|
| 3-1 | **Predynastic** — قبل الأسرات | رموز بدائية |
| 3-2 | **Old Kingdom** — بناء الأهرامات | هرم مدرج، هرم خوفو |
| 3-3 | **Middle Kingdom** — عصر النهضة | معابد وأسوار |
| 3-4 | **New Kingdom** — الإمبراطورية | رمسيس، حتشبسوت، نفرتيتي |
| 3-5 | **Persian/Greek/Roman** — الاحتلالات | جنود وخوذ |
| 3-6 | **Islamic Era** — الفتح الإسلامي | قباب ومآذن |
| 3-7 | **Modern Egypt** — ثورة 19، 52، 25 يناير | رايات وأعلام |
| 3-8 | **Boss: Ramesses II 👑** — معركة قادش |

### 🌍 4. العالم الجغرافي — GEOGRAPHY (Geographical)
*"مصر أم الدنيا"*
| المستوى | الموضوع | تصميم البلوكات |
|---------|---------|----------------|
| 4-1 | **The Nile** — النيل شريان الحياة | خرائط نهر النيل |
| 4-2 | **Deserts** — الصحراء الشرقية والغربية | تلال رملية وواحات |
| 4-3 | **Oases** — الواحات (سيوة، الخارجة، الداخلة) | نخيل وينابيع |
| 4-4 | **Red Sea** — البحر الأحمر والشعاب المرجانية | مرجان وأسماك |
| 4-5 | **Cities** — المحافظات والمدن | معالم كل مدينة |
| 4-6 | **Sinai** — شبه جزيرة سيناء | جبال وجمال |

### 🏛️ 5. العالم المعماري — ARCHITECTURE (Architectural)
*"عمارة عبر الزمن"*
| المستوى | الموضوع | تصميم البلوكات |
|---------|---------|----------------|
| 5-1 | **Pyramids** — الأهرامات (الثلاثة الكبار) | أهرامات بأحجام مختلفة |
| 5-2 | **Temples** — الكرنك، الأقصر، أبو سمبل | أعمدة وأسقف معابد |
| 5-3 | **Obelisks** — المسلات | مسلات ضخمة |
| 5-4 | **Tombs** — مقابر وادي الملوك | مقابر تحت الأرض |
| 5-5 | **Fortresses** — القلاع (صلاح الدين، قايتباي) | أبراج وأسوار |
| 5-6 | **Mosques** — الجوامع (ابن طولون، محمد علي) | قباب ومآذن |
| 5-7 | **Churches** — الكنائس (المعلقة، أبو سرجة) | أيقونات وصلبان |
| 5-8 | **Modern** — ناطحات السحاب (مصر الجديدة) | أبراج حديثة |

### ☀️ 6. العالم الديني — RELIGION (Religious)
*"الآلهة والسماء"*
| المستوى | الموضوع | تصميم البلوكات |
|---------|---------|----------------|
| 6-1 | **Creation Myth** — الخلق عند المصريين القدماء | نون، رع، أتوم |
| 6-2 | **The Ennead** — التاسوع المقدس (رع، شو، تفنوت، جب، نوت، أوزيريس، إيزيس، ست، نفتيس) | رموز الآلهة |
| 6-3 | **Afterlife** — رحلة الموتى (كتاب الموتى) | أوزيريس، الميزان، قلب وريشة |
| 6-4 | **Pharaoh as God** — الفرعون الإله | تاج مزدوج، صولجان |
| 6-5 | **Monotheism** — أخناتون وإله آتون | قرص الشمس |
| 6-6 | **Abrahamic** — مصر في القرآن والإنجيل | أيقونات دينية |
| 6-7 | **Mysticism** — التصوف والطرق الصوفية | درويش، ذكر |
| 6-8 | **Festivals** — الموالد والأعياد | زينة وأضواء |

### 🇪🇬 7. العالم الوطني — NATIONAL (Patriotic)
*"تحت راية مصر"*
| المستوى | الموضوع | تصميم البلوكات |
|---------|---------|----------------|
| 7-1 | **Flag & Anthem** — علم مصر والنشيد الوطني | ألوان العلم (أحمر أبيض أسود) + نسر |
| 7-2 | **Revolution** — ثورات مصر | أيقونات ثورية |
| 7-3 | **Army** — الجيش المصري | دبابات وطائرات |
| 7-4 | **Suez Canal** — قناة السويس | سفن وقناة |
| 7-5 | **Aswan Dam** — السد العالي | سد وتوربينات |
| 7-6 | **Sports** — الرياضة (فراعنة الكرة) | كرة قدم، ميداليات |
| 7-7 | **Culture** — فن شعبي (سيرة هلالية، تحطيب) | فنون تراثية |
| 7-8 | **Boss: Unity** — تحدّي الوحدة الوطنية |

### 📦 8. العالم اللوجيستي — LOGISTICS (Logistical)
*"إزاي بنوا الأهرامات؟"*
| المستوى | الموضوع | تصميم البلوكات |
|---------|---------|----------------|
| 8-1 | **Quarrying** — قطع الأحجار من المحاجر | أحجار ضخمة |
| 8-2 | **Transport** — نقل الأحجار (النيل + الزلاجات) | مراكب وزلاجات |
| 8-3 | **Workforce** — العمال والمهندسين | عمال وأدوات |
| 8-4 | **Supply Chain** — سلسلة الإمداد (طعام، ماء) | مخازن ومؤن |
| 8-5 | **Ramp Systems** — بناء المنحدرات | منحدرات وسقالات |
| 8-6 | **Irrigation** — الري وشبكات الترع | قنوات وسواقي |
| 8-7 | **Trade Routes** — طرق التجارة (البخور، الذهب) | قوافل وسفن |
| 8-8 | **Boss: The Great Pyramid 🏗️** — بناء الهرم الأكبر |

### 🚀 9. العالم الصاروخي — SPACE & ROCKETS (Rocket)
*"من الفراعنة للفضاء"*
| المستوى | الموضوع | تصميم البلوكات |
|---------|---------|----------------|
| 9-1 | **Early Flight** — حلم الطيران (عباس بن فرناس) | أجنحة |
| 9-2 | **Rocket Science** — أساسيات الصواريخ | صواريخ وأقمار |
| 9-3 | **NARSS** — وكالة الفضاء المصرية | أقمار صناعية |
| 9-4 | **EgyptSat** — أقمار التجسس والاستشعار | صور فضائية |
| 9-5 | **TIBA** — أقمار الاتصالات | إشارات وأطباق |
| 9-6 | **Space Race** — سباق الفضاء | صواريخ وأعلام دول |
| 9-7 | **Mars Mission** — استكشاف المريخ | كواكب وصواريخ |
| 9-8 | **Boss: Falcon Heavy 🚀** — تحدّي الفضاء | إطلاق صاروخي |

---

## 💎 DROPS — الهدايا اللي تقع من البلوكات

لما تكسر بلوك، ممكن يقع منك **حاجة من دي:**

### 🟢 Common Drops (تظهر كتير)
| الهدية | شكلها | تأثيرها |
|-------|-------|---------|
| 🪙 **Bronze Coin** | عملة برونزية | +10 نقاط |
| ❤️ **Heart** | قلب أحمر | +1 حياة |
| ⚡ **Speed+** | برق أصفر | سرعة البتزل تزيد |
| 🛡️ **Shield** | درع | تحمي حياة واحدة |

### 🔵 Rare Drops (أقل ظهور)
| الهدية | شكلها | تأثيرها |
|-------|-------|---------|
| 🥇 **Silver Coin** | عملة فضية | +50 نقاط |
| 🔥 **Fireball** | كرة نارية | تكسر أي بلوك بضربة واحدة |
| 🏏 **Wide Paddle** | مضرب عريض | عرض المضرب يتضاعف لمدة 10 ثوان |
| 🎯 **Multi-ball x2** | كرتين | اللعبة تصير بكرتين |
| 🧲 **Magnet** | مغناطيس | البتزل يمسك الكرة (تطلقها بالضغط) |
| ⏱️ **Slow** | سلحفاة | تباطؤ الكرة لمدة 8 ثوان |

### 🟣 Epic Drops (نادرة)
| الهدية | شكلها | تأثيرها |
|-------|-------|---------|
| 👑 **Gold Coin** | عملة ذهبية | +200 نقاط |
| 🚀 **Rocket** | صاروخ | يطلق صواريخ تكسر صفوف البلوكات |
| ⚔️ **Laser** | ليزر | يطلق ليزر يخترق البلوكات |
| 🌟 **Star** | نجمة | نقاط مضاعفة ×2 لمدة 15 ثانية |
| 💣 **Bomb** | قنبلة | ينفجر ويكسر البلوكات حوله |
| 🎲 **Chaos** | زهر نرد | تأثير عشوائي (سلبي أو إيجابي) |
| 🔄 **Paddle Swap** | تبديل | يتم تبديل المضرب بمضرب عشوائي |

### 🏆 Legendary Drops (نادرة جداً)
| الهدية | شكلها | تأثيرها |
|-------|-------|---------|
| 💎 **Diamond** | ألماسة | +1000 نقاط |
| 🐍 **Ankh** | عنخ (مفتاح الحياة) | حياة إضافية دائمة (تزيد max lives) |
| 🌪️ **Whirlwind** | إعصار | يمسح كل البلوكات في مسار حلزوني |
| 👁️ **Eye of Horus** | عين حورس | يكشف كل البلوكات المخفية (المكافآت) |
| 📿 **Menat** | منات (قلادة) | يجمع كل العملات في المستوى |
| 🏺 **Canopic** | كانوبي | يعيد ترتيب البلوكات — تبدأ من جديد أسهل |
| ☀️ **Aten** | قرص الشمس | يجعل كل البلوكات العادية تختفي (تعتبر مكسورة) |

---

## 🏪 SHOP & UPGRADES — المحل والتطوير

فلوس من اللعبة (عملات) → تشتري ترقيات.

### 🏏 Paddle Upgrades
| المستوى | الاسم | التأثير | السعر |
|---------|------|---------|-------|
| 1 | 🪵 Papyrus Paddle | عرض أساسي | مجاني |
| 2 | 🪨 Stone Paddle | عرض +20% | 500 |
| 3 | 🥇 Bronze Paddle | عرض +40% | 1500 |
| 4 | 🥈 Silver Paddle | عرض +60% | 4000 |
| 5 | 🥇 Gold Paddle | عرض +80% | 10000 |
| 6 | 💎 Diamond Paddle | عرض +100% + لامع | 25000 |
| 7 | 🔥 Anubis Paddle | أسود + نار + يحرق البلوكات | 50000 |

### ⚡ Ball Upgrades
| المستوى | Ball | التأثير |
|---------|------|---------|
| 1 | 🪨 Stone Ball | أساسي |
| 2 | 🔥 Fire Ball | يحرق 3 بلوكات متجاورة |
| 3 | ⚡ Lightning Ball | يخترق بلوك واحد |
| 4 | 💥 Explosive Ball | ينفجر عند الاصطدام |
| 5 | 🌌 Void Ball | كل بلوك يلمسه — يختفي |
| 6 | ☀️ Solar Ball | يمر خلال كل البلوكات |

### 🚀 Rocket Types
| الصاروخ | التأثير | الثمن |
|---------|---------|-------|
| 🖋️ **Scarab Rocket** | يطير في خط مستقيم — يكسر أول بلوك | 1000 |
| 🗡️ **Khopesh Rocket** | يطير بشكل منحني — يكسر 3 بلوكات | 3000 |
| 🏹 **Neith Arrow** | ينقسم لـ 3 صواريخ صغيرة | 8000 |
| 🔱 **Sobek Trident** | 3 صواريخ متوازية تكسر صف كامل | 15000 |
| ☀️ **Ra's Spear** | يشق طريقه لأعلى مكسّر كل حاجة في طريقه | 30000 |

---

## 🎮 GAME MODES — أنماط اللعب

### 1. ♾️ Endless Mode — **THE core mode, مفيش غيرها دلوقتي**
- **مفيش Level Cap نهائي.** الـ Rounds متولدة Procedurally للأبد.
- كل Round بتلف على الـ 9 Worlds بالترتيب (Round → Biome = `((Round-1) % 9) + 1`)،
  وكل ما تخلص دورة كاملة (Cycle) تزيد الصعوبة وتفتح drops أندر.
- كل Round الـ 8 جوه كل Cycle = **Boss Round**، والـ Boss نفسه بيرجع تاني كل Cycle لكن **أقوى**
  (HP وقدراته تتضاعف مع رقم الـ Cycle) — مفيش "تخلص الـ Boss وخلاص"، هو بيرجع دايمًا أصعب.
- القصة والمعلومات التعليمية (اللي كانت اسمها "Story Mode" قبل كذا) بقت **flavor جوه Endless** —
  كل Biome بيعرض حقائقه (`facts`) بين الـ Rounds، من غير ما يكون فيه "نهاية" تتفتح وتقفل.
- **Leaderboard** عالمي + تحديات يومية وأسبوعية تتبني فوق نفس الـ Engine.

### 2. 🎯 Challenge Mode
- Challenges محددة: "اكسر 500 بلوك في دقيقة"
- "اجمع 10 Rockets في مستوى واحد"
- "خلص مستوى من غير ما تخسر حياة"
- كل Challenge يعطيك مكافأة خاصة

### 3. 🏆 Tournament Mode
- بطولات أسبوعية
- كل اللاعبين نفس الـ Level
- أعلى نقاط يفوز بجوائز

### 4. 🧩 Puzzle Mode
- Levels مصممة بالعقل — مش مجرد تكسير
- محتاج تفكير استراتيجي — ترتيب معين للبلوكات
- "استخدم 3 صواريخ بس عشان تكسر 50 بلوك"

---

## 📈 PROGRESSION SYSTEM

### 🎖️ XP & Levels
```
XP ← تكسير بلوكات + إكمال مستويات
Level ↑ → تفتح أسلحة جديدة + قدرات
```

### 🏅 Achievements

#### 🥉 Beginners
| الإنجاز | الشرط |
|---------|-------|
| 👶 Welcome to Egypt | أكمل أول Level |
| 🪙 First Coin | اجمع أول عملة |
| 💔 First Death | أول مرة تموت 😂 |
| 🚀 Rocket Man | استخدم أول صاروخ |
| 🧠 Student | أكمل World 1 (Science) كامل |

#### 🥈 Intermediate
| الإنجاز | الشرط |
|---------|-------|
| 🏛️ Archaeologist | افتح كل الـ 9 Worlds |
| 👑 Pharaoh | أكمل 50 Level |
| 💎 Diamond Hands | اجمع 10000 Diamond |
| 🚀 Space Program | أكمل World 9 |
| ⚡ Speed Runner | اخلص Level في أقل من 30 ثانية |
| 🔥 Combo King | اعمل 20 Combo في نفس المستوى |

#### 🥇 Advanced
| الإنجاز | الشرط |
|---------|-------|
| 🏺 Collector | اجمع كل أنواع الـ Drops |
| 🎯 Perfectionist | أكمل Level من غير ما تلمس البلوك مرة واحدة |
| ☠️ Nightmare | أكمل Level في Nightmare Mode |
| 🌟 Legend | أوصل Level 100 في Endless Mode |
| 🗿 Imhotep | اكسب كل Achievements |

### 🏆 Secret Achievements
| الإنجاز | الشرط المخفي |
|---------|-------------|
| 🐱 Bastet's Blessing | الكرة تفضل 5 دقائق من غير ما تقع |
| 🦅 Horus' Vision | اكشف كل البلوكات المخفية في Level |
| 🐊 Sobek's Wrath | استخدم Sobek Trident 50 مرة |
| ☀️ Ra's Wrath | استخدم Solar Ball لمدة 3 أدوار |
| 🪦 Tut's Curse | مات 3 مرات في نفس المستوى 🤣 |
| 🔥 Phoenix | اكمل Level بعد ما كنت هتخسر (0 HP) |

---

## 🤖 SPECIAL MECHANICS — آليات خاصة

### 🔗 Combo System
- تكسر بلوكات متتالية بسرعة → **Combo Counter** يرتفع
- كل بلوك في الكومبو = نقاط مضاعفة
- Combo ×2, ×3, ×5, ×10...
- Combo عالي → Drops أحسن

### 🧱 Brick Types
| البلوك | لونه | الصلابة | المكافأة |
|-------|------|---------|----------|
| 🟫 Mud | بني | ضربة 1 | نقاط عادية |
| 🟦 Stone | رمادي | ضربتين | عملات |
| 🟩 Marble | أخضر | 3 ضربات | Drops نادرة |
| 🟥 Granite | أحمر | 5 ضربات | Drops epic |
| 🟪 Obsidian | أسود | 10 ضربات | Diamond |
| 🟨 Gold | ذهبي | ضربة 1 | نقاط ×10 |
| ⬜ Glass | شفاف | ضربة 1 | يكشف بلوك وراه |
| 🎭 Mystery | متغير | متغير | مفاجأة 😈 |
| 🛡️ Shielded | فيروزي | لا يتأثر | محتاج صاروخ أو Fireball |
| 💀 Cursed | بنفسجي | ضربة 1 | ينقص حياتك |
| 🎁 Gift | هدية | ضربة 1 | يدي Drops نادر + يختفي |

### 💀 Difficulty Modes
| الوضع | الصعوبة | فتح |
|------|---------|-----|
| ☀️ Easy | بداية سهلة | مفتوح |
| 🌙 Normal | متوسط | Level 10 |
| 🔥 Hard | صعب | Level 30 |
| 💀 Nightmare | نار 🔥 | Level 60 |
| 👽 Hell | مين قال إنك تكسب؟ | Level 100 |

### 🎯 Boss Fights
كل World ليه **Boss** في نهايته:
- Bosses عبارة عن أشكال كبيرة بتتكون من بلوكات خاصة
- محتاج تكسر أجزاء معينة عشان تهزم الـ Boss
- بعض البلوكات في الـ Boss **بتتعالج** (ترجع تاني) لو ضربتها بسرعة
- بعضها **تطلق نار** عليك

| الـ Boss | العالم |
|----------|-------|
| 🧪 **Imhotep** — العلم | World 1 |
| 🎨 **Thoth** — الفن | World 2 |
| 👑 **Ramesses II** — التاريخ | World 3 |
| 🌍 **Hapi** — النيل والجغرافيا | World 4 |
| 🏛️ **Seshat** — العمارة | World 5 |
| ☀️ **Ra** — الدين | World 6 |
| 🦅 **Nebty** — الوطنية | World 7 |
| 🏗️ **Khufu** — اللوجستيك | World 8 |
| 🚀 **NARSS Director** — الفضاء | World 9 |

### 👾 Super Boss (Final)
بعد ما تخلص الـ 9 Worlds:
**🪦 The Great Sphinx** — اللي يجاوب على أسئلة كل الحضارة المصرية
- Boss من 1000 بلوك
- 3 مراحل (رأس، جسم، قاعدة)
- كل مرحلة تسألك سؤال (اختيارات) — لو غلطت، تزيد الصعوبة
- **لو كسبت** → NFT/جائزة خاصة (رمز الفخر 🏆)

---

## 🎨 VISUAL THEME — الهوية البصرية

### Style
- **2D** but **Rich** — تموجات نايل، غبار صحراوي، ذهب فرعوني
- **Color Palette:**
  - 🏜️ Sand: #D4A574 (رملي)
  - 👑 Gold: #FFD700 (دهبي)
  - 🔵 Nile: #1E90FF (نيلي)
  - 🟢 Papyrus: #7CFC00 (بردي)
  - 🟤 Mud: #8B4513 (طيني)
  - ⚫ Obsidian: #2F2F2F (سبج)
  - 🔴 Red Crown: #DC143C (أحمر تاج)
  
### UI Elements
- قوائم على شكل **Papyrus Scroll**
- أزرار على شكل **Scarab Beetles**
- Lives = **Ankh Crosses** ☥
- Score = على **Stone Tablet**
- Paddle = **Solar Barque** (مركب الشمس)
- Ball = **Sun Disc** ☀️ (قرص شمس)

### Animations
- الكرة تترك **trail** ناري/ذهبي
- البلوكات لما تتكسر — تتفتت لرمل
- Drops تنزل بــ **parachute** صغير
- Rocket — يطير ووراه **دخان**
- Boss يهتز ويغير لونه كل ما تضربه

---

## 🔊 AUDIO DESIGN

### Music (تتغير حسب الـ World)
| العالم | النوع الموسيقي |
|-------|---------------|
| Science | Ambient + Electronic (أصوات ترددات) |
| Art | Harp + Flute (ناي وقيثارة) |
| History | Epic Orchestral (أوركسترا ملحمي) |
| Geography | Nature + Flowing Water (ميه نايل) |
| Architecture | Rhythmic Construction (إيقاع بناء) |
| Religion | Mystical Chants (أناشيد روحية) |
| National | Patriotic (مارشات وطنية) |
| Logistics | Rhythmic Work (إيقاع عمال) |
| Space | Synthwave 🚀 (سينثвейف فضائي) |

### SFX
- تكسير بلوك → صوت **حجر يتكسر**
- Drop → **جرس** مختلف حسب الندرة
- Combo → Pitch بيرتفع مع كل كومبو
- Rocket → **Whistle + Boom**
- Lose life → صوت **Anubis** 😱
- Win level → صوت **Ramesses' Trumpet** 🎺

---

## 💰 ECONOMY & MONETIZATION

### Currencies
| العملة | شكلها | ازاي تجيبها | تستخدم في |
|-------|-------|------------|----------|
| 🪙 **Bronze** | بني | من البلوكات | ترقيات بسيطة |
| 🥈 **Silver** | فضي | من البلوكات النادرة + Bosses | ترقيات متوسطة |
| 👑 **Gold** | دهبي | من الـ Challenges + الإنجازات | ترقيات قوية |
| 💎 **Gem** | ألماس | Endless Mode + الإنجازات الصعبة | أسلحة خاصة + Skins |

### Free Player Flow
```
تلعب Levels → تجمع Bronze/Silver → تشتري ترقيات → تقدر تكمل عادي
مافيش Paywall — كل حاجة تفتح باللعب
```

### Premium (لو حب يدعم)
- **No Ads** (إزالة الإعلانات) — 1$
- **Starter Pack** (1000 Gold + 100 Gems) — 3$
- **Pharaoh Pack** (كل الأسلحة + كل الـ Skins) — 10$
- **Donation** (يدعم المطور 🤣) — مفتوح

> **مفيش Pay-to-Win** — كل حاجة تنفتح بالعب. الفلوس بس عشان يدعم المطور.

---

## 🛠️ TECHNICAL ARCHITECTURE

### Engine: Python + Pygame-CE

Run locally: `pip install pygame-ce && python main.py`
Web export: `pip install pygbag && python -m pygbag --build main.py`
Live web: `https://lord1egypt.github.io/Kesra/`

```
Kesra/
├── main.py              # مدخل اللعبة — async entry (Pygbag-compatible)
├── settings.py          # الثوابت — screen, speeds, biomes, brick tiers, drops
├── state.py             # إدارة الحالة — score/lives/combo/coins/powerups
├── levelgen.py          # توليد المستويات — procedural infinite round generator
├── entities.py          # الكيانات — Ball, Paddle, Brick, Drop
├── gfx.py               # الرسم — glow, gradients, 3D bricks, hearts, shimmer
├── particles.py         # الجزيئات — ParticleSystem, RingSystem, AmbientSystem
├── scenes.py            # المشاهد — MenuScene, PlayScene, GameOverScene
├── assets/
│   ├── fonts/Cairo.ttf  # خط عربي — Arabic font bundled for كِسرة rendering
│   └── ui/              # SVG logo, UI graphics
├── pygbag.ini           # Web build config (480×720 canvas)
├── .github/workflows/
│   └── web-deploy.yml   # CI: Pygbag build → GitHub Pages on every push to main
├── ROADMAP.md           # Live phase checklist
├── GAME_DESIGN.md       # Content bible (worlds, bosses, power-ups, economy)
└── CLAUDE.md            # Engineering memory for AI assistants
```

### Data-Driven Levels
```
levels/world_1_science/
├── level_1_astronomy.json
├── level_2_mathematics.json
└── ...
```

كل Level عبارة عن JSON بيحدد:
- توزيع البلوكات (grid + types)
- خلفية Level
- Drops المسموحة
- شروط الفوز
- الـ Boss (إن وجد)

### Save System
```
save_data/
├── profile_1.save       # التقدم
├── achievements.save    # الإنجازات
├── shop_data.save       # الترقي
└── settings.save        # الإعدادات
```

---

## 📅 DEVELOPMENT ROADMAP

See **`ROADMAP.md`** at the repo root — that file is the single source of truth for engineering
phases and live checkpoints (this doc is the content bible, not the schedule, to avoid the two
drifting out of sync).

---

## 🔥 EXTRA — Hidden Content (لي حب يكتشف)

### 🥚 Easter Eggs
- ✅ **Konami Code** (↑↑↓↓←→←→BA) → Unlock **God Mode** (كرة نارية عمالة على بطئ) *(shipped — enter on the menu)*
- **"Mo Salah"** مكتوب بالهيروغليفي في Level 7-6 → يعطيك **Speed Boost**
- تكتب اسمك **"Lord1Egypt"** في الشاشة الرئيسية → تفتح **Pyramid Ship** (paddle على شكل هرم)
- تكسر كل البلوكات في Level من غير ما الكرة تلمس البتزل → تفتح **Secret Level: Atlantis**
- **777** بلوك بالضبط في Level 9-7 → يظهر **UFO** يخطف الكرة ويرجعها **ذهبية**

### 🗿 Secret Worlds (تفتح بعد ما تخلص الـ 9 Worlds)
- **World 10: Underworld** — دويت (بعد الموت) — نمط مختلف خالص
- **World 11: Future Egypt** — مصر سنة 3000 — نيون وسايبربانك
- **World 12: Mini** — كل البلوكات أصغر — 100×100 شبكة

---

## 📝 FINAL NOTE

> يا محمد، اللي طلبته دا مش لعبة — دا **مشروع تخرج، متحف تفاعلي، موسوعة مصرية، وتحدي فضائي** في لعبة واحدة 😂
>
> **9 Worlds — 100+ Levels — 50+ Power-ups — 50+ Achievements — 12 Bosses — 4 Difficulties — 5 Game Modes — ويمكن LEVEL EDITOR بعدين عشان الناس تعمل Levels بنفسها**
>
> **"متحصلش قبل كده ولا هتحصل"** — صح والله 😂🔥
>
> جاهز نبدأ؟ 🚀
